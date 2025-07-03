import datetime
from typing import Any

import openrouteservice  # type: ignore
from fastapi import APIRouter, HTTPException, status

from app.api.deps import (
    CurrentUser,
    ORS_Client,
    SessionDep,
)
from app.crud import get_or_create_location
from app.models import Car, Ride, RideCreate, RidePublic

router = APIRouter(prefix="/rides", tags=["rides"])


@router.post("/", response_model=RidePublic, status_code=status.HTTP_201_CREATED)
def create_ride(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    ors_client: ORS_Client,
    ride_in: RideCreate,
) -> Any:
    """
    Create a new ride by providing start and end addresses.

    The backend will geocode the addresses, save them as locations,
    and calculate the route geometry between them.
    """

    car = session.get(Car, ride_in.car_id)
    if not car or car.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found or you are not the owner.",
        )

    # Get or create the location objects
    start_location = get_or_create_location(ride_in.start_location, session, ors_client)
    end_location = get_or_create_location(ride_in.end_location, session, ors_client)

    try:
        route_request = {
            "coordinates": [
                (start_location.longitude, start_location.latitude),
                (end_location.longitude, end_location.latitude),
            ],
            "format": "geojson",
            "profile": "driving-car",
        }
        route_data = ors_client.directions(**route_request)

    except openrouteservice.exceptions.ApiError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No route could be found between the specified start and end locations."
            " Please ensure they are reachable by car.",
        )

    route_summary = route_data["features"][0]["properties"]["summary"]

    geometry = route_data["features"][0]["geometry"]["coordinates"]

    duration_seconds = route_summary.get("duration", 0)
    distance_meters = route_summary.get("distance", 0)

    estimated_duration = datetime.timedelta(seconds=duration_seconds)
    arrival_datetime = datetime.datetime.combine(
        ride_in.arrival_date, ride_in.arrival_time
    )
    departure_datetime = arrival_datetime - estimated_duration

    db_ride = Ride.model_validate(
        ride_in.model_dump(exclude={"start_location", "end_location"}),
        update={
            "driver_id": current_user.id,
            "start_location_id": start_location.id,
            "end_location_id": end_location.id,
            "departure_date": departure_datetime.date(),
            "departure_time": departure_datetime.time(),
            "route_geometry": geometry,
            "estimated_duration_seconds": round(duration_seconds),
            "estimated_distance_meters": round(distance_meters),
        },
    )

    session.add(db_ride)
    session.commit()
    session.refresh(db_ride)

    ride_public = RidePublic.model_validate(db_ride)

    return ride_public