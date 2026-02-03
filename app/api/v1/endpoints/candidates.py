"""
Candidates API Endpoints

This module handles all candidate-related HTTP operations including:
- Candidate registration for jobs
- CV upload and AI-powered evaluation
- Candidate report generation
"""

import logging
import os
import uuid
from io import BytesIO

import PyPDF2
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import models
from app.api.v1 import schemas
from app.core.db import get_db
from app.services import evaluation_service, pdf_service

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/jobs/{job_id}/candidates",
    response_model=schemas.CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Candidates"],
    summary="Register a new candidate",
    description="Register a new candidate for a specific job posting."
)
def create_candidate_for_job(
    job_id: int,
    candidate_create: schemas.CandidateCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new candidate for a specific job.
    
    Args:
        job_id: The ID of the job to apply for
        candidate_create: Candidate registration data (name, email)
        db: Database session
        
    Returns:
        CandidateResponse: The created candidate object
        
    Raises:
        HTTPException 404: If job is not found
        HTTPException 400: If candidate email already exists for this job
    """
    # Check if the job exists
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID {job_id} not found"
        )

    # Check if candidate already exists for this job
    existing_candidate = db.query(models.Candidate).filter(
        models.Candidate.email == candidate_create.email,
        models.Candidate.job_id == job_id
    ).first()
    
    if existing_candidate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A candidate with this email is already registered for this job."
        )

    # Create new candidate
    try:
        new_candidate = models.Candidate(
            **candidate_create.model_dump(),
            job_id=job_id
        )
        db.add(new_candidate)
        db.commit()
        db.refresh(new_candidate)
        logger.info(f"Created new candidate: {new_candidate.id} for job: {job_id}")
        return new_candidate
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating candidate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create candidate. Please try again."
        )

@router.post("/candidates/{candidate_id}/cv", response_model=schemas.CVEvaluationResponse, tags=["Candidates"])
async def upload_and_evaluate_cv(candidate_id: uuid.UUID, cv_file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a CV (PDF) for a candidate and trigger its evaluation against the job requirements.
    """
    # Validate file type
    if cv_file.content_type != 'application/pdf':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid file type. Please upload a PDF file."
        )

    # Extract text from PDF
    cv_text = ""
    try:
        pdf_content = await cv_file.read()
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
        
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                cv_text += extracted_text + "\n"
                
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Failed to read PDF file: {str(e)}"
        )
        
    # Validate extracted content
    if len(cv_text.strip()) < 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="The PDF seems to be empty or could not be read properly. Please ensure the PDF contains readable text."
        )

    # Evaluate the CV using the evaluation service
    try:
        evaluation = evaluation_service.evaluate_candidate_cv(
            db=db, 
            candidate_id=candidate_id, 
            cv_content=cv_text
        )
        return evaluation
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An error occurred during CV evaluation: {str(e)}"
        )

@router.get("/candidates/{candidate_id}/report", tags=["Candidates"])
def get_candidate_report(candidate_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Generate and download a comprehensive PDF report for a candidate's evaluation.
    """
    try:
        # Retrieve candidate with all evaluation data
        candidate = evaluation_service.get_candidate_with_evaluations(db=db, candidate_id=candidate_id)
        
        # Generate PDF report
        pdf_path = pdf_service.create_candidate_report_pdf(candidate)
        
        # Return the PDF file
        return FileResponse(
            path=pdf_path,
            media_type='application/pdf',
            filename=f"candidate_report_{candidate.name.replace(' ', '_')}_{str(candidate_id)[:8]}.pdf"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        # Clean up the temporary file if it was created
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            os.unlink(pdf_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An error occurred while generating the report: {str(e)}"
        )