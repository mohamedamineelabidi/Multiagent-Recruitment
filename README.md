# ARYA API 🤖

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![Azure](https://img.shields.io/badge/Azure-OpenAI-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**AI-Powered Recruitment Assessment Platform**

[Live Demo](https://arya-recruitment-api-v2.azurewebsites.net/docs) • [Documentation](#-documentation) • [Getting Started](#-quick-start) • [Contributing](CONTRIBUTING.md)

</div>

---

## 📋 Overview

ARYA (**A**I **R**ecruitment & **Y**ield **A**ssessment) is a sophisticated backend API that revolutionizes the hiring process by leveraging artificial intelligence to:

- 🎯 **Analyze job descriptions** and extract requirements automatically
- 📝 **Generate AI-resistant assessments** with multi-phase projects
- 📄 **Evaluate CVs** against job requirements using NLP
- 📊 **Rank candidates** with weighted scoring algorithms
- 📑 **Generate professional reports** in PDF format

## 🌐 Live Deployment

| Resource | URL |
|----------|-----|
| **API Base URL** | https://arya-recruitment-api-v2.azurewebsites.net |
| **Swagger UI** | https://arya-recruitment-api-v2.azurewebsites.net/docs |
| **ReDoc** | https://arya-recruitment-api-v2.azurewebsites.net/redoc |

## ✨ Key Features

### 🤖 Multi-Agent Architecture
Seven specialized agents working together:
- **Jobs Agent** - Job posting management
- **Candidates Agent** - Candidate registration & CV processing
- **Submissions Agent** - Project submission handling
- **Evaluation Agent** - AI-powered assessment
- **Project Agent** - Assessment generation
- **PDF Agent** - Document generation
- **OpenAI Agent** - Azure OpenAI integration

### 🧠 AI-Powered Capabilities
- Intelligent job requirement extraction
- AI-resistant 3-phase project generation
- Automated CV evaluation and scoring
- Multi-dimensional candidate assessment
- Smart candidate ranking

### 📊 Comprehensive Evaluation
- CV match scoring (0-100)
- Technical competency assessment
- Soft skills evaluation
- Weighted final rankings
- Professional PDF reports

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│           (Web Apps / Mobile / API Consumers)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                    HTTPS (TLS 1.3)
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Jobs Agent  │  │ Candidates  │  │ Submissions │              │
│  │             │  │   Agent     │  │   Agent     │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Project    │  │ Evaluation  │  │    PDF      │              │
│  │  Service    │  │  Service    │  │  Service    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌─────────────────┐   ┌───────────────┐
│ Azure OpenAI  │   │   PostgreSQL    │   │ File System   │
│   (GPT-4o)    │   │    Database     │   │ (PDF Storage) │
└───────────────┘   └─────────────────┘   └───────────────┘
```

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
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# Run the application
uvicorn app.main:app --reload
```

### Docker

```bash
# Build the image
docker build -t arya-api .

# Run the container
docker run -p 8000:8000 --env-file .env arya-api
```

## 📚 API Endpoints

### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/jobs` | Create job with AI assessment |
| `GET` | `/api/v1/jobs/{id}` | Get job details |
| `GET` | `/api/v1/jobs/{id}/reference-guide` | Download PDF guide |
| `GET` | `/api/v1/jobs/{id}/rankings` | Get candidate rankings |

### Candidates

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/jobs/{id}/candidates` | Register candidate |
| `POST` | `/api/v1/candidates/{id}/cv` | Upload & evaluate CV |
| `GET` | `/api/v1/candidates/{id}/report` | Download PDF report |

### Submissions

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/candidates/{id}/submissions` | Submit phase work |
| `GET` | `/api/v1/candidates/{id}/submissions` | Get all submissions |
| `GET` | `/api/v1/candidates/{id}/submissions/{phase}` | Get phase details |

## 🗂️ Project Structure

```
Multiagent-Recruitment/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/      # API route handlers
│   │   │   ├── jobs.py
│   │   │   ├── candidates.py
│   │   │   └── submissions.py
│   │   └── schemas.py      # Pydantic models
│   ├── core/
│   │   ├── config.py       # Configuration
│   │   └── db.py           # Database setup
│   ├── models/             # SQLAlchemy models
│   │   ├── job.py
│   │   ├── candidate.py
│   │   ├── project.py
│   │   └── submission.py
│   ├── services/           # Business logic
│   │   ├── openai_service.py
│   │   ├── project_service.py
│   │   ├── evaluation_service.py
│   │   └── pdf_service.py
│   └── main.py             # FastAPI app
├── docs/                   # Documentation
├── scripts/                # Deployment scripts
├── Dockerfile
├── requirements.txt
└── README.md
```

## ⚙️ Configuration

Create a `.env` file based on `.env.example`:

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require

# Azure OpenAI
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_BASE=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Azure deployment guide |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [Architecture Analysis](docs/SYSTEM_ARCHITECTURE_ANALYSIS.md) | Detailed system architecture |

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| **Framework** | FastAPI |
| **Database** | PostgreSQL / SQLAlchemy |
| **AI** | Azure OpenAI (GPT-4o) |
| **Validation** | Pydantic v2 |
| **PDF** | FPDF / PyPDF2 |
| **Container** | Docker |
| **Cloud** | Microsoft Azure |

## 📊 Scoring Algorithm

Candidates are ranked using a weighted algorithm:

```
Final Score = (CV Score × 0.30) + (Avg Submission Score × 0.70)
```

Performance levels:
- **90-100**: Outstanding - Strong recommend for immediate hire
- **80-89**: Excellent - Recommend for hire
- **70-79**: Good - Consider with potential
- **60-69**: Fair - Proceed with caution
- **< 60**: Below expectations - Not recommended

## 🔒 Security

- HTTPS/TLS encryption for all traffic
- SQL injection prevention via ORM
- Input validation with Pydantic
- Environment-based secrets management
- CORS middleware configuration

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a PR.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Mohamed Amine Elabidi**

- GitHub: [@mohamedamineelabidi](https://github.com/mohamedamineelabidi)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) - AI capabilities
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit

---

<div align="center">

Made with ❤️ using AI-powered development

⭐ Star this repo if you find it helpful!

</div>
