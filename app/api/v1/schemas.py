from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# ===================================================================
#                       Base & Common Schemas
# ===================================================================

class ProjectBase(BaseModel):
    title: str
    objective: str
    phases: List[Dict[str, Any]]

class ProjectResponse(ProjectBase):
    id: int

    class Config:
        orm_mode = True

# ===================================================================
#                           Job Schemas
# ===================================================================

class JobBase(BaseModel):
    title: str
    industry: str
    tech_skills: List[str]
    soft_skills: List[str]
    job_description: str

class JobCreate(BaseModel):
    job_description: str
    project_based: bool = True

class JobResponse(JobBase):
    id: int
    created_at: datetime
    project: Optional[ProjectResponse] = None

    class Config:
        orm_mode = True

# ===================================================================
#                        Candidate Schemas
# ===================================================================

class CandidateBase(BaseModel):
    name: str
    email: str

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: uuid.UUID
    job_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

# ===================================================================
#                       Evaluation Schemas
# ===================================================================

class CVEvaluationResponse(BaseModel):
    match_score: int
    experience_match: int
    skills_coverage: List[str]
    skills_gaps: List[str]
    strengths: List[str]
    development_areas: List[str]
    overall_assessment: str
    interview_recommendations: List[str]

# ===================================================================
#                       Submission Schemas
# ===================================================================

class SubmissionCreate(BaseModel):
    phase_number: int = Field(..., ge=1, le=3)  # Greater/equal 1, less/equal 3
    primary_submission: str
    secondary_submission: Optional[str] = None

class SubmissionEvaluationResponse(BaseModel):
    hiring_recommendation: str
    overall_score: int
    technical_score: int
    cultural_fit_score: int
    problem_solving_score: int
    communication_score: int
    technical_strengths: List[str]
    technical_weaknesses: List[str]
    behavioral_strengths: List[str]
    behavioral_weaknesses: List[str]
    red_flags: List[str]
    interview_questions: List[str]
    hiring_manager_summary: str

# ===================================================================
#                         Ranking Schemas
# ===================================================================

class CandidateRankingDetail(BaseModel):
    rank: int
    candidate_name: str
    final_score: float
    performance_level: str
    cv_score: int
    average_project_score: float

class RankingResponse(BaseModel):
    job_title: str
    rankings: List[CandidateRankingDetail]