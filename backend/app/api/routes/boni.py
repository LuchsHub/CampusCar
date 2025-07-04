import uuid
from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import Bonus, BonusCreate, BonusUpdate, BonusPublic, Message, User

router = APIRouter(prefix="/boni", tags=["boni"])


@router.get("/all/", response_model=list[BonusPublic])
def get_boni(
    session: SessionDep,
) -> Sequence[BonusPublic]:
    """Get all boni."""
    boni = session.exec(select(Bonus)).all()
    return boni


@router.post("/boni/", response_model=BonusPublic, status_code=status.HTTP_201_CREATED)
def create_boni(
    bonus_in: BonusCreate,
    session: SessionDep,
) -> BonusPublic:
    """Create a new boni."""
    bonus = Bonus.model_validate(bonus_in)
    session.add(bonus)
    session.commit()
    session.refresh(bonus)
    return bonus


@router.get("/", response_model=list[Bonus])
def get_boni_by_user(
    session: SessionDep,
    current_user: CurrentUser,
) -> Sequence[Bonus]:
    """Get boni for current user."""
    boni = session.exec(select(Bonus).where(Bonus.assigned_user == current_user)).all()
    return boni


@router.get("/assign", response_model=list[Bonus])
def get_boni_by_user(
    bonus_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Sequence[Bonus]:
    """Assigns bonus for current user."""
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    boni = session.get(Bonus, bonus_id)
    if not boni:
        raise HTTPException(status_code=404, detail="Bonus not found")

    current_user.boni.append(boni)

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
