"""
ARYA API - AI-Powered Recruitment Assessment Platform

This is the main entry point for the ARYA FastAPI application.
It initializes the application, configures middleware, and sets up routing.

Author: Mohamed Amine Elabidi
Version: 1.0.0
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import candidates, jobs, submissions
from app.core.db import Base, engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_tables() -> None:
    """
    Create all database tables defined in SQLAlchemy models.
    
    Note: In production, consider using Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)


# --- FastAPI Application ---
app = FastAPI(
    title="ARYA API",
    description="""
## AI-Powered Recruitment Assessment Platform 🤖

ARYA (AI Recruitment & Yield Assessment) revolutionizes hiring through:

- **Intelligent Job Analysis** - AI-powered extraction of job requirements
- **Project-Based Assessments** - AI-resistant multi-phase candidate evaluations
- **Automated CV Evaluation** - Smart resume parsing and scoring
- **Candidate Ranking** - Weighted scoring algorithms for objective comparison

### Resources
- [GitHub Repository](https://github.com/mohamedamineelabidi/Multiagent-Recruitment)
- [Documentation](https://github.com/mohamedamineelabidi/Multiagent-Recruitment/blob/main/docs/SYSTEM_ARCHITECTURE_ANALYSIS.md)
    """,
    version="1.0.0",
    contact={
        "name": "Mohamed Amine Elabidi",
        "url": "https://github.com/mohamedamineelabidi",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Event Handlers ---
@app.on_event("startup")
async def on_startup() -> None:
    """Initialize application on startup."""
    logger.info("Starting ARYA API...")
    create_tables()
    logger.info("Database tables created successfully.")


# --- API Routers ---
app.include_router(jobs.router, prefix="/api/v1", tags=["Jobs"])
app.include_router(candidates.router, prefix="/api/v1", tags=["Candidates"])
app.include_router(submissions.router, prefix="/api/v1", tags=["Submissions"])


# --- Health Check ---
@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - Health check.
    
    Returns a welcome message confirming the API is running.
    """
    return {
        "message": "Welcome to ARYA API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns the current health status of the API.
    """
    return {
        "status": "healthy",
        "service": "arya-api",
        "version": "1.0.0"
    }