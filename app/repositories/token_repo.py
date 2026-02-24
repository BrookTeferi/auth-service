from sqlalchemy.orm import Session
from app.models.token import RefreshToken
from datetime import datetime

class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_refresh_token(self, user_id: str, token_hash: str, expires_at: datetime) -> RefreshToken:
        token = RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def revoke_token(self, token_id: str):
        token = self.db.query(RefreshToken).filter(RefreshToken.id==token_id).first()
        if token:
            token.revoked = True
            self.db.commit()

    def get_valid_token(self, token_hash: str):
        return self.db.query(RefreshToken).filter(
            RefreshToken.token_hash==token_hash,
            RefreshToken.revoked==False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()