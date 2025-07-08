# ARYA API Project Structure

This document provides an overview of the project structure and key files.

## 📁 Project Structure

```
arya_api/
├── 📄 README.md                     # Comprehensive documentation
├── 📄 requirements.txt              # Python dependencies
├── 📄 .env                         # Environment variables (not in repo)
├── 📄 .gitignore                   # Git ignore rules
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 📂 app/                         # Main application directory
│   ├── 📄 __init__.py              # Package initialization
│   ├── 📄 main.py                  # FastAPI application entry point
│   ├── 📂 api/                     # API layer
│   │   └── 📂 v1/                  # API version 1
│   │       ├── 📄 __init__.py      
│   │       ├── 📄 schemas.py       # Pydantic schemas for validation
│   │       └── 📂 endpoints/       # API endpoint handlers
│   │           ├── 📄 __init__.py
│   │           ├── 📄 jobs.py      # Job-related endpoints
│   │           ├── 📄 candidates.py # Candidate endpoints
│   │           └── 📄 submissions.py # Submission endpoints
│   ├── 📂 core/                    # Core configuration
│   │   ├── 📄 __init__.py
│   │   ├── 📄 config.py            # Application settings
│   │   └── 📄 db.py                # Database configuration
│   ├── 📂 models/                  # SQLAlchemy database models
│   │   ├── 📄 __init__.py
│   │   ├── 📄 job.py               # Job model
│   │   ├── 📄 candidate.py         # Candidate model
│   │   ├── 📄 project.py           # Project model
│   │   └── 📄 submission.py        # Submission model
│   └── 📂 services/                # Business logic services
│       ├── 📄 __init__.py
│       ├── 📄 project_service.py   # Job and project management
│       ├── 📄 evaluation_service.py # Candidate evaluation logic
│       ├── 📄 openai_service.py    # AI integration service
│       └── 📄 pdf_service.py       # PDF generation service
└── 📂 generated_files/             # Temporary files (git ignored)
    ├── 📄 *.pdf                    # Generated PDF reports
    └── 📄 *.tmp                    # Temporary processing files
```

## 🔧 Key Files Description

### **Core Application Files**
- **`app/main.py`**: FastAPI application setup, middleware, and routing
- **`app/core/config.py`**: Environment variables and application settings
- **`app/core/db.py`**: Database connection and session management

### **API Layer**
- **`app/api/v1/schemas.py`**: Pydantic models for request/response validation
- **`app/api/v1/endpoints/`**: HTTP endpoint handlers for each resource

### **Data Layer**
- **`app/models/`**: SQLAlchemy ORM models for database tables
- **Database**: SQLite for development, PostgreSQL for production

### **Business Logic Layer**
- **`app/services/`**: Core business logic and external service integration
- **`openai_service.py`**: AI-powered evaluation and project generation
- **`evaluation_service.py`**: Candidate assessment and ranking algorithms

### **Configuration Files**
- **`requirements.txt`**: Python package dependencies
- **`.env`**: Environment variables (create from .env.example)
- **`.gitignore`**: Files and directories to exclude from version control

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ValhkoLabs/AI-Recruitment-Yield-Assessment.git
   cd AI-Recruitment-Yield-Assessment
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

## 📚 Documentation

The comprehensive documentation is available in `README.md`, including:
- Complete API documentation
- Architecture and design decisions
- Analysis and conception process
- Deployment guides
- Testing strategies

## 🤝 Contributing

Please refer to the contributing guidelines in the main README.md file.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
