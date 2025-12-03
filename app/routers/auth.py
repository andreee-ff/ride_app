from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError

from app.injections import (
    get_user_repository, 
)
from app.repositories import (
    UserRepository,
)
from app.schemas import (
    UserResponse,
    TokenResponse,
)
from app.security import create_access_token, decode_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ------------- AUTH ROUTES ------------- #
@router.post(
    "/login",
    response_model=TokenResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {}},    
)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> TokenResponse:
    user = user_repository.get_by_username(username=form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(subject=str(user.id))

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],  
) -> UserResponse:
    try:
        payload = decode_access_token(token)

        sub = payload.get("sub")
        if sub is None:
            raise JWTError("Subject not found in token")
        
        user_id = int(sub)
    
    except (ValueError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
        
    user = user_repository.get_by_id(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return UserResponse.model_validate(user)

@router.get(
    "/me",
    response_model=UserResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {}},
)
def get_me(current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> UserResponse:
    return current_user
