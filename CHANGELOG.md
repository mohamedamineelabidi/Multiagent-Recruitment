# Changelog

All notable changes to the ARYA API project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Authentication and authorization system
- Rate limiting middleware
- Batch candidate import
- Webhook notifications
- Admin dashboard API

---

## [1.0.0] - 2026-02-03

### Added
- 🚀 Initial public release of ARYA API
- **Multi-Agent Architecture**: 7 specialized agents for recruitment workflow
  - Jobs Agent: Job posting and assessment management
  - Candidates Agent: Candidate registration and CV processing
  - Submissions Agent: Project phase submission handling
  - Project Service Agent: Job/project orchestration
  - Evaluation Service Agent: AI-powered assessment and ranking
  - PDF Service Agent: Document generation
  - OpenAI Agent: Azure OpenAI integration for AI capabilities

- **API Endpoints**:
  - `POST /api/v1/jobs` - Create job with AI-generated assessment
  - `GET /api/v1/jobs/{id}` - Get job details
  - `GET /api/v1/jobs/{id}/reference-guide` - Download PDF reference guide
  - `GET /api/v1/jobs/{id}/rankings` - Get candidate rankings
  - `POST /api/v1/jobs/{id}/candidates` - Register candidate
  - `POST /api/v1/candidates/{id}/cv` - Upload and evaluate CV
  - `GET /api/v1/candidates/{id}/report` - Download candidate report
  - `POST /api/v1/candidates/{id}/submissions` - Submit phase work
  - `GET /api/v1/candidates/{id}/submissions` - Get all submissions
  - `GET /api/v1/candidates/{id}/submissions/{phase}` - Get phase details

- **AI Features**:
  - Intelligent job description parsing
  - AI-resistant 3-phase project generation
  - Automated CV evaluation and scoring
  - Submission assessment with detailed feedback
  - Weighted candidate ranking algorithm

- **Database**:
  - PostgreSQL support for production
  - SQLite support for development
  - SQLAlchemy ORM with relationship management
  - 4 core entities: Jobs, Projects, Candidates, Submissions

- **Document Generation**:
  - PDF candidate evaluation reports
  - PDF reference guides for evaluators
  - Unicode text handling and sanitization

- **Azure Integration**:
  - Azure OpenAI (GPT-4o) for AI processing
  - Azure Container Registry for Docker images
  - Azure App Service deployment
  - Comprehensive deployment documentation

- **Developer Experience**:
  - FastAPI with automatic OpenAPI documentation
  - Pydantic models for request/response validation
  - Comprehensive logging
  - Docker containerization
  - Environment-based configuration

### Technical Stack
- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- Pydantic 2.x
- Azure OpenAI SDK
- PyPDF2 & FPDF
- Docker
- PostgreSQL

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2026-02-03 | Initial public release |

---

## Upgrade Guide

### From Pre-release to 1.0.0

If you were using a pre-release version:

1. Update your environment variables to use Azure OpenAI format
2. Migrate database schema (backup first!)
3. Update API client calls to use new response formats

---

## Links

- [Documentation](./README.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Architecture Analysis](./docs/SYSTEM_ARCHITECTURE_ANALYSIS.md)
- [Contributing Guidelines](./CONTRIBUTING.md)
