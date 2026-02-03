# ARYA System Architecture Diagrams

**Version:** 2.0  
**Last Updated:** February 2026  
**Author:** Mohamed Amine Elabidi

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Multi-Agent Architecture](#2-multi-agent-architecture)
3. [Data Flow Diagrams](#3-data-flow-diagrams)
4. [API Request Flow](#4-api-request-flow)
5. [Database Schema](#5-database-schema)
6. [Deployment Architecture](#6-deployment-architecture)
7. [Sequence Diagrams](#7-sequence-diagrams)
8. [Component Diagrams](#8-component-diagrams)
9. [State Machine Diagrams](#9-state-machine-diagrams)

---

## 1. System Overview

### 1.1 High-Level Architecture

The ARYA system follows a modern cloud-native architecture deployed on Microsoft Azure. The platform integrates multiple services to provide intelligent recruitment assessment capabilities.

<!-- High-Level Architecture Diagram -->
<div align="center">
  <img src="../img/architecture_arya_multiagent_azure.png" alt="High-Level Architecture" width="800"/>
  <br/>
  <em>Figure 1.1: ARYA High-Level System Architecture</em>
</div>

```mermaid
graph TB
    subgraph "Clients"
        WEB[Web Application]
        MOB[Mobile App]
        API_C[Third-Party APIs]
    end

    subgraph "Azure Cloud"
        subgraph "Azure App Service"
            ARYA[ARYA API - FastAPI Application]
        end
        
        subgraph "Azure OpenAI"
            GPT[GPT-4o Model]
        end
        
        subgraph "Database"
            PG[(PostgreSQL)]
        end
        
        subgraph "Container Registry"
            ACR[Azure Container Registry]
        end
    end

    WEB -->|HTTPS| ARYA
    MOB -->|HTTPS| ARYA
    API_C -->|HTTPS| ARYA
    
    ARYA <-->|SQL| PG
    ARYA <-->|API| GPT
    ACR -->|Deploy| ARYA
```

### 1.2 Technology Stack Overview

<!-- IMAGE PLACEHOLDER: Technology Stack Diagram -->
<div align="center">
  <img src="../assets/diagrams/technology-stack.png" alt="Technology Stack" width="700"/>
  <br/>
  <em>Figure 1.2: Technology Stack Overview</em>
</div>

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Presentation** | Swagger UI, ReDoc | API Documentation |
| **API** | FastAPI 0.109+ | Request handling, routing |
| **Business Logic** | Python Services | Core business operations |
| **Data Access** | SQLAlchemy 2.x | ORM, database abstraction |
| **Database** | PostgreSQL 14+ | Data persistence |
| **AI Services** | Azure OpenAI GPT-4o | NLP, content generation |
| **Infrastructure** | Azure App Service | Cloud hosting |

---

## 2. Multi-Agent Architecture

### 2.1 Agent Hierarchy

The ARYA platform implements a multi-agent architecture pattern where each agent has specialized responsibilities. This design ensures separation of concerns, maintainability, and scalability.

<!-- IMAGE PLACEHOLDER: Agent Hierarchy Diagram -->
<div align="center">
  <img src="../assets/diagrams/agent-hierarchy.png" alt="Agent Hierarchy" width="800"/>
  <br/>
  <em>Figure 2.1: Multi-Agent Hierarchy</em>
</div>

```mermaid
graph TB
    subgraph "Endpoint Agents"
        JA[Jobs Agent]
        CA[Candidates Agent]
        SA[Submissions Agent]
    end

    subgraph "Service Agents"
        PS[Project Service]
        ES[Evaluation Service]
        PDF[PDF Service]
    end

    subgraph "External Agents"
        OAI[OpenAI Agent]
        DB[Database Agent]
    end

    JA --> PS
    JA --> PDF
    CA --> ES
    CA --> PDF
    SA --> ES

    PS --> OAI
    PS --> DB
    ES --> OAI
    ES --> DB
    PDF --> DB
```

### 2.2 Agent Responsibilities

| Agent | Type | Responsibilities |
|-------|------|------------------|
| **Jobs Agent** | Endpoint | Job creation, retrieval, rankings management |
| **Candidates Agent** | Endpoint | Candidate registration, CV processing, report generation |
| **Submissions Agent** | Endpoint | Project submission handling, evaluation triggering |
| **Project Service** | Service | Job workflow orchestration, assessment generation |
| **Evaluation Service** | Service | CV scoring, submission evaluation, ranking calculation |
| **PDF Service** | Service | Document generation, PDF parsing |
| **OpenAI Agent** | External | AI-powered analysis and content generation |
| **Database Agent** | External | Data persistence, query execution |

### 2.3 Agent Communication Flow

<!-- IMAGE PLACEHOLDER: Agent Communication Flow -->
<div align="center">
  <img src="../assets/diagrams/agent-communication.png" alt="Agent Communication" width="700"/>
  <br/>
  <em>Figure 2.2: Agent Communication Flow</em>
</div>

```mermaid
graph LR
    CLIENT((Client)) --> |HTTP| FASTAPI[FastAPI]
    FASTAPI --> |Route| ENDPOINT[Endpoint Agent]
    ENDPOINT --> |Call| SERVICE[Service Agent]
    SERVICE --> |Query| EXTERNAL[External Agent]
    EXTERNAL --> |Response| SERVICE
    SERVICE --> |Response| ENDPOINT
    ENDPOINT --> |JSON| FASTAPI
    FASTAPI --> |HTTP| CLIENT
```

---

## 3. Data Flow Diagrams

### 3.1 Job Creation Flow

This diagram illustrates the complete flow from job description input to assessment project generation.

<!-- IMAGE PLACEHOLDER: Job Creation Flow -->
<div align="center">
  <img src="../assets/diagrams/job-creation-flow.png" alt="Job Creation Flow" width="800"/>
  <br/>
  <em>Figure 3.1: Job Creation Data Flow</em>
</div>

```mermaid
flowchart TD
    START((Start)) --> INPUT[Receive Job Description]
    INPUT --> VALIDATE{Validate Input}
    
    VALIDATE -->|Invalid| ERROR1[Return 422 Error]
    VALIDATE -->|Valid| ANALYZE[AI Analyzes Job Description]
    
    ANALYZE --> EXTRACT[Extract Skills and Requirements]
    EXTRACT --> GENERATE[Generate Assessment Project]
    
    GENERATE --> PHASES[Create 3 Project Phases]
    PHASES --> CRITERIA[Define Evaluation Criteria]
    
    CRITERIA --> SAVE[Save to Database]
    SAVE --> PDF_GEN[Generate Reference Guide PDF]
    
    PDF_GEN --> RESPONSE[Return Job with Project]
    RESPONSE --> END_S((End))
    ERROR1 --> END_E((End))
```

**Process Steps:**

1. **Input Validation** - Verify required fields and data format
2. **AI Analysis** - GPT-4o extracts skills and requirements from job description
3. **Project Generation** - AI creates role-specific assessment project
4. **Phase Creation** - Generate three progressive evaluation phases
5. **Criteria Definition** - Establish scoring criteria for each phase
6. **Persistence** - Save job and project to database
7. **PDF Generation** - Create reference guide for evaluators

### 3.2 CV Evaluation Flow

<!-- IMAGE PLACEHOLDER: CV Evaluation Flow -->
<div align="center">
  <img src="../assets/diagrams/cv-evaluation-flow.png" alt="CV Evaluation Flow" width="800"/>
  <br/>
  <em>Figure 3.2: CV Evaluation Data Flow</em>
</div>

```mermaid
flowchart TD
    START((Start)) --> UPLOAD[Upload CV PDF]
    UPLOAD --> PARSE[Parse PDF - Extract Text]
    
    PARSE --> VALID{Valid PDF}
    VALID -->|No| ERROR[Return Error]
    VALID -->|Yes| FETCH[Fetch Job Requirements]
    
    FETCH --> AI_EVAL[AI Evaluates CV vs Requirements]
    AI_EVAL --> SCORES[Calculate Scores]
    
    SCORES --> SAVE[Save Evaluation]
    SAVE --> UPDATE[Update Candidate Status]
    UPDATE --> RESPONSE[Return Evaluation Result]
    RESPONSE --> END_S((End))
    ERROR --> END_E((End))
```

### 3.3 Candidate Ranking Flow

<!-- IMAGE PLACEHOLDER: Ranking Algorithm Flow -->
<div align="center">
  <img src="../assets/diagrams/ranking-flow.png" alt="Ranking Flow" width="700"/>
  <br/>
  <em>Figure 3.3: Candidate Ranking Algorithm</em>
</div>

**Scoring Formula:**

```
Final Score = (CV Score × 0.30) + (Average Project Score × 0.70)
```

| Component | Weight | Description |
|-----------|--------|-------------|
| CV Score | 30% | Skills match, experience fit, industry relevance |
| Project Score | 70% | Average of all phase submission scores |

---

## 4. API Request Flow

### 4.1 Request Lifecycle

<!-- IMAGE PLACEHOLDER: Request Lifecycle -->
<div align="center">
  <img src="../assets/diagrams/request-lifecycle.png" alt="Request Lifecycle" width="800"/>
  <br/>
  <em>Figure 4.1: Complete API Request Lifecycle</em>
</div>

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant F as FastAPI
    participant M as Middleware
    participant R as Router
    participant E as Endpoint
    participant S as Service
    participant AI as OpenAI
    participant DB as Database

    C->>F: HTTP Request
    F->>M: Process Request
    M->>M: CORS Check
    M->>M: Validate Headers
    M->>R: Route Request
    R->>E: Call Endpoint Handler
    
    E->>S: Business Logic
    
    par AI Processing
        S->>AI: Send Prompt
        AI-->>S: AI Response
    and Database Query
        S->>DB: Query/Save Data
        DB-->>S: Result
    end
    
    S-->>E: Processed Result
    E-->>R: Response Data
    R-->>M: Format Response
    M-->>F: Add Headers
    F-->>C: HTTP Response
```

### 4.2 Error Handling

| HTTP Status | Error Type | Description |
|-------------|------------|-------------|
| 400 | Bad Request | Malformed request syntax |
| 401 | Unauthorized | Authentication required |
| 404 | Not Found | Resource does not exist |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | External service failure |

---

## 5. Database Schema

### 5.1 Entity Relationship Diagram

<!-- IMAGE PLACEHOLDER: Entity Relationship Diagram -->
<div align="center">
  <img src="../assets/diagrams/erd.png" alt="Entity Relationship Diagram" width="800"/>
  <br/>
  <em>Figure 5.1: Database Entity Relationship Diagram</em>
</div>

```mermaid
erDiagram
    JOB ||--o{ CANDIDATE : "has many"
    JOB ||--|| PROJECT : "has one"
    CANDIDATE ||--o{ SUBMISSION : "has many"
    
    JOB {
        int id PK
        string title
        text description
        json extracted_skills
        string status
        datetime created_at
    }
    
    PROJECT {
        int id PK
        int job_id FK
        string title
        text overview
        json phases
        json evaluation_criteria
        text reference_guide
    }
    
    CANDIDATE {
        int id PK
        int job_id FK
        string name
        string email
        float cv_score
        string cv_evaluation
        text cv_text
        string status
        datetime created_at
    }
    
    SUBMISSION {
        int id PK
        int candidate_id FK
        int phase_number
        text content
        float score
        text feedback
        datetime submitted_at
    }
```

### 5.2 Table Specifications

#### Jobs Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| title | VARCHAR(255) | NOT NULL | Job title |
| description | TEXT | NOT NULL | Full job description |
| extracted_skills | JSON | - | AI-extracted skills |
| status | VARCHAR(50) | DEFAULT 'active' | Job status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

#### Candidates Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| job_id | INTEGER | FOREIGN KEY | Reference to jobs |
| name | VARCHAR(255) | NOT NULL | Candidate name |
| email | VARCHAR(255) | NOT NULL, UNIQUE per job | Contact email |
| cv_score | FLOAT | - | CV evaluation score (0-100) |
| cv_evaluation | TEXT | - | AI evaluation summary |
| cv_text | TEXT | - | Extracted CV content |
| status | VARCHAR(50) | DEFAULT 'registered' | Candidate status |
| created_at | TIMESTAMP | DEFAULT NOW() | Registration timestamp |

---

## 6. Deployment Architecture

### 6.1 Azure Infrastructure

<!-- IMAGE PLACEHOLDER: Azure Infrastructure Diagram -->
<div align="center">
  <img src="../assets/diagrams/azure-infrastructure.png" alt="Azure Infrastructure" width="800"/>
  <br/>
  <em>Figure 6.1: Azure Cloud Infrastructure</em>
</div>

```mermaid
graph TB
    subgraph "Internet"
        USER[Users]
    end
    
    subgraph "Azure Cloud - France Central"
        subgraph "Virtual Network"
            subgraph "App Service Plan - Linux B1"
                APP[ARYA API]
            end
            
            subgraph "Database"
                PG[(PostgreSQL Flexible Server)]
            end
        end
        
        subgraph "AI Services"
            AOAI[Azure OpenAI - GPT-4o]
        end
        
        subgraph "Container Services"
            ACR[Azure Container Registry]
        end
        
        subgraph "DevOps"
            GH[GitHub Actions]
        end
    end
    
    USER -->|HTTPS :443| APP
    APP <-->|TCP :5432| PG
    APP <-->|HTTPS| AOAI
    GH -->|Push| ACR
    ACR -->|Deploy| APP
```

### 6.2 Infrastructure Components

| Component | Azure Service | SKU/Tier | Purpose |
|-----------|--------------|----------|---------|
| **API Server** | App Service | Linux B1 | Application hosting |
| **Database** | PostgreSQL Flexible Server | Burstable B1ms | Data persistence |
| **AI Service** | Azure OpenAI | Standard | GPT-4o model access |
| **Container Registry** | Container Registry | Basic | Docker image storage |
| **CI/CD** | GitHub Actions | - | Automated deployment |

### 6.3 CI/CD Pipeline

<!-- IMAGE PLACEHOLDER: CI/CD Pipeline -->
<div align="center">
  <img src="../assets/diagrams/cicd-pipeline.png" alt="CI/CD Pipeline" width="800"/>
  <br/>
  <em>Figure 6.2: Continuous Integration and Deployment Pipeline</em>
</div>

```mermaid
flowchart LR
    subgraph "Development"
        DEV[Developer]
        CODE[Code Changes]
    end
    
    subgraph "GitHub"
        REPO[Repository]
        PR[Pull Request]
        MAIN[Main Branch]
    end
    
    subgraph "GitHub Actions"
        LINT[Lint]
        TEST[Test]
        BUILD[Build Image]
        PUSH[Push to ACR]
    end
    
    subgraph "Azure"
        ACR[Container Registry]
        APP[App Service]
    end
    
    DEV --> CODE
    CODE --> REPO
    REPO --> PR
    PR --> MAIN
    MAIN --> LINT
    LINT --> TEST
    TEST --> BUILD
    BUILD --> PUSH
    PUSH --> ACR
    ACR --> APP
```

---

## 7. Sequence Diagrams

### 7.1 Job Creation Sequence

<!-- IMAGE PLACEHOLDER: Job Creation Sequence -->
<div align="center">
  <img src="../assets/diagrams/sequence-job-creation.png" alt="Job Creation Sequence" width="800"/>
  <br/>
  <em>Figure 7.1: Job Creation Sequence Diagram</em>
</div>

```mermaid
sequenceDiagram
    autonumber
    actor HR as HR Manager
    participant API as ARYA API
    participant PS as Project Service
    participant OAI as OpenAI
    participant DB as Database
    participant PDF as PDF Service

    HR->>+API: POST /api/v1/jobs
    Note over HR,API: Request body: {title, description}
    
    API->>+PS: create_job_with_project()
    
    PS->>+OAI: analyze_job_description()
    OAI-->>-PS: extracted_skills, requirements
    
    PS->>+OAI: generate_assessment_project()
    OAI-->>-PS: project with 3 phases
    
    PS->>+DB: save Job
    DB-->>-PS: job_id
    
    PS->>+DB: save Project
    DB-->>-PS: project_id
    
    PS->>+PDF: generate_reference_guide()
    PDF-->>-PS: PDF content
    
    PS-->>-API: Job with Project
    API-->>-HR: 201 Created
```

### 7.2 Candidate Registration and CV Upload

<!-- IMAGE PLACEHOLDER: Candidate Flow Sequence -->
<div align="center">
  <img src="../assets/diagrams/sequence-candidate-flow.png" alt="Candidate Flow" width="800"/>
  <br/>
  <em>Figure 7.2: Candidate Registration and CV Upload Sequence</em>
</div>

```mermaid
sequenceDiagram
    autonumber
    actor C as Candidate
    participant API as ARYA API
    participant ES as Evaluation Service
    participant OAI as OpenAI
    participant PDF as PDF Service
    participant DB as Database

    C->>+API: POST /api/v1/jobs/{id}/candidates
    Note over C,API: Request body: {name, email}
    
    API->>+DB: Check existing candidate
    DB-->>-API: Not found
    
    API->>+DB: Create candidate
    DB-->>-API: candidate_id
    
    API-->>-C: 201 Created
    
    C->>+API: POST /api/v1/candidates/{id}/cv
    Note over C,API: Multipart form: PDF file
    
    API->>+PDF: parse_pdf()
    PDF-->>-API: extracted_text
    
    API->>+ES: evaluate_cv()
    ES->>+OAI: analyze CV vs job requirements
    OAI-->>-ES: evaluation + score
    ES-->>-API: cv_score, cv_evaluation
    
    API->>+DB: Update candidate
    DB-->>-API: Updated
    
    API-->>-C: 200 OK
```

---

## 8. Component Diagrams

### 8.1 Application Components

<!-- IMAGE PLACEHOLDER: Application Components -->
<div align="center">
  <img src="../assets/diagrams/application-components.png" alt="Application Components" width="800"/>
  <br/>
  <em>Figure 8.1: Application Component Architecture</em>
</div>

```mermaid
graph TB
    subgraph "FastAPI Application"
        subgraph "API Layer"
            MAIN[main.py]
            JOBS_EP[jobs.py]
            CAND_EP[candidates.py]
            SUB_EP[submissions.py]
            SCHEMAS[schemas.py]
        end
        
        subgraph "Service Layer"
            PROJ_SVC[project_service.py]
            EVAL_SVC[evaluation_service.py]
            PDF_SVC[pdf_service.py]
            OAI_SVC[openai_service.py]
        end
        
        subgraph "Data Layer"
            CONFIG[config.py]
            DB_CORE[db.py]
            JOB_MODEL[job.py]
            CAND_MODEL[candidate.py]
            PROJ_MODEL[project.py]
            SUB_MODEL[submission.py]
        end
    end
    
    MAIN --> JOBS_EP
    MAIN --> CAND_EP
    MAIN --> SUB_EP
    
    JOBS_EP --> PROJ_SVC
    CAND_EP --> EVAL_SVC
    SUB_EP --> EVAL_SVC
    
    PROJ_SVC --> OAI_SVC
    EVAL_SVC --> OAI_SVC
    
    PROJ_SVC --> DB_CORE
    EVAL_SVC --> DB_CORE
    PDF_SVC --> DB_CORE
```

### 8.2 Directory Structure

```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── jobs.py           # Job endpoints
│       │   ├── candidates.py     # Candidate endpoints
│       │   └── submissions.py    # Submission endpoints
│       └── schemas.py            # Pydantic models
├── core/
│   ├── config.py                 # Configuration
│   └── db.py                     # Database setup
├── models/
│   ├── job.py                    # Job ORM model
│   ├── candidate.py              # Candidate ORM model
│   ├── project.py                # Project ORM model
│   └── submission.py             # Submission ORM model
├── services/
│   ├── openai_service.py         # AI integration
│   ├── project_service.py        # Job orchestration
│   ├── evaluation_service.py     # Scoring logic
│   └── pdf_service.py            # PDF generation
└── main.py                       # Application entry
```

---

## 9. State Machine Diagrams

### 9.1 Job Lifecycle

<!-- IMAGE PLACEHOLDER: Job State Machine -->
<div align="center">
  <img src="../assets/diagrams/state-job-lifecycle.png" alt="Job Lifecycle" width="700"/>
  <br/>
  <em>Figure 9.1: Job State Machine</em>
</div>

```mermaid
stateDiagram-v2
    [*] --> Draft: Create Job
    Draft --> Active: Publish
    Draft --> Cancelled: Cancel
    
    Active --> Evaluating: Candidates Apply
    Evaluating --> Active: No Candidates
    Evaluating --> Completed: All Evaluated
    
    Active --> Closed: Manual Close
    Evaluating --> Closed: Manual Close
    Completed --> Closed: Archive
    
    Closed --> [*]
    Cancelled --> [*]
```

| State | Description | Allowed Transitions |
|-------|-------------|---------------------|
| **Draft** | Job created, not yet published | Active, Cancelled |
| **Active** | Accepting candidate applications | Evaluating, Closed |
| **Evaluating** | Processing candidate submissions | Active, Completed, Closed |
| **Completed** | All evaluations finished | Closed |
| **Closed** | Job archived | Terminal |
| **Cancelled** | Job cancelled before publishing | Terminal |

### 9.2 Candidate Lifecycle

<!-- IMAGE PLACEHOLDER: Candidate State Machine -->
<div align="center">
  <img src="../assets/diagrams/state-candidate-lifecycle.png" alt="Candidate Lifecycle" width="800"/>
  <br/>
  <em>Figure 9.2: Candidate State Machine</em>
</div>

```mermaid
stateDiagram-v2
    [*] --> Registered: Apply to Job
    
    Registered --> CV_Uploaded: Upload CV
    CV_Uploaded --> CV_Evaluated: AI Evaluation
    
    CV_Evaluated --> Phase1_Pending: Start Project
    Phase1_Pending --> Phase1_Submitted: Submit Phase 1
    Phase1_Submitted --> Phase1_Evaluated: AI Scores
    
    Phase1_Evaluated --> Phase2_Pending: Continue
    Phase2_Pending --> Phase2_Submitted: Submit Phase 2
    Phase2_Submitted --> Phase2_Evaluated: AI Scores
    
    Phase2_Evaluated --> Phase3_Pending: Continue
    Phase3_Pending --> Phase3_Submitted: Submit Phase 3
    Phase3_Submitted --> Phase3_Evaluated: AI Scores
    
    Phase3_Evaluated --> Completed: All Done
    Completed --> Ranked: Final Score
    
    Ranked --> [*]
```

---

## Appendix A: Image Assets

The following image placeholders should be replaced with actual diagram exports:

| Figure | Filename | Recommended Format | Dimensions |
|--------|----------|-------------------|------------|
| 1.1 | high-level-architecture.png | PNG | 1600x900 |
| 1.2 | technology-stack.png | PNG | 1400x800 |
| 2.1 | agent-hierarchy.png | PNG | 1600x1000 |
| 2.2 | agent-communication.png | PNG | 1400x600 |
| 3.1 | job-creation-flow.png | PNG | 1600x1200 |
| 3.2 | cv-evaluation-flow.png | PNG | 1600x1000 |
| 3.3 | ranking-flow.png | PNG | 1400x600 |
| 4.1 | request-lifecycle.png | PNG | 1600x1000 |
| 5.1 | erd.png | PNG | 1600x900 |
| 6.1 | azure-infrastructure.png | PNG | 1600x1000 |
| 6.2 | cicd-pipeline.png | PNG | 1600x600 |
| 7.1 | sequence-job-creation.png | PNG | 1600x1200 |
| 7.2 | sequence-candidate-flow.png | PNG | 1600x1200 |
| 8.1 | application-components.png | PNG | 1600x1200 |
| 9.1 | state-job-lifecycle.png | PNG | 1400x800 |
| 9.2 | state-candidate-lifecycle.png | PNG | 1600x1000 |

**Directory structure for assets:**
```
assets/
└── diagrams/
    ├── high-level-architecture.png
    ├── technology-stack.png
    ├── agent-hierarchy.png
    └── ...
```

---

## Appendix B: Diagram Tools

Recommended tools for creating and exporting diagrams:

| Tool | Purpose | Export Formats |
|------|---------|----------------|
| [Draw.io](https://draw.io) | General diagrams | PNG, SVG, PDF |
| [Lucidchart](https://lucidchart.com) | Professional diagrams | PNG, SVG, PDF |
| [Mermaid Live](https://mermaid.live) | Mermaid rendering | PNG, SVG |
| [PlantUML](https://plantuml.com) | UML diagrams | PNG, SVG |
| [Excalidraw](https://excalidraw.com) | Hand-drawn style | PNG, SVG |

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure App Service Documentation](https://learn.microsoft.com/azure/app-service/)
- [Mermaid Diagram Syntax](https://mermaid.js.org/intro/)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | January 2026 | Mohamed Amine Elabidi | Initial version |
| 2.0 | February 2026 | Mohamed Amine Elabidi | Added image placeholders, professional formatting |

---

*This document is part of the ARYA Multi-Agent Recruitment System technical documentation.*
