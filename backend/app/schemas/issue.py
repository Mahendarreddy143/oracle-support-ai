"""Issue schemas"""

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class IssueCreate(BaseModel):
    title: str
    description: str
    category: str
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    code_snippet: Optional[str] = None
    environment: Optional[str] = None
    severity: str = "medium"


class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    error_code: Optional[str]
    status: str
    severity: str
    view_count: int
    upvote_count: int
    created_at: datetime
    created_by: int

    class Config:
        from_attributes = True


class IssueListResponse(BaseModel):
    data: List[IssueResponse]
    total: int
    limit: int
    offset: int
