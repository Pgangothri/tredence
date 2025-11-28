# app/schemas.py
from pydantic import BaseModel


class RoomCreateResponse(BaseModel):
    roomId: str


class AutocompleteRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str = "python"


class AutocompleteResponse(BaseModel):
    suggestion: str
