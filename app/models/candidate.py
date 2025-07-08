import uuid

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    status = Column(String(50), default="Applied")  # e.g., Applied, Phase 1 Complete, Rejected
    cv_evaluation = Column(JSON, nullable=True)  # Stores the CV evaluation result
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    job = relationship("Job", back_populates="candidates")
    submissions = relationship("Submission", back_populates="candidate", cascade="all, delete-orphan")