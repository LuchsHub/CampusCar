import uuid
from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import Car, CarCreate, CarUpdate, Message

router = APIRouter(tags=["cars"])


@router.get("/cars/", response_model=list[Car])
def get_cars(
    session: SessionDep,
    current_user: CurrentUser,
) -> Sequence[Car]:
    """Get all cars for current user."""
    cars = session.exec(select(Car).where(Car.owner_id == current_user.id)).all()
    return cars


@router.post("/cars/", response_model=Car, status_code=status.HTTP_201_CREATED)
def create_car(
    car_in: CarCreate,
    session: SessionDep,
    current_user: CurrentUser,
) -> Car:
    """Create a new car."""
    car = Car.model_validate(car_in, update={"owner_id": current_user.id})
    session.add(car)
    session.commit()
    session.refresh(car)
    return car


@router.patch("/cars/{car_id}", response_model=Car)
def update_car(
    car_id: uuid.UUID,
    car_update: CarUpdate,
    session: SessionDep,
    current_user: CurrentUser,
) -> Car:
    """Update a car."""
    db_car = session.get(Car, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")

    if db_car.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in car_update.dict(exclude_unset=True).items():
        setattr(db_car, key, value)

    session.add(db_car)
    session.commit()
    session.refresh(db_car)
    return db_car


@router.delete("/cars/{car_id}", response_model=Message)
def delete_car(
    car_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Message:
    """Delete a car."""
    db_car = session.get(Car, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    if db_car.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    session.delete(db_car)
    session.commit()
    return Message(message="Car deleted")
