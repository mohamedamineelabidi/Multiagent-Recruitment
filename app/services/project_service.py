from sqlalchemy.orm import Session
import uuid

from app.services.openai_service import openai_service
from app import models
from app.api.v1 import schemas

def create_job_and_assessment(db: Session, job_create: schemas.JobCreate) -> models.Job:
    """
    Orchestrates the creation of a job and its associated project assessment.
    
    Args:
        db: Database session
        job_create: Pydantic schema with job creation data
        
    Returns:
        The created Job model instance with associated project
        
    Raises:
        ValueError: If job details cannot be extracted or project generation fails
    """
    # 1. Extract details from the job description using OpenAI
    extracted_details = openai_service.extract_job_details(job_create.job_description)
    if not extracted_details:
        raise ValueError("Could not extract details from job description. Please ensure the description is clear and contains job requirements.")

    # 2. Generate a project dictionary if project-based assessment is requested
    project_data = None
    if job_create.project_based:
        # Generate a placeholder applicant_id for project template creation
        placeholder_applicant_id = str(uuid.uuid4())[:8]
        
        try:
            project_data = openai_service.generate_project_dict(
                job_title=extracted_details["title"],
                tech_skills=extracted_details["tech_skills"],
                soft_skills=extracted_details["soft_skills"],
                industry=extracted_details["industry"],
                applicant_id=placeholder_applicant_id
            )
        except Exception as e:
            raise ValueError(f"Failed to generate project assessment: {str(e)}")

    # 3. Create the Job database object
    new_job = models.Job(
        title=extracted_details["title"],
        industry=extracted_details["industry"],
        tech_skills=extracted_details["tech_skills"],
        soft_skills=extracted_details["soft_skills"],
        job_description=job_create.job_description
    )

    # 4. If a project was generated, create the associated Project database object
    if project_data:
        new_project = models.Project(
            title=project_data.get("title", "Assessment Project"),
            objective=project_data.get("objective", "Complete the multi-phase assessment"),
            phases=project_data.get("phases", []),
            job=new_job  # This establishes the one-to-one relationship
        )
        db.add(new_project)

    # 5. Save to database
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    return new_job

def get_job_with_project(db: Session, job_id: int) -> models.Job:
    """
    Retrieves a job with its associated project data.
    
    Args:
        db: Database session
        job_id: ID of the job to retrieve
        
    Returns:
        Job model instance with project relationship loaded
        
    Raises:
        ValueError: If job is not found
    """
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise ValueError(f"Job with ID {job_id} not found.")
    return job