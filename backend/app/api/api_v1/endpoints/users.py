from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me/", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/search/", response_model=List[schemas.User])
def search_users(
    q: str = Query(..., description="Поисковый запрос"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Поиск пользователей по username или email.
    """
    if len(q.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Поисковый запрос должен содержать минимум 2 символа"
        )
    
    users = crud.crud_user.search_users(db, query=q, skip=skip, limit=limit)
    # Исключаем текущего пользователя из результатов
    users = [user for user in users if user.id != current_user.id]
    return users


@router.put("/me/profile/", response_model=schemas.User)
def update_profile(
    profile_in: schemas.ProfileUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update current user profile.
    """
    user = crud.crud_user.update_profile(
        db, 
        user_id=current_user.id, 
        avatar_url=profile_in.avatar_url,
        bio=profile_in.bio
    )
    return user


@router.get("/{user_id}/", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.crud_user.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user 