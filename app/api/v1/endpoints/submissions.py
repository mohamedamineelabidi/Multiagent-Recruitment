from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app.core.db import get_db
from app import models
from app.api.v1 import schemas
from app.services import evaluation_service

router = APIRouter()

@router.post("/candidates/{candidate_id}/submissions", response_model=schemas.SubmissionEvaluationResponse, status_code=status.HTTP_201_CREATED, tags=["Submissions"])
def create_submission(candidate_id: uuid.UUID, submission_create: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    """
    Submit work for a project phase, trigger an evaluation, and store the result.
    
    This endpoint allows candidates to submit their work for any phase of the project assessment.
    The submission is immediately evaluated using AI and the results are stored in the database.
    """
    try:
        # Validate and process the submission through the evaluation service
        evaluation = evaluation_service.evaluate_and_store_submission(
            db=db, 
            candidate_id=candidate_id, 
            submission_data=submission_create
        )
        return evaluation
        
    except ValueError as e:
        # Handle specific business logic errors (candidate not found, phase not found, etc.)
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif "already exists" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
            
    except Exception as e:
        # Generic error for other potential issues
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An unexpected error occurred while processing the submission: {str(e)}"
        )

@router.get("/candidates/{candidate_id}/submissions", response_model=list[schemas.SubmissionEvaluationResponse], tags=["Submissions"])
def get_candidate_submissions(candidate_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Retrieve all submissions and their evaluations for a specific candidate.
    """
    try:
        # Get candidate with submissions
        candidate = evaluation_service.get_candidate_with_evaluations(db=db, candidate_id=candidate_id)
        
        # Extract evaluations from submissions
        evaluations = []
        for submission in sorted(candidate.submissions, key=lambda s: s.phase_number):
            if submission.evaluation:
                # Add phase information to the evaluation
                evaluation_data = submission.evaluation.copy()
                evaluation_data["phase_number"] = submission.phase_number
                evaluation_data["submitted_at"] = submission.submitted_at.isoformat()
                evaluations.append(evaluation_data)
        
        return evaluations
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An error occurred while retrieving submissions: {str(e)}"
        )

@router.get("/candidates/{candidate_id}/submissions/{phase_number}", response_model=schemas.SubmissionEvaluationResponse, tags=["Submissions"])
def get_submission_by_phase(candidate_id: uuid.UUID, phase_number: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific submission and its evaluation by candidate ID and phase number.
    """
    try:
        # Find the specific submission
        submission = db.query(models.Submission).filter(
            models.Submission.candidate_id == candidate_id,
            models.Submission.phase_number == phase_number
        ).first()
        
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No submission found for candidate {candidate_id} in phase {phase_number}"
            )
        
        if not submission.evaluation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No evaluation found for submission in phase {phase_number}"
            )
        
        # Return the evaluation with additional metadata
        evaluation_data = submission.evaluation.copy()
        evaluation_data["phase_number"] = submission.phase_number
        evaluation_data["submitted_at"] = submission.submitted_at.isoformat()
        
        return evaluation_data
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An error occurred while retrieving the submission: {str(e)}"
        )