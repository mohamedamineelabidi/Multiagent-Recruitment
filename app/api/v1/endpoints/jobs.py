from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.core.db import get_db
from app import models
from app.api.v1 import schemas
from app.services import project_service, evaluation_service, pdf_service, openai_service

router = APIRouter()

@router.post("/jobs", response_model=schemas.JobResponse, status_code=status.HTTP_201_CREATED, tags=["Jobs"])
def create_job_and_assessment(job_create: schemas.JobCreate, db: Session = Depends(get_db)):
    """
    Create a new job posting and generate its project-based assessment.
    
    This endpoint processes the job description to extract details and generates
    a multi-phase project assessment for candidate evaluation.
    """
    try:
        new_job = project_service.create_job_and_assessment(db=db, job_create=job_create)
        return new_job
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the job: {str(e)}"
        )

@router.get("/jobs/{job_id}", response_model=schemas.JobResponse, tags=["Jobs"])
def get_job_details(job_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the details for a specific job and its associated project.
    """
    try:
        job = project_service.get_job_with_project(db=db, job_id=job_id)
        return job
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the job: {str(e)}"
        )

@router.get("/jobs/{job_id}/reference-guide", tags=["Jobs"])
def get_job_reference_guide(job_id: int, db: Session = Depends(get_db)):
    """
    Generate and download a PDF reference guide for the job's project assessment.
    
    This guide contains the project details, phase descriptions, and evaluation criteria
    that can be used by hiring managers and evaluators.
    """
    try:
        # Get job with project data
        job = project_service.get_job_with_project(db=db, job_id=job_id)
        
        if not job.project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No project assessment found for this job"
            )
        
        # Prepare project data for PDF generation
        project_data = {
            "title": job.project.title,
            "objective": job.project.objective,
            "phases": job.project.phases
        }
        
        # Optionally generate ideal responses using OpenAI (for reference)
        # This could be expanded to include AI-generated ideal responses for each phase
        ideal_responses = {}
        
        # Generate PDF reference guide
        pdf_path = pdf_service.create_reference_guide_pdf(
            job_title=job.title,
            project_data=project_data,
            ideal_responses=ideal_responses
        )
        
        # Return the PDF file
        return FileResponse(
            path=pdf_path,
            media_type='application/pdf',
            filename=f"reference_guide_{job.title.replace(' ', '_')}_{job_id}.pdf"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        # Clean up the temporary file if it was created
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            os.unlink(pdf_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while generating the reference guide: {str(e)}"
        )

@router.get("/jobs/{job_id}/rankings", response_model=schemas.RankingResponse, tags=["Jobs"])
def get_job_candidate_rankings(job_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a ranked list of all candidates for a specific job based on their
    CV evaluations and project submission performances.
    """
    try:
        # Verify job exists
        job = project_service.get_job_with_project(db=db, job_id=job_id)
        
        # Get candidate rankings
        rankings = evaluation_service.rank_candidates_for_job(db=db, job_id=job_id)
        
        return {
            "job_title": job.title,
            "rankings": rankings
        }
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while ranking candidates: {str(e)}"
        )