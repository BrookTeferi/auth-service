from datetime import datetime, timedelta
from app.repositories.user_repo import UserRepository
from app.repositories.token_repo import TokenRepository
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token
from app.utils.token_utils import generate_refresh_token, hash_refresh_token
import os

class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.refresh_token_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30))

    def register(self, email: str, password: str):
        pw_hash = hash_password(password)
        return self.user_repo.create_user(email=email, password_hash=pw_hash)

    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise Exception("Invalid credentials")

        access_token = create_access_token(subject=str(user.id), roles=["user"])
        raw_refresh_token = generate_refresh_token()
        hashed_token = hash_refresh_token(raw_refresh_token)
        expires_at = datetime.utcnow() + timedelta(days=self.refresh_token_days)
        self.token_repo.create_refresh_token(user_id=str(user.id), token_hash=hashed_token, expires_at=expires_at)

        return {
            "access_token": access_token,
            "refresh_token": raw_refresh_token,
            "user_id": str(user.id)
        }

    def refresh(self, raw_refresh_token: str):
        hashed_token = hash_refresh_token(raw_refresh_token)
        token = self.token_repo.get_valid_token(hashed_token)
        if not token:
            raise Exception("Invalid or expired refresh token")

        # Revoke old token
        self.token_repo.revoke_token(token.id)

        # Issue new tokens
        user = self.user_repo.get_by_id(token.user_id)
        access_token = create_access_token(subject=str(user.id), roles=["user"])
        new_raw_refresh_token = generate_refresh_token()
        new_hashed = hash_refresh_token(new_raw_refresh_token)
        expires_at = datetime.utcnow() + timedelta(days=self.refresh_token_days)
        self.token_repo.create_refresh_token(user_id=str(user.id), token_hash=new_hashed, expires_at=expires_at)

        return {
            "access_token": access_token,
            "refresh_token": new_raw_refresh_token
        }

    def logout(self, raw_refresh_token: str):
        hashed_token = hash_refresh_token(raw_refresh_token)
        token = self.token_repo.get_valid_token(hashed_token)
        if token:
            self.token_repo.revoke_token(token.id)