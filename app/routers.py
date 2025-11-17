from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.injections import get_user_repository
from app.repositories import UserRepository
from app.schemas import UserResponse, CreateUser

user_router = APIRouter()

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