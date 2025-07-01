import datetime
import uuid
from typing import Optional

from pydantic import EmailStr
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    user_name: str = Field(unique=True, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    user_name: str = Field(max_length=255)


# Properties to receive via API on update, all are optional
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


# Database model, database table inferred from class name
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

    stops: list["Stop"] = Relationship(back_populates="user")

    rides: list["Ride"] = Relationship(back_populates="driver")

    points: int = Field(default=0)

    profile_picture: bytes | None = None
    has_license: bool = Field(default=False)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    location: Optional["LocationPublic"]
    has_license: bool


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


class Stop(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="stops")

    ride_id: uuid.UUID = Field(foreign_key="ride.id")
    ride: "Ride" = Relationship(back_populates="stops")

    location_id: uuid.UUID = Field(foreign_key="location.id")
    location: "Location" = Relationship(back_populates="stops")

    time_of_arrival: datetime.datetime = Field()


class Location(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    inhabitants: list["User"] = Relationship(back_populates="location")

    stops: list["Stop"] = Relationship(back_populates="location")

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
    city: str
    street: str
    house_number: str
    latitude: float
    longitude: float


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
    recurring_id: uuid.UUID | None = Field(default=None)

    driver_id: uuid.UUID = Field(foreign_key="user.id")
    driver: "User" = Relationship(back_populates="rides")

    car_id: uuid.UUID = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="rides")

    stops: list["Stop"] = Relationship(back_populates="ride")

    start_location_id: uuid.UUID = Field(foreign_key="location.id")
    end_location_id: uuid.UUID = Field(foreign_key="location.id")

    start_location: Optional["Location"] = Relationship(
        back_populates="ride_starts",
        sa_relationship_kwargs={"foreign_keys": "[Ride.start_location_id]"},
    )
    end_location: Optional["Location"] = Relationship(
        back_populates="ride_ends",
        sa_relationship_kwargs={"foreign_keys": "[Ride.end_location_id]"},
    )

    recurring_mon: bool = Field(default=False)
    recurring_tue: bool = Field(default=False)
    recurring_wed: bool = Field(default=False)
    recurring_thu: bool = Field(default=False)
    recurring_fri: bool = Field(default=False)
    recurring_sat: bool = Field(default=False)
    recurring_sun: bool = Field(default=False)

    n_co_driver: int = Field()
    max_request_distance: float | None = Field()

    starting_time: datetime.datetime = Field()
    time_of_arrival: datetime.datetime = Field()

    route_geometry: list[list[float]] = Field(default=[], sa_column=Column(JSON))
    estimated_duration_seconds: int = Field()
    estimated_distance_meters: int = Field()


class RideCreate(SQLModel):
    """Properties to receive via API on ride creation."""

    car_id: uuid.UUID
    n_co_driver: int
    max_request_distance: float | None

    starting_time: datetime.datetime | None
    arrival_time: datetime.datetime | None

    start_location: LocationCreate
    end_location: LocationCreate

    recurring_mon: bool = False
    recurring_tue: bool = False
    recurring_wed: bool = False
    recurring_thu: bool = False
    recurring_fri: bool = False
    recurring_sat: bool = False
    recurring_sun: bool = False


class RidePublic(SQLModel):
    """Properties to return via API for a single ride."""

    id: uuid.UUID
    driver_id: uuid.UUID
    car_id: uuid.UUID
    starting_time: datetime.datetime
    time_of_arrival: datetime.datetime
    n_co_driver: int

    start_location: LocationPublic
    end_location: LocationPublic

    route_geometry: list[list[float]]
    max_request_distance: float | None
    estimated_duration_seconds: int
    estimated_distance_meters: float

    recurring_mon: bool
    recurring_tue: bool
    recurring_wed: bool
    recurring_thu: bool
    recurring_fri: bool
    recurring_sat: bool
    recurring_sun: bool


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
