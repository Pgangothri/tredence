# app/services/room_service.py
import uuid
from sqlalchemy.orm import Session
import models


def create_room(db: Session) -> str:
    room_id = uuid.uuid4().hex[:8]
    room = models.Room(room_id=room_id, code="")
    db.add(room)
    db.commit()
    db.refresh(room)
    return room.room_id


def get_room(db: Session, room_id: str) -> models.Room | None:
    return db.query(models.Room).filter(models.Room.room_id == room_id).first()


def update_room_code(db: Session, room_id: str, code: str) -> None:
    room = get_room(db, room_id)
    if not room:
        return
    room.code = code
    db.commit()
