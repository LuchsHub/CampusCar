from typing import Any

import openrouteservice # type: ignore
from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Location, LocationCreate, User, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def get_or_create_location(
    address: LocationCreate,
    session: Session,
    ors_client: openrouteservice.Client,
) -> Location:
    statement = select(Location).where(
        Location.country == address.country,
        Location.street == address.street,
        Location.house_number == address.house_number,
        Location.postal_code == address.postal_code,
        Location.city == address.city,
    )
    db_location = session.exec(statement).first()

    if db_location:
        return db_location

    address_str = f"{address.street} {address.house_number}, {address.postal_code} {address.city}, {address.country}"
    geocode_result = ors_client.pelias_search(text=address_str, size=1)

    if not (geocode_result and geocode_result.get("features")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The provided address could not be found: '{address_str}'. "
            "Please check for typos or provide a valid address.",
        )

    lon, lat = geocode_result["features"][0]["geometry"]["coordinates"]

    new_location = Location.model_validate(
        address.model_dump(), update={"latitude": lat, "longitude": lon}
    )
    session.add(new_location)
    session.commit()
    session.refresh(new_location)
    return new_location
