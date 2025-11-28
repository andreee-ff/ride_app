from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from typing import Any, List
import secrets, string

from app.models import UserModel, RideModel, ParticipationModel


class UserRepository:
    session: Session

    def __init__(self, *, session: Session):
        self.session = session
    
    def create_user(self, *,  username: str, password: str) -> UserModel:
        new_user = UserModel(username=username, password=password)
        self.session.add(new_user)
        self.session.flush()

        return new_user
     
    def get_by_username(self, *, username: str) -> UserModel | None:
        return (
            self.session.query(UserModel)
            .filter(UserModel.username == username)
            .first()
        )
    
    def get_by_id(self, *, user_id: int) -> UserModel | None:
        return (
            self.session.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )
    
    def get_all_users(self) -> List[UserModel]:
        statement = select(UserModel)
        return(self.session.execute(statement).scalars().all()) 

class RideRepository:
    session: Session

    def __init__ (self, *, session: Session):
        self.session = session

    def _generate_string_code(self, length: int = 6) -> str:
        characters = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    def _generate_unique_code(self) -> str:
        while True:
            code = self._generate_string_code()
            statement = select(RideModel).where(RideModel.code == code)
            existintg_ride = self.session.execute(statement).scalar_one_or_none()

            if existintg_ride is None:
                return code
            
    def create_ride(
            self,
            *,
            title: str,
            description: str | None,
            start_time: datetime,
            created_by_user_id: int,
        ) -> RideModel:
        unique_code = self._generate_unique_code()
        new_ride = RideModel(
            code=unique_code,
            title=title,
            description=description,
            start_time=start_time,
            created_by_user_id=created_by_user_id,
        ) 

        self.session.add(new_ride)
        self.session.flush()

        return new_ride
    
    def get_all_rides(self) -> List[RideModel]:
        statement = select(RideModel)
        return(self.session.execute(statement).scalars().all())
 

    def get_by_code(self, *, ride_code: str) -> RideModel | None:
        statement = select(RideModel).where(RideModel.code == ride_code) 
        return(self.session.execute(statement).scalar_one_or_none())
    
    def get_by_id(self, *, ride_id: int) -> RideModel | None:
        statement = select(RideModel).where(RideModel.id == ride_id)
        return(self.session.execute(statement).scalar_one_or_none())
    
    def delete_ride(self, *, ride: RideModel) -> None:
        self.session.delete(ride)
        self.session.flush()

    def update_ride(
            self,
            ride: RideModel,         
            *,           
            title: str | None = None,
            description: str | None = None,
            start_time: datetime | None = None,
            is_active: bool | None = None,
        ) -> RideModel:
        ride_to_update ={
            "title": title,
            "description": description,
            "start_time": start_time,
            "is_active": is_active,
        }

        for key, value in ride_to_update.items():
            if value is not None:
                setattr(ride, key, value)

        self.session.add(ride)
        self.session.flush()
        return ride


class ParticipationRepository:
    session: Session

    def __init__(self, *, session: Session):
        self.session = session

    def create_participation(
            self,
            *,
            user_id: int,
            ride_id: int,
            latitude: float | None=None,
            longitude: float | None=None,
            updated_at: datetime | None=None,
    ) -> ParticipationModel:
        new_participation = ParticipationModel(
            user_id = user_id,
            ride_id = ride_id,
            latitude = latitude,
            longitude = longitude,
            updated_at = updated_at,
        )

        self.session.add(new_participation)
        self.session.flush()

        return new_participation
    
    def get_by_id(self, *, participation_id: int) -> ParticipationModel | None:
        return self.session.get(ParticipationModel, participation_id)
    
    def get_all_participations(self) -> List[ParticipationModel]:
        statement = select(ParticipationModel)
        return (self.session.execute(statement).scalars().all())

    def update_participation(
        self,
        participation: ParticipationModel,
        *,
        latitude: float,
        longitude: float, 
        updated_at: datetime
    ) -> ParticipationModel:
        
        participation_to_update ={
            "latitude": latitude,
            "longitude": longitude,
            "updated_at": updated_at,
        }

        for key, value in participation_to_update.items():
            if value is not None:
                setattr(participation, key, value)

        self.session.add(participation)
        self.session.flush()

        return participation