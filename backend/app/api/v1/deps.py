from fastapi import Depends, HTTPException, status, Request
from app.modules.user.user import User
from app.modules.core.database import get_db
from sqlalchemy.orm import Session
from app.modules.core.security import verify_token
from typing import Optional

def extract_token_from_request(request: Request) -> Optional[str]:
    # Check Authorization header (Bearer)
    # FastAPI stores headers in a special way, check the raw scope first for compatibility
    auth_header = None
    if hasattr(request, 'scope'):
        for header_name, header_value in request.scope.get("headers", []):
            if header_name.lower() == b"authorization":
                auth_header = header_value.decode("utf-8")
                break
    
    # Fallback to FastAPI's headers.get() method
    if not auth_header:
        auth_header = request.headers.get("Authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[len("Bearer "):]
    
    # Fallback to cookie
    return request.cookies.get("access_token")

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = extract_token_from_request(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if not any(role.name == "admin" for role in user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user
