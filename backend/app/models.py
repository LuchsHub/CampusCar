import uuid
import datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


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


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    location_id: uuid.UUID = Field(foreign_key="location.id", unique=True)
    cars: list["Car"] = Relationship(back_populates="user")
    received_ratings: list["UserRating"] = Relationship(back_populates="user")

    hashed_password: str
    first_name: str
    last_name: str
    user_name: str

    # profile_picture
    email: str
    points: int
    rating: float


class Car(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="cars")

    n_seats: int
    model: str
    brand: str


class Stop(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship()
    ride_id: uuid.UUID = Field(foreign_key="ride.id")
    ride: "Ride" = Relationship(back_populates="stops")
    location_id: uuid.UUID = Field(foreign_key="location.id", unique=True)

    time_of_arrial: datetime.datetime


class Ride(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    serial_id: uuid.UUID

    driver: uuid.UUID = Field(foreign_key="user.id")
    car_id:  uuid.UUID = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="ride")
    stops: list["Stop"] = Relationship(back_populates="ride")
    start_location_id: uuid.UUID = Field(foreign_key="location.id", unique=True)
    start_location: "Location" = Relationship(back_populates="ride")
    end_location_id: uuid.UUID = Field(foreign_key="location.id", unique=True)
    end_location: "Location" = Relationship(back_populates="ride")

    recurring: bool
    n_co_driver: int
    starting_time: datetime.datetime
    time_of_arrial: datetime.datetime


class Location(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    postal_code: str
    city: str
    street: str


class UserRating(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="received_ratings")

    rater_id: uuid.UUID = Field(foreign_key="user.id")
    rater: "User" = Relationship()

    rating_value: int
