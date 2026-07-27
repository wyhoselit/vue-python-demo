import logging
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import EmailAlreadyExistsError, InvalidCredentialsError

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register")
def register(credentials: dict, db: Session = Depends(get_db)):
    email = credentials.get("email")
    password = credentials.get("password")
    
    if not email or not password:
        raise InvalidCredentialsError("Email and password are required")
    
    logger.info("Registration attempt", extra={"email": email})
    
    user = db.query(User).filter(User.email == email).first()
    if user:
        logger.warning("Registration failed - email exists", extra={"email": email})
        raise EmailAlreadyExistsError()
    
    hashed_pwd = hash_password(password)
    new_user = User(email=email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info("Registration successful", extra={"user_id": new_user.id, "email": email})
    return {"id": new_user.id, "email": new_user.email}

@router.post("/login")
def login(credentials: dict, response: Response, db: Session = Depends(get_db)):
    email = credentials.get("email")
    password = credentials.get("password")
    
    if not email or not password:
        raise InvalidCredentialsError("Email and password are required")
    
    logger.info("Login attempt", extra={"email": email})
    
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        logger.warning("Login failed - invalid credentials", extra={"email": email})
        raise InvalidCredentialsError()
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=15 * 60
    )
    
    logger.info("Login successful", extra={"user_id": user.id, "email": email})
    return {"message": "Login successful"}