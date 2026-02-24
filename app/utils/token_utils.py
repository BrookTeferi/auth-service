import secrets
from hashlib import sha256

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def hash_refresh_token(token: str) -> str:
    return sha256(token.encode()).hexdigest()