from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
from sqlalchemy import Numeric


class DbModel(DeclarativeBase): 
    pass

class UserModel(DbModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=25), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    organized_rides: Mapped[list["RideModel"]] = relationship(back_populates="organizer")
    participated_in_rides: Mapped[list["ParticipationModel"]] = relationship(back_populates="participant")

    def __repr__(self) -> str:
        return f"UserModel(id={self.id!r}, username={self.username!r})"

class RideModel(DbModel):
    __tablename__ = "rides"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(length=6), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(length=100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(length=255), nullable=True) 
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    organizer: Mapped["UserModel"] = relationship(back_populates="organized_rides")
    has_participants: Mapped[list["ParticipationModel"]] = relationship(back_populates="ride")

    def __repr__(self) -> str:
        return f"RideModel(id={self.id!r}, code={self.code!r}, title={self.title!r})"


class ParticipationModel(DbModel):
    __tablename__ = "participations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    ride_id: Mapped[int] = mapped_column(ForeignKey("rides.id"), nullable=False)
    latitude: Mapped[float] = mapped_column(Numeric(10, 8), nullable=True)
    longitude: Mapped[float] = mapped_column(Numeric(10, 8), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] =  mapped_column(DateTime(timezone=True), nullable=True)

    participant: Mapped["UserModel"] = relationship(back_populates="participated_in_rides")
    ride: Mapped["RideModel"] = relationship(back_populates="has_participants")

    def __repr__(self) -> str:
        return f"ParticipationModel(id={self.id!r}, user_id={self.user_id!r}, ride_id={self.ride_id!r})"

