"""User schemas"""

from typing import Optional
from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    is_verified: bool
    bio: Optional[str]
    expertise_areas: Optional[str]

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    expertise_areas: Optional[str] = None
