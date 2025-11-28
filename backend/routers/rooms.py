# app/routers/rooms.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import RoomCreateResponse
from services import room_service

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/", response_model=RoomCreateResponse)
def create_room_endpoint(db: Session = Depends(get_db)):
    room_id = room_service.create_room(db)
    return RoomCreateResponse(roomId=room_id)
