from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.repositories.token_repo import TokenRepository
from app.services.auth_service import AuthService
from app.core.config import get_db

router = APIRouter()

class AuthRequest(BaseModel):
    email: str
    password: str

class TokenRequest(BaseModel):
    refresh_token: str

@router.post("/register")
def register(req: AuthRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    token_repo = TokenRepository(db)
    service = AuthService(user_repo, token_repo)
    try:
        user = service.register(req.email, req.password)
        return {"id": str(user.id), "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(req: AuthRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    token_repo = TokenRepository(db)
    service = AuthService(user_repo, token_repo)
    try:
        return service.login(req.email, req.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh")
def refresh(req: TokenRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    token_repo = TokenRepository(db)
    service = AuthService(user_repo, token_repo)
    try:
        return service.refresh(req.refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
def logout(req: TokenRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    token_repo = TokenRepository(db)
    service = AuthService(user_repo, token_repo)
    service.logout(req.refresh_token)
    return {"message": "Logged out successfully"}