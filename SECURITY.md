# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in ARYA API, please follow these steps:

### 1. Do Not Open Public Issues

Please **do not** report security vulnerabilities through public GitHub issues.

### 2. Report Privately

Send a detailed report to the maintainers through one of these methods:

- **GitHub Security Advisory**: Use the "Report a vulnerability" button in the Security tab
- **Email**: Contact the repository owner directly through GitHub

### 3. Include Details

Your report should include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 4. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 5 business days
- **Fix Timeline**: Depends on severity

### 5. Disclosure

- We will work with you to understand and resolve the issue
- We will acknowledge your contribution in the security advisory
- We will release a patch and public disclosure together

## Security Best Practices

When deploying ARYA API:

1. **Environment Variables**: Never commit `.env` files
2. **API Keys**: Rotate Azure OpenAI keys regularly
3. **Database**: Use SSL/TLS for database connections
4. **CORS**: Configure allowed origins for production
5. **Updates**: Keep dependencies updated

Thank you for helping keep ARYA API secure!
