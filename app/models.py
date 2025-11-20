from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional


class DbModel(DeclarativeBase): ...

class UserModel(DbModel):
    __tablename__ = "participant"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=25), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)

    organized_rides: Mapped[list["RideModel"]] = relationship(back_populates="organizer")

    def __repr__(self) -> str:
        return f"UserModel(id={self.id!r}, username={self.username!r})"

class RideModel(DbModel):
    __tablename__ = "rides"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(length=6), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(length=100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(length=255), nullable=False) 
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("participant.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    organizer: Mapped["UserModel"] = relationship(back_populates="organized_rides")

    def __repr__(self) -> str:
        return f"RideModel(id={self.id!r}, code={self.code!r}, title={self.title!r})"
