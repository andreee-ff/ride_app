from typing import Annotated, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.injections import (
    get_ride_repository,
    get_participation_repository,
)
from app.repositories import (
    RideRepository,
    ParticipationRepository,
)
from app.schemas import (
    UserResponse,
    ParticipationCreate,
    ParticipationResponse,
    ParticipationUpdate,
)
from app.routers.dependencies import get_current_user

router = APIRouter()


# ------------- PARTICIPANTS ROUTES ------------- #

@router.get(
        "/",
        response_model=List[ParticipationResponse],
        status_code=status.HTTP_200_OK,
)
def get_list_participations(
    participation_repository: Annotated[
        ParticipationRepository,
        Depends(get_participation_repository),
        ]
) -> List[ParticipationResponse]:
    
    participations = participation_repository.get_all_participations()
    return [ParticipationResponse.model_validate(r) for r in participations]

@router.post(
    "/",
    response_model= ParticipationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {}},
)
def create_participation(
    participation_to_create: ParticipationCreate,
    participation_repository: Annotated[ParticipationRepository, Depends(get_participation_repository)],
    ride_repository: Annotated[RideRepository, Depends(get_ride_repository)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> ParticipationResponse:
    current_ride = ride_repository.get_by_code(ride_code = participation_to_create.ride_code)
    if not current_ride:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    
    try:
        participation_model = participation_repository.create_participation(
            user_id = current_user.id,
            ride_id = current_ride.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
    
    return ParticipationResponse.model_validate(participation_model)

@router.get(
        "/{id}",
        response_model=ParticipationResponse,
        status_code=status.HTTP_200_OK,
        responses={status.HTTP_404_NOT_FOUND: {}},
)
def get_participation_by_id(
        id: int,
        participation_repository: Annotated[
            ParticipationRepository, 
            Depends(get_participation_repository),
        ],
) -> ParticipationResponse:

    participation = participation_repository.get_by_id(participation_id=id)
    if not participation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return ParticipationResponse.model_validate(participation)

@router.put(
    "/{id}",
    response_model=ParticipationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {},       
        status.HTTP_403_FORBIDDEN: {},
    },
)
def update_participation_by_id(
    id: int,
    participation_to_update: ParticipationUpdate,
    participation_repository: Annotated[
        ParticipationRepository,
        Depends(get_participation_repository),
    ],
    current_user: Annotated[
        UserResponse,
        Depends(get_current_user),
    ],
) -> ParticipationResponse:
    
    existing_participation = participation_repository.get_by_id(participation_id=id)
    if not existing_participation:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    

    if existing_participation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this participation. It belongs to another user",
            )
    
    participation_model = participation_repository.update_participation(
        existing_participation,
        latitude = participation_to_update.latitude,
        longitude = participation_to_update.longitude,
        location_timestamp = participation_to_update.location_timestamp,
    )

    return ParticipationResponse.model_validate(participation_model)
