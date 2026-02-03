# Contributing to ARYA API 🤝

First off, thank you for considering contributing to ARYA! It's people like you that make ARYA such a great tool for AI-powered recruitment.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Multiagent-Recruitment.git
   cd Multiagent-Recruitment
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/mohamedamineelabidi/Multiagent-Recruitment.git
   ```

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

When creating a bug report, please include:

- **Clear title** describing the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs **actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Error messages** and stack traces if applicable
- **Screenshots** if relevant

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use case**: Why is this enhancement needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: What other approaches did you consider?
- **Additional context**: Any other information that might help

### 🔧 Pull Requests

1. **Create a branch** for your feature/fix:
   ```bash
   git checkout -b feature/amazing-feature
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes** following our style guidelines

3. **Test your changes** thoroughly

4. **Commit your changes** using our commit message format

5. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request** against the `main` branch

## Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL (for production) or SQLite (for development)
- Azure OpenAI API access

### Local Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Run the application
uvicorn app.main:app --reload
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## Style Guidelines

### Python Code Style

We follow **PEP 8** with some modifications:

- **Line length**: Maximum 100 characters
- **Imports**: Use `isort` for sorting imports
- **Formatting**: Use `black` for code formatting
- **Type hints**: Required for all function signatures
- **Docstrings**: Google style docstrings for all public functions

```python
def example_function(param1: str, param2: int) -> dict:
    """
    Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
    """
    pass
```

### Code Organization

```
app/
├── api/           # API endpoints (thin controllers)
├── core/          # Core configuration and utilities
├── models/        # SQLAlchemy models
└── services/      # Business logic (keep endpoints thin!)
```

### Best Practices

1. **Keep endpoints thin**: Business logic belongs in services
2. **Use dependency injection**: Leverage FastAPI's `Depends()`
3. **Handle errors gracefully**: Use appropriate HTTP status codes
4. **Log appropriately**: Use the logging module, not print statements
5. **Write tests**: Aim for >80% coverage

## Commit Messages

We follow the **Conventional Commits** specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(api): add candidate bulk import endpoint
fix(evaluation): correct CV scoring algorithm edge case
docs(readme): update deployment instructions
refactor(services): extract common validation logic
```

## Pull Request Process

1. **Ensure all tests pass** before submitting
2. **Update documentation** if needed
3. **Add tests** for new functionality
4. **Follow the PR template** (if provided)
5. **Request review** from maintainers
6. **Address feedback** promptly

### PR Checklist

- [ ] Code follows the project's style guidelines
- [ ] Self-review of the code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if applicable)
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No new warnings introduced

## Questions?

Feel free to open an issue with the `question` label or reach out to the maintainers.

---

Thank you for contributing to ARYA! 🎉
