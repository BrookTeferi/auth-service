import os
from datetime import datetime, timedelta

from jose import jwt

PRIVATE_KEY = open(os.getenv("JWT_PRIVATE_KEY_PATH")).read()
ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")


def create_access_token(subject: str, roles: list[str], expires_minutes: int = 15):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "roles": roles, "exp": expire}
    return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)
