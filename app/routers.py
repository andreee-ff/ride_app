from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError

from app.injections import (
    get_user_repository, 
    get_ride_repository,
    get_participation_repository,
)
from app.repositories import (
    UserRepository,
    RideRepository,
    ParticipationRepository,
)
from app.models import UserModel
from app.schemas import (
    UserResponse,
    UserCreate,
    TokenResponse,
    RideResponse,
    RideCreate,
    RideUpdate,
    ParticipationCreate,
    ParticipationResponse,
    ParticipationUpdate,
)

from app.security import create_access_token, decode_access_token

user_router = APIRouter()
auth_router = APIRouter()
ride_router = APIRouter()
participation_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ------------- USER ROUTES ------------- #

@user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {}},
)
def create_user(
    user_to_create: UserCreate,
    user_repository: Annotated[
        UserRepository, Depends(get_user_repository)
    ],
) -> UserResponse:
    existing_user = user_repository.get_by_username(username=user_to_create.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    try:
        user_model = user_repository.create_user(
            username=user_to_create.username, password=user_to_create.password
        )   
        return UserResponse.model_validate(user_model)
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
    return UserResponse.model_validate(user)

@user_router.get(
     "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK
)
def get_list_users(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> List[UserResponse]:
    
    users = user_repository.get_all_users()
    return [UserResponse.model_validate(user) for user in users]


# ------------- AUTH ROUTES ------------- #
@auth_router.post(
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

def get_current_user_model(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],  
) -> UserModel:
    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if subject is None:
            raise JWTError("Subject not found in token")
        user_id = int(subject)
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
    return user


@auth_router.get(
    "/me",
    response_model=UserResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {}},
)
def get_me(current_user: Annotated[UserModel, Depends(get_current_user_model)],
) -> UserResponse:
    return UserResponse.model_validate(current_user)


# ------------- RIDE ROUTES ------------- #

@ride_router.post(
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
    
@ride_router.get(
    "/",
    response_model=List[RideResponse],
    status_code=status.HTTP_200_OK
)
def get_list_rides(
    ride_repository: Annotated[RideRepository, Depends(get_ride_repository)],
) -> List[RideResponse]:
    
    rides = ride_repository.get_all_rides()
    return [RideResponse.model_validate(ride) for ride in rides]

@ride_router.get(
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

@ride_router.get(
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

@ride_router.delete(
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
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@ride_router.put(
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


# ------------- PARTICIPANTS ROUTES ------------- #

@participation_router.post(
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
    
    participation_model = participation_repository.create_participation(
        user_id = current_user.id,
        ride_id = current_ride.id,
        latitude = participation_to_create.latitude,
        longitude = participation_to_create.longitude,
        updated_at = participation_to_create.updated_at,
    )
    return ParticipationResponse.model_validate(participation_model)

@participation_router.get(
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


@participation_router.put(
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
        updated_at = participation_to_update.updated_at,
    )

    return ParticipationResponse.model_validate(participation_model)
