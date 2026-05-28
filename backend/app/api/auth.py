from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.auth_user import AuthUser
from app.schemas.auth_schema import SignupRequest, LoginRequest, AuthResponse
from app.services.auth_service import hash_password, verify_password

router = APIRouter()

@router.post("/auth/signup", response_model=AuthResponse)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(AuthUser).filter(AuthUser.email == payload.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = AuthUser(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return AuthResponse(
        message="Signup successful",
        user_id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=user.role
    )

@router.post("/auth/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(AuthUser).filter(AuthUser.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return AuthResponse(
        message="Login successful",
        user_id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=user.role
    )