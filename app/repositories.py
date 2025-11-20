from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import UserModel, RideModel

import secrets, string

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
    
    def get_by_code(self, *, ride_code: str) -> RideModel | None:
        statement = select(RideModel).where(RideModel.code == ride_code) 
        return(self.session.execute(statement).scalar_one_or_none())

