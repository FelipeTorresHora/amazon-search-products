"""User database model."""
from sqlalchemy import Boolean, Column, String, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class UserRole(str, enum.Enum):
    """User roles for RBAC."""
    USER = "user"
    PRO = "pro"
    BUSINESS = "business"
    ADMIN = "admin"


class User(BaseModel):
    """User account model."""

    __tablename__ = "users"

    # Basic Info
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)

    # Role
    role = Column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )

    # Relationships
    # subscription = relationship("Subscription", back_populates="user", uselist=False)
    # alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    # search_history = relationship("SearchHistory", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"
