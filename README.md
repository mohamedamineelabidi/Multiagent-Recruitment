<div align="center">

# 🤖 ARYA API

### AI-Powered Recruitment Assessment Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Azure](https://img.shields.io/badge/Azure_OpenAI-GPT--4o-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

*Revolutionizing the hiring process through intelligent multi-agent systems*

[🚀 Live Demo](https://arya-recruitment-api-v2.azurewebsites.net/docs) • [📖 Documentation](#-documentation) • [🏗️ Architecture](#-system-architecture) • [🤝 Contributing](CONTRIBUTING.md)

---

</div>

## 👨‍💻 About the Author

<table>
<tr>
<td width="150">
<img src="https://github.com/mohamedamineelabidi.png" width="150" style="border-radius: 50%"/>
</td>
<td>

### Mohamed Amine Elabidi

**AI & Data Engineer**

I'm a passionate AI and Data Engineer with expertise in building intelligent systems that solve real-world business problems. My focus areas include:

- 🧠 **Artificial Intelligence** - LLMs, NLP, Machine Learning
- 📊 **Data Engineering** - Pipelines, ETL, Data Architecture  
- ☁️ **Cloud Computing** - Azure, AWS, Containerization
- 🏗️ **System Design** - Microservices, Multi-Agent Architectures

[![GitHub](https://img.shields.io/badge/GitHub-mohamedamineelabidi-181717?style=flat-square&logo=github)](https://github.com/mohamedamineelabidi)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/mohamedamineelabidi)

</td>
</tr>
</table>

---

## 🎯 Project Overview

**ARYA** (**A**I **R**ecruitment & **Y**ield **A**ssessment) is an enterprise-grade API platform that transforms traditional hiring processes using cutting-edge AI technology. Built with a sophisticated **multi-agent architecture**, ARYA automates and enhances every step of candidate evaluation.

### 💼 The Business Problem

Traditional recruitment faces critical challenges:

| Challenge | Impact |
|-----------|--------|
| ⏰ Time-consuming manual CV screening | 23 hours per hire on average |
| 🎯 Inconsistent evaluation criteria | Subjective bias in assessments |
| 📊 Lack of data-driven decisions | Poor hire quality predictions |
| 🔄 Repetitive assessment creation | Inefficient use of HR resources |

### ✨ The ARYA Solution

ARYA addresses these challenges through intelligent automation:

| Feature | Benefit |
|---------|---------|
| 🤖 **AI-Powered Job Analysis** | Automatically extracts skills & requirements |
| 📝 **Smart Assessment Generation** | Creates AI-resistant, role-specific projects |
| 📄 **Intelligent CV Evaluation** | Objective scoring against job criteria |
| 📊 **Data-Driven Rankings** | Weighted algorithms for fair comparison |
| 📑 **Professional Reporting** | Automated PDF generation for stakeholders |

---

## 🌐 Live Deployment

The API is deployed on **Microsoft Azure** and ready for integration:

| Environment | URL | Status |
|-------------|-----|--------|
| **Production API** | https://arya-recruitment-api-v2.azurewebsites.net | 🟢 Live |
| **Swagger UI** | https://arya-recruitment-api-v2.azurewebsites.net/docs | 🟢 Live |
| **ReDoc** | https://arya-recruitment-api-v2.azurewebsites.net/redoc | 🟢 Live |

---

## 🏗️ System Architecture

ARYA follows an **enterprise-grade multi-agent architecture** pattern, similar to systems used at leading tech companies. Each agent has specialized responsibilities, ensuring separation of concerns, scalability, and maintainability.

### Agent Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│                    (Web Apps • Mobile • Third-party Integrations)            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                             HTTPS (TLS 1.3)
                                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY LAYER                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                        FastAPI Application                              ││
│  │     ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐       ││
│  │     │   CORS   │    │Validation│    │  Routing │    │ Logging  │       ││
│  │     └──────────┘    └──────────┘    └──────────┘    └──────────┘       ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ENDPOINT AGENTS LAYER                                │
│      ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│      │   🎯 Jobs Agent   │  │ 👤 Candidates    │  │ 📝 Submissions   │       │
│      │                  │  │     Agent        │  │     Agent        │       │
│      │ • Create Jobs    │  │ • Registration   │  │ • Submit Work    │       │
│      │ • Get Rankings   │  │ • CV Upload      │  │ • Track Progress │       │
│      │ • Reference PDFs │  │ • PDF Reports    │  │ • Get Evaluations│       │
│      └──────────────────┘  └──────────────────┘  └──────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SERVICE AGENTS LAYER                                │
│      ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│      │ 🔧 Project       │  │ 📊 Evaluation    │  │ 📄 PDF           │       │
│      │    Service       │  │    Service       │  │    Service       │       │
│      │                  │  │                  │  │                  │       │
│      │ • Orchestration  │  │ • CV Scoring     │  │ • Report Gen     │       │
│      │ • Job Creation   │  │ • Ranking Algo   │  │ • Guide Gen      │       │
│      │ • Assessment Gen │  │ • Status Updates │  │ • Text Cleanup   │       │
│      └──────────────────┘  └──────────────────┘  └──────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SERVICES LAYER                               │
│      ┌──────────────────────────┐      ┌──────────────────────────┐         │
│      │     🧠 OpenAI Agent      │      │    💾 Database Agent     │         │
│      │                          │      │                          │         │
│      │  • Job Analysis (NLP)    │      │  • PostgreSQL (Prod)     │         │
│      │  • Project Generation    │      │  • SQLite (Dev)          │         │
│      │  • CV Evaluation         │      │  • ORM Management        │         │
│      │  • Submission Scoring    │      │  • Session Handling      │         │
│      │                          │      │                          │         │
│      │  [Azure OpenAI GPT-4o]   │      │  [SQLAlchemy 2.x]        │         │
│      └──────────────────────────┘      └──────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

| Agent | Role | Key Functions |
|-------|------|---------------|
| **Jobs Agent** | Job management & orchestration | Create jobs, generate assessments, retrieve rankings |
| **Candidates Agent** | Applicant lifecycle management | Registration, CV processing, report generation |
| **Submissions Agent** | Project submission handling | Accept work, trigger evaluations, track progress |
| **Project Service** | Business logic orchestration | Coordinate job creation workflow |
| **Evaluation Service** | Assessment intelligence | Score CVs, evaluate submissions, rank candidates |
| **PDF Service** | Document generation | Create professional reports and guides |
| **OpenAI Agent** | AI capabilities | NLP analysis, content generation, scoring |

---

## 🔄 Development Process

This project follows **enterprise development practices** used at leading tech companies:

### 1️⃣ Analysis & Design Phase

```
📋 Requirements Analysis
    ├── Stakeholder interviews (HR, Hiring Managers)
    ├── Pain point identification
    ├── Success metrics definition
    └── Technical feasibility study

🏗️ System Design
    ├── Multi-agent architecture pattern
    ├── API-first design approach
    ├── Database schema modeling
    └── Integration planning (Azure OpenAI)
```

### 2️⃣ Development Phase

```
💻 Implementation
    ├── FastAPI application structure
    ├── SQLAlchemy ORM models
    ├── Service layer (business logic)
    ├── AI integration (Azure OpenAI)
    └── PDF generation engine

✅ Quality Assurance
    ├── Unit testing
    ├── Integration testing
    ├── API endpoint validation
    └── Code review & refactoring
```

### 3️⃣ Deployment Phase

```
🚀 CI/CD Pipeline
    ├── GitHub Actions workflows
    ├── Docker containerization
    ├── Azure Container Registry
    └── Azure App Service deployment

📊 Monitoring
    ├── Application logging
    ├── Health check endpoints
    ├── Error tracking
    └── Performance monitoring
```

---

## 📊 Scoring Algorithm

ARYA uses a **weighted scoring algorithm** for objective candidate ranking:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CANDIDATE FINAL SCORE                         │
│                                                                  │
│    Final Score = (CV Score × 0.30) + (Avg Project Score × 0.70) │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    CV Evaluation (30%)           Project Submissions (70%)       │
│    ├── Skills Match              ├── Technical Score            │
│    ├── Experience Fit            ├── Problem-Solving Score      │
│    ├── Industry Relevance        ├── Communication Score        │
│    └── Overall Assessment        └── Cultural Fit Score         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Performance Levels

| Score Range | Level | Recommendation |
|-------------|-------|----------------|
| **90-100** | 🏆 Outstanding | Strong recommend for immediate hire |
| **80-89** | ⭐ Excellent | Recommend for hire |
| **70-79** | ✅ Good | Consider with development potential |
| **60-69** | ⚠️ Fair | Proceed with caution |
| **< 60** | ❌ Below Expectations | Not recommended |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (production) or SQLite (development)
- Azure OpenAI API access

### Installation

```bash
# Clone the repository
git clone https://github.com/mohamedamineelabidi/Multiagent-Recruitment.git
cd Multiagent-Recruitment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run the application
uvicorn app.main:app --reload
```

### Docker Deployment

```bash
# Build image
docker build -t arya-api .

# Run container
docker run -p 8000:8000 --env-file .env arya-api
```

---

## 📚 API Reference

### Jobs Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/jobs` | Create job with AI-generated assessment |
| `GET` | `/api/v1/jobs/{id}` | Retrieve job details |
| `GET` | `/api/v1/jobs/{id}/reference-guide` | Download evaluator PDF guide |
| `GET` | `/api/v1/jobs/{id}/rankings` | Get ranked candidate list |

### Candidates Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/jobs/{id}/candidates` | Register new candidate |
| `POST` | `/api/v1/candidates/{id}/cv` | Upload & evaluate CV (PDF) |
| `GET` | `/api/v1/candidates/{id}/report` | Download evaluation report |

### Submissions Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/candidates/{id}/submissions` | Submit project phase work |
| `GET` | `/api/v1/candidates/{id}/submissions` | Get all submissions |
| `GET` | `/api/v1/candidates/{id}/submissions/{phase}` | Get specific phase details |

---

## 🛠️ Technology Stack

<table>
<tr>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=python" width="48" height="48" alt="Python" />
<br>Python
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=fastapi" width="48" height="48" alt="FastAPI" />
<br>FastAPI
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=postgres" width="48" height="48" alt="PostgreSQL" />
<br>PostgreSQL
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=docker" width="48" height="48" alt="Docker" />
<br>Docker
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=azure" width="48" height="48" alt="Azure" />
<br>Azure
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=github" width="48" height="48" alt="GitHub" />
<br>GitHub
</td>
</tr>
</table>

| Category | Technology | Purpose |
|----------|------------|---------|
| **Framework** | FastAPI | High-performance async API |
| **ORM** | SQLAlchemy 2.x | Database abstraction |
| **Validation** | Pydantic v2 | Request/response validation |
| **AI** | Azure OpenAI (GPT-4o) | NLP & content generation |
| **Database** | PostgreSQL | Production data storage |
| **PDF** | FPDF + PyPDF2 | Document generation & parsing |
| **Container** | Docker | Application containerization |
| **Cloud** | Azure App Service | Production hosting |
| **CI/CD** | GitHub Actions | Automated testing & deployment |

---

## 📁 Project Structure

```
Multiagent-Recruitment/
├── 📂 app/
│   ├── 📂 api/v1/
│   │   ├── 📂 endpoints/          # API route handlers
│   │   │   ├── jobs.py            # Jobs endpoints
│   │   │   ├── candidates.py      # Candidates endpoints
│   │   │   └── submissions.py     # Submissions endpoints
│   │   └── schemas.py             # Pydantic models
│   ├── 📂 core/
│   │   ├── config.py              # Configuration management
│   │   └── db.py                  # Database setup
│   ├── 📂 models/                 # SQLAlchemy models
│   │   ├── job.py
│   │   ├── candidate.py
│   │   ├── project.py
│   │   └── submission.py
│   ├── 📂 services/               # Business logic layer
│   │   ├── openai_service.py      # AI integration
│   │   ├── project_service.py     # Job orchestration
│   │   ├── evaluation_service.py  # Assessment logic
│   │   └── pdf_service.py         # Document generation
│   └── main.py                    # Application entry point
├── 📂 docs/                       # Documentation
├── 📂 scripts/                    # Deployment scripts
├── 📂 .github/                    # GitHub templates & workflows
├── Dockerfile                     # Container definition
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [📘 Architecture Analysis](docs/SYSTEM_ARCHITECTURE_ANALYSIS.md) | Complete system design documentation |
| [🚀 Deployment Guide](DEPLOYMENT.md) | Azure deployment instructions |
| [🤝 Contributing Guide](CONTRIBUTING.md) | How to contribute |
| [📋 Changelog](CHANGELOG.md) | Version history |
| [🔒 Security Policy](SECURITY.md) | Security guidelines |

---

## 🤝 Contributing

Contributions are welcome! This project follows enterprise contribution standards.

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### 🌟 Star this repo if you find it useful!

Built with ❤️ by [Mohamed Amine Elabidi](https://github.com/mohamedamineelabidi)

[![GitHub stars](https://img.shields.io/github/stars/mohamedamineelabidi/Multiagent-Recruitment?style=social)](https://github.com/mohamedamineelabidi/Multiagent-Recruitment)
[![GitHub forks](https://img.shields.io/github/forks/mohamedamineelabidi/Multiagent-Recruitment?style=social)](https://github.com/mohamedamineelabidi/Multiagent-Recruitment)

</div>
