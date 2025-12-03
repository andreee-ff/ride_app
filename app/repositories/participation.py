from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from typing import Sequence



from app.models import ParticipationModel

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
    
    def get_all_participations(self) -> Sequence[ParticipationModel]:
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