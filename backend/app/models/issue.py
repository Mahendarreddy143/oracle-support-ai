"""Issue model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database import Base


class Issue(Base):
    """Issue model for problems and errors"""

    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)  # plsql, sql, forms, etc.
    error_code = Column(String(50), nullable=True, index=True)  # ORA-06502, etc.
    error_message = Column(Text, nullable=True)
    code_snippet = Column(Text, nullable=True)
    environment = Column(String(500), nullable=True)  # JSON: {"oracle_version": "19c", "os": "Linux"}
    status = Column(String(20), default="open", index=True)  # open, resolved, closed, duplicate
    severity = Column(String(20), default="medium")  # critical, high, medium, low
    resolution_time_minutes = Column(Integer, nullable=True)
    
    # Embeddings for semantic search
    embedding = Column(String(10000), nullable=True)  # Stored as string of floats
    embedding_vector_id = Column(String(100), nullable=True)  # Vector DB ID
    
    # Metadata
    view_count = Column(Integer, default=0)
    upvote_count = Column(Integer, default=0)
    downvote_count = Column(Integer, default=0)
    relevance_score = Column(Float, default=0.0)
    
    # Foreign keys
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # Relationships
    creator = relationship("User", back_populates="issues")
    solutions = relationship("Solution", back_populates="issue")
    chat_sessions = relationship("ChatSession", back_populates="issue")

    def __repr__(self):
        return f"<Issue {self.id}: {self.title}>"
