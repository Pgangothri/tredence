# app/routers/autocomplete.py
from fastapi import APIRouter
from schemas import AutocompleteRequest, AutocompleteResponse

router = APIRouter(prefix="/autocomplete", tags=["autocomplete"])

TRIGGERS = {
    "def": "def function_name():\n    ",
    "for": "for i in range():\n    ",
    "if": "if condition:\n    ",
    "print": "print()",
}


@router.post("/", response_model=AutocompleteResponse)
def autocomplete(req: AutocompleteRequest):
    prefix = req.code[: req.cursorPosition].rstrip()
    for key, completion in TRIGGERS.items():
        if prefix.endswith(key):
            return AutocompleteResponse(suggestion=completion[len(key) :])
    return AutocompleteResponse(suggestion="")
