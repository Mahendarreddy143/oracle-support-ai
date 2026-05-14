"""User model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    expertise_areas = Column(String(500), nullable=True)  # Comma-separated: plsql,sql,forms
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    issues = relationship("Issue", back_populates="creator")
    solutions = relationship("Solution", back_populates="author")
    chat_sessions = relationship("ChatSession", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"
