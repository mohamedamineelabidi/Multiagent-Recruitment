# Azure Deployment Guide - ARYA Recruitment API

## 🚀 Deployment Overview

This document provides step-by-step instructions for deploying the ARYA Recruitment API to Azure using Azure Container Registry (ACR) and Azure App Service.

## 📋 Deployed Resources

- **Resource Group**: `Arya-v2-recruitment-API`
- **Azure Container Registry**: `aryaregistryv2.azurecr.io`
- **App Service Plan**: `recruitment-plan` (Basic B1, Linux)
- **Web App**: `arya-recruitment-api-v2`
- **Location**: France Central

## 🌐 Live URLs

- **API Base URL**: https://arya-recruitment-api-v2.azurewebsites.net
- **Swagger UI**: https://arya-recruitment-api-v2.azurewebsites.net/docs
- **API Documentation**: https://arya-recruitment-api-v2.azurewebsites.net/redoc

## 🔧 Environment Variables

The application requires the following environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db?sslmode=require` |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | `your-api-key-here` |
| `AZURE_OPENAI_API_BASE` | Azure OpenAI endpoint URL | `https://your-resource.cognitiveservices.azure.com/` |
| `AZURE_OPENAI_API_VERSION` | API version | `2024-12-01-preview` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Model deployment name | `gpt-4o` |
| `WEBSITES_PORT` | Container port (auto-set) | `8000` |

## 🔄 Managing Environment Variables

### Method 1: Azure Portal (GUI)

1. **Navigate to your Web App**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Search for `arya-recruitment-api-v2`
   - Click on your App Service

2. **Access Configuration**:
   - In the left sidebar, click **Configuration**
   - Click on the **Application settings** tab

3. **Edit Variables**:
   - Click **+ New application setting** to add new variables
   - Click on existing settings to edit them
   - Click **OK** to save changes
   - Click **Save** at the top to apply changes
   - Click **Continue** to confirm restart

4. **Important Notes**:
   - Changes require an app restart
   - The portal will automatically restart the app when you save
   - Use URL encoding for special characters in passwords (e.g., `&` becomes `%26`)

### Method 2: Azure CLI (Command Line)

#### Prerequisites
```bash
# Login to Azure
az login

# Set variables
$RESOURCE_GROUP = "Arya-v2-recruitment-API"
$WEBAPP_NAME = "arya-recruitment-api-v2"
```

#### Update Single Environment Variable
```bash
# Update DATABASE_URL
az webapp config appsettings set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings "DATABASE_URL=your-new-database-url-here"

# Update Azure OpenAI API Key
az webapp config appsettings set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings "AZURE_OPENAI_API_KEY=your-new-api-key"
```

#### Update Multiple Environment Variables
```bash
az webapp config appsettings set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    DATABASE_URL="your-database-url" \
    AZURE_OPENAI_API_KEY="your-api-key" \
    AZURE_OPENAI_API_BASE="your-endpoint-url"
```

#### View Current Settings
```bash
# List all application settings
az webapp config appsettings list \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP

# View specific setting (values are redacted by default)
az webapp config appsettings list \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "[?name=='DATABASE_URL']"
```

#### Restart Application
```bash
# Restart to apply changes
az webapp restart \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP
```

### Method 3: PowerShell Script (Recommended for Bulk Updates)

Create a script file `update-env.ps1`:

```powershell
# Variables
$RESOURCE_GROUP = "Arya-v2-recruitment-API"
$WEBAPP_NAME = "arya-recruitment-api-v2"

# New environment variables
$DATABASE_URL = "postgresql://user:password@host:5432/db?sslmode=require"
$AZURE_OPENAI_API_KEY = "your-new-api-key"
$AZURE_OPENAI_API_BASE = "https://your-resource.cognitiveservices.azure.com/"
$AZURE_OPENAI_API_VERSION = "2024-12-01-preview"
$AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o"

Write-Host "Updating environment variables..." -ForegroundColor Yellow

# Update each variable
az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --settings "DATABASE_URL=$DATABASE_URL"
az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --settings "AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY"
az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --settings "AZURE_OPENAI_API_BASE=$AZURE_OPENAI_API_BASE"
az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --settings "AZURE_OPENAI_API_VERSION=$AZURE_OPENAI_API_VERSION"
az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --settings "AZURE_OPENAI_DEPLOYMENT_NAME=$AZURE_OPENAI_DEPLOYMENT_NAME"

Write-Host "Restarting application..." -ForegroundColor Yellow
az webapp restart --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

Write-Host "Environment variables updated successfully!" -ForegroundColor Green
```

Run the script:
```powershell
.\update-env.ps1
```

## 🔍 Monitoring and Troubleshooting

### View Application Logs
```bash
# Stream live logs
az webapp log tail --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

# Download logs
az webapp log download --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP
```

### Common Issues and Solutions

1. **Application Error on Startup**
   - Check if all required environment variables are set
   - Verify database connectivity
   - Check application logs for specific error messages

2. **Database Connection Issues**
   - Ensure PostgreSQL server allows connections from Azure
   - Verify connection string format
   - Check if password contains special characters (use URL encoding)

3. **Azure OpenAI Issues**
   - Verify API key is valid
   - Check if the deployment name exists
   - Ensure the endpoint URL is correct

### Health Check Endpoints
- **Root**: https://arya-recruitment-api-v2.azurewebsites.net/
- **Health**: https://arya-recruitment-api-v2.azurewebsites.net/health (if implemented)

## 🔄 Redeployment Process

### Update Application Code

1. **Build and Push New Image**:
```bash
# Build new image
az acr build --registry aryaregistryv2 --image recruitment-api:latest .

# Or with specific tag
az acr build --registry aryaregistryv2 --image recruitment-api:v1.1.0 .
```

2. **Update Web App Image**:
```bash
# Update to latest
az webapp config container set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name aryaregistryv2.azurecr.io/recruitment-api:latest

# Or specific version
az webapp config container set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name aryaregistryv2.azurecr.io/recruitment-api:v1.1.0
```

3. **Restart Application**:
```bash
az webapp restart --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP
```

## 📊 Scaling and Performance

### Scale Up (Vertical Scaling)
```bash
# Upgrade to Standard S1
az appservice plan update \
  --name recruitment-plan \
  --resource-group $RESOURCE_GROUP \
  --sku S1
```

### Scale Out (Horizontal Scaling)
```bash
# Scale to 2 instances
az appservice plan update \
  --name recruitment-plan \
  --resource-group $RESOURCE_GROUP \
  --number-of-workers 2
```

## 🔐 Security Best Practices

1. **Environment Variables**:
   - Never commit sensitive values to code
   - Use Azure Key Vault for production secrets
   - Rotate API keys regularly

2. **Database Security**:
   - Use strong passwords
   - Enable SSL connections
   - Restrict network access

3. **Application Security**:
   - Keep dependencies updated
   - Enable HTTPS only
   - Implement proper authentication

## 📝 Maintenance Tasks

### Regular Maintenance
- Monitor application logs
- Update Docker images
- Review and rotate secrets
- Monitor resource usage
- Update dependencies

### Backup Strategy
- Database: Automated backups via Azure Database
- Configuration: Export ARM templates
- Code: Git repository

## 📞 Support and Resources

- **Azure Documentation**: https://docs.microsoft.com/azure/
- **Azure CLI Reference**: https://docs.microsoft.com/cli/azure/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Container Registry**: https://docs.microsoft.com/azure/container-registry/

---

## 📋 Quick Reference Commands

```bash
# Login
az login

# Check app status
az webapp show --name arya-recruitment-api-v2 --resource-group Arya-v2-recruitment-API

# View logs
az webapp log tail --name arya-recruitment-api-v2 --resource-group Arya-v2-recruitment-API

# Restart app
az webapp restart --name arya-recruitment-api-v2 --resource-group Arya-v2-recruitment-API

# Update environment variable
az webapp config appsettings set --name arya-recruitment-api-v2 --resource-group Arya-v2-recruitment-API --settings "VARIABLE_NAME=value"

# Build new image
az acr build --registry aryaregistryv2 --image recruitment-api:latest .
```
