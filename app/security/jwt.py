import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Final

from jose import jwt  # type: ignore[import-untyped]

PRIVATE_KEY_PATH = os.getenv("JWT_PRIVATE_KEY_PATH")
if PRIVATE_KEY_PATH is None:
    raise RuntimeError("JWT_PRIVATE_KEY_PATH environment variable is not set")

PRIVATE_KEY_FILE = Path(PRIVATE_KEY_PATH)
PRIVATE_KEY: Final[str] = PRIVATE_KEY_FILE.read_text(encoding="utf-8")

ALGORITHM: Final[str] = os.getenv("JWT_ALGORITHM", "RS256")


def create_access_token(subject: str, roles: list[str], expires_minutes: int = 15) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "roles": roles, "exp": expire}
    return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)
