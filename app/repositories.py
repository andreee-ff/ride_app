from sqlalchemy.orm import Session

from app.models import UserModel
from app.schemas import UserResponse

class UserRepository:
    session: Session

    def __init__(self, *, session: Session):
        self.session = session
    
    def create_user(self, *,  username: str, password: str) -> UserResponse:
        new_user = UserModel(username=username, password=password)
        self.session.add(new_user)
        self.session.flush()
        return UserResponse.model_validate(new_user)
     
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
