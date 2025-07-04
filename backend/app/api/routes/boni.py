import uuid
from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import Bonus, BonusCreate, BonusUpdate, Message

router = APIRouter(tags=["boni"])


@router.get("/all/", response_model=list[Bonus])
def get_cars(
    session: SessionDep,
) -> Sequence[Bonus]:
    """Get all cars for current user."""
    boni = session.exec(select(Bonus)).all()
    return boni


@router.post("/boni/", response_model=Bonus, status_code=status.HTTP_201_CREATED)
def create_car(
    bonus_in: BonusCreate,
    session: SessionDep,
) -> Bonus:
    """Create a new car."""
    bonus = Bonus.model_validate(bonus_in)
    session.add(bonus)
    session.commit()
    session.refresh(bonus)
    return bonus


# @router.patch("/cars/{car_id}", response_model=Car)
# def update_car(
#     car_id: uuid.UUID,
#     car_update: CarUpdate,
#     session: SessionDep,
#     current_user: CurrentUser,
# ) -> Car:
#     """Update a car."""
#     db_car = session.get(Car, car_id)
#     if not db_car:
#         raise HTTPException(status_code=404, detail="Car not found")

#     if db_car.owner_id != current_user.id and not current_user.is_superuser:
#         raise HTTPException(status_code=403, detail="Not authorized")

#     for key, value in car_update.dict(exclude_unset=True).items():
#         setattr(db_car, key, value)

#     session.add(db_car)
#     session.commit()
#     session.refresh(db_car)
#     return db_car


# @router.delete("/cars/{car_id}", response_model=Message)
# def delete_car(
#     car_id: uuid.UUID,
#     session: SessionDep,
#     current_user: CurrentUser,
# ) -> Message:
#     """Delete a car."""
#     db_car = session.get(Car, car_id)
#     if not db_car:
#         raise HTTPException(status_code=404, detail="Car not found")
#     if db_car.owner_id != current_user.id and not current_user.is_superuser:
#         raise HTTPException(status_code=403, detail="Not authorized")
#     session.delete(db_car)
#     session.commit()
#     return Message(message="Car deleted")
