from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.injections import get_user_repository
from app.repositories import UserRepository
from app.schemas import (
    UserResponse,
    CreateUser,
    LoginRequest,
    TokenResponse,
)

from app.security import create_access_token, decode_access_token

user_router = APIRouter()
auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {}},
)

def create_user(
    user_to_create: CreateUser,
    user_repository: Annotated[
        UserRepository, Depends(get_user_repository)
    ],
) -> UserResponse:
    existing_user = user_repository.get_by_username(username=user_to_create.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    try:
        return user_repository.create_user(username=user_to_create.username, password=user_to_create.password)
    except Exception as exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT) from exception
    
@user_router.get(
    "/{id}",
    response_model=UserResponse,
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def get_user(
    id: int,
    user_repository: Annotated[
        UserRepository, Depends(get_user_repository)
    ],
) -> UserResponse:
    user = user_repository.get_by_id(user_id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


# ------------- AUTH ROUTES ------------- #
@auth_router.post(
    "/login",
    response_model=TokenResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {}},    
)

def login(
    login_data: LoginRequest,
    user_repository: Annotated[
        UserRepository, Depends(get_user_repository)
    ],
) -> TokenResponse:
    user = user_repository.get_by_username(username=login_data.username)
    if not user or user.password != login_data.password:
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
    user_repository: Annotated[
        UserRepository, Depends(get_user_repository)
    ],  
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



@auth_router.get(
    "/me",
    response_model=UserResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {}},
)

def get_me(
    current_user: Annotated[
        UserResponse, Depends(get_current_user)
    ],
) -> UserResponse:
    return current_user