# app/models.py
from sqlalchemy import Column, Integer, String, Text
from database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String(32), unique=True, index=True, nullable=False)
    code = Column(Text, default="", nullable=False)
