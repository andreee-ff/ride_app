from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    username: str
    password: str

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




