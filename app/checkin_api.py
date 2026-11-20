"""FastAPI entry point for a read-only brain dump preview."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, StrictStr

from app.Services.checkin_parser import MAX_TEXT_LENGTH, parse_checkin

router = APIRouter()


class CheckInText(BaseModel):
    text: StrictStr = Field(
        description=f"English check-in text, up to {MAX_TEXT_LENGTH} characters."
    )


@router.post("/parse_checkin", tags=["Check-in preview"])
def preview_checkin(body: CheckInText):
    if len(body.text) > MAX_TEXT_LENGTH:
        raise HTTPException(422, f"Use at most {MAX_TEXT_LENGTH} characters.")
    if not body.text.strip():
        raise HTTPException(422, "Enter a check-in before parsing.")
    return parse_checkin(body.text)
