from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.token import Token
from app.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/register/", response_model=User)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Register a new user.
    """
    try:
        user = crud.crud_user.get_user_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="A user with this email already exists.",
            )
        user = crud.crud_user.get_user_by_username(db, username=user_in.username)
        if user:
            raise HTTPException(
                status_code=400,
                detail="A user with this username already exists.",
            )
        user = crud.crud_user.create_user(db, user_in=user_in)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/login/", response_model=Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    try:
        user = crud.crud_user.authenticate_user(
            db, username=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 
    