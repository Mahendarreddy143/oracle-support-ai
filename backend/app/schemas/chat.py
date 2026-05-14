"""Chat schemas"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ChatMessageCreate(BaseModel):
    content: str
    code_context: Optional[str] = None


class ChatSessionCreate(BaseModel):
    issue_id: Optional[int] = None
    title: Optional[str] = None


class ChatSessionResponse(BaseModel):
    id: int
    issue_id: Optional[int]
    user_id: int
    title: Optional[str]
    message_count: int
    created_at: datetime

    class Config:
        from_attributes = True
