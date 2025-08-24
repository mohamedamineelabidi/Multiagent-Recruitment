# Azure Deployment Template for Future Projects

This guide provides a step-by-step template for deploying containerized applications (FastAPI, Node.js, etc.) to Azure using Azure Container Registry and App Service.

## 🎯 Prerequisites

### Tools Required
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (optional, for local builds)
- [Git](https://git-scm.com/)
- PowerShell (Windows) or Bash (Linux/Mac)

### Azure Resources Needed
- Azure Subscription
- Resource Group
- Azure Container Registry (ACR)
- Azure App Service Plan
- Azure Web App

## 📋 Project Preparation Checklist

Before starting deployment, ensure your project has:

### 1. Dockerfile
Create a `Dockerfile` in your project root:

```dockerfile
# Example for FastAPI project
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (adjust as needed)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start command (adjust for your app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Environment Variables Configuration
Create `.env.example` with all required environment variables:

```bash
# Database
DATABASE_URL=postgresql://username:password@host:5432/database?sslmode=require

# API Keys
API_KEY=your-api-key-here
SECRET_KEY=your-secret-key

# External Services
EXTERNAL_SERVICE_URL=https://api.example.com
EXTERNAL_SERVICE_KEY=your-service-key

# App Configuration
DEBUG=false
LOG_LEVEL=info
```

### 3. Application Configuration
Ensure your app:
- Reads environment variables for configuration
- Has health check endpoints (optional but recommended)
- Handles graceful shutdown
- Uses proper logging

## 🚀 Step-by-Step Deployment Process

### Step 1: Project Variables Setup

```powershell
# Define your project variables
$PROJECT_NAME = "your-project-name"
$RESOURCE_GROUP = "$PROJECT_NAME-rg"
$LOCATION = "eastus"  # or your preferred location
$ACR_NAME = "${PROJECT_NAME}registry"  # must be unique globally
$IMAGE_NAME = "$PROJECT_NAME-api"
$IMAGE_TAG = "latest"
$APP_PLAN = "$PROJECT_NAME-plan"
$WEBAPP_NAME = "$PROJECT_NAME-app"  # must be unique globally

# Display configuration
Write-Host "=== Deployment Configuration ===" -ForegroundColor Green
Write-Host "Project: $PROJECT_NAME"
Write-Host "Resource Group: $RESOURCE_GROUP"
Write-Host "Location: $LOCATION"
Write-Host "ACR: $ACR_NAME"
Write-Host "Web App: $WEBAPP_NAME"
```

### Step 2: Azure Login and Resource Group

```powershell
# Login to Azure
az login

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION
```

### Step 3: Create Azure Container Registry

```powershell
# Create ACR
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

# Enable admin access
az acr update --name $ACR_NAME --admin-enabled true

# Get login server
$ACR_LOGIN_SERVER = az acr show --name $ACR_NAME --query loginServer -o tsv
Write-Host "ACR Login Server: $ACR_LOGIN_SERVER"
```

### Step 4: Build and Push Docker Image

**Option A: Remote Build (Recommended)**
```powershell
# Build image remotely in ACR
az acr build --registry $ACR_NAME --image "$IMAGE_NAME`:$IMAGE_TAG" .
```

**Option B: Local Build**
```powershell
# Build image locally
docker build -t "$ACR_LOGIN_SERVER/$IMAGE_NAME`:$IMAGE_TAG" .

# Login to ACR
$ACR_USER = az acr credential show --name $ACR_NAME --query username -o tsv
$ACR_PASS = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv
docker login $ACR_LOGIN_SERVER --username $ACR_USER --password $ACR_PASS

# Push image
docker push "$ACR_LOGIN_SERVER/$IMAGE_NAME`:$IMAGE_TAG"
```

### Step 5: Create App Service Plan

```powershell
# Create App Service Plan (Linux)
az appservice plan create --name $APP_PLAN --resource-group $RESOURCE_GROUP --sku B1 --is-linux
```

### Step 6: Create Web App

```powershell
# Create Web App with container
az webapp create --resource-group $RESOURCE_GROUP --plan $APP_PLAN --name $WEBAPP_NAME --deployment-container-image-name "$ACR_LOGIN_SERVER/$IMAGE_NAME`:$IMAGE_TAG"
```

### Step 7: Configure Container Access

```powershell
# Get ACR credentials
$ACR_USER = az acr credential show --name $ACR_NAME --query username -o tsv
$ACR_PASS = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv

# Configure container settings
az webapp config container set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --docker-custom-image-name "$ACR_LOGIN_SERVER/$IMAGE_NAME`:$IMAGE_TAG" --docker-registry-server-url "https://$ACR_LOGIN_SERVER" --docker-registry-server-user $ACR_USER --docker-registry-server-password $ACR_PASS
```

### Step 8: Configure App Settings

```powershell
# Set the port (adjust based on your app)
az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --settings WEBSITES_PORT=8000

# Set your environment variables (replace with actual values)
az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --settings `
  DATABASE_URL="your-database-connection-string" `
  API_KEY="your-api-key" `
  SECRET_KEY="your-secret-key" `
  EXTERNAL_SERVICE_URL="your-service-url" `
  EXTERNAL_SERVICE_KEY="your-service-key"
```

### Step 9: Enable Production Settings

```powershell
# Enable Always On
az webapp config set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --always-on true

# Enable container logging
az webapp log config --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --docker-container-logging filesystem

# Optional: Set health check path
az webapp config set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --health-check-path "/"
```

### Step 10: Test Deployment

```powershell
# Restart app
az webapp restart --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

# Open in browser
az webapp browse --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

# Check logs
az webapp log tail --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP
```

## 🔧 Create Reusable Scripts

### 1. Deployment Script Template

Create `deploy.ps1`:

```powershell
param(
    [string]$ProjectName,
    [string]$Location = "eastus",
    [string]$ImageTag = "latest"
)

# Validate parameters
if ([string]::IsNullOrEmpty($ProjectName)) {
    Write-Host "Error: ProjectName is required" -ForegroundColor Red
    Write-Host "Usage: .\deploy.ps1 -ProjectName 'my-project'"
    exit 1
}

# Set variables
$RESOURCE_GROUP = "$ProjectName-rg"
$ACR_NAME = "${ProjectName}registry"
$IMAGE_NAME = "$ProjectName-api"
$APP_PLAN = "$ProjectName-plan"
$WEBAPP_NAME = "$ProjectName-app"

Write-Host "Starting deployment for: $ProjectName" -ForegroundColor Green

# Add your deployment steps here...
# (Copy from the steps above)

Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host "App URL: https://$WEBAPP_NAME.azurewebsites.net"
```

### 2. Environment Management Script Template

Create `manage-env.ps1`:

```powershell
param(
    [string]$WebAppName,
    [string]$ResourceGroup,
    [hashtable]$Settings,
    [switch]$ShowCurrent
)

if ($ShowCurrent) {
    az webapp config appsettings list --name $WebAppName --resource-group $ResourceGroup
    return
}

if ($Settings) {
    foreach ($key in $Settings.Keys) {
        Write-Host "Setting $key..." -ForegroundColor Yellow
        az webapp config appsettings set --name $WebAppName --resource-group $ResourceGroup --settings "$key=$($Settings[$key])"
    }
    
    Write-Host "Restarting app..." -ForegroundColor Yellow
    az webapp restart --name $WebAppName --resource-group $ResourceGroup
}
```

### 3. Update/Redeploy Script Template

Create `update.ps1`:

```powershell
param(
    [string]$ProjectName,
    [string]$ImageTag = "latest"
)

$ACR_NAME = "${ProjectName}registry"
$IMAGE_NAME = "$ProjectName-api"
$WEBAPP_NAME = "$ProjectName-app"
$RESOURCE_GROUP = "$ProjectName-rg"

Write-Host "Building new image..." -ForegroundColor Cyan
az acr build --registry $ACR_NAME --image "$IMAGE_NAME`:$ImageTag" .

Write-Host "Updating web app..." -ForegroundColor Cyan
$ACR_LOGIN_SERVER = az acr show --name $ACR_NAME --query loginServer -o tsv
az webapp config container set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --docker-custom-image-name "$ACR_LOGIN_SERVER/$IMAGE_NAME`:$ImageTag"

Write-Host "Restarting app..." -ForegroundColor Cyan
az webapp restart --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

Write-Host "Update completed!" -ForegroundColor Green
```

## 📁 Project Structure Template

For future projects, use this structure:

```
your-project/
├── app/                    # Application code
├── scripts/               # Deployment scripts
│   ├── deploy.ps1        # Main deployment script
│   ├── manage-env.ps1    # Environment management
│   └── update.ps1        # Update/redeploy script
├── docs/                 # Documentation
│   └── DEPLOYMENT.md     # Deployment guide
├── Dockerfile           # Container definition
├── requirements.txt     # Dependencies
├── .env.example        # Environment variables template
├── .gitignore         # Git ignore file
└── README.md          # Project documentation
```

## 🔄 Common Deployment Patterns

### Pattern 1: Simple Web API
- Single container
- Database connection
- Environment variables for configuration
- Health check endpoint

### Pattern 2: Microservices
- Multiple containers
- Service-to-service communication
- Shared database or separate databases
- API Gateway (optional)

### Pattern 3: Full-Stack Application
- Frontend container (React, Vue, Angular)
- Backend API container
- Database
- Static file storage (Azure Storage)

## 🛠️ Customization Points

### For Different Frameworks

**Node.js/Express:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

**Python/Django:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**ASP.NET Core:**
```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:7.0
WORKDIR /app
COPY . .
EXPOSE 80
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

### For Different Databases

**MongoDB:**
```bash
MONGODB_CONNECTION_STRING=mongodb://username:password@host:27017/database
```

**MySQL:**
```bash
MYSQL_CONNECTION_STRING=mysql://username:password@host:3306/database
```

**Redis:**
```bash
REDIS_URL=redis://host:6379
```

## 📋 Deployment Checklist

- [ ] Dockerfile created and tested locally
- [ ] Environment variables documented in .env.example
- [ ] Application reads configuration from environment
- [ ] Health check endpoint implemented (optional)
- [ ] Logging configured
- [ ] Security considerations addressed
- [ ] Database migrations handled
- [ ] Secrets properly managed
- [ ] Monitoring and alerting planned
- [ ] Backup strategy defined

## 🔒 Security Best Practices

1. **Use Managed Identity** instead of admin credentials when possible
2. **Store secrets in Azure Key Vault** for production
3. **Enable HTTPS only** for web apps
4. **Implement proper authentication** and authorization
5. **Use least privilege** for service connections
6. **Regular security updates** for base images
7. **Network security** with Virtual Networks (for production)

## 📊 Monitoring and Maintenance

### Essential Monitoring
- Application logs
- Container health
- Resource usage (CPU, Memory)
- Response times
- Error rates

### Regular Maintenance
- Update base images
- Rotate secrets/keys
- Monitor costs
- Review security settings
- Update dependencies

## 🆘 Troubleshooting Template

Create a troubleshooting section in your deployment docs:

### Common Issues
1. **Container won't start** - Check environment variables and logs
2. **Database connection fails** - Verify connection string and firewall rules
3. **404 errors** - Check port configuration (WEBSITES_PORT)
4. **Slow startup** - Review container size and startup time

### Debug Commands
```bash
# View logs
az webapp log tail --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

# Check app settings
az webapp config appsettings list --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

# Restart app
az webapp restart --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP
```

This template provides a complete foundation for deploying any containerized application to Azure. Customize it based on your specific technology stack and requirements!
