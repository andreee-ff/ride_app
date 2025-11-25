from datetime import datetime, timezone
from typing import Annotated
from pydantic import BaseModel, ConfigDict, AwareDatetime, AfterValidator, field_serializer

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)

class RideCreate(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime

class RideResponse(BaseModel):
    id: int
    code: str
    title: str
    description: str | None = None
    start_time: datetime
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

    
class RideUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    is_active: bool | None = None




