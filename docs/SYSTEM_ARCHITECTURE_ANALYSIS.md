# 🏗️ ARYA - Multiagent Recruitment System: Complete Architecture Analysis

**Document Version:** 1.0  
**Last Updated:** February 3, 2026  
**System Name:** ARYA (AI Recruitment & Yield Assessment)  
**Author:** AI & Data Engineering Team

---

## 📋 Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Overview](#2-system-overview)
3. [Multiagent Architecture](#3-multiagent-architecture)
4. [Data Flow & Pipelines](#4-data-flow--pipelines)
5. [Database Design](#5-database-design)
6. [AI/ML Components](#6-aiml-components)
7. [API Architecture](#7-api-architecture)
8. [Azure Cloud Infrastructure](#8-azure-cloud-infrastructure)
9. [Deployment Pipeline](#9-deployment-pipeline)
10. [Security Considerations](#10-security-considerations)
11. [Scalability & Performance](#11-scalability--performance)
12. [Complete System Diagram](#12-complete-system-diagram)

---

## 1. Executive Summary

ARYA is a sophisticated **AI-powered recruitment assessment platform** built using a **multiagent architecture pattern**. The system automates the hiring process through:

- **Intelligent Job Analysis**: AI-powered extraction of job requirements
- **Project-Based Assessment Generation**: AI-resistant, multi-phase candidate evaluations
- **Automated CV Evaluation**: Smart resume parsing and scoring
- **Candidate Ranking**: Weighted scoring algorithms for objective comparison
- **PDF Report Generation**: Professional documentation for hiring decisions

### Key Metrics
| Metric | Value |
|--------|-------|
| **Total Agents** | 7 specialized agents |
| **API Endpoints** | 10 RESTful endpoints |
| **Database Tables** | 4 core entities |
| **Assessment Phases** | 3-phase project workflow |
| **Scoring Components** | 5 evaluation dimensions |

---

## 2. System Overview

### 2.1 Technology Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           TECHNOLOGY STACK                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  FRONTEND LAYER          │  Any HTTP Client (Web/Mobile/API Tools)          │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  API FRAMEWORK           │  FastAPI (Python 3.11+)                          │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  ORM                     │  SQLAlchemy 2.x                                  │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  DATABASE                │  PostgreSQL (Production) / SQLite (Dev)         │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  AI/ML ENGINE            │  Azure OpenAI (GPT-4o)                           │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  DOCUMENT PROCESSING     │  PyPDF2, FPDF                                    │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  VALIDATION              │  Pydantic v2                                     │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  CLOUD PLATFORM          │  Microsoft Azure                                 │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  CONTAINERIZATION        │  Docker                                          │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  CONTAINER REGISTRY      │  Azure Container Registry (ACR)                  │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  HOSTING                 │  Azure App Service (Linux B1)                    │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 2.2 Project Structure

```
arya_api/
├── 📄 main.py                    # FastAPI application entry point
├── 📂 api/                       # API Layer (Endpoint Agents)
│   └── 📂 v1/
│       ├── 📄 schemas.py         # Pydantic data models
│       └── 📂 endpoints/
│           ├── 📄 jobs.py        # Jobs Agent
│           ├── 📄 candidates.py  # Candidates Agent
│           └── 📄 submissions.py # Submissions Agent
├── 📂 core/                      # Core Infrastructure
│   ├── 📄 config.py              # Configuration Agent
│   └── 📄 db.py                  # Database Agent
├── 📂 models/                    # Data Models (ORM)
│   ├── 📄 job.py                 # Job Entity
│   ├── 📄 candidate.py           # Candidate Entity
│   ├── 📄 project.py             # Project Entity
│   └── 📄 submission.py          # Submission Entity
└── 📂 services/                  # Service Agents (Business Logic)
    ├── 📄 openai_service.py      # OpenAI Agent (AI Brain)
    ├── 📄 project_service.py     # Project Service Agent
    ├── 📄 evaluation_service.py  # Evaluation Service Agent
    └── 📄 pdf_service.py         # PDF Service Agent
```

---

## 3. Multiagent Architecture

### 3.1 Agent Hierarchy Diagram

```
                    ┌─────────────────────────────────────┐
                    │          CLIENT LAYER               │
                    │  (Web App / Mobile / API Tools)     │
                    └─────────────────┬───────────────────┘
                                      │
                          HTTP Requests/Responses
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          API GATEWAY LAYER                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     FastAPI Application                              │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │   │
│  │  │CORS Handler │  │Rate Limiter │  │  Validator  │  │ Serializer │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ENDPOINT AGENTS LAYER                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐      │
│  │   Jobs Agent    │  │ Candidates Agent │  │   Submissions Agent    │      │
│  │   (jobs.py)     │  │ (candidates.py)  │  │   (submissions.py)     │      │
│  │                 │  │                  │  │                        │      │
│  │ • Create Job    │  │ • Register       │  │ • Submit Phase Work    │      │
│  │ • Get Job       │  │ • Upload CV      │  │ • Get Submissions      │      │
│  │ • Reference PDF │  │ • Get Report PDF │  │ • Get Phase Details    │      │
│  │ • Get Rankings  │  │                  │  │                        │      │
│  └────────┬────────┘  └────────┬─────────┘  └───────────┬────────────┘      │
└───────────┼─────────────────────┼──────────────────────┼────────────────────┘
            │                     │                      │
            └─────────────────────┼──────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SERVICE AGENTS LAYER                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐      │
│  │ Project Service │  │Evaluation Service│  │    PDF Service         │      │
│  │     Agent       │  │     Agent        │  │      Agent             │      │
│  │                 │  │                  │  │                        │      │
│  │ • Create Job    │  │ • Evaluate CV    │  │ • Candidate Report     │      │
│  │ • Generate      │  │ • Evaluate       │  │ • Reference Guide      │      │
│  │   Assessment    │  │   Submission     │  │ • Text Cleaning        │      │
│  │ • Get Job Data  │  │ • Rank Candidates│  │                        │      │
│  │                 │  │ • Update Status  │  │                        │      │
│  └────────┬────────┘  └────────┬─────────┘  └───────────────────────┘      │
└───────────┼─────────────────────┼───────────────────────────────────────────┘
            │                     │
            └─────────┬───────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL AGENTS LAYER                                 │
│  ┌─────────────────────────┐  ┌──────────────────────────────────────┐      │
│  │     OpenAI Agent        │  │         Database Agent               │      │
│  │   (openai_service.py)   │  │           (db.py)                    │      │
│  │                         │  │                                      │      │
│  │ • Extract Job Details   │  │ • SQLAlchemy Engine                  │      │
│  │ • Generate Project      │  │ • Session Management                 │      │
│  │ • Evaluate CV           │  │ • Connection Pooling                 │      │
│  │ • Evaluate Submission   │  │ • Transaction Handling               │      │
│  │                         │  │                                      │      │
│  │ [Azure OpenAI GPT-4o]   │  │ [PostgreSQL / SQLite]               │      │
│  └─────────────────────────┘  └──────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Agent Specifications

#### 🔵 Agent 1: Jobs Agent (`jobs.py`)

| Property | Description |
|----------|-------------|
| **Role** | HTTP request handling for job-related operations |
| **Input** | HTTP requests with job data |
| **Output** | JSON responses, PDF files |
| **Dependencies** | ProjectService, EvaluationService, PDFService |

**Endpoints:**
```
POST   /api/v1/jobs                    → Create job + assessment
GET    /api/v1/jobs/{job_id}           → Get job details
GET    /api/v1/jobs/{job_id}/reference-guide → Download PDF guide
GET    /api/v1/jobs/{job_id}/rankings  → Get candidate rankings
```

#### 🟢 Agent 2: Candidates Agent (`candidates.py`)

| Property | Description |
|----------|-------------|
| **Role** | Candidate registration and CV processing |
| **Input** | HTTP requests, PDF files (multipart) |
| **Output** | JSON responses, PDF reports |
| **Dependencies** | EvaluationService, PDFService |

**Endpoints:**
```
POST   /api/v1/jobs/{job_id}/candidates     → Register candidate
POST   /api/v1/candidates/{id}/cv           → Upload & evaluate CV
GET    /api/v1/candidates/{id}/report       → Download PDF report
```

#### 🟡 Agent 3: Submissions Agent (`submissions.py`)

| Property | Description |
|----------|-------------|
| **Role** | Project phase submission handling |
| **Input** | JSON submission payloads |
| **Output** | Evaluation results |
| **Dependencies** | EvaluationService |

**Endpoints:**
```
POST   /api/v1/candidates/{id}/submissions              → Submit phase work
GET    /api/v1/candidates/{id}/submissions              → Get all submissions
GET    /api/v1/candidates/{id}/submissions/{phase}      → Get phase details
```

#### 🟣 Agent 4: OpenAI Agent (`openai_service.py`)

| Property | Description |
|----------|-------------|
| **Role** | AI-powered analysis and generation |
| **Input** | Text data (job descriptions, CVs, submissions) |
| **Output** | Structured JSON evaluations |
| **External API** | Azure OpenAI (GPT-4o) |

**Core Functions:**
```python
extract_job_details(job_description)      → Dict[title, tech_skills, soft_skills, industry]
generate_project_dict(job_info)           → Dict[title, objective, phases[3]]
evaluate_cv(cv_text, job_requirements)    → Dict[scores, assessment, recommendations]
evaluate_submission(submission, phase)     → Dict[scores, feedback, recommendation]
```

#### 🟠 Agent 5: Project Service Agent (`project_service.py`)

| Property | Description |
|----------|-------------|
| **Role** | Job and project orchestration |
| **Input** | JobCreate schema |
| **Output** | Job + Project database records |
| **Dependencies** | OpenAI Agent, Database Agent |

**Workflow:**
```
1. Receive job description
2. Call OpenAI → extract job details
3. Call OpenAI → generate 3-phase project
4. Create Job record in database
5. Create Project record (linked to Job)
6. Return complete Job entity
```

#### 🔴 Agent 6: Evaluation Service Agent (`evaluation_service.py`)

| Property | Description |
|----------|-------------|
| **Role** | Candidate assessment and ranking |
| **Input** | CV content, submissions |
| **Output** | Evaluations, rankings |
| **Dependencies** | OpenAI Agent, Database Agent |

**Core Functions:**
```python
evaluate_candidate_cv(candidate_id, cv_content)     → CV evaluation dict
evaluate_and_store_submission(candidate_id, data)   → Submission evaluation dict
rank_candidates_for_job(job_id)                     → List[CandidateRanking]
```

**Ranking Algorithm:**
```
Final Score = (CV Score × 0.30) + (Avg Submission Score × 0.70)

Performance Levels:
├── 90-100: Outstanding - Strong recommend for immediate hire
├── 80-89:  Excellent - Recommend for hire
├── 70-79:  Good - Consider for hire with potential
├── 60-69:  Fair - Proceed with caution
└── <60:    Below expectations - Not recommended
```

#### ⚫ Agent 7: PDF Service Agent (`pdf_service.py`)

| Property | Description |
|----------|-------------|
| **Role** | Document generation |
| **Input** | Candidate/Job data |
| **Output** | PDF files |
| **Library** | FPDF |

**Generated Documents:**
- **Candidate Report PDF**: Complete evaluation summary
- **Reference Guide PDF**: Project assessment details for evaluators

---

## 4. Data Flow & Pipelines

### 4.1 Job Creation Pipeline

```
┌──────────────┐     ┌───────────────┐     ┌──────────────────┐     ┌────────────────┐
│   Client     │────▶│  Jobs Agent   │────▶│ Project Service  │────▶│ OpenAI Agent   │
│ (Job Desc)   │     │  (Validate)   │     │  (Orchestrate)   │     │ (AI Analysis)  │
└──────────────┘     └───────────────┘     └──────────────────┘     └────────────────┘
                                                    │                        │
                                                    │   ┌────────────────────┘
                                                    │   │
                                                    ▼   ▼
                                           ┌──────────────────┐
                                           │  Database Agent  │
                                           │  (Store Job +    │
                                           │   Project)       │
                                           └──────────────────┘
                                                    │
                                                    ▼
                                           ┌──────────────────┐
                                           │   JSON Response  │
                                           │  (Job + Project) │
                                           └──────────────────┘
```

**Step-by-Step:**
1. Client sends `POST /api/v1/jobs` with job description
2. Jobs Agent validates input using Pydantic schema
3. Project Service orchestrates the creation workflow
4. OpenAI Agent extracts: title, tech_skills, soft_skills, industry
5. OpenAI Agent generates 3-phase AI-resistant project
6. Database Agent stores Job and Project records
7. Response returned with complete job details

### 4.2 CV Evaluation Pipeline

```
┌──────────────┐     ┌─────────────────┐     ┌───────────────┐
│   Client     │────▶│Candidates Agent │────▶│  PyPDF2       │
│ (PDF Upload) │     │ (File Handler)  │     │ (Text Extract)│
└──────────────┘     └─────────────────┘     └───────────────┘
                                                     │
                                                     ▼
┌──────────────┐     ┌─────────────────┐     ┌───────────────┐
│   Response   │◀────│  Database       │◀────│ OpenAI Agent  │
│ (Evaluation) │     │  (Store Eval)   │     │ (CV Analysis) │
└──────────────┘     └─────────────────┘     └───────────────┘
```

**CV Evaluation Output Structure:**
```json
{
  "match_score": 85,
  "experience_match": 78,
  "skills_coverage": ["Python", "SQL", "Machine Learning"],
  "skills_gaps": ["Kubernetes", "Terraform"],
  "strengths": ["Strong ML background", "Team leadership"],
  "development_areas": ["DevOps skills", "Cloud certification"],
  "overall_assessment": "Strong candidate with relevant experience...",
  "interview_recommendations": ["Probe cloud experience", "Discuss ML projects"]
}
```

### 4.3 Submission Evaluation Pipeline

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────────┐
│   Client     │────▶│Submissions Agent │────▶│Evaluation Service │
│ (Phase Work) │     │   (Validate)     │     │  (Orchestrate)    │
└──────────────┘     └──────────────────┘     └───────────────────┘
                                                       │
                              ┌─────────────────────────┘
                              │
                              ▼
┌──────────────┐     ┌───────────────┐     ┌───────────────┐
│   Response   │◀────│   Database    │◀────│ OpenAI Agent  │
│ (Evaluation) │     │(Store Result) │     │  (Analysis)   │
└──────────────┘     └───────────────┘     └───────────────┘
```

**Submission Evaluation Output:**
```json
{
  "hiring_recommendation": "Recommend",
  "overall_score": 82,
  "technical_score": 85,
  "problem_solving_score": 80,
  "communication_score": 78,
  "cultural_fit_score": 84,
  "technical_strengths": ["Clean code", "Good architecture"],
  "technical_weaknesses": ["Limited testing"],
  "behavioral_strengths": ["Clear communication"],
  "behavioral_weaknesses": ["Could be more concise"],
  "red_flags": [],
  "interview_questions": ["Discuss testing approach"],
  "hiring_manager_summary": "Strong technical candidate..."
}
```

### 4.4 Candidate Ranking Pipeline

```
┌──────────────┐     ┌─────────────┐     ┌───────────────────┐
│   Client     │────▶│ Jobs Agent  │────▶│Evaluation Service │
│  (Request)   │     │ (Route)     │     │(Calculate Ranks)  │
└──────────────┘     └─────────────┘     └───────────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │    Database     │
                                         │(Fetch Candidates│
                                         │ + Submissions)  │
                                         └─────────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │   Algorithm     │
                                         │ CV(30%) +       │
                                         │ Projects(70%)   │
                                         └─────────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │ Ranked List     │
                                         │ (JSON Response) │
                                         └─────────────────┘
```

---

## 5. Database Design

### 5.1 Entity-Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DATABASE SCHEMA (PostgreSQL)                          │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐          ┌─────────────────┐
    │      JOBS       │          │    PROJECTS     │
    ├─────────────────┤          ├─────────────────┤
    │ id (PK)         │──────────│ id (PK)         │
    │ title           │    1:1   │ job_id (FK, UQ) │
    │ industry        │◀─────────│ title           │
    │ tech_skills[]   │          │ objective       │
    │ soft_skills[]   │          │ phases[] (JSON) │
    │ job_description │          └─────────────────┘
    │ created_at      │
    └────────┬────────┘
             │
             │ 1:N
             ▼
    ┌─────────────────┐          ┌─────────────────┐
    │   CANDIDATES    │          │   SUBMISSIONS   │
    ├─────────────────┤          ├─────────────────┤
    │ id (PK, UUID)   │──────────│ id (PK)         │
    │ job_id (FK)     │    1:N   │ candidate_id(FK)│
    │ name            │◀─────────│ phase_number    │
    │ email (UQ)      │          │ primary_sub     │
    │ status          │          │ secondary_sub   │
    │ cv_evaluation[] │          │ submitted_at    │
    │ created_at      │          │ evaluation[]    │
    └─────────────────┘          └─────────────────┘
```

### 5.2 Table Specifications

#### Jobs Table
```sql
CREATE TABLE jobs (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    industry        VARCHAR(255),
    tech_skills     JSON,           -- ["Python", "SQL", "AWS"]
    soft_skills     JSON,           -- ["Communication", "Leadership"]
    job_description TEXT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_jobs_title ON jobs(title);
```

#### Projects Table
```sql
CREATE TABLE projects (
    id        SERIAL PRIMARY KEY,
    job_id    INTEGER UNIQUE NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    title     VARCHAR(255) NOT NULL,
    objective TEXT,
    phases    JSON            -- [{phase: 1, task: "...", submit: "...", ai_resistant_tactic: "..."}]
);

-- Indexes
CREATE INDEX idx_projects_job_id ON projects(job_id);
```

#### Candidates Table
```sql
CREATE TABLE candidates (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id        INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    name          VARCHAR(255) NOT NULL,
    email         VARCHAR(255) UNIQUE NOT NULL,
    status        VARCHAR(50) DEFAULT 'Applied',
    cv_evaluation JSON,         -- AI evaluation result
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_candidates_email ON candidates(email);
CREATE INDEX idx_candidates_job_id ON candidates(job_id);
```

#### Submissions Table
```sql
CREATE TABLE submissions (
    id                   SERIAL PRIMARY KEY,
    candidate_id         UUID NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    phase_number         INTEGER NOT NULL CHECK (phase_number BETWEEN 1 AND 3),
    primary_submission   TEXT NOT NULL,
    secondary_submission TEXT,
    submitted_at         TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    evaluation           JSON,   -- AI evaluation result
    
    UNIQUE(candidate_id, phase_number)
);

-- Indexes
CREATE INDEX idx_submissions_candidate ON submissions(candidate_id);
```

### 5.3 JSON Data Structures

#### Project Phases JSON
```json
{
  "phases": [
    {
      "phase": 1,
      "task": "Design and implement a data pipeline incorporating unique identifier ABC123...",
      "submit": "Technical implementation + changelog of key decisions",
      "ai_resistant_tactic": "Requires personalized implementation with verifiable unique elements"
    },
    {
      "phase": 2,
      "task": "Iterate on Phase 1 + add compliance for GDPR regulations",
      "submit": "Updated work + 300-word limitation analysis",
      "ai_resistant_tactic": "Builds on previous work requiring continuity verification"
    },
    {
      "phase": 3,
      "task": "Write a postmortem document for stakeholders",
      "submit": "Final report + audio note explaining trade-offs",
      "ai_resistant_tactic": "Requires personal reflection and verbal presentation"
    }
  ]
}
```

#### CV Evaluation JSON
```json
{
  "match_score": 85,
  "experience_match": 78,
  "skills_coverage": ["Python", "SQL", "Machine Learning", "Data Engineering"],
  "skills_gaps": ["Kubernetes", "Terraform", "Spark"],
  "strengths": [
    "Strong ML background with production experience",
    "Team leadership experience",
    "Clear communication skills"
  ],
  "development_areas": [
    "DevOps and infrastructure skills",
    "Cloud certification recommended",
    "More experience with distributed systems"
  ],
  "overall_assessment": "Strong candidate with 5+ years relevant experience...",
  "interview_recommendations": [
    "Probe cloud infrastructure experience",
    "Discuss previous ML projects in detail",
    "Evaluate system design capabilities"
  ]
}
```

---

## 6. AI/ML Components

### 6.1 Azure OpenAI Integration

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AZURE OPENAI CONFIGURATION                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  Model:              GPT-4o (gpt-4o)                                        │
│  API Version:        2024-12-01-preview                                     │
│  Endpoint:           https://<resource>.cognitiveservices.azure.com/        │
│  Authentication:     API Key                                                │
│  Region:             France Central                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 AI Agent Functions

| Function | Purpose | Temperature | Max Tokens |
|----------|---------|-------------|------------|
| `extract_job_details()` | Parse job description | 0.3 | 400 |
| `generate_project_dict()` | Create assessment project | 0.7 | 800 |
| `evaluate_cv()` | Analyze resume fit | 0.3 | 1500 |
| `evaluate_submission()` | Score phase work | 0.3 | 1500 |

### 6.3 Prompt Engineering

#### Job Details Extraction Prompt
```
Extract the following details from the job description:
1. Job Title: Extract the exact job title
2. Technical Skills: Programming languages, cloud platforms, tools, frameworks
3. Soft Skills: Required soft skills or infer typical ones
4. Industry: Most specific industry that fits

Job Description: {job_description}

Format:
**Job Title**: [job title]
**Technical Skills**: [comma-separated list]
**Soft Skills**: [comma-separated list]
**Industry**: [industry]
```

#### Project Generation Prompt
```
GOAL: Design a 3-phase async project for a role in the {industry} industry 
that evaluates {tech_skills} and {soft_skills}.

The project must be resistant to AI/LLM shortcuts while allowing async submissions.

STRUCTURE:
- Phase 1: Task + Submit + AI-Resistant Tactic
- Phase 2: Iterate + New constraint + AI-Resistant Tactic
- Phase 3: Reflective/creative task + Audio + AI-Resistant Tactic
```

### 6.4 AI-Resistant Assessment Design

The system generates projects specifically designed to prevent AI-generated submissions:

| Phase | Anti-AI Strategy |
|-------|------------------|
| **Phase 1** | Unique identifiers, real-world constraints, changelog requirements |
| **Phase 2** | Building on Phase 1 (continuity verification), self-critique |
| **Phase 3** | Audio presentation, personal reflection, stakeholder communication |

---

## 7. API Architecture

### 7.1 Complete API Specification

```yaml
openapi: 3.0.0
info:
  title: ARYA API
  version: 1.0.0
  description: AI-Powered Recruitment Assessment Platform

servers:
  - url: https://arya-recruitment-api-v2.azurewebsites.net
    description: Production (Azure)
  - url: http://localhost:8000
    description: Development

paths:
  # Jobs Endpoints
  /api/v1/jobs:
    post:
      summary: Create job with AI-generated assessment
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                job_description: {type: string}
                project_based: {type: boolean, default: true}
      responses:
        201: {description: Job created successfully}
        400: {description: Invalid job description}
        500: {description: AI service error}

  /api/v1/jobs/{job_id}:
    get:
      summary: Get job details with project
      responses:
        200: {description: Job details}
        404: {description: Job not found}

  /api/v1/jobs/{job_id}/reference-guide:
    get:
      summary: Download PDF reference guide
      responses:
        200: {description: PDF file}
        404: {description: No project found}

  /api/v1/jobs/{job_id}/rankings:
    get:
      summary: Get ranked candidate list
      responses:
        200: {description: Ranking list}
        404: {description: Job not found}

  # Candidate Endpoints
  /api/v1/jobs/{job_id}/candidates:
    post:
      summary: Register candidate for job
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                name: {type: string}
                email: {type: string, format: email}
      responses:
        201: {description: Candidate registered}
        400: {description: Duplicate email}
        404: {description: Job not found}

  /api/v1/candidates/{candidate_id}/cv:
    post:
      summary: Upload and evaluate CV
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                cv_file: {type: string, format: binary}
      responses:
        200: {description: CV evaluation results}
        400: {description: Invalid PDF}
        404: {description: Candidate not found}

  /api/v1/candidates/{candidate_id}/report:
    get:
      summary: Download candidate evaluation report
      responses:
        200: {description: PDF report}
        404: {description: Candidate not found}

  # Submission Endpoints
  /api/v1/candidates/{candidate_id}/submissions:
    post:
      summary: Submit phase work
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                phase_number: {type: integer, minimum: 1, maximum: 3}
                primary_submission: {type: string}
                secondary_submission: {type: string}
      responses:
        201: {description: Submission evaluated}
        404: {description: Candidate/Phase not found}
        409: {description: Phase already submitted}
    get:
      summary: Get all submissions
      responses:
        200: {description: List of submissions}

  /api/v1/candidates/{candidate_id}/submissions/{phase_number}:
    get:
      summary: Get specific phase submission
      responses:
        200: {description: Submission details}
        404: {description: Submission not found}
```

### 7.2 Response Schemas

#### JobResponse
```json
{
  "id": 1,
  "title": "Senior Data Engineer",
  "industry": "Technology",
  "tech_skills": ["Python", "SQL", "Spark", "AWS"],
  "soft_skills": ["Communication", "Problem-solving"],
  "job_description": "...",
  "created_at": "2026-02-03T10:00:00Z",
  "project": {
    "id": 1,
    "title": "Data Pipeline Challenge",
    "objective": "Build a scalable data pipeline...",
    "phases": [...]
  }
}
```

#### RankingResponse
```json
{
  "job_title": "Senior Data Engineer",
  "rankings": [
    {
      "rank": 1,
      "candidate_name": "John Doe",
      "final_score": 87.5,
      "performance_level": "Excellent candidate - Recommend for hire",
      "cv_score": 85,
      "average_project_score": 88.3
    },
    {
      "rank": 2,
      "candidate_name": "Jane Smith",
      "final_score": 82.1,
      "performance_level": "Excellent candidate - Recommend for hire",
      "cv_score": 78,
      "average_project_score": 83.9
    }
  ]
}
```

---

## 8. Azure Cloud Infrastructure

### 8.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AZURE CLOUD INFRASTRUCTURE                         │
│                            (France Central Region)                           │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │    Internet      │
                              │    (HTTPS)       │
                              └────────┬─────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Resource Group: Arya-v2-recruitment-API                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│    ┌─────────────────────────────────────────────────────────────────┐      │
│    │              Azure App Service (Linux)                          │      │
│    │              Plan: recruitment-plan (B1 Basic)                  │      │
│    │              Web App: arya-recruitment-api-v2                   │      │
│    │                                                                  │      │
│    │    ┌─────────────────────────────────────────────────────────┐  │      │
│    │    │                Docker Container                         │  │      │
│    │    │    ┌───────────────────────────────────────────────┐   │  │      │
│    │    │    │           FastAPI Application                  │   │  │      │
│    │    │    │              (Port 8000)                       │   │  │      │
│    │    │    │                                                │   │  │      │
│    │    │    │  ┌──────────┐ ┌──────────┐ ┌──────────────┐   │   │  │      │
│    │    │    │  │   Jobs   │ │Candidates│ │ Submissions  │   │   │  │      │
│    │    │    │  │  Agent   │ │  Agent   │ │    Agent     │   │   │  │      │
│    │    │    │  └────┬─────┘ └────┬─────┘ └──────┬───────┘   │   │  │      │
│    │    │    │       └───────────┼───────────────┘           │   │  │      │
│    │    │    │                   ▼                           │   │  │      │
│    │    │    │  ┌────────────────────────────────────────┐   │   │  │      │
│    │    │    │  │         Service Layer                  │   │   │  │      │
│    │    │    │  │  (OpenAI, Evaluation, PDF, Project)    │   │   │  │      │
│    │    │    │  └────────────────────────────────────────┘   │   │  │      │
│    │    │    └───────────────────────────────────────────────┘   │  │      │
│    │    └─────────────────────────────────────────────────────────┘  │      │
│    │                                                                  │      │
│    │    Image: aryaregistryv2.azurecr.io/recruitment-api:latest      │      │
│    └─────────────────────────────────────────────────────────────────┘      │
│                                      │                                       │
│                                      │                                       │
│    ┌─────────────────────────────────┼─────────────────────────────────┐    │
│    │        Azure Container Registry │ (aryaregistryv2)                │    │
│    │                                 │                                  │    │
│    │    ┌────────────────────────────▼─────────────────────────────┐   │    │
│    │    │              recruitment-api:latest                       │   │    │
│    │    │              (Docker Image)                               │   │    │
│    │    └───────────────────────────────────────────────────────────┘   │    │
│    └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
          │                                              │
          │                                              │
          ▼                                              ▼
┌──────────────────────────┐              ┌──────────────────────────────────┐
│   External: PostgreSQL   │              │    External: Azure OpenAI        │
│   Database Server        │              │    (Cognitive Services)          │
│                          │              │                                  │
│   Connection: SSL/TLS    │              │   Model: GPT-4o                  │
│   Port: 5432             │              │   API Version: 2024-12-01        │
└──────────────────────────┘              └──────────────────────────────────┘
```

### 8.2 Azure Resources Summary

| Resource | Name | SKU/Tier | Purpose |
|----------|------|----------|---------|
| **Resource Group** | Arya-v2-recruitment-API | - | Container for all resources |
| **Container Registry** | aryaregistryv2 | Basic | Store Docker images |
| **App Service Plan** | recruitment-plan | B1 (Linux) | Compute resources |
| **Web App** | arya-recruitment-api-v2 | - | Host the API |
| **Azure OpenAI** | (External) | GPT-4o | AI processing |
| **PostgreSQL** | (External) | - | Data storage |

### 8.3 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db?sslmode=require` |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI authentication | `your-api-key` |
| `AZURE_OPENAI_API_BASE` | Azure OpenAI endpoint | `https://resource.cognitiveservices.azure.com/` |
| `AZURE_OPENAI_API_VERSION` | API version | `2024-12-01-preview` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Model deployment | `gpt-4o` |
| `WEBSITES_PORT` | Container port (auto-set) | `8000` |

### 8.4 URLs

| Environment | URL |
|-------------|-----|
| **Production API** | https://arya-recruitment-api-v2.azurewebsites.net |
| **Swagger Docs** | https://arya-recruitment-api-v2.azurewebsites.net/docs |
| **ReDoc** | https://arya-recruitment-api-v2.azurewebsites.net/redoc |

---

## 9. Deployment Pipeline

### 9.1 Docker Configuration

```dockerfile
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies (PostgreSQL client)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Production settings
ENV PYTHONUNBUFFERED=1

# Start with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 9.2 Deployment Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DEPLOYMENT PIPELINE                                │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
     │   Developer  │────▶│    GitHub    │────▶│   Build      │
     │  (Code Push) │     │  Repository  │     │  (ACR Task)  │
     └──────────────┘     └──────────────┘     └──────────────┘
                                                      │
                                                      ▼
     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
     │   Live API   │◀────│  App Service │◀────│     ACR      │
     │  (Azure)     │     │  (Pull Image)│     │(Store Image) │
     └──────────────┘     └──────────────┘     └──────────────┘
```

### 9.3 Deployment Commands

```bash
# 1. Login to Azure
az login

# 2. Build and push Docker image to ACR
az acr build --registry aryaregistryv2 --image recruitment-api:latest .

# 3. Update environment variables
az webapp config appsettings set \
  --name arya-recruitment-api-v2 \
  --resource-group Arya-v2-recruitment-API \
  --settings "DATABASE_URL=<url>" \
             "AZURE_OPENAI_API_KEY=<key>" \
             "AZURE_OPENAI_API_BASE=<endpoint>" \
             "AZURE_OPENAI_API_VERSION=2024-12-01-preview" \
             "AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o"

# 4. Restart the application
az webapp restart \
  --name arya-recruitment-api-v2 \
  --resource-group Arya-v2-recruitment-API

# 5. View logs
az webapp log tail \
  --name arya-recruitment-api-v2 \
  --resource-group Arya-v2-recruitment-API
```

---

## 10. Security Considerations

### 10.1 Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SECURITY LAYERS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ TRANSPORT LAYER                                                        │  │
│  │ • HTTPS/TLS encryption for all API traffic                            │  │
│  │ • SSL/TLS for database connections                                     │  │
│  │ • SSL/TLS for Azure OpenAI connections                                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ APPLICATION LAYER                                                      │  │
│  │ • CORS middleware (configurable origins)                              │  │
│  │ • Pydantic input validation                                           │  │
│  │ • SQL injection prevention (SQLAlchemy ORM)                           │  │
│  │ • File type validation (PDF only for CV uploads)                      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ INFRASTRUCTURE LAYER                                                   │  │
│  │ • Environment variables for secrets (not in code)                     │  │
│  │ • Azure Key Vault integration (recommended)                           │  │
│  │ • Container isolation (Docker)                                        │  │
│  │ • Managed identity for Azure resources (recommended)                  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ DATA LAYER                                                             │  │
│  │ • Database connection with SSL mode required                          │  │
│  │ • Unique email constraint (prevent duplicates)                        │  │
│  │ • UUID for candidate IDs (non-sequential)                             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 10.2 Security Recommendations

| Category | Current Status | Recommendation |
|----------|----------------|----------------|
| **Authentication** | ⚠️ None | Implement OAuth 2.0/JWT |
| **Rate Limiting** | ⚠️ Basic | Add Azure API Management |
| **Secrets** | ✅ Env Variables | Migrate to Azure Key Vault |
| **Logging** | ✅ Basic | Add Azure Application Insights |
| **CORS** | ⚠️ All Origins | Restrict to known domains |

---

## 11. Scalability & Performance

### 11.1 Current Limitations

| Component | Limit | Impact |
|-----------|-------|--------|
| App Service B1 | 1.75 GB RAM, 1 vCPU | ~100 concurrent users |
| Single Container | 1 instance | No horizontal scaling |
| OpenAI API | Rate limited | Affects evaluation throughput |

### 11.2 Scaling Strategy

```
                           HORIZONTAL SCALING ARCHITECTURE
                           
                    ┌─────────────────────────────────────┐
                    │        Azure Traffic Manager        │
                    │         (Global Load Balancer)      │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────┼───────────────────┐
                    │                 │                   │
                    ▼                 ▼                   ▼
             ┌──────────┐      ┌──────────┐       ┌──────────┐
             │ App Svc  │      │ App Svc  │       │ App Svc  │
             │ Instance │      │ Instance │       │ Instance │
             │    1     │      │    2     │       │    3     │
             └────┬─────┘      └────┬─────┘       └────┬─────┘
                  │                 │                   │
                  └─────────────────┼───────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
             ┌──────────┐    ┌──────────┐    ┌──────────┐
             │  Azure   │    │  Redis   │    │PostgreSQL│
             │ OpenAI   │    │  Cache   │    │ Primary  │
             │          │    │          │    │ + Replica│
             └──────────┘    └──────────┘    └──────────┘
```

### 11.3 Performance Optimization Recommendations

1. **Caching Layer**: Add Redis for CV evaluation caching
2. **Async Processing**: Queue long-running AI evaluations
3. **Database Optimization**: Add read replicas, connection pooling
4. **CDN**: Cache static content (PDF reports)
5. **Batch Processing**: Bulk candidate imports

---

## 12. Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    ARYA MULTIAGENT RECRUITMENT SYSTEM - COMPLETE ARCHITECTURE                        │
│                                              End-to-End System Overview                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

                                                    ┌─────────────────┐
                                                    │    CLIENTS      │
                                                    │  (Web/Mobile/   │
                                                    │   API Tools)    │
                                                    └────────┬────────┘
                                                             │
                                                    HTTPS (TLS 1.3)
                                                             │
                                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                              AZURE CLOUD PLATFORM                                                    │
│                                            (France Central Region)                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                      │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   AZURE APP SERVICE (Linux B1)                                               │   │
│   │                                arya-recruitment-api-v2.azurewebsites.net                                     │   │
│   ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────┤   │
│   │                                                                                                              │   │
│   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐   │   │
│   │   │                           DOCKER CONTAINER (recruitment-api:latest)                                  │   │   │
│   │   │                                        Port 8000                                                     │   │   │
│   │   ├─────────────────────────────────────────────────────────────────────────────────────────────────────┤   │   │
│   │   │                                                                                                      │   │   │
│   │   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────┐   │   │   │
│   │   │   │                              FASTAPI APPLICATION (v1.0.0)                                    │   │   │   │
│   │   │   │                                                                                              │   │   │   │
│   │   │   │   ┌─────────────────────────────┐                                                            │   │   │   │
│   │   │   │   │      MIDDLEWARE LAYER       │                                                            │   │   │   │
│   │   │   │   │  ┌───────┐ ┌───────┐ ┌───┐  │                                                            │   │   │   │
│   │   │   │   │  │ CORS  │ │Pydantic│ │SSL│  │                                                            │   │   │   │
│   │   │   │   │  └───────┘ └───────┘ └───┘  │                                                            │   │   │   │
│   │   │   │   └──────────────┬──────────────┘                                                            │   │   │   │
│   │   │   │                  │                                                                            │   │   │   │
│   │   │   │                  ▼                                                                            │   │   │   │
│   │   │   │   ┌──────────────────────────────────────────────────────────────────────────────────────┐   │   │   │   │
│   │   │   │   │                           ENDPOINT AGENTS LAYER                                       │   │   │   │   │
│   │   │   │   │                                                                                       │   │   │   │   │
│   │   │   │   │   ┌────────────────┐    ┌────────────────────┐    ┌─────────────────────────┐        │   │   │   │   │
│   │   │   │   │   │  JOBS AGENT    │    │  CANDIDATES AGENT  │    │   SUBMISSIONS AGENT     │        │   │   │   │   │
│   │   │   │   │   │   (jobs.py)    │    │  (candidates.py)   │    │   (submissions.py)      │        │   │   │   │   │
│   │   │   │   │   │                │    │                    │    │                         │        │   │   │   │   │
│   │   │   │   │   │ POST /jobs     │    │ POST /candidates   │    │ POST /submissions       │        │   │   │   │   │
│   │   │   │   │   │ GET /jobs/{id} │    │ POST /cv           │    │ GET /submissions        │        │   │   │   │   │
│   │   │   │   │   │ GET /reference │    │ GET /report        │    │ GET /submissions/{phase}│        │   │   │   │   │
│   │   │   │   │   │ GET /rankings  │    │                    │    │                         │        │   │   │   │   │
│   │   │   │   │   └───────┬────────┘    └─────────┬──────────┘    └───────────┬─────────────┘        │   │   │   │   │
│   │   │   │   │           │                       │                           │                      │   │   │   │   │
│   │   │   │   └───────────┼───────────────────────┼───────────────────────────┼──────────────────────┘   │   │   │   │
│   │   │   │               │                       │                           │                          │   │   │   │
│   │   │   │               └───────────────────────┼───────────────────────────┘                          │   │   │   │
│   │   │   │                                       │                                                      │   │   │   │
│   │   │   │                                       ▼                                                      │   │   │   │
│   │   │   │   ┌──────────────────────────────────────────────────────────────────────────────────────┐   │   │   │   │
│   │   │   │   │                           SERVICE AGENTS LAYER                                        │   │   │   │   │
│   │   │   │   │                                                                                       │   │   │   │   │
│   │   │   │   │   ┌────────────────┐    ┌────────────────────┐    ┌─────────────────────────┐        │   │   │   │   │
│   │   │   │   │   │PROJECT SERVICE │    │EVALUATION SERVICE  │    │     PDF SERVICE         │        │   │   │   │   │
│   │   │   │   │   │    AGENT       │    │      AGENT         │    │       AGENT             │        │   │   │   │   │
│   │   │   │   │   │                │    │                    │    │                         │        │   │   │   │   │
│   │   │   │   │   │• Create Job    │    │• Evaluate CV       │    │• Candidate Report       │        │   │   │   │   │
│   │   │   │   │   │• Generate      │    │• Evaluate Submission│   │• Reference Guide        │        │   │   │   │   │
│   │   │   │   │   │  Assessment    │    │• Rank Candidates   │    │• Text Cleaning          │        │   │   │   │   │
│   │   │   │   │   │• Get Job Data  │    │• Update Status     │    │                         │        │   │   │   │   │
│   │   │   │   │   └───────┬────────┘    └─────────┬──────────┘    └─────────────────────────┘        │   │   │   │   │
│   │   │   │   │           │                       │                                                   │   │   │   │   │
│   │   │   │   └───────────┼───────────────────────┼───────────────────────────────────────────────────┘   │   │   │   │
│   │   │   │               │                       │                                                      │   │   │   │
│   │   │   │               └───────────┬───────────┘                                                      │   │   │   │
│   │   │   │                           │                                                                  │   │   │   │
│   │   │   │                           ▼                                                                  │   │   │   │
│   │   │   │   ┌──────────────────────────────────────────────────────────────────────────────────────┐   │   │   │   │
│   │   │   │   │                           EXTERNAL AGENTS LAYER                                       │   │   │   │   │
│   │   │   │   │                                                                                       │   │   │   │   │
│   │   │   │   │   ┌─────────────────────────────────┐    ┌────────────────────────────────────────┐   │   │   │   │   │
│   │   │   │   │   │         OPENAI AGENT            │    │          DATABASE AGENT                │   │   │   │   │   │
│   │   │   │   │   │      (openai_service.py)        │    │             (db.py)                    │   │   │   │   │   │
│   │   │   │   │   │                                 │    │                                        │   │   │   │   │   │
│   │   │   │   │   │ • extract_job_details()        │    │ • SQLAlchemy Engine                    │   │   │   │   │   │
│   │   │   │   │   │ • generate_project_dict()      │    │ • SessionLocal Factory                 │   │   │   │   │   │
│   │   │   │   │   │ • evaluate_cv()                │    │ • get_db() Dependency                  │   │   │   │   │   │
│   │   │   │   │   │ • evaluate_submission()        │    │ • Connection Pool                      │   │   │   │   │   │
│   │   │   │   │   │                                 │    │                                        │   │   │   │   │   │
│   │   │   │   │   │ [AzureOpenAI Client]           │    │ [create_engine()]                      │   │   │   │   │   │
│   │   │   │   │   └────────────┬────────────────────┘    └───────────────────┬────────────────────┘   │   │   │   │   │
│   │   │   │   │                │                                             │                        │   │   │   │   │
│   │   │   │   └────────────────┼─────────────────────────────────────────────┼────────────────────────┘   │   │   │   │
│   │   │   │                    │                                             │                            │   │   │   │
│   │   │   └────────────────────┼─────────────────────────────────────────────┼────────────────────────────┘   │   │   │
│   │   │                        │                                             │                                │   │   │
│   │   └────────────────────────┼─────────────────────────────────────────────┼────────────────────────────────┘   │   │
│   │                            │                                             │                                    │   │
│   └────────────────────────────┼─────────────────────────────────────────────┼────────────────────────────────────┘   │
│                                │                                             │                                        │
│   ┌────────────────────────────┼─────────────────────────────────────────────┼────────────────────────────────────┐   │
│   │                            │     AZURE CONTAINER REGISTRY (ACR)          │                                    │   │
│   │                            │         aryaregistryv2.azurecr.io           │                                    │   │
│   │                            │                                             │                                    │   │
│   │                            │   ┌─────────────────────────────────────┐   │                                    │   │
│   │                            │   │     recruitment-api:latest          │   │                                    │   │
│   │                            │   │        (Docker Image)               │   │                                    │   │
│   │                            │   └─────────────────────────────────────┘   │                                    │   │
│   └────────────────────────────┼─────────────────────────────────────────────┼────────────────────────────────────┘   │
│                                │                                             │                                        │
└────────────────────────────────┼─────────────────────────────────────────────┼────────────────────────────────────────┘
                                 │                                             │
                                 ▼                                             ▼
              ┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
              │         AZURE OPENAI SERVICE         │     │           POSTGRESQL DATABASE        │
              │   (Cognitive Services - External)    │     │            (External Server)         │
              │                                      │     │                                      │
              │   ┌──────────────────────────────┐   │     │   ┌──────────────────────────────┐   │
              │   │    GPT-4o Deployment         │   │     │   │       jobs                   │   │
              │   │                              │   │     │   │       projects               │   │
              │   │   • Job Analysis             │   │     │   │       candidates             │   │
              │   │   • Project Generation       │   │     │   │       submissions            │   │
              │   │   • CV Evaluation            │   │     │   │                              │   │
              │   │   • Submission Scoring       │   │     │   │   Connection: SSL/TLS        │   │
              │   │                              │   │     │   │   Port: 5432                 │   │
              │   │   API Version: 2024-12-01    │   │     │   │                              │   │
              │   └──────────────────────────────┘   │     │   └──────────────────────────────┘   │
              │                                      │     │                                      │
              └──────────────────────────────────────┘     └──────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                               DATA FLOW SUMMARY                                                      │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                      │
│   1. JOB CREATION FLOW                                                                                               │
│      Client → Jobs Agent → Project Service → OpenAI Agent → Database Agent → Response                               │
│                                                                                                                      │
│   2. CV EVALUATION FLOW                                                                                              │
│      Client (PDF) → Candidates Agent → PyPDF2 → Evaluation Service → OpenAI Agent → Database Agent → Response       │
│                                                                                                                      │
│   3. SUBMISSION EVALUATION FLOW                                                                                      │
│      Client (JSON) → Submissions Agent → Evaluation Service → OpenAI Agent → Database Agent → Response              │
│                                                                                                                      │
│   4. CANDIDATE RANKING FLOW                                                                                          │
│      Client → Jobs Agent → Evaluation Service → Database Agent (Fetch All) → Ranking Algorithm → Response           │
│                                                                                                                      │
│   5. PDF GENERATION FLOW                                                                                             │
│      Client → Endpoint Agent → PDF Service → FPDF → Temp File → FileResponse                                        │
│                                                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Appendix A: Dependencies

```plaintext
# Python Dependencies (requirements.txt)
fastapi              # Web framework
uvicorn[standard]    # ASGI server
sqlalchemy           # ORM
pydantic[email]      # Data validation
pydantic-settings    # Settings management
python-dotenv        # Environment loading
python-multipart     # File uploads
openai               # Azure OpenAI SDK
fpdf                 # PDF generation
PyPDF2               # PDF reading
psycopg2-binary      # PostgreSQL driver
```

---

## Appendix B: Quick Reference Commands

```bash
# Local Development
uvicorn app.main:app --reload --port 8000

# Docker Build & Run
docker build -t arya-api .
docker run -p 8000:8000 --env-file .env arya-api

# Azure Deployment
az acr build --registry aryaregistryv2 --image recruitment-api:latest .
az webapp restart --name arya-recruitment-api-v2 --resource-group Arya-v2-recruitment-API

# View Logs
az webapp log tail --name arya-recruitment-api-v2 --resource-group Arya-v2-recruitment-API

# Health Check
curl https://arya-recruitment-api-v2.azurewebsites.net/
```

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-03 | AI & Data Engineering Team | Initial comprehensive analysis |

---

*This document provides a complete end-to-end analysis of the ARYA Multiagent Recruitment System architecture, including all agents, data flows, database design, AI components, Azure infrastructure, and deployment processes.*
