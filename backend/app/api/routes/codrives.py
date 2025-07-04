import datetime
import math
import uuid
from collections.abc import Sequence
from typing import Any, TypedDict

import openrouteservice  # type: ignore
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.api.deps import CurrentUser, ORS_Client, SessionDep
from app.crud import get_or_create_location
from app.models import (
    Codrive,
    CodriveCreate,
    CodrivePassenger,
    CodrivePublic,
    CodriveRequestPublic,
    Location,
    LocationPublic,
    Message,
    PassengerArrival,
    PassengerArrivalTime,
    Ride,
    RidePublic,
    RouteUpdate,
    RouteUpdatePublic,
    User,
    UserPublic,
)

router = APIRouter(prefix="/codrives", tags=["codrives"])


def dist_sq(p1: Sequence[float], p2: Sequence[float]) -> float:
    """Calculate the squared Euclidean distance between two points."""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def project_point_on_segment(
    p: Sequence[float], a: Sequence[float], b: Sequence[float]
) -> tuple[float, float]:
    """Project a point p onto a line segment (a, b)."""
    l2 = dist_sq(a, b)
    if l2 == 0:
        return (a[0], a[1])
    t = max(
        0, min(1, ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / l2)
    )
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def get_projection_distance(
    point_coord: Sequence[float], polyline_coords: Sequence[Sequence[float]]
) -> float:
    """Find the closest point on a polyline and return the distance along it."""
    min_dist_sq, total_polyline_dist, proj_dist = float("inf"), 0.0, 0.0
    for i in range(len(polyline_coords) - 1):
        seg_start = polyline_coords[i]
        seg_end = polyline_coords[i + 1]
        projection = project_point_on_segment(point_coord, seg_start, seg_end)
        current_dist_sq = dist_sq(point_coord, projection)
        if current_dist_sq < min_dist_sq:
            min_dist_sq = current_dist_sq
            proj_dist = total_polyline_dist + math.sqrt(dist_sq(seg_start, projection))
        total_polyline_dist += math.sqrt(dist_sq(seg_start, seg_end))
    return proj_dist


class Projection(TypedDict):
    location: Location
    proj_dist: float


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
    ride = session.get(
        Ride,
        ride_id,
        options=[
            selectinload(Ride.start_location),
            selectinload(Ride.end_location),
            selectinload(Ride.codrives).options(selectinload(Codrive.location)),
        ],
    )
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found"
        )
    if not ride.route_geometry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ride has no route."
        )
    if ride.driver_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot join own ride."
        )
    departure_datetime = datetime.datetime.combine(
        ride.departure_date, ride.departure_time
    )
    if departure_datetime <= datetime.datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ride is in the past."
        )
    if ride.n_codrives >= ride.max_n_codrives:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Ride is full."
        )
    if session.exec(
        select(Codrive).where(
            Codrive.ride_id == ride.id, Codrive.user_id == current_user.id
        )
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Request already sent."
        )

    new_pickup_location = get_or_create_location(
        address=codrive_in.location, session=session, ors_client=ors_client
    )
    accepted_codrives = [c for c in ride.codrives if c.accepted]

    all_passengers_by_loc_id = {c.location_id: c.user_id for c in accepted_codrives}
    all_pickup_locations = (
        [ride.start_location]
        + [c.location for c in accepted_codrives]
        + [new_pickup_location]
    )
    projections: list[Projection] = [
        {
            "location": loc,
            "proj_dist": get_projection_distance(
                (loc.longitude, loc.latitude), ride.route_geometry
            ),
        }
        for loc in all_pickup_locations
    ]
    projections.sort(key=lambda x: x["proj_dist"])
    ordered_pickup_locations = [p["location"] for p in projections]

    final_route_locations = ordered_pickup_locations + [ride.end_location]
    final_route_coords = [
        (loc.longitude, loc.latitude) for loc in final_route_locations
    ]
    try:
        final_route_data = ors_client.directions(
            coordinates=final_route_coords, format="geojson", profile="driving-car"
        )
    except openrouteservice.exceptions.ApiError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not calculate route for pickup.",
        )

    summary = final_route_data["features"][0]["properties"]["summary"]
    added_distance = summary["distance"] - ride.estimated_distance_meters
    if (
        ride.max_request_distance is not None
        and added_distance > ride.max_request_distance
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Detour of {round(added_distance)}m exceeds allowed {round(ride.max_request_distance)}m.",
        )

    new_duration = datetime.timedelta(seconds=summary["duration"])
    arrival_datetime = datetime.datetime.combine(ride.arrival_date, ride.arrival_time)
    new_departure_datetime = arrival_datetime - new_duration

    segments = final_route_data["features"][0]["properties"]["segments"]
    updated_codriver_arrival_times: dict[str, PassengerArrival] = {}
    duration_to_stop = 0.0
    for i, loc in enumerate(ordered_pickup_locations):
        if i == 0:
            continue
        duration_to_stop += segments[i - 1]["duration"]
        passenger_arrival_datetime = new_departure_datetime + datetime.timedelta(
            seconds=duration_to_stop
        )
        user_id = (
            current_user.id
            if loc.id == new_pickup_location.id
            else all_passengers_by_loc_id[loc.id]
        )
        updated_codriver_arrival_times[str(user_id)] = PassengerArrival(
            date=passenger_arrival_datetime.date(),
            time=passenger_arrival_datetime.time(),
        )

    route_update_obj = RouteUpdate(
        geometry=final_route_data["features"][0]["geometry"]["coordinates"],
        distance_meters=round(summary["distance"]),
        duration_seconds=round(summary["duration"]),
        codriver_arrival_times=updated_codriver_arrival_times,
        updated_ride_departure_date=new_departure_datetime.date(),
        updated_ride_departure_time=new_departure_datetime.time(),
    )

    current_user_arrival = updated_codriver_arrival_times[str(current_user.id)]
    codrive_db = Codrive(
        user_id=current_user.id,
        ride_id=ride.id,
        location_id=new_pickup_location.id,
        arrival_date=current_user_arrival.date,
        arrival_time=current_user_arrival.time,
        point_contribution=round(added_distance / 100),
        message=codrive_in.message,
        route_update=route_update_obj.model_dump(mode="json"),
    )
    session.add(codrive_db)
    session.commit()
    session.refresh(codrive_db)

    db_route_update = RouteUpdate.model_validate(codrive_db.route_update)
    user_ids_to_fetch = [
        uuid.UUID(uid) for uid in db_route_update.codriver_arrival_times
    ]
    users = session.exec(select(User).where(User.id.in_(user_ids_to_fetch))).all()  # type: ignore[attr-defined]
    users_by_id = {str(user.id): user for user in users}

    locations_by_user_id = {str(c.user_id): c.location for c in accepted_codrives}
    locations_by_user_id[str(current_user.id)] = new_pickup_location

    passenger_arrivals: list[PassengerArrivalTime] = []
    for (
        user_id_str,
        arrival_details,
    ) in db_route_update.codriver_arrival_times.items():
        user_obj = users_by_id.get(user_id_str)
        location_obj = locations_by_user_id.get(user_id_str)
        if user_obj and location_obj:
            passenger_arrivals.append(
                PassengerArrivalTime(
                    user=UserPublic.model_validate(user_obj),
                    location=LocationPublic.model_validate(location_obj),
                    arrival_date=arrival_details.date,
                    arrival_time=arrival_details.time,
                )
            )

    route_update_public = RouteUpdatePublic(
        geometry=db_route_update.geometry,
        distance_meters=db_route_update.distance_meters,
        duration_seconds=db_route_update.duration_seconds,
        updated_ride_departure_date=db_route_update.updated_ride_departure_date,
        updated_ride_departure_time=db_route_update.updated_ride_departure_time,
        codriver_arrival_times=passenger_arrivals,
    )

    return CodrivePublic(
        id=codrive_db.id,
        user_id=codrive_db.user_id,
        ride_id=codrive_db.ride_id,
        location=LocationPublic.model_validate(new_pickup_location),
        accepted=codrive_db.accepted,
        paid=codrive_db.paid,
        point_contribution=codrive_db.point_contribution,
        route_update=route_update_public,
    )


@router.get("/{codrive_id}", response_model=CodrivePublic)
def read_codrive(
    *, session: SessionDep, current_user: CurrentUser, codrive_id: uuid.UUID
) -> Any:
    """
    Get a specific codrive by its ID. Can be viewed by the passenger or the driver.
    """
    codrive = session.get(
        Codrive,
        codrive_id,
        options=[
            selectinload(Codrive.user).options(selectinload(User.location)),
            selectinload(Codrive.location),
            selectinload(Codrive.ride).options(
                selectinload(Ride.driver),
                selectinload(Ride.codrives).options(
                    selectinload(Codrive.user), selectinload(Codrive.location)
                ),
            ),
        ],
    )

    if not codrive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Codrive not found"
        )

    if current_user.id != codrive.user_id and current_user.id != codrive.ride.driver_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this codrive.",
        )

    if not codrive.route_update:
        return CodrivePublic.model_validate(codrive, update={"route_update": None})

    db_route_update = RouteUpdate.model_validate(codrive.route_update)

    all_codrives_on_ride = codrive.ride.codrives
    users_by_id = {str(c.user_id): c.user for c in all_codrives_on_ride}
    locations_by_user_id = {str(c.user_id): c.location for c in all_codrives_on_ride}
    users_by_id[str(codrive.user_id)] = codrive.user
    locations_by_user_id[str(codrive.user_id)] = codrive.location

    passenger_arrivals: list[PassengerArrivalTime] = []
    for (
        user_id_str,
        arrival_details,
    ) in db_route_update.codriver_arrival_times.items():
        user_obj = users_by_id.get(user_id_str)
        location_obj = locations_by_user_id.get(user_id_str)
        if user_obj and location_obj:
            passenger_arrivals.append(
                PassengerArrivalTime(
                    user=UserPublic.model_validate(user_obj),
                    location=LocationPublic.model_validate(location_obj),
                    arrival_date=arrival_details.date,
                    arrival_time=arrival_details.time,
                )
            )

    route_update_public = RouteUpdatePublic.model_validate(
        db_route_update, update={"codriver_arrival_times": passenger_arrivals}
    )

    return CodrivePublic.model_validate(
        codrive, update={"route_update": route_update_public}
    )


@router.patch("/{codrive_id}/accept", response_model=RidePublic)
def accept_codrive(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    ors_client: ORS_Client,
    codrive_id: uuid.UUID,
) -> Any:
    codrive_to_accept = session.get(
        Codrive,
        codrive_id,
        options=[
            selectinload(Codrive.ride).options(  # type: ignore[arg-type]
                selectinload(Ride.driver).options(selectinload(User.location)),  # type: ignore[arg-type]
                selectinload(Ride.car),  # type: ignore[arg-type]
                selectinload(Ride.start_location),  # type: ignore[arg-type]
                selectinload(Ride.end_location),  # type: ignore[arg-type]
                selectinload(Ride.codrives).options(  # type: ignore[arg-type]
                    selectinload(Codrive.user).options(selectinload(User.location)),  # type: ignore[arg-type]
                    selectinload(Codrive.location),  # type: ignore[arg-type]
                ),
            )
        ],
    )
    if not codrive_to_accept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Codrive request not found."
        )

    ride = codrive_to_accept.ride
    if ride.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not your ride."
        )
    if codrive_to_accept.accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Request already accepted."
        )
    if ride.n_codrives >= ride.max_n_codrives:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Ride is full."
        )

    update_data = RouteUpdate.model_validate(codrive_to_accept.route_update)

    ride.route_geometry = update_data.geometry
    ride.estimated_distance_meters = update_data.distance_meters
    ride.estimated_duration_seconds = update_data.duration_seconds
    ride.departure_date = update_data.updated_ride_departure_date
    ride.departure_time = update_data.updated_ride_departure_time
    ride.n_codrives += 1
    ride.total_points += codrive_to_accept.point_contribution

    codrive_to_accept.accepted = True
    codrive_to_accept.route_update = None  # Clear the proposal

    for codrive in ride.codrives:
        if not codrive.accepted and codrive.id != codrive_to_accept.id:
            continue
        user_id_str = str(codrive.user_id)
        if user_id_str in update_data.codriver_arrival_times:
            arrival_details = update_data.codriver_arrival_times[user_id_str]
            codrive.arrival_date = arrival_details.date
            codrive.arrival_time = arrival_details.time
            session.add(codrive)

    session.add(codrive_to_accept)
    session.add(ride)

    # Update other pending requests
    pending_requests = [
        c for c in ride.codrives if not c.accepted and c.id != codrive_to_accept.id
    ]
    if pending_requests:
        accepted_codrives = [c for c in ride.codrives if c.accepted] + [
            codrive_to_accept
        ]
        accepted_codrive_locations = [c.location for c in accepted_codrives]
        for pending_codrive in pending_requests:
            all_passengers_by_loc_id = {
                c.location_id: c.user_id for c in accepted_codrives
            }
            all_pickup_locations = (
                [ride.start_location]
                + accepted_codrive_locations
                + [pending_codrive.location]
            )
            projections: list[Projection] = [
                {
                    "location": loc,
                    "proj_dist": get_projection_distance(
                        (loc.longitude, loc.latitude), ride.route_geometry
                    ),
                }
                for loc in all_pickup_locations
            ]
            projections.sort(key=lambda x: x["proj_dist"])
            ordered_pickup_locations = [p["location"] for p in projections]
            final_route_locations = ordered_pickup_locations + [ride.end_location]
            final_route_coords = [
                (loc.longitude, loc.latitude) for loc in final_route_locations
            ]
            try:
                final_route_data = ors_client.directions(
                    coordinates=final_route_coords,
                    format="geojson",
                    profile="driving-car",
                )
            except openrouteservice.exceptions.ApiError:
                continue

            summary = final_route_data["features"][0]["properties"]["summary"]
            added_distance = summary["distance"] - ride.estimated_distance_meters
            new_duration = datetime.timedelta(seconds=summary["duration"])
            arrival_datetime = datetime.datetime.combine(
                ride.arrival_date, ride.arrival_time
            )
            new_departure_datetime = arrival_datetime - new_duration
            segments = final_route_data["features"][0]["properties"]["segments"]
            updated_codriver_arrival_times: dict[str, PassengerArrival] = {}
            duration_to_stop = 0.0
            for i, loc in enumerate(ordered_pickup_locations):
                if i == 0:
                    continue
                duration_to_stop += segments[i - 1]["duration"]
                passenger_arrival_datetime = (
                    new_departure_datetime
                    + datetime.timedelta(seconds=duration_to_stop)
                )
                user_id = (
                    pending_codrive.user_id
                    if loc.id == pending_codrive.location_id
                    else all_passengers_by_loc_id.get(loc.id)
                )
                if user_id:
                    updated_codriver_arrival_times[str(user_id)] = PassengerArrival(
                        date=passenger_arrival_datetime.date(),
                        time=passenger_arrival_datetime.time(),
                    )
            route_update_obj = RouteUpdate(
                geometry=final_route_data["features"][0]["geometry"]["coordinates"],
                distance_meters=round(summary["distance"]),
                duration_seconds=round(summary["duration"]),
                codriver_arrival_times=updated_codriver_arrival_times,
                updated_ride_departure_date=new_departure_datetime.date(),
                updated_ride_departure_time=new_departure_datetime.time(),
            )
            pending_codrive.route_update = route_update_obj.model_dump(mode="json")
            pending_codrive.point_contribution = round(added_distance / 100)
            user_arrival = updated_codriver_arrival_times[str(pending_codrive.user_id)]
            pending_codrive.arrival_date = user_arrival.date
            pending_codrive.arrival_time = user_arrival.time
            session.add(pending_codrive)

    session.commit()
    session.refresh(ride)

    accepted_codrives_public = []
    requested_codrives_public = []

    users_by_id = {str(ride.driver.id): UserPublic.model_validate(ride.driver)}
    for c in ride.codrives:
        users_by_id[str(c.user_id)] = UserPublic.model_validate(c.user)

    locations_by_user_id = {str(c.user_id): c.location for c in ride.codrives}

    for codrive in ride.codrives:
        if codrive.accepted:
            accepted_codrives_public.append(CodrivePassenger.model_validate(codrive))
        elif codrive.route_update:
            db_route_update = RouteUpdate.model_validate(codrive.route_update)
            passenger_arrivals: list[PassengerArrivalTime] = []
            for (
                user_id_str,
                arrival_details,
            ) in db_route_update.codriver_arrival_times.items():
                user_public_obj = users_by_id.get(user_id_str)
                location_obj = locations_by_user_id.get(user_id_str)
                if user_public_obj and location_obj:
                    passenger_arrivals.append(
                        PassengerArrivalTime(
                            user=user_public_obj,
                            location=LocationPublic.model_validate(location_obj),
                            arrival_date=arrival_details.date,
                            arrival_time=arrival_details.time,
                        )
                    )
            route_update_public = RouteUpdatePublic(
                geometry=db_route_update.geometry,
                distance_meters=db_route_update.distance_meters,
                duration_seconds=db_route_update.duration_seconds,
                updated_ride_departure_date=db_route_update.updated_ride_departure_date,
                updated_ride_departure_time=db_route_update.updated_ride_departure_time,
                codriver_arrival_times=passenger_arrivals,
            )
            requested_codrives_public.append(
                CodriveRequestPublic(
                    id=codrive.id,
                    user=UserPublic.model_validate(codrive.user),
                    location=LocationPublic.model_validate(codrive.location),
                    route_update=route_update_public,
                    point_contribution=codrive.point_contribution,
                    message=codrive.message,
                )
            )

    return RidePublic.model_validate(
        ride,
        update={
            "codrives": accepted_codrives_public,
            "requested_codrives": requested_codrives_public,
        },
    )

@router.delete("/{codrive_id}/own", response_model=Any)
def delete_own_codrive(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    ors_client: ORS_Client,
    codrive_id: uuid.UUID,
) -> Any:
    """
    Delete your own codrive request or leave a ride you already joined.
    If the request was not accepted, it is simply deleted.
    If you leave an accepted ride, the ride is recalculated and returned.
    """
    codrive_to_delete = session.get(
        Codrive,
        codrive_id,
        options=[
            selectinload(Codrive.ride).options(
                selectinload(Ride.driver).options(selectinload(User.location)),
                selectinload(Ride.car),
                selectinload(Ride.start_location),
                selectinload(Ride.end_location),
                selectinload(Ride.codrives).options(
                    selectinload(Codrive.user).options(selectinload(User.location)),
                    selectinload(Codrive.location),
                ),
            )
        ],
    )
    if not codrive_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Codrive request not found."
        )

    if codrive_to_delete.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own codrive requests.",
        )

    ride = codrive_to_delete.ride

    if not codrive_to_delete.accepted:
        session.delete(codrive_to_delete)
        session.commit()
        return Message(message="Your codrive request has been withdrawn.")

    # --- User is leaving an accepted ride, recalculations are needed ---

    ride.n_codrives -= 1
    ride.total_points -= codrive_to_delete.point_contribution

    remaining_codrives = [c for c in ride.codrives if c.id != codrive_to_delete.id]
    accepted_codrives = [c for c in remaining_codrives if c.accepted]
    pending_requests = [c for c in remaining_codrives if not c.accepted]

    all_accepted_locations = [ride.start_location] + [
        c.location for c in accepted_codrives
    ]

    # Recalculate the main ride route with the remaining accepted passengers
    final_route_coords = [
        (loc.longitude, loc.latitude) for loc in all_accepted_locations
    ] + [(ride.end_location.longitude, ride.end_location.latitude)]

    try:
        new_route_data = ors_client.directions(
            coordinates=final_route_coords, format="geojson", profile="driving-car"
        )
    except openrouteservice.exceptions.ApiError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not calculate a new route for the remaining passengers.",
        )

    summary = new_route_data["features"][0]["properties"]["summary"]
    new_duration = datetime.timedelta(seconds=summary["duration"])
    arrival_datetime = datetime.datetime.combine(ride.arrival_date, ride.arrival_time)
    new_departure_datetime = arrival_datetime - new_duration

    ride.route_geometry = new_route_data["features"][0]["geometry"]["coordinates"]
    ride.estimated_distance_meters = round(summary["distance"])
    ride.estimated_duration_seconds = round(summary["duration"])
    ride.departure_date = new_departure_datetime.date()
    ride.departure_time = new_departure_datetime.time()

    # Update arrival times for remaining accepted codrivers
    if accepted_codrives:
        segments = new_route_data["features"][0]["properties"]["segments"]
        duration_to_stop = 0.0
        # The new route has n-1 segments for n accepted locations.
        # The loop should go over the remaining accepted codrives.
        # `all_accepted_locations` starts with the driver, so we have to align.
        for i, codrive in enumerate(accepted_codrives):
            # The duration to the first passenger is in segments[0].
            duration_to_stop += segments[i]["duration"]
            passenger_arrival_dt = new_departure_datetime + datetime.timedelta(
                seconds=duration_to_stop
            )
            codrive.arrival_date = passenger_arrival_dt.date()
            codrive.arrival_time = passenger_arrival_dt.time()
            session.add(codrive)

    # Update all pending requests based on the new ride state
    if pending_requests:
        for pending_codrive in pending_requests:
            passengers_for_proposal_by_loc_id = {
                c.location_id: c.user_id for c in accepted_codrives
            }
            proposal_pickup_locs = all_accepted_locations + [pending_codrive.location]

            projections: list[Projection] = [
                {
                    "location": loc,
                    "proj_dist": get_projection_distance(
                        (loc.longitude, loc.latitude), ride.route_geometry
                    ),
                }
                for loc in proposal_pickup_locs
            ]
            projections.sort(key=lambda x: x["proj_dist"])
            ordered_pickup_locations = [p["location"] for p in projections]

            proposal_route_coords = [
                (loc.longitude, loc.latitude) for loc in ordered_pickup_locations
            ] + [(ride.end_location.longitude, ride.end_location.latitude)]

            try:
                # FIX: Added format="geojson" and profile="driving-car"
                proposal_route_data = ors_client.directions(
                    coordinates=proposal_route_coords,
                    format="geojson",
                    profile="driving-car",
                )
            except openrouteservice.exceptions.ApiError:
                # If a route can't be found for this pending request, we can't create a valid proposal
                continue

            proposal_summary = proposal_route_data["features"][0]["properties"][
                "summary"
            ]
            added_distance = proposal_summary["distance"] - ride.estimated_distance_meters
            proposal_duration = datetime.timedelta(seconds=proposal_summary["duration"])
            proposal_departure_datetime = arrival_datetime - proposal_duration

            proposal_segments = proposal_route_data["features"][0]["properties"][
                "segments"
            ]
            updated_codriver_arrival_times: dict[str, PassengerArrival] = {}
            duration_to_stop = 0.0
            for i, loc in enumerate(ordered_pickup_locations):
                if i == 0:
                    continue
                duration_to_stop += proposal_segments[i - 1]["duration"]
                arrival_dt = proposal_departure_datetime + datetime.timedelta(
                    seconds=duration_to_stop
                )
                user_id = (
                    pending_codrive.user_id
                    if loc.id == pending_codrive.location_id
                    else passengers_for_proposal_by_loc_id.get(loc.id)
                )
                if user_id:
                    updated_codriver_arrival_times[str(user_id)] = PassengerArrival(
                        date=arrival_dt.date(), time=arrival_dt.time()
                    )

            route_update_obj = RouteUpdate(
                geometry=proposal_route_data["features"][0]["geometry"]["coordinates"],
                distance_meters=round(proposal_summary["distance"]),
                duration_seconds=round(proposal_summary["duration"]),
                codriver_arrival_times=updated_codriver_arrival_times,
                updated_ride_departure_date=proposal_departure_datetime.date(),
                updated_ride_departure_time=proposal_departure_datetime.time(),
            )

            pending_codrive.route_update = route_update_obj.model_dump(mode="json")
            pending_codrive.point_contribution = round(added_distance / 100)
            user_arrival = updated_codriver_arrival_times[str(pending_codrive.user_id)]
            pending_codrive.arrival_date = user_arrival.date
            pending_codrive.arrival_time = user_arrival.time
            session.add(pending_codrive)

    session.delete(codrive_to_delete)
    session.add(ride)
    session.commit()

    # Re-fetch the ride with all its relations to build the final object
    final_ride = session.get(
        Ride,
        ride.id,
        options=[
            selectinload(Ride.driver).options(selectinload(User.location)),
            selectinload(Ride.car),
            selectinload(Ride.start_location),
            selectinload(Ride.end_location),
            selectinload(Ride.codrives).options(
                selectinload(Codrive.user).options(selectinload(User.location)),
                selectinload(Codrive.location),
            ),
        ],
    )
    if not final_ride:  # Should not happen, but for type safety
        raise HTTPException(status_code=500, detail="Failed to retrieve updated ride.")

    # --- Construction logic from read_ride_by_id to return the updated RidePublic ---
    accepted_codrives_public = []
    requested_codrives_public = []

    users_by_id = {
        str(final_ride.driver.id): UserPublic.model_validate(final_ride.driver)
    }
    for c in final_ride.codrives:
        users_by_id[str(c.user_id)] = UserPublic.model_validate(c.user)
    locations_by_user_id = {str(c.user_id): c.location for c in final_ride.codrives}

    for codrive in final_ride.codrives:
        if codrive.accepted:
            accepted_codrives_public.append(CodrivePassenger.model_validate(codrive))
        elif codrive.route_update:
            db_route_update = RouteUpdate.model_validate(codrive.route_update)
            passenger_arrivals: list[PassengerArrivalTime] = []
            for (
                user_id_str,
                arrival_details,
            ) in db_route_update.codriver_arrival_times.items():
                user_public_obj = users_by_id.get(user_id_str)
                location_obj = locations_by_user_id.get(user_id_str)
                if user_public_obj and location_obj:
                    passenger_arrivals.append(
                        PassengerArrivalTime(
                            user=user_public_obj,
                            location=LocationPublic.model_validate(location_obj),
                            arrival_date=arrival_details.date,
                            arrival_time=arrival_details.time,
                        )
                    )

            route_update_public = RouteUpdatePublic(
                geometry=db_route_update.geometry,
                distance_meters=db_route_update.distance_meters,
                duration_seconds=db_route_update.duration_seconds,
                updated_ride_departure_date=db_route_update.updated_ride_departure_date,
                updated_ride_departure_time=db_route_update.updated_ride_departure_time,
                codriver_arrival_times=passenger_arrivals,
            )
            requested_codrives_public.append(
                CodriveRequestPublic(
                    id=codrive.id,
                    user=UserPublic.model_validate(codrive.user),
                    location=LocationPublic.model_validate(codrive.location),
                    route_update=route_update_public,
                    point_contribution=codrive.point_contribution,
                    message=codrive.message,
                )
            )

    return RidePublic.model_validate(
        final_ride,
        update={
            "codrives": accepted_codrives_public,
            "requested_codrives": requested_codrives_public,
        },
    )


@router.delete("/{codrive_id}/passenger", response_model=Message)
def refuse_codrive_request(
    *, session: SessionDep, current_user: CurrentUser, codrive_id: uuid.UUID
) -> Message:
    """
    Refuse a passenger's request to join your ride.
    """
    codrive = session.get(Codrive, codrive_id, options=[selectinload(Codrive.ride)])
    if not codrive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Codrive request not found."
        )
    if codrive.ride.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the driver of this ride.",
        )
    if codrive.accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot refuse a request that has already been accepted.",
        )

    session.delete(codrive)
    session.commit()

    return Message(message="Codrive request has been refused and deleted.")
