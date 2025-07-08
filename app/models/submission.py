from sqlalchemy import Column, Integer, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    phase_number = Column(Integer, nullable=False)
    primary_submission = Column(Text, nullable=False)
    secondary_submission = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    evaluation = Column(JSON, nullable=True)  # Stores the submission evaluation result

    # Relationship
    candidate = relationship("Candidate", back_populates="submissions")