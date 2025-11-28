# app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Dict, List
import json

from database import Base, engine, get_db

# from backend import models
from routers import rooms, autocomplete
from services import room_service

# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pair Programming Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)
app.include_router(autocomplete.router)


# @app.on_event("startup")
# async def startup():
#     Base.metadata.create_all(bind=engine)


class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self.rooms.setdefault(room_id, []).append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.rooms:
            self.rooms[room_id].remove(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def broadcast(self, room_id: str, message: dict):
        if room_id not in self.rooms:
            return
        data = json.dumps(message)
        for ws in self.rooms[room_id]:
            await ws.send_text(data)


manager = ConnectionManager()


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, room_id: str, db: Session = Depends(get_db)
):
    room = room_service.get_room(db, room_id)
    if not room:
        await websocket.close(code=1008)
        return

    await manager.connect(room_id, websocket)

    # send initial code state
    await websocket.send_text(json.dumps({"type": "init", "code": room.code}))

    try:
        while True:
            text = await websocket.receive_text()
            payload = json.loads(text)

            if payload.get("type") == "code_update":
                code = payload.get("code", "")
                room_service.update_room_code(db, room_id, code)
                await manager.broadcast(room_id, {"type": "code_update", "code": code})
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
