import datetime
import math
import uuid
from typing import Any
from zoneinfo import ZoneInfo

import openrouteservice  # type: ignore
from fastapi import APIRouter, Body, HTTPException, Query, status
from sqlalchemy.orm import selectinload
from sqlmodel import func, or_, select
from sqlmodel.sql.expression import SelectOfScalar

from app.api.deps import (
    CurrentUser,
    ORS_Client,
    SessionDep,
)
from app.crud import get_or_create_location
from app.models import (
    Car,
    Codrive,
    CodrivePassenger,
    CodriveRequestPublic,
    Location,
    LocationPublic,
    Message,
    PassengerArrivalTime,
    Ride,
    RideCreate,
    RidePublic,
    RidesPublic,
    RideUpdate,
    RouteUpdate,
    RouteUpdatePublic,
    User,
    UserPublic,
)

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

    german_tz = ZoneInfo("Europe/Berlin")
    now_in_germany = datetime.datetime.now(german_tz)

    arrival_datetime = datetime.datetime.combine(
        ride_in.arrival_date, ride_in.arrival_time, tzinfo=german_tz
    )
    departure_datetime = arrival_datetime - estimated_duration

    if departure_datetime <= now_in_germany:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The calculated departure time is in the past. Please choose a later arrival time.",
        )

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
    ride_from_db = session.get(
        Ride,
        db_ride.id,
        options=[
            selectinload(Ride.driver).options(selectinload(User.location)),  # type: ignore[arg-type]
            selectinload(Ride.car),  # type: ignore[arg-type]
            selectinload(Ride.start_location),  # type: ignore[arg-type]
            selectinload(Ride.end_location),  # type: ignore[arg-type]
        ],
    )
    if not ride_from_db:
        raise HTTPException(status_code=500, detail="Could not retrieve created ride")

    return RidePublic.model_validate(
        ride_from_db, update={"codrives": [], "requested_codrives": []}
    )


def get_rides_statement() -> SelectOfScalar[Ride]:
    """Returns a statement to select rides with all related data eagerly loaded."""
    return select(Ride).options(
        selectinload(Ride.driver).options(selectinload(User.location)),  # type: ignore[arg-type]
        selectinload(Ride.car),  # type: ignore[arg-type]
        selectinload(Ride.start_location),  # type: ignore[arg-type]
        selectinload(Ride.end_location),  # type: ignore[arg-type]
        selectinload(Ride.codrives).options(  # type: ignore[arg-type]
            selectinload(Codrive.user).options(selectinload(User.location)),  # type: ignore[arg-type]
            selectinload(Codrive.location),  # type: ignore[arg-type]
        ),
    )


@router.get("/", response_model=RidesPublic)
def read_rides(
    session: SessionDep,
    ors_client: ORS_Client,
    offset: int = 0,
    limit: int = Query(default=100, le=200),
    earliest_arrival_date: datetime.date | None = Query(
        default=None, description="Filter for rides arriving on or after this date."
    ),
    latest_arrival_date: datetime.date | None = Query(
        default=None, description="Filter for rides arriving on or before this date."
    ),
    latest_arrival_time: datetime.time | None = Query(
        default=None,
        description="Filter for rides arriving on latest_arrival_date at or before this time. Requires latest_arrival_date to be set.",
    ),
    location_address: str | None = Query(
        default=None,
        description="An address to search for rides starting or ending nearby.",
    ),
    max_distance_km: float = Query(
        default=10.0,
        description="The maximum distance in km from the location_address to search for rides.",
    ),
) -> Any:
    """
    Get all rides, with optional filters for arrival time and location.
    """
    if latest_arrival_time and not latest_arrival_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="latest_arrival_time requires latest_arrival_date to be set.",
        )

    stmt = get_rides_statement()

    if earliest_arrival_date:
        stmt = stmt.where(Ride.arrival_date >= earliest_arrival_date)

    if latest_arrival_date:
        if latest_arrival_time:
            stmt = stmt.where(
                or_(
                    Ride.arrival_date < latest_arrival_date,
                    (Ride.arrival_date == latest_arrival_date)
                    & (Ride.arrival_time <= latest_arrival_time),
                )
            )
        else:
            stmt = stmt.where(Ride.arrival_date <= latest_arrival_date)

    if location_address:
        try:
            geocode = ors_client.pelias_search(text=location_address, size=1)
            lon, lat = geocode["features"][0]["geometry"]["coordinates"]
        except (openrouteservice.exceptions.ApiError, IndexError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not find coordinates for address: {location_address}",
            )

        lat_delta = max_distance_km / 111.0
        lon_delta = max_distance_km / (111.0 * math.cos(math.radians(lat)))

        nearby_loc_subquery = (
            select(Location.id)
            .where(Location.latitude.between(lat - lat_delta, lat + lat_delta))  # type: ignore[attr-defined]
            .where(Location.longitude.between(lon - lon_delta, lon + lon_delta))  # type: ignore[attr-defined]
        ).scalar_subquery()

        stmt = stmt.where(
            or_(
                Ride.start_location_id.in_(nearby_loc_subquery),  # type: ignore[attr-defined]
                Ride.end_location_id.in_(nearby_loc_subquery),  # type: ignore[attr-defined]
            )
        )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    count = session.exec(count_stmt).one()

    rides_stmt = stmt.offset(offset).limit(limit)
    rides = session.exec(rides_stmt).all()

    public_rides = []
    for ride in rides:
        accepted_codrives_public = []
        requested_codrives_public = []

        users_by_id = {str(ride.driver.id): UserPublic.model_validate(ride.driver)}
        for c in ride.codrives:
            users_by_id[str(c.user_id)] = UserPublic.model_validate(c.user)

        locations_by_user_id = {str(c.user_id): c.location for c in ride.codrives}

        for codrive in ride.codrives:
            if codrive.accepted:
                accepted_codrives_public.append(
                    CodrivePassenger.model_validate(codrive)
                )
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

        public_rides.append(
            RidePublic.model_validate(
                ride,
                update={
                    "codrives": accepted_codrives_public,
                    "requested_codrives": requested_codrives_public,
                },
            )
        )

    return RidesPublic(data=public_rides, count=count)


@router.get("/by_driver/{user_id}", response_model=RidesPublic)
def read_rides_by_driver(
    user_id: uuid.UUID,
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=200),
) -> Any:
    """
    Get all rides for a specific driver.
    """
    stmt = get_rides_statement().where(Ride.driver_id == user_id)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    count = session.exec(count_stmt).one()

    rides_stmt = stmt.offset(offset).limit(limit)
    rides = session.exec(rides_stmt).all()

    public_rides = []
    for ride in rides:
        accepted_codrives_public = []
        requested_codrives_public = []

        users_by_id = {str(ride.driver.id): UserPublic.model_validate(ride.driver)}
        for c in ride.codrives:
            users_by_id[str(c.user_id)] = UserPublic.model_validate(c.user)

        locations_by_user_id = {str(c.user_id): c.location for c in ride.codrives}

        for codrive in ride.codrives:
            if codrive.accepted:
                accepted_codrives_public.append(
                    CodrivePassenger.model_validate(codrive)
                )
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

        public_rides.append(
            RidePublic.model_validate(
                ride,
                update={
                    "codrives": accepted_codrives_public,
                    "requested_codrives": requested_codrives_public,
                },
            )
        )

    return RidesPublic(data=public_rides, count=count)


@router.get("/me", response_model=RidesPublic)
def read_own_rides(
    session: SessionDep,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = Query(default=100, le=200),
) -> Any:
    """
    Get all rides for the current user.
    """
    stmt = get_rides_statement().where(Ride.driver_id == current_user.id)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    count = session.exec(count_stmt).one()

    rides_stmt = stmt.offset(offset).limit(limit)
    rides = session.exec(rides_stmt).all()

    public_rides = []
    for ride in rides:
        accepted_codrives_public = []
        requested_codrives_public = []

        users_by_id = {str(ride.driver.id): UserPublic.model_validate(ride.driver)}
        for c in ride.codrives:
            users_by_id[str(c.user_id)] = UserPublic.model_validate(c.user)

        locations_by_user_id = {str(c.user_id): c.location for c in ride.codrives}

        for codrive in ride.codrives:
            if codrive.accepted:
                accepted_codrives_public.append(
                    CodrivePassenger.model_validate(codrive)
                )
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

        public_rides.append(
            RidePublic.model_validate(
                ride,
                update={
                    "codrives": accepted_codrives_public,
                    "requested_codrives": requested_codrives_public,
                },
            )
        )

    return RidesPublic(data=public_rides, count=count)


@router.get("/{ride_id}", response_model=RidePublic)
def read_ride_by_id(ride_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific ride by its ID.
    """
    stmt = get_rides_statement().where(Ride.id == ride_id)
    ride = session.exec(stmt).first()

    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found"
        )

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


@router.patch("/{ride_id}", response_model=RidePublic)
def update_ride(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    ride_id: uuid.UUID,
    ride_in: RideUpdate = Body(...),
) -> Any:
    """
    Update a ride's details. Only the driver can perform this action.
    """
    ride = session.get(Ride, ride_id)
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found"
        )
    if ride.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the driver of this ride.",
        )

    ride_data = ride_in.model_dump(exclude_unset=True)

    if "max_n_codrives" in ride_data and ride_data["max_n_codrives"] < ride.n_codrives:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"max_n_codrives cannot be less than the current number of accepted passengers ({ride.n_codrives}).",
        )

    if "car_id" in ride_data:
        car = session.get(Car, ride_data["car_id"])
        if not car or car.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found or you are not the owner.",
            )

    ride.sqlmodel_update(ride_data)
    session.add(ride)
    session.commit()
    session.refresh(ride)

    # Re-fetch with all relations to return the full public object
    updated_ride = session.exec(get_rides_statement().where(Ride.id == ride.id)).one()

    # Re-use the transformation logic from the read_ride_by_id endpoint
    return read_ride_by_id(ride_id=updated_ride.id, session=session)


@router.patch("/{ride_id}/complete", response_model=Message)
def complete_ride(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    ride_id: uuid.UUID,
) -> Message:
    """
    Mark a ride as completed. This can only be done by the driver after the ride's
    arrival time. Points will be transferred to the driver.
    """
    ride = session.get(
        Ride,
        ride_id,
        options=[
            selectinload(Ride.driver),  # type: ignore[arg-type]
            selectinload(Ride.codrives).options(selectinload(Codrive.user)),  # type: ignore[arg-type]
        ],
    )

    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found"
        )
    if ride.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the driver of this ride.",
        )
    if ride.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This ride has already been marked as completed.",
        )

    german_tz = ZoneInfo("Europe/Berlin")
    arrival_datetime = datetime.datetime.combine(
        ride.arrival_date, ride.arrival_time, tzinfo=german_tz
    )
    now_in_germany = datetime.datetime.now(german_tz)

    if arrival_datetime > now_in_germany:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot mark a ride as complete before its arrival time.",
        )

    ride.completed = True
    ride.driver.points += ride.total_points
    session.add(ride.driver)
    session.add(ride)
    session.commit()

    return Message(message="Ride marked as complete and points have been transferred.")


@router.delete("/{ride_id}", response_model=Message)
def delete_ride(
    *, session: SessionDep, current_user: CurrentUser, ride_id: uuid.UUID
) -> Message:
    """
    Delete a ride. This will also delete all associated codrive requests.
    """
    ride = session.get(Ride, ride_id)
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found"
        )
    if ride.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the driver of this ride.",
        )

    session.delete(ride)
    session.commit()
    return Message(message="Ride and all associated requests deleted successfully.")
