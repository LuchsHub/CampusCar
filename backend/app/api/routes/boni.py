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

router = APIRouter(prefix="/boni", tags=["boni"])


@router.get("/get-my-boni", response_model=list[Any])
def get_boni_by_user(
    session: SessionDep,
    current_user: CurrentUser,
) -> Sequence[Any]:
    """Get boni for current user."""
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


@router.get("/get-all-boni", response_model=list[BonusPublic])
def get_boni(
    session: SessionDep,
) -> Sequence[Any]:
    """Get all boni."""
    boni = session.exec(select(Bonus)).all()
    return boni


@router.post(
    "/add-new-boni/", response_model=BonusPublic, status_code=status.HTTP_201_CREATED
)
def create_boni(
    bonus_in: BonusCreate,
    session: SessionDep,
) -> Any:
    """Create a new boni."""
    bonus = Bonus.model_validate(bonus_in)

    session.add(bonus)
    session.commit()
    session.refresh(bonus)
    return bonus


@router.post("/redeem/{bonus_id}", response_model=list[BonusPublic])
def add_boni_to_current_user(
    bonus_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Sequence[Any]:
    """Assigns bonus for current user."""
    bonus: Bonus | None = session.get(Bonus, bonus_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not bonus:
        raise HTTPException(status_code=404, detail="Bonus not found")
    elif current_user.points < bonus.cost:
        raise HTTPException(status_code=401, detail="User has too little money")
    else:
        current_user.points = current_user.points - bonus.cost
        current_user.boni.append(bonus)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)
    return current_user.boni


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
