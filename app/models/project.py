from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    objective = Column(Text)
    phases = Column(JSON)  # Stores the list of phase dictionaries

    # Relationship
    job = relationship("Job", back_populates="project")