from datetime import datetime, timezone
from typing import Annotated
from pydantic import BaseModel, ConfigDict, AwareDatetime, AfterValidator, field_serializer

#------------------------ USER

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


#------------------------ TOKEN

class TokenResponse(BaseModel):
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

class RideResponse(RideBase):
    id: int
    code: str
    created_by_user_id: int
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("start_time", "created_at")
    def serialize_dt(self, dt: datetime, _info) -> str:
        # Convert to UTC and format with +00:00 instead of Z for consistency
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        # Use isoformat() and replace Z with +00:00 for consistency
        iso_str = dt.astimezone(timezone.utc).isoformat()
        return iso_str.replace("Z", "+00:00")

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

class ParticipationResponse(ParticipationBase):
    id: int
    user_id: int
    ride_id: int

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("updated_at")
    def serialize_dt(self, dt: datetime | None, _info) -> str | None:
        # Convert to UTC and format with +00:00 instead of Z for consistency
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        # Use isoformat() and replace Z with +00:00 for consistency
        iso_str = dt.astimezone(timezone.utc).isoformat()
        return iso_str.replace("Z", "+00:00")






