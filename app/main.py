from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the database Base and engine
from app.core.db import Base, engine

# Import the API routers that you have created
from app.api.v1.endpoints import jobs, candidates, submissions

# Create all database tables
# This should be done carefully in production (e.g., with Alembic migrations)
# For this project, we create them on startup.
def create_tables():
    Base.metadata.create_all(bind=engine)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="ARYA API",
    description="AI-Powered Recruitment Assessment Platform",
    version="1.0.0"
)

# --- Middleware ---
# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Event Handlers ---
@app.on_event("startup")
async def on_startup():
    """
    Event handler to run on application startup.
    """
    print("Starting up ARYA API...")
    create_tables()
    print("Database tables created successfully (if they didn't exist).")

# --- API Routers ---
# Include all the routers with a common prefix for API versioning
app.include_router(jobs.router, prefix="/api/v1", tags=["Jobs"])
app.include_router(candidates.router, prefix="/api/v1", tags=["Candidates"])
app.include_router(submissions.router, prefix="/api/v1", tags=["Submissions"])

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the ARYA API. Visit /docs for the API documentation."}