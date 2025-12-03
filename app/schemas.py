from datetime import datetime, timezone
from typing import Annotated
from pydantic import BaseModel, ConfigDict, AwareDatetime, AfterValidator, field_serializer


class TimestampMixin(BaseModel):
    @field_serializer("*")# Serialize all datetime fields
    @classmethod
    def serialize_dt(cls, value, _info): 
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            iso_str = value.astimezone(timezone.utc).isoformat()
            return iso_str.replace("Z", "+00:00")
        return value

#------------------------ USER

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(TimestampMixin):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


#------------------------ TOKEN

class TokenResponse(TimestampMixin):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)


#------------------------ RIDE
class RideBase(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime

class RideCreate(RideBase):
    pass

class RideResponse(RideBase, TimestampMixin):
    id: int
    code: str
    created_by_user_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class RideUpdate(RideBase):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    is_active: bool | None = None


#------------------------ PARTICIPATION
class ParticipationBase(BaseModel):
    latitude: float | None = None
    longitude: float | None = None
    updated_at: datetime | None = None

class ParticipationCreate(ParticipationBase):
    ride_code: str

class ParticipationUpdate(ParticipationBase):
    latitude: float
    longitude: float
    updated_at: datetime

class ParticipationResponse(ParticipationBase, TimestampMixin):
    id: int
    user_id: int
    ride_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)






