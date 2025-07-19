import datetime
import uuid
from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlmodel import JSON, Column, DateTime, Field, Relationship, SQLModel, text


class UserBonusLink(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    bonus_id: uuid.UUID = Field(foreign_key="bonus.id")
    redemption_time: datetime.datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("TIMEZONE('Europe/Berlin', now())"),
            nullable=False,
        )
    )


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    user_name: str = Field(unique=True, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    user_name: str = Field(max_length=255)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    user_name: str | None = Field(default=None, max_length=255)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    location: Optional["LocationCreate"] = Field(default=None)
    has_license: bool | None = Field(default=None)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

    location_id: uuid.UUID | None = Field(default=None, foreign_key="location.id")
    location: Optional["Location"] = Relationship(back_populates="inhabitants")

    cars: list["Car"] = Relationship(back_populates="owner")

    ratings: list["Rating"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[Rating.user_id]"},
    )
    given_ratings: list["Rating"] = Relationship(
        back_populates="rater",
        sa_relationship_kwargs={"foreign_keys": "[Rating.rater_id]"},
    )

    codrives: list["Codrive"] = Relationship(back_populates="user")

    rides: list["Ride"] = Relationship(back_populates="driver")

    points: int = Field(default=0)
    cash: float = Field(default=0.0)
    bonuses: list["Bonus"] = Relationship(
        back_populates="assigned_user", link_model=UserBonusLink
    )
    avg_rating: float = Field(default=0.0)
    n_ratings: int = Field(default=0)

    profile_picture: bytes | None = None
    profile_picture_content_type: str | None = Field(default=None)
    has_license: bool = Field(default=False)


class UserPublic(UserBase):
    id: uuid.UUID
    location: Optional["LocationPublic"]
    has_license: bool
    points: int
    avg_rating: float
    n_ratings: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class Car(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    owner_id: uuid.UUID = Field(foreign_key="user.id")
    owner: "User" = Relationship(back_populates="cars")

    n_seats: int = Field()
    model: str | None = Field(default=None, max_length=255)
    brand: str | None = Field(default=None, max_length=255)
    color: str | None = Field(default=None, max_length=255)
    license_plate: str | None = Field(default=None, max_length=255)

    rides: list["Ride"] = Relationship(back_populates="car")


class CarCreate(SQLModel):
    n_seats: int = Field()
    model: str | None = Field(default=None, max_length=255)
    brand: str | None = Field(default=None, max_length=255)
    color: str | None = Field(default=None, max_length=255)
    license_plate: str | None = Field(default=None, max_length=255)


class CarUpdate(SQLModel):
    n_seats: int | None = Field(default=None)
    model: str | None = Field(default=None, max_length=255)
    brand: str | None = Field(default=None, max_length=255)
    color: str | None = Field(default=None, max_length=255)
    license_plate: str | None = Field(default=None, max_length=255)


class CarPublic(SQLModel):
    id: uuid.UUID
    n_seats: int
    model: str | None
    brand: str | None
    color: str | None


class Bonus(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(default=None, max_length=255)
    cost: int = Field(default=None)
    assigned_user: list["User"] = Relationship(
        back_populates="bonuses", link_model=UserBonusLink
    )


class BonusCreate(SQLModel):
    name: str = Field(default=None, max_length=255)
    cost: int = Field(default=None)


class BonusUpdate(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(default=None, max_length=255)
    cost: int = Field(default=None)


class BonusPublic(SQLModel):
    id: uuid.UUID
    name: str | None
    cost: int | None


class RedeemedBonusPublic(SQLModel):
    id: uuid.UUID
    name: str | None
    cost: int | None
    redemption_time: datetime.datetime | None


class Location(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    inhabitants: list["User"] = Relationship(back_populates="location")

    codrives: list["Codrive"] = Relationship(back_populates="location")

    ride_starts: list["Ride"] = Relationship(
        back_populates="start_location",
        sa_relationship_kwargs={"foreign_keys": "[Ride.start_location_id]"},
    )
    ride_ends: list["Ride"] = Relationship(
        back_populates="end_location",
        sa_relationship_kwargs={"foreign_keys": "[Ride.end_location_id]"},
    )

    country: str = Field(max_length=255)
    postal_code: str = Field(min_length=5, max_length=5)
    city: str = Field(max_length=255)
    street: str = Field(max_length=255)
    house_number: str = Field(max_length=10)

    latitude: float = Field(index=True)
    longitude: float = Field(index=True)


class LocationCreate(SQLModel):
    """Schema for receiving address information via API."""

    country: str = Field(max_length=255)
    postal_code: str = Field(min_length=5, max_length=5)
    city: str = Field(max_length=255)
    street: str = Field(max_length=255)
    house_number: str = Field(max_length=10)


class LocationPublic(SQLModel):
    id: uuid.UUID
    country: str
    postal_code: str
    city: str
    street: str
    house_number: str
    latitude: float
    longitude: float


class PassengerArrival(SQLModel):
    date: datetime.date
    time: datetime.time


class RouteUpdate(SQLModel):
    geometry: list[list[float]]
    distance_meters: int
    duration_seconds: int
    codriver_arrival_times: dict[str, PassengerArrival]
    updated_ride_departure_date: datetime.date
    updated_ride_departure_time: datetime.time


class PassengerArrivalTime(SQLModel):
    user: UserPublic
    location: LocationPublic
    arrival_date: datetime.date
    arrival_time: datetime.time


class RouteUpdatePublic(SQLModel):
    geometry: list[list[float]]
    distance_meters: int
    duration_seconds: int
    codriver_arrival_times: list[PassengerArrivalTime]
    updated_ride_departure_date: datetime.date
    updated_ride_departure_time: datetime.time


class Codrive(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="codrives")
    ride_id: uuid.UUID = Field(foreign_key="ride.id")
    ride: "Ride" = Relationship(back_populates="codrives")
    location_id: uuid.UUID = Field(foreign_key="location.id")
    location: "Location" = Relationship(back_populates="codrives")
    n_passengers: int = Field(default=1)
    arrival_date: datetime.date = Field()
    arrival_time: datetime.time = Field()
    point_contribution: int = Field(default=0)
    message: str | None = Field(default=None)
    route_update: RouteUpdate | None = Field(default=None, sa_column=Column(JSON))
    accepted: bool = Field(default=False)
    paid: bool = Field(default=False)
    rating_given: bool = Field(default=False)


class CodriveCreate(SQLModel):
    location: LocationCreate
    message: str | None = Field(default=None)
    n_passengers: int = Field(default=1, ge=1)


class CodriveCostPreview(SQLModel):
    point_contribution: int
    added_distance_meters: int


class CodrivePay(SQLModel):
    rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="Optional rating for the driver from 1 to 5.",
    )


class CodrivePublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    ride_id: uuid.UUID
    location: LocationPublic
    n_passengers: int
    accepted: bool
    paid: bool
    point_contribution: int
    route_update: RouteUpdatePublic | None


class CodrivePassenger(SQLModel):
    id: uuid.UUID
    user: UserPublic
    location: LocationPublic
    arrival_date: datetime.date
    arrival_time: datetime.time
    point_contribution: int
    n_passengers: int


class CodriveRequestPublic(SQLModel):
    id: uuid.UUID
    user: UserPublic
    location: LocationPublic
    route_update: RouteUpdatePublic
    point_contribution: int
    n_passengers: int
    message: str | None = Field(default=None)


class Rating(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(
        back_populates="ratings",
        sa_relationship_kwargs={"foreign_keys": "[Rating.user_id]"},
    )

    rater_id: uuid.UUID = Field(foreign_key="user.id")
    rater: "User" = Relationship(
        back_populates="given_ratings",
        sa_relationship_kwargs={"foreign_keys": "[Rating.rater_id]"},
    )

    rating_value: int = Field(nullable=False)


class Ride(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    driver_id: uuid.UUID = Field(foreign_key="user.id")
    driver: "User" = Relationship(back_populates="rides")

    car_id: uuid.UUID = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="rides")

    codrives: list["Codrive"] = Relationship(
        back_populates="ride", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    n_codrives: int = Field(default=0)
    total_points: int = Field(default=0)

    start_location_id: uuid.UUID = Field(foreign_key="location.id")
    end_location_id: uuid.UUID = Field(foreign_key="location.id")

    start_location: "Location" = Relationship(
        back_populates="ride_starts",
        sa_relationship_kwargs={"foreign_keys": "[Ride.start_location_id]"},
    )
    end_location: "Location" = Relationship(
        back_populates="ride_ends",
        sa_relationship_kwargs={"foreign_keys": "[Ride.end_location_id]"},
    )

    max_n_codrives: int = Field()
    max_request_distance: float | None = Field()

    departure_date: datetime.date = Field()
    departure_time: datetime.time = Field()
    arrival_date: datetime.date = Field()
    arrival_time: datetime.time = Field()

    route_geometry: list[list[float]] = Field(default=[], sa_column=Column(JSON))
    estimated_duration_seconds: int = Field()
    estimated_distance_meters: int = Field()
    completed: bool = Field(default=False)


class RideCreate(SQLModel):
    """Properties to receive via API on ride creation."""

    car_id: uuid.UUID
    max_n_codrives: int
    max_request_distance: float | None

    arrival_date: datetime.date
    arrival_time: datetime.time

    start_location: LocationCreate
    end_location: LocationCreate


class RideUpdate(SQLModel):
    """Properties to receive via API on ride update."""

    car_id: uuid.UUID | None = None
    max_n_codrives: int | None = None
    max_request_distance: float | None = None


class RidePublic(SQLModel):
    """Properties to return via API for a single ride, including related data."""

    id: uuid.UUID
    driver: UserPublic
    car: CarPublic
    codrives: list[CodrivePassenger]
    requested_codrives: list[CodriveRequestPublic]

    departure_date: datetime.date
    departure_time: datetime.time
    arrival_date: datetime.date
    arrival_time: datetime.time

    max_n_codrives: int
    n_codrives: int
    total_points: int

    start_location: LocationPublic
    end_location: LocationPublic

    route_geometry: list[list[float]]
    max_request_distance: float | None
    estimated_duration_seconds: int
    estimated_distance_meters: int
    completed: bool


class RidesPublic(SQLModel):
    data: list[RidePublic]
    count: int


class CodriveStatus(str, Enum):
    REQUESTED = "requested"
    ACCEPTED = "accepted"


class TimeFrame(str, Enum):
    PAST = "past"
    FUTURE = "future"


class UserCodrivePublic(SQLModel):
    """
    Represents a codrive from the user's perspective, containing the full ride context.
    """

    id: uuid.UUID
    accepted: bool
    paid: bool
    message: str | None
    point_contribution: int
    n_passengers: int
    route_update: RouteUpdatePublic | None = None
    ride: RidePublic


class UserCodrivesPublic(SQLModel):
    data: list[UserCodrivePublic]
    count: int


class Message(SQLModel):
    message: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
