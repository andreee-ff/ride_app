from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from typing import Sequence
import secrets, string

from app.models import RideModel


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
    
    def get_all_rides(self) -> Sequence[RideModel]:
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
