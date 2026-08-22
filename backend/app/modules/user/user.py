"""User model and related database operations.

Defines the SQLAlchemy User model with role-based access control
support.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.modules.admin.models.role.role import user_roles
from app.modules.core.database import Base


class User(Base):
    """SQLAlchemy model for application users.

    Attributes:
        id: Primary key.
        email: Unique email address.
        hashed_password: Bcrypt-hashed password.
        roles: Many-to-many relationship with Role.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    roles = relationship("Role", secondary=user_roles, back_populates="users")
