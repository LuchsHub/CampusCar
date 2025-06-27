import datetime
import uuid
from typing import Any

from app.crud import get_or_create_location
from fastapi import APIRouter, HTTPException, status
import openrouteservice
from sqlalchemy.orm import selectinload
from sqlmodel import func, select

from app.api.deps import CurrentUser, ORS_Client, SessionDep
from app.core.config import settings
from app.models import (
    Codrive,
    CodriveCreate,
    CodrivePublic,
    Ride,
)

router = APIRouter(prefix="/codrives", tags=["codrives"])


@router.post(
    "/{ride_id}", response_model=CodrivePublic, status_code=status.HTTP_201_CREATED
)
def request_codrive(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    ors_client: ORS_Client,
    ride_id: uuid.UUID,
    codrive_in: CodriveCreate,
) -> Any:
    """
    Request to join a ride.
    This calculates a new potential route including the new passenger and
    the associated extra distance (point_contribution).
    """
    ride = session.get(
        Ride, ride_id, options=[selectinload(Ride.start_location), selectinload(Ride.end_location)]
    )
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found"
        )

    if ride.driver_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot request to join your own ride.",
        )
    if ride.starting_time <= datetime.datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This ride has already started or is in the past.",
        )
    if ride.n_codrives >= ride.max_n_codrives:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This ride is already full."
        )
    if session.exec(
        select(Codrive).where(
            Codrive.ride_id == ride.id, Codrive.user_id == current_user.id
        )
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already sent a request for this ride.",
        )

    new_pickup_location = get_or_create_location(
        address=codrive_in.location, session=session, ors_client=ors_client
    )

    # Get locations of already accepted codrivers
    accepted_codrives_stmt = select(Codrive).where(Codrive.ride_id == ride.id, Codrive.accepted == True).options(selectinload(Codrive.location))
    accepted_codrives = session.exec(accepted_codrives_stmt).all()

    waypoints = [ (ride.start_location.longitude, ride.start_location.latitude) ]
    waypoints.extend([(c.location.longitude, c.location.latitude) for c in accepted_codrives])
    waypoints.append((new_pickup_location.longitude, new_pickup_location.latitude))
    waypoints.append((ride.end_location.longitude, ride.end_location.latitude))

    try:
        new_route_data = ors_client.directions(coordinates = waypoints, format="geojson", profile="driving-car", optimize_waypoints=True)
    except openrouteservice.exceptions.ApiError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No route could be found for the requested pickup location."
        )

    # Extract new route info
    new_route_summary = new_route_data["features"][0]["properties"]["summary"]
    new_total_distance = new_route_summary["distance"]
    new_route_geometry = new_route_data["features"][0]["geometry"]["coordinates"]

    # Calculate point contribution and validate against max distance
    added_distance = new_total_distance - ride.estimated_distance_meters
    if (
        ride.max_request_distance is not None
        and added_distance > ride.max_request_distance
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requested pickup location is too far off the original route. "
                   f"Detour of {round(added_distance)}m exceeds the allowed "
                   f"{round(ride.max_request_distance)}m."
        )

    # Calculate arrival time at the new pickup point by summing segment durations
    segments = new_route_data["features"][0]["properties"]["segments"]
    # The last segment is from the new pickup to the final destination. We need all segments before that.
    duration_to_pickup_seconds = sum(s["duration"] for s in segments[:-1])
    arrival_at_pickup = ride.starting_time + datetime.timedelta(
        seconds=duration_to_pickup_seconds
    )

    codrive_db = Codrive(
        user_id=current_user.id,
        ride_id=ride.id,
        location_id=new_pickup_location.id,
        time_of_arrival=arrival_at_pickup,
        point_contribution=round(point_contribution),
        updated_route_geometry=new_route_geometry,
    )

    session.add(codrive_db)
    session.commit()
    session.refresh(codrive_db)

    return CodrivePublic.model_validate(codrive_db)