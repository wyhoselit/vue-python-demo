import logging
from sqlalchemy.orm import Session
from app.modules.core.database import SessionLocal, Base, engine
from app.modules.user.user import User
from app.modules.admin.models.role.role import Role
from app.modules.core.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if admin role exists, if not, create it
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)
    
    # Check if user role exists, if not, create it
    user_role = db.query(Role).filter(Role.name == "user").first()
    if not user_role:
        user_role = Role(name="user")
        db.add(user_role)
        db.commit()
        db.refresh(user_role)
    
    # Check if admin user exists, if not, create it
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin_user:
        hashed_pwd = hash_password("admin123")
        admin_user = User(email="admin@example.com", hashed_password=hashed_pwd)
        admin_user.roles.append(admin_role)
        db.add(admin_user)
        db.commit()
        logger.info("Default admin user created")
    
    db.close()

if __name__ == "__main__":
    init_db()
