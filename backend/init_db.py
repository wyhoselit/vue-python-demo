import logging
import os
import secrets
from dotenv import dotenv_values
from sqlalchemy.orm import Session
from app.modules.core.database import SessionLocal, Base, engine
from app.modules.user.user import User
from app.modules.admin.models.role.role import Role
from app.modules.core.security import hash_password
from app.modules.system.models.system_setting import SystemSetting

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN_FILE = ".token"

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

    # Check if tracing is exists, if not, create it with default false
    tracing = db.query(SystemSetting).filter(SystemSetting.key == "system.tracing").first()
    if not tracing:
        tracing = SystemSetting(key="system.tracing", settings=False)
        db.add(tracing)
        db.commit()
        logger.info("Default tracing seeded to database")

    #Check if logfile path is exists, if not, create it with default value
    log_file_path = db.query(SystemSetting).filter(SystemSetting.key == "system.log_file_path").first()
    if not log_file_path:
        log_file_path = SystemSetting(key="system.log_file_path", settings="./backend/logs")
        db.add(log_file_path)
        db.commit()
        logger.info("Default logfile path seeded to database")

    

    # Sync default bearer token
    token = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token = f.read().strip()
    
    if not token:
        token = secrets.token_urlsafe(32)
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        logger.info("Generated new default bearer token")

    setting = db.query(SystemSetting).filter(SystemSetting.key == "system.default_bearer_token").first()
    if not setting:
        setting = SystemSetting(key="system.default_bearer_token", settings=token)
        db.add(setting)
        db.commit()
        logger.info("Default bearer token seeded to database")

    # check auth_method exists in db, if not, create it with default value
    auth_method = db.query(SystemSetting).filter(SystemSetting.key == "system.auth_method").first()
    if not auth_method:
        auth_method = SystemSetting(key="system.auth_method", settings="cookie_or_bearer")
        db.add(auth_method)
        db.commit()
        logger.info("Default auth_method seeded to database")

    # check token_expiry_hours exists in db, if not, create it with default value
    token_expiry_hours = db.query(SystemSetting).filter(SystemSetting.key == "system.token_expiry_hours").first()
    if not token_expiry_hours:
        token_expiry_hours = SystemSetting(key="system.token_expiry_hours", settings="24")
        db.add(token_expiry_hours)
        db.commit()
        logger.info("Default token_expiry_hours seeded to database")

    # load all .env value to db
    env_file = dotenv_values(".env")
    for key, value in env_file.items():
        setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
        if not setting:
            setting = SystemSetting(key=key, settings=value)
            db.add(setting)
            db.commit()
            logger.info(f"Default {key} seeded to database")



    db.close()

if __name__ == "__main__":
    init_db()
