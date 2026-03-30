"""Settings repository -- key-value store for app configuration."""
import hashlib
import base64
from sqlalchemy.orm import Session
from backend.models.settings_models import AppSetting


def get_setting(db: Session, key: str) -> str | None:
    """Get a setting value by key. Returns None if not found."""
    setting = db.query(AppSetting).filter(AppSetting.key == key).first()
    if setting is None:
        return None
    return setting.value


def set_setting(db: Session, key: str, value: str) -> None:
    """Set a setting value. Creates or updates."""
    setting = db.query(AppSetting).filter(AppSetting.key == key).first()
    if setting is None:
        setting = AppSetting(key=key, value=value)
        db.add(setting)
    else:
        setting.value = value
    db.commit()


def delete_setting(db: Session, key: str) -> bool:
    """Delete a setting. Returns True if it existed."""
    setting = db.query(AppSetting).filter(AppSetting.key == key).first()
    if setting is None:
        return False
    db.delete(setting)
    db.commit()
    return True


def has_setting(db: Session, key: str) -> bool:
    """Check if a setting exists without revealing its value."""
    return db.query(AppSetting).filter(AppSetting.key == key).count() > 0
