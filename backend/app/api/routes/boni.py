import uuid
from collections.abc import Sequence
from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Bonus,
    BonusCreate,
    BonusPublic,
    Message,
    RedeemedBonusPublic,
    UserBonusLink,
)

router = APIRouter(prefix="/bonuses", tags=["bonuses"])


@router.get("/me", response_model=list[Any])
def get_my_bonuses(
    session: SessionDep,
    current_user: CurrentUser,
) -> Sequence[Any]:
    """Get bonuses for current user."""
    query = (
        select(Bonus, UserBonusLink.redemption_time)
        .join_from(Bonus, UserBonusLink)
        .where(UserBonusLink.user_id == current_user.id)
    )
    results = session.exec(query).all()

    response_data = []
    for bonus, redemption_time in results:
        bonus_data = bonus.model_dump()
        bonus_data["redemption_time"] = redemption_time
        response_data.append(RedeemedBonusPublic(**bonus_data))

    return response_data


@router.get("/", response_model=list[BonusPublic])
def get_bonuses(
    session: SessionDep,
) -> Sequence[Any]:
    """Get all bonuses."""
    bonuses = session.exec(select(Bonus)).all()
    return bonuses


@router.post("/", response_model=BonusPublic, status_code=status.HTTP_201_CREATED)
def create_bonus(
    bonus_in: BonusCreate,
    session: SessionDep,
) -> Any:
    """Create a new bonus."""
    bonus = Bonus.model_validate(bonus_in)

    session.add(bonus)
    session.commit()
    session.refresh(bonus)
    return bonus


@router.post("/redeem/{bonus_id}", response_model=list[BonusPublic])
def add_bonus_to_current_user(
    bonus_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Sequence[Any]:
    """Redeem bonus for current user."""
    bonus: Bonus | None = session.get(Bonus, bonus_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not bonus:
        raise HTTPException(status_code=404, detail="Bonus not found")
    elif current_user.points < bonus.cost:
        raise HTTPException(status_code=403, detail="User has too little points")
    else:
        current_user.points = current_user.points - bonus.cost
        current_user.bonuses.append(bonus)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)
    return current_user.bonuses


@router.delete("/{bonus_id}", response_model=Message)
def delete_bonus(
    bonus_id: uuid.UUID,
    session: SessionDep,
) -> Message:
    """Delete a bonus."""
    bonus = session.get(Bonus, bonus_id)
    if not bonus:
        raise HTTPException(status_code=404, detail="Bonus not found")

    session.delete(bonus)
    session.commit()
    return Message(message="Bonus deleted")
