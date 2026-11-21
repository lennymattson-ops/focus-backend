"""FastAPI entry point for a read-only brain dump preview."""

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field, StrictStr

from app.Services.checkin_parser import MAX_TEXT_LENGTH, parse_checkin
from app.Services.checkin_ai_preview import (
    FixtureInputRequired, PreviewDisabled, PreviewUnavailable, preview_ai,
)

router = APIRouter()


class CheckInText(BaseModel):
    text: StrictStr = Field(
        description=f"English check-in text, up to {MAX_TEXT_LENGTH} characters."
    )


def validate_text(text):
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(422, f"Use at most {MAX_TEXT_LENGTH} characters.")
    if not text.strip():
        raise HTTPException(422, "Enter a check-in before parsing.")


@router.post("/parse_checkin", tags=["Check-in preview"])
def preview_checkin(body: CheckInText):
    validate_text(body.text)
    return parse_checkin(body.text)


@router.post("/preview_ai_checkin", tags=["Check-in preview"])
async def preview_ai_checkin(body: CheckInText, response: Response):
    """Return an interpretation for debugging only. Does not save a check-in."""
    validate_text(body.text)
    response.headers["Cache-Control"] = "no-store"
    try:
        return await preview_ai(body.text)
    except FixtureInputRequired:
        raise HTTPException(422, "Demo mode accepts only the fictional Case 7 résumé example.") from None
    except PreviewDisabled:
        raise HTTPException(503, "AI preview is disabled. The rules parser is still available.") from None
    except PreviewUnavailable:
        raise HTTPException(502, "AI preview did not complete. The rules parser is still available.") from None
