"""Settings endpoints -- manage app configuration like API keys."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.settings_repository import get_setting, set_setting, delete_setting, has_setting

router = APIRouter(prefix="/settings", tags=["settings"])

ANTHROPIC_KEY = "anthropic_api_key"


class ApiKeyRequest(BaseModel):
    api_key: str


class ApiKeyStatus(BaseModel):
    is_set: bool


@router.get("/api-key/status", response_model=ApiKeyStatus)
def get_api_key_status(db: Session = Depends(get_db)):
    """Check if the Anthropic API key is configured. Never returns the key itself."""
    return ApiKeyStatus(is_set=has_setting(db, ANTHROPIC_KEY))


@router.post("/api-key")
def set_api_key(body: ApiKeyRequest, db: Session = Depends(get_db)):
    """Set the Anthropic API key. The key is stored but never returned."""
    key = body.api_key.strip()
    if not key:
        raise HTTPException(status_code=422, detail="API key cannot be empty")
    set_setting(db, ANTHROPIC_KEY, key)
    # Reset the cached Anthropic client so it picks up the new key
    try:
        import backend.engine.rag_engine as rag_mod
        rag_mod._anthropic_client = None
    except Exception:
        pass
    return {"detail": "API key saved"}


@router.delete("/api-key")
def remove_api_key(db: Session = Depends(get_db)):
    """Remove the stored Anthropic API key."""
    deleted = delete_setting(db, ANTHROPIC_KEY)
    if not deleted:
        raise HTTPException(status_code=404, detail="No API key was configured")
    try:
        import backend.engine.rag_engine as rag_mod
        rag_mod._anthropic_client = None
    except Exception:
        pass
    return {"detail": "API key removed"}
