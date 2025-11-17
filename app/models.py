from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class DbModel(DeclarativeBase): ...

class UserModel(DbModel):
    __tablename__ = "participant"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=25), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(length=255), nullable=True)
