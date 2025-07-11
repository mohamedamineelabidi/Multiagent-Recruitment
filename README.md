# ARYA API 🤖

**AI-Powered Recruitment Assessment Platform**

ARYA (AI Recruitment & Yield Assessment) is a sophisticated backend API that revolutionizes the hiring process by leveraging artificial intelligence to create project-based assessments, evaluate candidates, and provide intelligent rankings.

## 🏗️ System Architecture & Agent Framework

ARYA API follows a **multi-agent architecture** where each component acts as a specialized agent with distinct responsibilities. This design ensures separation of concerns, scalability, and maintainability.

## 🎭 Agent Overview

The system consists of **7 primary agent types** that communicate in a hierarchical, event-driven manner:

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Web App   │  │  Mobile App │  │   API Docs  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
                    HTTP Requests/Responses
                              │
┌─────────────────────────────────────────────────────────────────┐
│                     API GATEWAY LAYER                           │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                FastAPI Application                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │CORS Handler │  │Rate Limiter │  │  Validator  │       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    ENDPOINT AGENTS LAYER                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Jobs Agent  │  │Candidates   │  │Submissions  │             │
│  │            │  │   Agent     │  │   Agent     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                   SERVICE AGENTS LAYER                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Project    │  │ Evaluation  │  │    PDF      │             │
│  │  Service    │  │  Service    │  │  Service    │             │
│  │   Agent     │  │   Agent     │  │   Agent     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL AGENTS LAYER                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  OpenAI     │  │  Database   │  │File System │             │
│  │  Agent      │  │   Agent     │  │   Agent     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Detailed Agent Specifications

### 1. 🚪 **Endpoint Agents** (API Layer)
*Location: `app/api/v1/endpoints/`*

#### **Jobs Agent** (`jobs.py`)
```python
class JobsAgent:
    responsibilities = [
        "HTTP request validation and routing",
        "Job creation workflow orchestration", 
        "Reference guide generation coordination",
        "Candidate rankings aggregation"
    ]
    
    communication_patterns = {
        "receives_from": ["HTTP Clients", "Frontend Applications"],
        "delegates_to": ["ProjectService", "EvaluationService", "PDFService"],
        "responds_to": ["HTTP Clients with JSON/PDF responses"]
    }
    
    key_operations = {
        "POST /jobs": "create_job_and_assessment()",
        "GET /jobs/{id}": "get_job_details()",
        "GET /jobs/{id}/reference-guide": "get_job_reference_guide()",
        "GET /jobs/{id}/rankings": "get_job_candidate_rankings()"
    }
```

**Agent Behavior:**
- **Input Validation**: Validates JobCreate schema using Pydantic
- **Business Logic Delegation**: Never performs complex operations directly
- **Error Translation**: Converts service exceptions to HTTP status codes
- **Response Formatting**: Ensures consistent API response structure

#### **Candidates Agent** (`candidates.py`)
```python
class CandidatesAgent:
    responsibilities = [
        "Candidate registration and management",
        "CV upload and processing coordination",
        "Candidate data retrieval and reporting"
    ]
    
    communication_patterns = {
        "receives_from": ["HTTP Clients with multipart/form-data"],
        "delegates_to": ["EvaluationService", "PDFService"],
        "coordinates_with": ["JobsAgent for job validation"]
    }
    
    key_operations = {
        "POST /jobs/{job_id}/candidates": "create_candidate_for_job()",
        "POST /candidates/{id}/cv": "upload_and_evaluate_cv()",
        "GET /candidates/{id}": "get_candidate_details()",
        "GET /candidates/{id}/report": "get_candidate_report()"
    }
```

**Agent Behavior:**
- **File Processing**: Handles multipart uploads and PDF extraction
- **Relationship Management**: Ensures candidates are linked to valid jobs
- **Duplicate Prevention**: Checks for existing candidates with same email
- **Asynchronous Operations**: Manages file processing workflows

#### **Submissions Agent** (`submissions.py`)
```python
class SubmissionsAgent:
    responsibilities = [
        "Project submission intake and validation",
        "Evaluation workflow coordination",
        "Submission history management"
    ]
    
    communication_patterns = {
        "receives_from": ["HTTP Clients with JSON payloads"],
        "delegates_to": ["EvaluationService for AI assessment"],
        "validates_with": ["DatabaseAgent for candidate/job existence"]
    }
    
    key_operations = {
        "POST /candidates/{id}/submissions": "create_submission()",
        "GET /candidates/{id}/submissions": "get_candidate_submissions()",
        "GET /candidates/{id}/submissions/{phase}": "get_phase_submission()"
    }
```

### 2. 🔧 **Service Agents** (Business Logic Layer)
*Location: `app/services/`*

#### **Project Service Agent** (`project_service.py`)
```python
class ProjectServiceAgent:
    responsibilities = [
        "Job analysis and skill extraction coordination",
        "Project generation workflow orchestration",
        "Job-project relationship management"
    ]
    
    intelligence_level = "Orchestration Intelligence"
    decision_making = [
        "Determines project complexity based on job requirements",
        "Coordinates between OpenAI and Database agents",
        "Manages transaction boundaries for job creation"
    ]
    
    communication_flow = {
        "step_1": "Receive job description from EndpointAgent",
        "step_2": "Request skill extraction from OpenAIAgent",
        "step_3": "Request project generation from OpenAIAgent", 
        "step_4": "Coordinate data persistence with DatabaseAgent",
        "step_5": "Return structured job data to EndpointAgent"
    }
```

**Agent Intelligence:**
- **Workflow Orchestration**: Manages complex multi-step job creation
- **Error Recovery**: Handles partial failures and rollback scenarios
- **Data Transformation**: Converts between API models and database models
- **Business Rules**: Enforces job creation policies and constraints

#### **Evaluation Service Agent** (`evaluation_service.py`)
```python
class EvaluationServiceAgent:
    responsibilities = [
        "CV evaluation workflow management",
        "Submission assessment coordination", 
        "Candidate ranking algorithm execution",
        "Performance analytics calculation"
    ]
    
    intelligence_level = "Assessment Intelligence"
    decision_making = [
        "Determines evaluation criteria based on job context",
        "Manages multi-phase assessment progression",
        "Calculates weighted scores and final rankings",
        "Identifies evaluation inconsistencies and bias"
    ]
    
    evaluation_pipeline = {
        "cv_evaluation": {
            "step_1": "Extract and validate CV content",
            "step_2": "Gather job context from DatabaseAgent",
            "step_3": "Request AI evaluation from OpenAIAgent",
            "step_4": "Store evaluation results via DatabaseAgent"
        },
        "submission_evaluation": {
            "step_1": "Validate submission against phase requirements",
            "step_2": "Gather candidate context and history",
            "step_3": "Request AI assessment with full context",
            "step_4": "Calculate progression metrics",
            "step_5": "Store comprehensive evaluation"
        },
        "ranking_calculation": {
            "step_1": "Aggregate all candidate evaluations",
            "step_2": "Apply weighted scoring algorithm",
            "step_3": "Generate performance level classifications",
            "step_4": "Return ranked candidate list"
        }
    }
```

**Agent Intelligence:**
- **Context Awareness**: Considers full candidate journey in evaluations
- **Adaptive Assessment**: Adjusts evaluation criteria based on job requirements
- **Quality Assurance**: Implements consistency checks and bias detection
- **Predictive Analytics**: Calculates success probability and performance trends

#### **PDF Service Agent** (`pdf_service.py`)
```python
class PDFServiceAgent:
    responsibilities = [
        "Document generation and formatting",
        "Unicode character handling and sanitization",
        "Template-based report creation",
        "File system management for temporary files"
    ]
    
    intelligence_level = "Document Intelligence"
    capabilities = [
        "Dynamic PDF layout based on content complexity",
        "Multi-language text processing and cleanup",
        "Template selection based on document type",
        "Resource management for temporary file cleanup"
    ]
    
    document_types = {
        "candidate_report": {
            "sections": ["Header", "CV Summary", "Submissions", "Recommendation"],
            "complexity": "High - Multi-page with dynamic content"
        },
        "reference_guide": {
            "sections": ["Overview", "Phases", "Evaluation Criteria"],
            "complexity": "Medium - Structured template-based"
        }
    }
```

### 3. 🤖 **External Service Agents**

#### **OpenAI Service Agent** (`openai_service.py`)
```python
class OpenAIServiceAgent:
    responsibilities = [
        "Natural language processing and analysis",
        "Intelligent content generation",
        "Evaluation and scoring algorithms",
        "AI model interaction management"
    ]
    
    intelligence_level = "Artificial Intelligence"
    capabilities = [
        "Job requirement extraction from descriptions",
        "AI-resistant project generation",
        "Multi-dimensional candidate evaluation",
        "Contextual assessment with bias awareness"
    ]
    
    ai_operations = {
        "extract_job_details": {
            "input": "Raw job description text",
            "processing": "NLP analysis for skills and requirements",
            "output": "Structured job data (title, skills, industry)"
        },
        "generate_project_dict": {
            "input": "Job requirements and constraints",
            "processing": "Creative project design with AI-resistance",
            "output": "3-phase project with unique challenges"
        },
        "evaluate_cv": {
            "input": "CV text + job requirements",
            "processing": "Comprehensive candidate assessment",
            "output": "Multi-dimensional evaluation scores"
        },
        "evaluate_submission": {
            "input": "Submission + phase context + candidate history",
            "processing": "Contextual performance analysis",
            "output": "Detailed evaluation with recommendations"
        }
    }
    
    ai_resistance_strategies = [
        "Unique identifier injection for personalization",
        "Context-dependent challenge generation",
        "Multi-phase continuity requirements",
        "Human verification components (audio/video)"
    ]
```

#### **Database Agent** (`app/core/db.py` + `app/models/`)
```python
class DatabaseAgent:
    responsibilities = [
        "Data persistence and retrieval",
        "Relationship integrity management",
        "Transaction coordination",
        "Query optimization and caching"
    ]
    
    intelligence_level = "Data Intelligence"
    data_models = {
        "Job": {
            "relationships": ["Project (1:1)", "Candidates (1:many)"],
            "intelligence": "Stores job requirements and metadata"
        },
        "Project": {
            "relationships": ["Job (1:1)"],
            "intelligence": "Contains AI-generated assessment phases"
        },
        "Candidate": {
            "relationships": ["Job (many:1)", "Submissions (1:many)"],
            "intelligence": "Tracks candidate journey and evaluations"
        },
        "Submission": {
            "relationships": ["Candidate (many:1)"],
            "intelligence": "Stores phase work and AI evaluations"
        }
    }
    
    operations = {
        "session_management": "Provides database sessions to service agents",
        "relationship_loading": "Eager loads related data for complex queries",
        "transaction_handling": "Ensures ACID compliance for multi-table operations",
        "connection_pooling": "Manages database connections efficiently"
    }
```

## 🔄 Agent Communication Patterns

### **1. Request Flow Architecture**
```
Client Request → Endpoint Agent → Service Agent → External Agents → Response
```

### **2. Job Creation Flow**
```mermaid
sequenceDiagram
    participant C as Client
    participant JA as Jobs Agent
    participant PS as Project Service
    participant OA as OpenAI Agent
    participant DA as Database Agent

    C->>JA: POST /jobs (job_description)
    JA->>PS: create_job_and_assessment()
    PS->>OA: extract_job_details(description)
    OA-->>PS: {title, skills, industry}
    PS->>OA: generate_project_dict()
    OA-->>PS: {project_phases}
    PS->>DA: save_job_and_project()
    DA-->>PS: job_with_id
    PS-->>JA: complete_job_object
    JA-->>C: 201 Created + job_data
```

### **3. Submission Evaluation Flow**
```mermaid
sequenceDiagram
    participant C as Client
    participant SA as Submissions Agent
    participant ES as Evaluation Service
    participant DA as Database Agent
    participant OA as OpenAI Agent

    C->>SA: POST /candidates/{id}/submissions
    SA->>ES: evaluate_and_store_submission()
    ES->>DA: get_candidate_context()
    DA-->>ES: {candidate, job, history}
    ES->>OA: evaluate_submission(context)
    OA-->>ES: {evaluation_scores}
    ES->>DA: save_evaluation()
    DA-->>ES: confirmation
    ES-->>SA: complete_evaluation
    SA-->>C: 201 Created + evaluation
```

## 🧠 Agent Intelligence Levels

### **Level 1: Protocol Intelligence** (Endpoint Agents)
- **Responsibilities**: HTTP protocol handling, validation, routing
- **Decision Making**: Route determination, error code selection
- **Memory**: Stateless, request-scoped only

### **Level 2: Orchestration Intelligence** (Service Agents)
- **Responsibilities**: Business logic coordination, workflow management
- **Decision Making**: Process flow control, error recovery strategies
- **Memory**: Transaction-scoped, maintains operation context

### **Level 3: Domain Intelligence** (OpenAI Agent)
- **Responsibilities**: Natural language understanding, content generation
- **Decision Making**: Assessment criteria, evaluation scoring, bias detection
- **Memory**: Context-aware, learns from interaction patterns

### **Level 4: Data Intelligence** (Database Agent)
- **Responsibilities**: Data integrity, relationship management, optimization
- **Decision Making**: Query optimization, caching strategies, connection pooling
- **Memory**: Persistent, maintains all system state

## 🔒 Agent Security & Access Control

### **Agent Permission Matrix**
```
┌─────────────────┬─────────┬─────────┬─────────┬─────────┐
│ Agent Type      │ Read DB │ Write DB│ Call AI │ File I/O│
├─────────────────┼─────────┼─────────┼─────────┼─────────┤
│ Endpoint Agents │    ❌   │    ❌   │    ❌   │    ❌   │
│ Service Agents  │    ✅   │    ✅   │    ✅   │    ✅   │
│ OpenAI Agent    │    ❌   │    ❌   │    ✅   │    ❌   │
│ Database Agent  │    ✅   │    ✅   │    ❌   │    ❌   │
│ PDF Agent       │    ❌   │    ❌   │    ❌   │    ✅   │
└─────────────────┴─────────┴─────────┴─────────┴─────────┘
```

### **Data Flow Security**
- **Endpoint → Service**: Validated data only
- **Service → External**: Sanitized and context-aware requests
- **External → Service**: Validated responses with error handling
- **Service → Endpoint**: Structured responses with proper status codes

## 📊 Agent Performance Metrics

### **Response Time Targets**
```
Endpoint Agents:     < 50ms   (validation + routing)
Service Agents:      < 200ms  (orchestration + logic)
OpenAI Agent:        < 5000ms (AI processing)
Database Agent:      < 100ms  (query execution)
PDF Agent:           < 1000ms (document generation)
```

### **Scalability Characteristics**
- **Endpoint Agents**: Stateless, horizontally scalable
- **Service Agents**: Stateless business logic, scalable with connection pooling
- **OpenAI Agent**: Rate-limited by external API, requires queueing for scale
- **Database Agent**: Vertically scalable with read replicas for scale
- **PDF Agent**: CPU-bound, benefits from worker processes

This agent-based architecture ensures **separation of concerns**, **maintainable code**, **scalable design**, and **clear responsibility boundaries** throughout the ARYA API system.

## 🚀 Features

- **AI-Powered Job Analysis**: Automatically extracts skills and requirements from job descriptions
- **Dynamic Project Generation**: Creates custom, AI-resistant project assessments
- **CV Evaluation**: Intelligent analysis of candidate resumes with detailed scoring
- **Submission Assessment**: Comprehensive evaluation of project submissions
- **Smart Candidate Ranking**: AI-driven ranking system based on multiple criteria
- **Multi-language Support**: Handles job descriptions in various languages
- **Interactive Documentation**: Built-in Swagger UI for API testing

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **AI Integration**: OpenAI GPT models
- **PDF Processing**: PyPDF2, python-multipart
- **Documentation**: Automatic OpenAPI/Swagger generation

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Git

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd arya_api
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./arya.db

# For production (Azure PostgreSQL):
DATABASE_URL=postgresql://postgres:password@arya-database-dev-server.postgres.database.azure.com:5432/arya_db?sslmode=require
```

### 4. Run the Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the API
- **API Base URL**: `http://localhost:8000`
- **Interactive Documentation**: `http://localhost:8000/docs`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 📚 API Documentation

### 🏢 Jobs Endpoints

#### Create Job and Assessment
**POST** `/api/v1/jobs`

Creates a new job posting and automatically generates a project-based assessment.

**Request Body:**
```json
{
  "job_description": "We are seeking a Senior Data Scientist...",
  "project_based": true
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Senior Data Scientist",
  "industry": "Healthcare",
  "tech_skills": ["Python", "R", "SQL", "TensorFlow"],
  "soft_skills": ["Communication", "Problem-solving"],
  "job_description": "...",
  "created_at": "2025-07-08T14:11:27",
  "project": {
    "id": 1,
    "title": "Vital Insights: Navigating Data in Healthcare",
    "objective": "Design a predictive model...",
    "phases": [...]
  }
}
```

**Features:**
- Automatic skill extraction from job descriptions
- AI-generated project assessments with 3 phases
- Anti-AI tactics to ensure authentic candidate evaluation
- Support for multiple languages

#### Get Job Details
**GET** `/api/v1/jobs/{job_id}`

Retrieves complete job information including the associated project.

**Response:** Same structure as job creation response.

#### Get Job Reference Guide
**GET** `/api/v1/jobs/{job_id}/reference-guide`

Downloads a PDF reference guide for the job's project assessment.

**Response:** PDF file download containing project instructions and guidelines.

#### Get Job Candidate Rankings
**GET** `/api/v1/jobs/{job_id}/rankings`

Returns a ranked list of all candidates for the specified job.

**Response:**
```json
{
  "job_title": "Senior Data Scientist",
  "rankings": [
    {
      "rank": 1,
      "candidate_name": "Jane Doe",
      "final_score": 87.5,
      "performance_level": "Excellent",
      "cv_score": 85,
      "average_project_score": 90.0
    }
  ]
}
```

### 👥 Candidates Endpoints

#### Create Candidate
**POST** `/api/v1/jobs/{job_id}/candidates`

Registers a new candidate for a specific job.

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "job_id": 1,
  "status": "active",
  "created_at": "2025-07-08T14:15:30"
}
```

#### Get Candidate Details
**GET** `/api/v1/candidates/{candidate_id}`

Retrieves detailed information about a specific candidate.

#### List Job Candidates
**GET** `/api/v1/jobs/{job_id}/candidates`

Returns all candidates registered for a specific job.

#### Evaluate Candidate CV
**POST** `/api/v1/candidates/{candidate_id}/cv`

Uploads and evaluates a candidate's CV/resume.

**Request:** Multipart form data with PDF file upload

**Response:**
```json
{
  "match_score": 82,
  "experience_match": 85,
  "skills_coverage": ["Python", "Machine Learning", "SQL"],
  "skills_gaps": ["TensorFlow", "Deep Learning"],
  "strengths": ["Strong programming background", "Relevant experience"],
  "development_areas": ["Could benefit from AI/ML specialization"],
  "overall_assessment": "Strong candidate with solid foundation...",
  "interview_recommendations": [
    "Ask about specific ML projects",
    "Discuss experience with healthcare data"
  ]
}
```

**Features:**
- PDF text extraction and analysis
- Skills matching against job requirements
- Comprehensive scoring system
- Interview preparation recommendations

### 📝 Submissions Endpoints

#### Submit Project Phase
**POST** `/api/v1/candidates/{candidate_id}/submissions`

Submits and evaluates a candidate's work for a specific project phase.

**Request Body:**
```json
{
  "phase_number": 1,
  "primary_submission": "Here is my Python code for the data processing pipeline...",
  "secondary_submission": "Changelog: I decided to use pandas for data manipulation..."
}
```

**Response:**
```json
{
  "hiring_recommendation": "Strong Hire",
  "overall_score": 87,
  "technical_score": 90,
  "cultural_fit_score": 85,
  "problem_solving_score": 88,
  "communication_score": 84,
  "technical_strengths": ["Clean code structure", "Proper error handling"],
  "technical_weaknesses": ["Could improve documentation"],
  "behavioral_strengths": ["Good problem-solving approach"],
  "behavioral_weaknesses": ["Limited stakeholder consideration"],
  "red_flags": [],
  "interview_questions": [
    "Can you explain your choice of pandas over other libraries?",
    "How would you scale this solution for larger datasets?"
  ],
  "hiring_manager_summary": "Candidate demonstrates strong technical skills..."
}
```

**Features:**
- Multi-dimensional scoring (technical, cultural, problem-solving, communication)
- Detailed strength and weakness analysis
- Red flag detection
- Custom interview question generation
- Hiring recommendation with rationale

## 🔄 Complete Workflow Example

### 1. Create a Job
```bash
curl -X POST "http://localhost:8000/api/v1/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "We are seeking a Senior Data Scientist to develop AI models for healthcare applications. Requirements: Python, R, SQL, TensorFlow, PyTorch.",
    "project_based": true
  }'
```

### 2. Register a Candidate
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/1/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane.doe@example.com"
  }'
```

### 3. Upload CV
```bash
curl -X POST "http://localhost:8000/api/v1/candidates/{candidate_id}/cv" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

### 4. Submit Project Work
```bash
curl -X POST "http://localhost:8000/api/v1/candidates/{candidate_id}/submissions" \
  -H "Content-Type: application/json" \
  -d '{
    "phase_number": 1,
    "primary_submission": "Python implementation...",
    "secondary_submission": "Development notes..."
  }'
```

### 5. View Rankings
```bash
curl -X GET "http://localhost:8000/api/v1/jobs/1/rankings"
```

## 🏗️ Project Structure

```
arya_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   └── v1/
│   │       ├── schemas.py      # Pydantic models
│   │       └── endpoints/
│   │           ├── jobs.py     # Job-related endpoints
│   │           ├── candidates.py # Candidate endpoints
│   │           └── submissions.py # Submission endpoints
│   ├── core/
│   │   ├── config.py          # Configuration
│   │   └── db.py              # Database setup
│   ├── models/                # SQLAlchemy models
│   │   ├── job.py
│   │   ├── candidate.py
│   │   ├── project.py
│   │   └── submission.py
│   └── services/              # Business logic
│       ├── project_service.py
│       ├── evaluation_service.py
│       ├── openai_service.py
│       └── pdf_service.py
├── arya.db                    # SQLite database
├── requirements.txt           # Dependencies
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI services | Yes | - | `sk-proj-...` |
| `DATABASE_URL` | Database connection string | No | `sqlite:///./arya.db` | See database configuration |
| `DEBUG` | Enable debug mode | No | `False` | `True`/`False` |

#### Azure PostgreSQL Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `AZURE_POSTGRESQL_HOST` | Azure PostgreSQL server host | For Azure | `myserver.postgres.database.azure.com` |
| `AZURE_POSTGRESQL_USER` | Database username (with @server) | For Azure | `admin@myserver` |
| `AZURE_POSTGRESQL_PASSWORD` | Database password | For Azure | `MySecurePassword123` |
| `AZURE_POSTGRESQL_DATABASE` | Database name | For Azure | `arya_production` |
| `AZURE_POSTGRESQL_PORT` | Database port | No | `5432` |
| `AZURE_POSTGRESQL_SSLMODE` | SSL connection mode | No | `require` |

### Database Configuration

The application uses **PostgreSQL** by default for production environments.  
SQLite is supported for local development and testing.

#### Local PostgreSQL Setup
```env
DATABASE_URL=postgresql://user:password@localhost:5432/arya_db
```

#### Azure Database for PostgreSQL

For production deployment with Azure Database for PostgreSQL:

**1. Create Azure PostgreSQL Database:**
- Go to Azure Portal
- Create "Azure Database for PostgreSQL - Flexible Server"
- Note the server name, admin username, and password

**2. Configure Connection String:**
```env
DATABASE_URL=postgresql://username%40servername:password@servername.postgres.database.azure.com:5432/database_name?sslmode=require
```

**Example Azure PostgreSQL Configuration:**
```env
# Azure PostgreSQL connection string
DATABASE_URL=postgresql://arya_admin%40arya-db-server:MySecurePassword123@arya-db-server.postgres.database.azure.com:5432/arya_production?sslmode=require

# Alternative format (URL encoded)
DATABASE_URL=postgresql://arya_admin%2540arya-db-server:MySecurePassword123@arya-db-server.postgres.database.azure.com:5432/arya_production?sslmode=require
```

**Important Notes for Azure PostgreSQL:**
- Username format: `username@servername` (URL encode @ as %40)
- SSL is required (`sslmode=require`)
- Ensure firewall rules allow your application's IP
- Consider using connection pooling for better performance

**3. Install PostgreSQL Driver:**
```bash
pip install psycopg2-binary
```

**4. Azure-Specific Environment Variables:**
```env
# Required for Azure PostgreSQL
DATABASE_URL=postgresql://admin%40myserver:password@myserver.postgres.database.azure.com:5432/arya_db?sslmode=require

# Optional: Azure-specific settings
AZURE_POSTGRESQL_HOST=myserver.postgres.database.azure.com
AZURE_POSTGRESQL_USER=admin@myserver
AZURE_POSTGRESQL_PASSWORD=your_secure_password
AZURE_POSTGRESQL_DATABASE=arya_db
AZURE_POSTGRESQL_PORT=5432
AZURE_POSTGRESQL_SSLMODE=require
```

**5. Connection String Builder for Azure:**
```python
# Alternative: Build connection string programmatically
import os

def build_azure_postgresql_url():
    host = os.getenv('AZURE_POSTGRESQL_HOST')
    user = os.getenv('AZURE_POSTGRESQL_USER')
    password = os.getenv('AZURE_POSTGRESQL_PASSWORD') 
    database = os.getenv('AZURE_POSTGRESQL_DATABASE')
    port = os.getenv('AZURE_POSTGRESQL_PORT', '5432')
    sslmode = os.getenv('AZURE_POSTGRESQL_SSLMODE', 'require')
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode={sslmode}"
```

**6. Verify Connection:**
Test your Azure PostgreSQL connection:
```python
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)
try:
    connection = engine.connect()
    result = connection.execute("SELECT version();")
    print("PostgreSQL version:", result.fetchone()[0])
    connection.close()
    print("✅ Azure PostgreSQL connection successful!")
except Exception as e:
    print("❌ Connection failed:", str(e))
```

## 🧪 Testing

### Manual Testing with Swagger UI

1. Start the server: `uvicorn app.main:app --reload`
2. Open `http://localhost:8000/docs`
3. Use the "Try it out" feature for each endpoint
4. Follow the complete workflow from job creation to candidate ranking

### Example Test Data

**Healthcare Data Scientist Job:**
```json
{
  "job_description": "We are seeking a Senior Data Scientist to develop AI models for healthcare applications. Responsibilities: Develop machine learning models for patient outcome prediction. Requirements: Python, R, SQL, TensorFlow, PyTorch. Strong communication skills."
}
```

**GIS Project Manager Job (French):**
```json
{
  "job_description": "Au sein de l'équipe SIG et DATA, vous piloterez des projets d'étude, de conseil et de développement d'outils... Requirements: FME Flow, GeoServer, PostGIS, Python, SQL."
}
```

## 🚨 Error Handling

The API provides comprehensive error handling with meaningful HTTP status codes:

- **200**: Success
- **201**: Created successfully
- **400**: Bad request (validation errors)
- **404**: Resource not found
- **422**: Unprocessable entity (schema validation)
- **500**: Internal server error

Error responses include detailed messages:
```json
{
  "detail": "Job with id 999 not found"
}
```

## � Production Deployment

### Azure Deployment Checklist

**1. Database Setup:**
- Create Azure Database for PostgreSQL - Flexible Server
- Configure firewall rules for your application
- Set up SSL connection (required)
- Create database and user with appropriate permissions

**2. Environment Configuration:**
```env
# Production environment variables
OPENAI_API_KEY=your_production_openai_key
DATABASE_URL=postgresql://user%40server:password@server.postgres.database.azure.com:5432/arya_prod?sslmode=require
DEBUG=False
```

**3. Dependencies:**
```bash
# Install PostgreSQL driver for production
pip install psycopg2-binary
```

**4. Database Migration:**
```python
# The application will automatically create tables on startup
# For existing data migration from SQLite to PostgreSQL:
# 1. Export SQLite data
# 2. Import to PostgreSQL using appropriate tools
```

**5. Azure App Service Configuration:**
- Set environment variables in Application Settings
- Enable "Always On" for consistent performance
- Configure appropriate pricing tier
- Set up application insights for monitoring

## �🔒 Security Considerations

- **CORS**: Configured for development (allow all origins)
- **File Upload**: Limited to PDF files for CV uploads
- **Input Validation**: Pydantic schema validation for all inputs
- **SQL Injection**: Protected by SQLAlchemy ORM

**Production Recommendations:**
- Implement authentication and authorization
- Configure CORS for specific domains
- Add rate limiting
- Use HTTPS
- Implement request size limits
- Add logging and monitoring

## 🎯 Performance Optimization

- **Database**: Proper indexing on frequently queried fields
- **AI Calls**: Caching for repeated evaluations
- **File Processing**: Async processing for large files
- **Response Caching**: Consider Redis for frequently accessed data

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Errors:**
- Verify API key is set correctly
- Check API quota and billing
- Monitor rate limits

**Database Issues:**
- Ensure write permissions for SQLite file
- Check database file location
- Verify SQLAlchemy connection string

**PDF Processing:**
- Ensure uploaded files are valid PDFs
- Check file size limits
- Verify PDF is not password-protected

### Logs and Debugging

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 API Improvements & Enhancement Roadmap

### 🚀 **Immediate Improvements (High Priority)**

#### **1. Authentication & Authorization**
```python
# Add JWT token-based authentication
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

# Implement role-based access control
- Admin: Can create/modify jobs, view all data
- HR Manager: Can view job results and rankings  
- Recruiter: Can manage candidates and submissions
- Candidate: Can only access their own data
```

#### **2. Input Validation & Security**
```python
# Enhanced file upload security
- File type validation (PDF only)
- File size limits (max 10MB)
- Virus scanning integration
- Content sanitization

# Request rate limiting
from slowapi import Limiter
@limiter.limit("5/minute")
async def create_job():
    pass

# Input sanitization for all text fields
- XSS protection
- SQL injection prevention
- Malicious prompt injection prevention
```

#### **3. Database Migrations**
```python
# Replace table creation on startup with Alembic
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Benefits:
- Safe schema updates in production
- Version control for database changes
- Rollback capabilities
```

#### **4. Async Operations & Performance**
```python
# Make AI calls asynchronous
import asyncio
from openai import AsyncOpenAI

async def evaluate_cv_async(cv_content: str):
    # Non-blocking AI evaluation
    
# Background task processing
from fastapi import BackgroundTasks

@router.post("/candidates/{id}/cv")
async def upload_cv(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_cv_async)
    return {"status": "processing"}
```

### 🔧 **Technical Enhancements (Medium Priority)**

#### **5. Caching Layer**
```python
# Redis integration for performance
import redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Cache AI responses to avoid duplicate API calls
@cache(expire=3600)  # 1 hour cache
async def get_job_skills(job_description: str):
    pass

# Cache database queries
- Frequently accessed job data
- Candidate rankings
- Project templates
```

#### **6. Advanced Error Handling & Logging**
```python
# Structured logging with correlation IDs
import structlog
from uuid import uuid4

@middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid4())
    # Add to all log entries and responses

# Custom exception handlers
from fastapi.exception_handlers import http_exception_handler

@app.exception_handler(OpenAIError)
async def openai_exception_handler(request, exc):
    # Handle AI service failures gracefully
    
# Health check endpoints
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": await check_db_connection(),
        "ai_service": await check_openai_connection()
    }
```

#### **7. Enhanced File Processing**
```python
# Support multiple file formats
- PDF, DOC, DOCX for CVs
- TXT, MD for submissions
- Image OCR for scanned documents

# Advanced PDF processing
from pdfplumber import PDF
import pytesseract

# Extract tables, images, and formatting
# Handle password-protected PDFs
# Support multi-language documents
```

### 📊 **Feature Enhancements (Medium Priority)**

#### **8. Advanced Analytics & Reporting**
```python
# Comprehensive analytics dashboard
- Hiring funnel metrics
- Time-to-hire tracking
- Success rate analysis
- Bias detection in evaluations

# Exportable reports
@router.get("/jobs/{job_id}/analytics")
async def get_job_analytics():
    return {
        "total_applicants": 50,
        "conversion_rates": {...},
        "average_scores": {...},
        "demographics": {...}
    }
```

#### **9. Real-time Notifications**
```python
# WebSocket integration for real-time updates
from fastapi import WebSocket

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket):
    # Real-time candidate submission updates
    # Live ranking changes
    # Status notifications

# Email/SMS notifications
from fastapi_mail import FastMail
- Candidate application confirmations
- Submission receipt acknowledgments
- Interview scheduling notifications
```

#### **10. AI Enhancement Features**
```python
# Advanced AI capabilities
- Custom evaluation criteria per job
- Bias detection and mitigation
- Multi-language support improvement
- Voice/video interview analysis

# AI model selection
@router.post("/jobs/{job_id}/ai-config")
async def configure_ai_model():
    return {
        "model": "gpt-4o",  # or claude, gemini
        "temperature": 0.7,
        "custom_prompts": {...}
    }
```

### 🌐 **Integration & API Enhancements (Low Priority)**

#### **11. Third-party Integrations**
```python
# ATS (Applicant Tracking System) integration
- Workday, BambooHR, Greenhouse
- Two-way candidate sync
- Status updates and workflow triggers

# Calendar integration for interviews
- Google Calendar, Outlook
- Automatic scheduling
- Timezone handling

# HR system integrations
- Background check services
- Reference checking automation
- Onboarding system connections
```

#### **12. Advanced Search & Filtering**
```python
# Elasticsearch integration for powerful search
from elasticsearch import AsyncElasticsearch

# Full-text search across all content
@router.get("/search")
async def search_candidates():
    # Search by skills, experience, location
    # Fuzzy matching and synonyms
    # Advanced filtering and sorting

# Recommendation engine
# Similar candidate suggestions
# Skill gap analysis
# Career progression recommendations
```

#### **13. API Versioning & Backwards Compatibility**
```python
# Proper API versioning strategy
/api/v1/jobs  # Current version
/api/v2/jobs  # Future enhanced version

# Deprecation warnings
@router.get("/api/v1/jobs", deprecated=True)
async def old_get_jobs():
    # Include deprecation headers
    
# Backwards compatibility layer
# Migration guides for API consumers
```

### 🔒 **Security & Compliance Enhancements**

#### **14. Data Privacy & GDPR Compliance**
```python
# Data anonymization
@router.delete("/candidates/{id}/gdpr-delete")
async def gdpr_delete_candidate():
    # Complete data removal
    
# Audit logging
- All data access logged
- Change tracking
- Retention policy enforcement

# Data encryption at rest
- Database field-level encryption
- File storage encryption
- Secure key management
```

#### **15. Advanced Security Features**
```python
# OAuth2 with multiple providers
- Google, Microsoft, LinkedIn SSO
- Multi-factor authentication
- Session management

# API security
- Request signing
- IP whitelisting
- Geographic restrictions
- Fraud detection
```

### 📱 **Mobile & Frontend Support**

#### **16. Mobile API Optimizations**
```python
# Mobile-optimized endpoints
@router.get("/mobile/candidates/{id}/summary")
async def get_mobile_candidate_summary():
    # Lightweight responses for mobile apps
    
# Offline support
- Data synchronization
- Conflict resolution
- Progressive web app support
```

### 🧪 **Testing & Quality Assurance**

#### **17. Comprehensive Testing Suite**
```python
# Unit tests for all services
pytest tests/unit/

# Integration tests
pytest tests/integration/

# API endpoint tests
pytest tests/api/

# Load testing
locust -f tests/load/locustfile.py

# AI evaluation quality tests
- Consistency testing
- Bias detection
- Performance benchmarking
```

### 📈 **Monitoring & Observability**

#### **18. Production Monitoring**
```python
# Application Performance Monitoring (APM)
from opentelemetry import trace
from prometheus_client import Counter

# Custom metrics
api_requests = Counter('api_requests_total')
ai_evaluation_duration = Histogram('ai_evaluation_seconds')

# Alerting
- API response time degradation
- Error rate spikes  
- AI service availability
- Database performance issues
```

### 🚀 **Deployment & DevOps**

#### **19. Container Orchestration**
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: arya-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: arya-api
        image: arya-api:latest
        
# Auto-scaling based on load
# Blue-green deployments
# Canary releases
```

#### **20. CI/CD Pipeline**
```yaml
# GitHub Actions workflow
name: ARYA API CI/CD
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run tests
      run: pytest
    - name: Security scan
      run: bandit -r app/
    - name: Deploy to staging
      if: github.ref == 'refs/heads/main'
```

### 💡 **Innovation & Future Technologies**

#### **21. Advanced AI Features**
- **Multi-modal AI**: Analyze video interviews, voice patterns
- **Predictive Analytics**: Job success probability scoring  
- **Natural Language Queries**: "Find candidates with Python and healthcare experience"
- **Automated Interview Scheduling**: AI-powered calendar optimization
- **Skill Gap Analysis**: Organizational capability assessment

#### **22. Emerging Technologies**
- **Blockchain**: Immutable candidate credentials
- **Edge Computing**: Local AI processing for sensitive data
- **Graph Databases**: Complex relationship analysis
- **Voice AI**: Automated phone screenings
- **AR/VR**: Immersive skill assessments

## 🎯 **Implementation Priority Matrix**

| Priority | Feature | Impact | Effort | Timeline |
|----------|---------|--------|--------|----------|
| **High** | Authentication & Authorization | High | Medium | 2-3 weeks |
| **High** | Input Validation & Security | High | Low | 1 week |
| **High** | Database Migrations | High | Low | 1 week |
| **Medium** | Async Operations | Medium | Medium | 2-3 weeks |
| **Medium** | Caching Layer | Medium | Medium | 2 weeks |
| **Medium** | Advanced Error Handling | Medium | Low | 1 week |
| **Low** | Third-party Integrations | Low | High | 4-6 weeks |
| **Low** | Mobile Optimizations | Low | Medium | 3-4 weeks |

## 🛡️ **Security Audit Checklist**

- [ ] **Authentication**: JWT tokens, session management
- [ ] **Authorization**: Role-based access control
- [ ] **Input Validation**: All endpoints properly validated
- [ ] **File Upload Security**: Type checking, size limits, scanning
- [ ] **SQL Injection Prevention**: Parameterized queries
- [ ] **XSS Protection**: Input sanitization
- [ ] **CORS Configuration**: Restricted origins in production
- [ ] **Rate Limiting**: API throttling implemented
- [ ] **Encryption**: Data at rest and in transit
- [ ] **Audit Logging**: All actions tracked
- [ ] **Error Handling**: No sensitive data in error messages
- [ ] **Dependencies**: Regular security updates

## 📋 **Performance Optimization Checklist**

- [ ] **Database Indexing**: Optimized queries
- [ ] **Caching Strategy**: Redis for frequent operations
- [ ] **Async Processing**: Non-blocking AI calls
- [ ] **Connection Pooling**: Database optimization
- [ ] **Content Compression**: Gzip responses
- [ ] **CDN Integration**: Static file delivery
- [ ] **Load Balancing**: Multiple API instances
- [ ] **Monitoring**: Response time tracking
- [ ] **Memory Management**: Efficient resource usage
- [ ] **Background Tasks**: Offload heavy operations

This roadmap provides a comprehensive path for evolving the ARYA API from its current functional state to a production-ready, enterprise-grade recruitment platform. Each improvement is categorized by priority and includes practical implementation examples.

## � **Enhanced Project Generation & Submission Evaluation**

### 🎯 **Current Project Generation Improvements**

#### **1. Advanced Project Template System**
```python
# Dynamic project templates based on industry and role level
PROJECT_TEMPLATES = {
    "senior_data_scientist_healthcare": {
        "complexity": "high",
        "phases": 3,
        "ai_resistance_level": "maximum",
        "industry_specific_requirements": ["HIPAA", "clinical_data", "FDA_compliance"]
    },
    "junior_frontend_developer": {
        "complexity": "medium", 
        "phases": 2,
        "focus_areas": ["responsive_design", "accessibility", "performance"]
    }
}

# Enhanced project generation with role-specific complexity
async def generate_adaptive_project(job_details: dict, experience_level: str):
    """Generate projects that scale with candidate experience level"""
    template = get_template(job_details.role, experience_level)
    return await create_project_from_template(template, job_details)
```

#### **2. Industry-Specific Project Enhancement**
```python
# Specialized project generators for different industries
class IndustryProjectGenerator:
    
    @staticmethod
    def healthcare_projects(tech_skills: list, compliance_requirements: list):
        """Generate healthcare-focused projects with real-world constraints"""
        return {
            "regulatory_compliance": compliance_requirements,
            "data_privacy": ["HIPAA", "GDPR", "clinical_trial_data"],
            "real_world_scenarios": [
                "patient_outcome_prediction",
                "drug_discovery_pipeline", 
                "medical_imaging_analysis"
            ]
        }
    
    @staticmethod
    def fintech_projects(tech_skills: list, risk_level: str):
        """Generate financial services projects with security focus"""
        return {
            "security_requirements": ["PCI_DSS", "SOX", "fraud_detection"],
            "performance_criteria": ["low_latency", "high_availability"],
            "compliance_standards": ["KYC", "AML", "stress_testing"]
        }
```

#### **3. AI-Resistance Enhancement Strategies**
```python
# Advanced anti-AI tactics for authentic candidate evaluation
class AIResistanceStrategy:
    
    @staticmethod
    def generate_unique_constraints(candidate_id: str, job_context: dict):
        """Create personalized constraints that prevent AI shortcuts"""
        return {
            "unique_identifier": f"candidate_{candidate_id[:8]}",
            "randomized_parameters": {
                "dataset_variation": generate_unique_dataset_id(),
                "business_context": create_fictional_company_scenario(),
                "technical_constraints": randomize_technical_requirements(),
                "timeline_pressure": simulate_real_world_deadlines()
            },
            "verification_mechanisms": [
                "code_explanation_required",
                "decision_rationale_documentation", 
                "alternative_approach_analysis",
                "personal_reflection_component"
            ]
        }
    
    @staticmethod
    def phase_continuity_checks(previous_phases: list):
        """Ensure each phase builds on previous work authentically"""
        return {
            "reference_requirements": "Must reference specific decisions from Phase 1",
            "iterative_improvement": "Explain why changes were made",
            "consistency_validation": "Maintain architectural decisions across phases",
            "learning_demonstration": "Show evolution of understanding"
        }
```

#### **4. Dynamic Difficulty Scaling**
```python
# Adaptive project difficulty based on candidate assessment
class ProjectDifficultyManager:
    
    @staticmethod
    def calculate_project_complexity(cv_analysis: dict, job_requirements: dict):
        """Dynamically adjust project difficulty based on candidate background"""
        experience_score = cv_analysis.get("experience_match", 50)
        skills_coverage = len(cv_analysis.get("skills_coverage", []))
        
        if experience_score > 80 and skills_coverage > 5:
            return {
                "difficulty": "senior",
                "additional_constraints": ["architectural_decisions", "scalability_planning"],
                "evaluation_criteria": ["system_design", "trade_off_analysis"]
            }
        elif experience_score > 60:
            return {
                "difficulty": "mid",
                "focus_areas": ["implementation_quality", "best_practices"],
                "evaluation_criteria": ["code_quality", "problem_solving"]
            }
        else:
            return {
                "difficulty": "junior", 
                "guided_structure": True,
                "evaluation_criteria": ["learning_ability", "foundational_skills"]
            }
```

### 📊 **Enhanced Submission Evaluation System**

#### **5. Multi-Dimensional Evaluation Framework**
```python
# Comprehensive evaluation system with weighted scoring
class AdvancedSubmissionEvaluator:
    
    EVALUATION_DIMENSIONS = {
        "technical_execution": {
            "weight": 0.35,
            "criteria": [
                "code_quality", "architecture", "best_practices", 
                "error_handling", "performance_considerations"
            ]
        },
        "problem_solving": {
            "weight": 0.25, 
            "criteria": [
                "approach_methodology", "creative_solutions",
                "constraint_handling", "edge_case_consideration"
            ]
        },
        "communication": {
            "weight": 0.20,
            "criteria": [
                "documentation_quality", "explanation_clarity",
                "stakeholder_communication", "presentation_skills"
            ]
        },
        "cultural_fit": {
            "weight": 0.20,
            "criteria": [
                "collaboration_indicators", "growth_mindset", 
                "accountability", "initiative_taking"
            ]
        }
    }
    
    async def evaluate_with_context(self, submission: dict, context: dict):
        """Evaluate submission with full candidate and job context"""
        scores = {}
        for dimension, config in self.EVALUATION_DIMENSIONS.items():
            dimension_score = await self._evaluate_dimension(
                submission, dimension, config["criteria"], context
            )
            scores[dimension] = {
                "score": dimension_score,
                "weight": config["weight"],
                "weighted_score": dimension_score * config["weight"]
            }
        
        return self._compile_final_evaluation(scores, context)
```

#### **6. Contextual Evaluation Enhancement**
```python
# Context-aware evaluation considering candidate background and job requirements
async def evaluate_with_full_context(submission_data: dict):
    """Enhanced evaluation considering candidate journey and job specifics"""
    
    context = {
        "candidate_background": await get_candidate_cv_analysis(submission_data["candidate_id"]),
        "job_requirements": await get_job_details(submission_data["job_id"]),
        "previous_submissions": await get_candidate_submission_history(submission_data["candidate_id"]),
        "industry_benchmarks": await get_industry_performance_standards(submission_data["industry"]),
        "phase_progression": calculate_learning_curve(submission_data["phase_number"])
    }
    
    # Adjust evaluation criteria based on context
    evaluation_prompt = build_contextual_prompt(submission_data, context)
    
    return {
        "base_evaluation": await evaluate_submission_content(submission_data),
        "contextual_adjustments": await apply_context_adjustments(base_evaluation, context),
        "progression_analysis": analyze_candidate_growth(context["previous_submissions"]),
        "hiring_prediction": predict_job_success_probability(evaluation_results, context)
    }
```

#### **7. Bias Detection and Mitigation**
```python
# Advanced bias detection in AI evaluations
class BiasDetectionSystem:
    
    BIAS_INDICATORS = [
        "name_based_bias", "educational_background_bias", 
        "communication_style_bias", "cultural_reference_bias"
    ]
    
    async def detect_evaluation_bias(self, evaluation_result: dict, candidate_info: dict):
        """Detect potential bias in AI evaluation results"""
        bias_analysis = {}
        
        # Check for language bias
        if "communication_score" in evaluation_result:
            bias_analysis["language_bias"] = await self._analyze_language_bias(
                evaluation_result["communication_score"], 
                candidate_info.get("native_language")
            )
        
        # Check for experience bias (over/under-valuing certain backgrounds)
        bias_analysis["experience_bias"] = await self._analyze_experience_bias(
            evaluation_result, candidate_info.get("background")
        )
        
        # Check for consistency across similar submissions
        bias_analysis["consistency_check"] = await self._check_evaluation_consistency(
            evaluation_result, candidate_info
        )
        
        return bias_analysis
    
    async def apply_bias_correction(self, evaluation: dict, bias_analysis: dict):
        """Apply corrections to mitigate detected bias"""
        corrected_evaluation = evaluation.copy()
        
        for bias_type, bias_score in bias_analysis.items():
            if bias_score > 0.7:  # High bias detected
                corrected_evaluation = await self._apply_correction(
                    corrected_evaluation, bias_type, bias_score
                )
        
        return corrected_evaluation
```

#### **8. Adaptive Questioning System**
```python
# Dynamic interview question generation based on submission analysis
class AdaptiveQuestionGenerator:
    
    async def generate_followup_questions(self, submission_evaluation: dict, candidate_context: dict):
        """Generate targeted interview questions based on submission analysis"""
        
        questions = {
            "technical_deep_dive": [],
            "problem_solving_verification": [],
            "cultural_fit_assessment": [],
            "growth_potential_exploration": []
        }
        
        # Technical questions based on implementation choices
        if submission_evaluation.get("technical_score", 0) > 80:
            questions["technical_deep_dive"].extend([
                f"Can you explain why you chose {technology} over {alternative}?",
                "How would you scale this solution for 10x the current load?",
                "What security considerations did you factor into your design?"
            ])
        
        # Problem-solving verification for high scores
        if submission_evaluation.get("problem_solving_score", 0) > 85:
            questions["problem_solving_verification"].extend([
                "Walk me through your thought process when you encountered [specific challenge]",
                "How did you validate your approach before implementation?",
                "What alternative solutions did you consider and why did you reject them?"
            ])
        
        # Red flag investigation
        for red_flag in submission_evaluation.get("red_flags", []):
            questions["clarification_needed"].append(
                f"I noticed {red_flag} in your submission. Can you explain your reasoning?"
            )
        
        return questions
```

### 🔄 **Improved Project Generation Workflow**

#### **9. Enhanced Project Creation Pipeline**
```python
# Comprehensive project generation workflow
async def create_enhanced_project_assessment(job_create: schemas.JobCreate, db: Session):
    """Enhanced project generation with multiple validation layers"""
    
    # Step 1: Enhanced job analysis
    job_analysis = await openai_service.extract_job_details_enhanced(job_create.job_description)
    
    # Step 2: Determine project complexity and scope
    project_scope = calculate_project_scope(job_analysis)
    
    # Step 3: Generate industry-specific constraints
    industry_constraints = generate_industry_constraints(job_analysis["industry"])
    
    # Step 4: Create AI-resistant elements
    ai_resistance_elements = generate_ai_resistance_strategy(
        job_analysis["tech_skills"], 
        project_scope["difficulty"]
    )
    
    # Step 5: Generate project with all enhancements
    project_data = await openai_service.generate_enhanced_project(
        job_analysis=job_analysis,
        scope=project_scope, 
        constraints=industry_constraints,
        ai_resistance=ai_resistance_elements
    )
    
    # Step 6: Validate project quality
    quality_validation = await validate_project_quality(project_data)
    
    # Step 7: Store with metadata
    return await store_project_with_metadata(db, project_data, quality_validation)
```

### 📈 **Improved Submission Evaluation Workflow**

#### **10. Enhanced Evaluation Pipeline**
```python
# Comprehensive submission evaluation workflow
async def evaluate_submission_enhanced(
    candidate_id: uuid.UUID, 
    submission_data: schemas.SubmissionCreate,
    db: Session
):
    """Enhanced submission evaluation with context and bias detection"""
    
    # Step 1: Gather comprehensive context
    evaluation_context = await build_evaluation_context(candidate_id, db)
    
    # Step 2: Pre-process submission content
    processed_submission = await preprocess_submission_content(submission_data)
    
    # Step 3: Multi-model evaluation for reliability
    evaluations = await run_multi_model_evaluation(processed_submission, evaluation_context)
    
    # Step 4: Bias detection and correction
    bias_analysis = await detect_evaluation_bias(evaluations, evaluation_context)
    corrected_evaluation = await apply_bias_corrections(evaluations, bias_analysis)
    
    # Step 5: Generate adaptive interview questions
    interview_questions = await generate_adaptive_questions(corrected_evaluation, evaluation_context)
    
    # Step 6: Calculate progression metrics
    progression_analysis = await analyze_candidate_progression(candidate_id, corrected_evaluation, db)
    
    # Step 7: Compile final evaluation with metadata
    final_evaluation = compile_comprehensive_evaluation(
        corrected_evaluation, 
        bias_analysis,
        interview_questions,
        progression_analysis
    )
    
    return final_evaluation
```

### 🎯 **Project Generation Enhancement Prompt Examples**

#### **11. Enhanced AI Prompts for Project Generation**
```python
ENHANCED_PROJECT_GENERATION_PROMPT = """
You are an expert technical recruiter and project designer. Create a sophisticated, multi-phase assessment project that meets these enhanced criteria:

**CONTEXT ANALYSIS:**
- Role: {job_title} ({experience_level})
- Industry: {industry} with specific regulations: {compliance_requirements}
- Technical Stack: {tech_skills} (Primary: {primary_skills}, Secondary: {secondary_skills})
- Team Context: {team_size} person team, {remote_policy} work environment
- Business Context: {company_stage} company in {market_segment} market

**ENHANCED PROJECT REQUIREMENTS:**

**Phase 1 - Foundation & Discovery** (Week 1):
- **Core Challenge**: Real-world scenario requiring {primary_skills[0]} and {primary_skills[1]}
- **Unique Constraint**: Incorporate dataset "ProjectID_{unique_id}" with {data_characteristics}
- **Deliverables**: 
  * Technical implementation
  * Architecture decision log with rationale
  * Assumptions and constraints documentation
- **AI Resistance**: Unique dataset + personal decision documentation prevents AI shortcuts
- **Success Metrics**: {phase1_metrics}

**Phase 2 - Enhancement & Integration** (Week 2):
- **Evolution Task**: Enhance Phase 1 with {additional_requirement} constraint
- **Real-world Pressure**: {business_constraint} (e.g., "regulatory audit incoming")
- **Deliverables**:
  * Updated implementation with migration strategy
  * Performance impact analysis (max 300 words)
  * Stakeholder communication plan
- **AI Resistance**: Requires building on previous work + performance trade-off analysis
- **Success Metrics**: {phase2_metrics}

**Phase 3 - Leadership & Communication** (Week 3):
- **Strategic Task**: {leadership_scenario} requiring {soft_skills} skills
- **Deliverables**:
  * Executive summary report (2 pages max)
  * 5-minute video presentation explaining trade-offs and future roadmap
  * Risk assessment matrix
- **AI Resistance**: Video presentation + personal strategic thinking cannot be AI-generated
- **Success Metrics**: {phase3_metrics}

**EVALUATION FRAMEWORK:**
For each phase, candidates will be evaluated on:
- Technical execution quality (40%)
- Problem-solving approach (30%) 
- Communication clarity (20%)
- Cultural fit indicators (10%)

**INDUSTRY-SPECIFIC REQUIREMENTS:**
{industry_specific_constraints}

**ANTI-AI VERIFICATION METHODS:**
1. Unique identifiers requiring personalization
2. Building on previous work (continuity check)
3. Personal reflection and decision rationale
4. Video/audio components requiring human presence
5. Real-time constraints preventing preparation time
"""
```

This enhanced system provides:
- **Dynamic project complexity** based on candidate experience
- **Industry-specific constraints** for realistic challenges  
- **Advanced AI-resistance** through multiple verification layers
- **Bias detection and mitigation** for fair evaluation
- **Contextual evaluation** considering candidate journey
- **Adaptive questioning** for targeted interviews
- **Multi-dimensional scoring** with weighted criteria
- **Progressive difficulty** that scales with candidate ability

The improvements ensure more accurate, fair, and comprehensive candidate assessment while maintaining the authenticity that prevents AI shortcuts.

## �📈 Future Enhancements

- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Integration with HR systems
- [ ] Multi-tenant support
- [ ] Advanced file format support
- [ ] Candidate feedback system
- [ ] Interview scheduling integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions and support:
- Check the API documentation at `/docs`
- Review this README
- Check the troubleshooting section
- Open an issue on the repository

---

**Built with ❤️ using FastAPI and OpenAI**
