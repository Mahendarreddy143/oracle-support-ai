"""Solution model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Solution(Base):
    """Solution/answer to an issue"""

    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=True)
    code_snippet = Column(Text, nullable=True)
    implementation_steps = Column(Text, nullable=True)  # JSON array
    verification_steps = Column(Text, nullable=True)  # JSON array
    references = Column(Text, nullable=True)  # JSON array of links
    
    # Metadata
    is_verified = Column(String(20), default="unverified")  # unverified, verified, ai_generated
    upvote_count = Column(Integer, default=0)
    downvote_count = Column(Integer, default=0)
    acceptance_rating = Column(Integer, default=0)  # 1-5 stars
    view_count = Column(Integer, default=0)
    
    # Foreign keys
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    issue = relationship("Issue", back_populates="solutions")
    author = relationship("User", back_populates="solutions")

    def __repr__(self):
        return f"<Solution {self.id}: {self.title}>"
