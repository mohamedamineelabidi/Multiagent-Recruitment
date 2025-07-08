from sqlalchemy.orm import Session, joinedload
import uuid
from typing import List

from app.services.openai_service import openai_service
from app import models
from app.api.v1 import schemas

def evaluate_candidate_cv(db: Session, candidate_id: uuid.UUID, cv_content: str) -> dict:
    """
    Evaluates a CV against job requirements, saves the result to the candidate, and returns it.
    
    Args:
        db: Database session
        candidate_id: UUID of the candidate
        cv_content: The extracted text content of the CV
        
    Returns:
        Dictionary containing the CV evaluation results
        
    Raises:
        ValueError: If candidate is not found
    """
    # 1. Fetch the candidate and their associated job with eager loading
    candidate = db.query(models.Candidate).options(
        joinedload(models.Candidate.job)
    ).filter(models.Candidate.id == candidate_id).first()
    
    if not candidate:
        raise ValueError(f"Candidate with ID {candidate_id} not found.")

    job = candidate.job
    
    # 2. Call OpenAI service to evaluate the CV against job requirements
    try:
        cv_evaluation = openai_service.evaluate_cv(
            cv_text=cv_content,
            job_title=job.title,
            tech_skills=job.tech_skills,
            soft_skills=job.soft_skills,
            industry=job.industry
        )
    except Exception as e:
        raise ValueError(f"Failed to evaluate CV: {str(e)}")

    # 3. Save the evaluation to the candidate record
    candidate.cv_evaluation = cv_evaluation
    db.commit()
    db.refresh(candidate)

    return cv_evaluation

def evaluate_and_store_submission(db: Session, candidate_id: uuid.UUID, submission_data: schemas.SubmissionCreate) -> dict:
    """
    Evaluates a project submission, creates a submission record, and returns the evaluation.
    
    Args:
        db: Database session
        candidate_id: UUID of the candidate
        submission_data: Pydantic schema with submission details
        
    Returns:
        Dictionary containing the submission evaluation results
        
    Raises:
        ValueError: If candidate, project, or phase is not found
    """
    # 1. Fetch candidate with job and project relationships
    candidate = db.query(models.Candidate).options(
        joinedload(models.Candidate.job).joinedload(models.Job.project)
    ).filter(models.Candidate.id == candidate_id).first()
    
    if not candidate:
        raise ValueError(f"Candidate with ID {candidate_id} not found.")
    
    if not candidate.job.project:
        raise ValueError(f"No project assessment found for candidate {candidate_id}.")

    project = candidate.job.project
    
    # 2. Find the specific phase details
    phase_details = next(
        (phase for phase in project.phases if phase.get('phase') == submission_data.phase_number), 
        None
    )
    if not phase_details:
        raise ValueError(f"Phase {submission_data.phase_number} not found in project assessment.")
    
    # 3. Check if submission already exists for this phase
    existing_submission = db.query(models.Submission).filter(
        models.Submission.candidate_id == candidate_id,
        models.Submission.phase_number == submission_data.phase_number
    ).first()
    
    if existing_submission:
        raise ValueError(f"Submission for phase {submission_data.phase_number} already exists for this candidate.")
        
    # 4. Combine primary and secondary submissions
    combined_submission = f"# Primary Submission\n{submission_data.primary_submission}"
    if submission_data.secondary_submission:
        combined_submission += f"\n\n# Secondary Submission\n{submission_data.secondary_submission}"

    # 5. Call OpenAI service to evaluate the submission
    try:
        submission_evaluation = openai_service.evaluate_submission(
            submission=combined_submission,
            phase_details=phase_details
        )
    except Exception as e:
        raise ValueError(f"Failed to evaluate submission: {str(e)}")

    # 6. Create and save the Submission record
    new_submission = models.Submission(
        candidate_id=candidate.id,
        phase_number=submission_data.phase_number,
        primary_submission=submission_data.primary_submission,
        secondary_submission=submission_data.secondary_submission,
        evaluation=submission_evaluation
    )
    
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    # 7. Update candidate status based on submission progress
    _update_candidate_status(db, candidate)

    return submission_evaluation

def get_candidate_with_evaluations(db: Session, candidate_id: uuid.UUID) -> models.Candidate:
    """
    Retrieves a candidate with all their evaluation data loaded.
    
    Args:
        db: Database session
        candidate_id: UUID of the candidate
        
    Returns:
        Candidate model with job, submissions, and evaluations loaded
        
    Raises:
        ValueError: If candidate is not found
    """
    candidate = db.query(models.Candidate).options(
        joinedload(models.Candidate.job).joinedload(models.Job.project),
        joinedload(models.Candidate.submissions)
    ).filter(models.Candidate.id == candidate_id).first()
    
    if not candidate:
        raise ValueError(f"Candidate with ID {candidate_id} not found.")
    
    return candidate

def rank_candidates_for_job(db: Session, job_id: int) -> List[dict]:
    """
    Ranks all candidates for a specific job based on their CV and submission evaluations.
    
    Args:
        db: Database session
        job_id: ID of the job to rank candidates for
        
    Returns:
        List of candidate ranking dictionaries sorted by final score
    """
    # Fetch all candidates for the job with their evaluations
    candidates = db.query(models.Candidate).options(
        joinedload(models.Candidate.submissions)
    ).filter(models.Candidate.job_id == job_id).all()
    
    if not candidates:
        return []
    
    rankings = []
    
    for candidate in candidates:
        # Calculate CV score
        cv_score = 0
        if candidate.cv_evaluation:
            cv_score = candidate.cv_evaluation.get('match_score', 0)
        
        # Calculate average submission score
        submission_scores = []
        for submission in candidate.submissions:
            if submission.evaluation:
                submission_scores.append(submission.evaluation.get('overall_score', 0))
        
        avg_submission_score = sum(submission_scores) / len(submission_scores) if submission_scores else 0
        
        # Calculate final score (weighted: CV 30%, submissions 70%)
        if submission_scores:
            final_score = (cv_score * 0.3) + (avg_submission_score * 0.7)
        else:
            final_score = cv_score
        
        # Determine performance level
        if final_score >= 90:
            performance_level = "Outstanding candidate - Strong recommend for immediate hire"
        elif final_score >= 80:
            performance_level = "Excellent candidate - Recommend for hire"
        elif final_score >= 70:
            performance_level = "Good candidate - Consider for hire with potential"
        elif final_score >= 60:
            performance_level = "Fair candidate - Proceed with caution"
        else:
            performance_level = "Below expectations - Not recommended"
        
        rankings.append({
            "candidate_name": candidate.name,
            "final_score": round(final_score, 1),
            "performance_level": performance_level,
            "cv_score": cv_score,
            "average_project_score": round(avg_submission_score, 1)
        })
    
    # Sort by final score (descending) and assign ranks
    rankings.sort(key=lambda x: x["final_score"], reverse=True)
    for i, ranking in enumerate(rankings):
        ranking["rank"] = i + 1
    
    return rankings

def _update_candidate_status(db: Session, candidate: models.Candidate) -> None:
    """
    Updates candidate status based on their submission progress.
    
    Args:
        db: Database session
        candidate: Candidate model instance
    """
    submission_count = len(candidate.submissions)
    
    if submission_count == 0:
        candidate.status = "Applied"
    elif submission_count == 1:
        candidate.status = "Phase 1 Complete"
    elif submission_count == 2:
        candidate.status = "Phase 2 Complete"
    elif submission_count >= 3:
        candidate.status = "Assessment Complete"
    
    db.commit()