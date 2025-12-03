from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer


from app.injections import (
    get_ride_repository,
)
from app.repositories import (
    RideRepository,
)

from app.schemas import (
    UserResponse,
    RideResponse,
    RideCreate,
    RideUpdate,
)

from app.routers.dependencies import get_current_user

router = APIRouter()

# ------------- RIDE ROUTES ------------- #

@router.post(
    "/",
    response_model=RideResponse,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {}},
)
def create_ride(
    ride_to_create: RideCreate,
    ride_repository: Annotated[RideRepository, Depends(get_ride_repository)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> RideResponse:

    ride_model = ride_repository.create_ride(
    title = ride_to_create.title,
    description = ride_to_create.description,
    start_time = ride_to_create.start_time,
    created_by_user_id = current_user.id,
    ) 
    return RideResponse.model_validate(ride_model)
    
@router.get(
    "/",
    response_model=List[RideResponse],
    status_code=status.HTTP_200_OK
)
def get_list_rides(
    ride_repository: Annotated[RideRepository, Depends(get_ride_repository)],
) -> List[RideResponse]:
    
    rides = ride_repository.get_all_rides()
    return [RideResponse.model_validate(ride) for ride in rides]

@router.get(
    "/code/{code}",
    response_model=RideResponse,    
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def get_ride_by_code(
    code: str,
    ride_repository: Annotated[
        RideRepository, Depends(get_ride_repository)
    ],
) -> RideResponse:
    ride = ride_repository.get_by_code(ride_code=code)
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RideResponse.model_validate(ride) 

@router.get(
        "/{id}",
        response_model=RideResponse,
        status_code=status.HTTP_200_OK,
        responses={status.HTTP_404_NOT_FOUND: {}},
)
def get_ride_by_id(
        id: int,
        ride_repository: Annotated[RideRepository, Depends(get_ride_repository)],
) -> RideResponse:
    ride = ride_repository.get_by_id(ride_id=id)
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RideResponse.model_validate(ride)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {},       
        status.HTTP_403_FORBIDDEN: {},
        },
)
def delete_ride_by_id(
    id: int,
    ride_repository: Annotated[RideRepository, Depends(get_ride_repository)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> None:
    selected_ride = ride_repository.get_by_id(ride_id=id)
    if not selected_ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if selected_ride.created_by_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowes to delete this ride. The ride was created by another user"
            )
    
    ride_repository.delete_ride(ride=selected_ride)    
    return

@router.put(
    "/{id}",
    response_model=RideResponse,        
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {},       
        status.HTTP_403_FORBIDDEN: {},
    }
)
def update_ride_by_id(
    id: int,
    ride_to_update: RideUpdate,
    ride_repository: Annotated[RideRepository, Depends(get_ride_repository)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> RideResponse:
    
    existing_ride = ride_repository.get_by_id(ride_id=id)
    if not existing_ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if existing_ride.created_by_user_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not allowes to update this ride. It belongs to another user",
            )
    
    ride_model = ride_repository.update_ride(
        existing_ride,
        title = ride_to_update.title,
        description = ride_to_update.description,
        start_time = ride_to_update.start_time,
        is_active = ride_to_update.is_active,
    )
    return RideResponse.model_validate(ride_model)