from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    industry = Column(String(255))
    tech_skills = Column(JSON)  # Stores a list of strings
    soft_skills = Column(JSON)  # Stores a list of strings
    job_description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    project = relationship("Project", back_populates="job", uselist=False, cascade="all, delete-orphan")
    candidates = relationship("Candidate", back_populates="job", cascade="all, delete-orphan")