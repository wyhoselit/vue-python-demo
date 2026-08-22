"""Role model for user permission management."""
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.modules.core.database import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

class Role(Base):
    """Role model for RBAC permission management.

    Attributes:
        id: Primary key identifier.
        name: Unique role name (e.g., 'admin', 'user').
        users: Relationship to users assigned this role.
    """

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    users = relationship("User", secondary=user_roles, back_populates="roles")
