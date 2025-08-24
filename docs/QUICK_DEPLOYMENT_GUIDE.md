# Quick Deployment Reference for Future Projects

This is a quick reference guide for deploying different types of applications to Azure using the deployment template.

## 🚀 Quick Start for Different Project Types

### FastAPI Project
```powershell
# Basic FastAPI deployment
.\scripts\deploy-template.ps1 -ProjectName "my-fastapi" -Port 8000 -EnvironmentVariables @{
    "DATABASE_URL" = "postgresql://user:pass@host:5432/db?sslmode=require"
    "SECRET_KEY" = "your-secret-key"
    "DEBUG" = "false"
}
```

### Node.js/Express Project
```powershell
# Node.js deployment
.\scripts\deploy-template.ps1 -ProjectName "my-nodejs-app" -Port 3000 -EnvironmentVariables @{
    "NODE_ENV" = "production"
    "DATABASE_URL" = "mongodb://user:pass@host:27017/db"
    "JWT_SECRET" = "your-jwt-secret"
}
```

### Django Project
```powershell
# Django deployment
.\scripts\deploy-template.ps1 -ProjectName "my-django-app" -Port 8000 -EnvironmentVariables @{
    "DJANGO_SETTINGS_MODULE" = "myproject.settings.production"
    "DATABASE_URL" = "postgresql://user:pass@host:5432/db"
    "SECRET_KEY" = "your-django-secret"
    "DEBUG" = "False"
}
```

### ASP.NET Core Project
```powershell
# ASP.NET Core deployment
.\scripts\deploy-template.ps1 -ProjectName "my-dotnet-app" -Port 80 -EnvironmentVariables @{
    "ASPNETCORE_ENVIRONMENT" = "Production"
    "ConnectionStrings__DefaultConnection" = "Server=host;Database=db;User=user;Password=pass"
}
```

## 📝 Project Setup Checklist

Before running the deployment script, ensure your project has:

### 1. Dockerfile Requirements

**FastAPI Example:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Node.js Example:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### 2. Environment Configuration

Create `.env.example` with all required variables:
```bash
# Database
DATABASE_URL=postgresql://username:password@host:5432/database

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# External Services
REDIS_URL=redis://host:6379
EMAIL_SERVICE_KEY=your-email-service-key

# Application
DEBUG=false
LOG_LEVEL=info
```

### 3. Application Code Requirements
- Read configuration from environment variables
- Handle graceful shutdown
- Implement health check endpoint (recommended)
- Use proper logging

## 🔧 Common Deployment Patterns

### Pattern 1: Simple API with Database
```powershell
# API + PostgreSQL
.\scripts\deploy-template.ps1 -ProjectName "my-api" -EnvironmentVariables @{
    "DATABASE_URL" = "postgresql://user:pass@host.postgres.database.azure.com:5432/db?sslmode=require"
    "API_KEY" = "your-api-key"
}
```

### Pattern 2: API with Multiple Services
```powershell
# API + Database + Redis + External Service
.\scripts\deploy-template.ps1 -ProjectName "my-complex-api" -EnvironmentVariables @{
    "DATABASE_URL" = "postgresql://user:pass@host:5432/db"
    "REDIS_URL" = "redis://host:6379"
    "EXTERNAL_API_KEY" = "external-service-key"
    "EXTERNAL_API_URL" = "https://api.external-service.com"
    "SECRET_KEY" = "your-secret-key"
}
```

### Pattern 3: Microservice Architecture
Deploy each service separately:
```powershell
# User Service
.\scripts\deploy-template.ps1 -ProjectName "user-service" -EnvironmentVariables @{
    "DATABASE_URL" = "postgresql://user:pass@host:5432/users_db"
    "SERVICE_NAME" = "user-service"
}

# Order Service
.\scripts\deploy-template.ps1 -ProjectName "order-service" -EnvironmentVariables @{
    "DATABASE_URL" = "postgresql://user:pass@host:5432/orders_db"
    "USER_SERVICE_URL" = "https://user-service-123.azurewebsites.net"
    "SERVICE_NAME" = "order-service"
}
```

## 📋 Environment Variables by Technology

### FastAPI Common Variables
```powershell
@{
    "DATABASE_URL" = "postgresql://..."
    "SECRET_KEY" = "your-secret-key"
    "ALGORITHM" = "HS256"
    "ACCESS_TOKEN_EXPIRE_MINUTES" = "30"
    "DEBUG" = "false"
    "CORS_ORIGINS" = "https://your-frontend.com"
}
```

### Node.js/Express Common Variables
```powershell
@{
    "NODE_ENV" = "production"
    "PORT" = "3000"
    "DATABASE_URL" = "mongodb://..."
    "JWT_SECRET" = "your-jwt-secret"
    "SESSION_SECRET" = "your-session-secret"
    "REDIS_URL" = "redis://..."
}
```

### Django Common Variables
```powershell
@{
    "DJANGO_SETTINGS_MODULE" = "myproject.settings.production"
    "SECRET_KEY" = "your-django-secret"
    "DEBUG" = "False"
    "DATABASE_URL" = "postgresql://..."
    "ALLOWED_HOSTS" = "your-domain.azurewebsites.net"
    "STATIC_URL" = "/static/"
}
```

## 🔄 Update and Redeploy

### Update Application Code
```powershell
# Build new image and update app
.\scripts\deploy-template.ps1 -ProjectName "my-app" -ImageTag "v1.1.0"
```

### Update Environment Variables Only
```powershell
# Use the management script from your existing deployment
.\scripts\update-env.ps1 -WebAppName "my-app-123" -ResourceGroup "my-app-rg" -Settings @{
    "NEW_VARIABLE" = "new-value"
    "UPDATED_VARIABLE" = "updated-value"
}
```

### Rolling Back
```powershell
# Deploy previous image version
.\scripts\deploy-template.ps1 -ProjectName "my-app" -ImageTag "v1.0.0" -SkipBuild
```

## 🏗️ Infrastructure as Code (Optional)

For production environments, consider using ARM templates or Bicep:

### Basic ARM Template Structure
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "projectName": {"type": "string"},
        "location": {"type": "string", "defaultValue": "eastus"}
    },
    "resources": [
        // Resource Group, ACR, App Service Plan, Web App
    ]
}
```

## 📊 Monitoring Setup

After deployment, set up monitoring:

### Application Insights
```powershell
# Create Application Insights
az monitor app-insights component create \
  --app my-app-insights \
  --location eastus \
  --resource-group my-app-rg

# Get instrumentation key
$instrumentationKey = az monitor app-insights component show \
  --app my-app-insights \
  --resource-group my-app-rg \
  --query instrumentationKey -o tsv

# Add to app settings
az webapp config appsettings set \
  --name my-app-123 \
  --resource-group my-app-rg \
  --settings "APPINSIGHTS_INSTRUMENTATIONKEY=$instrumentationKey"
```

### Health Checks
Add to your application:

**FastAPI:**
```python
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

**Node.js:**
```javascript
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});
```

## 🔐 Security Best Practices

### 1. Use Managed Identity (Production)
```powershell
# Enable managed identity
az webapp identity assign --name my-app-123 --resource-group my-app-rg

# Grant access to Key Vault
az keyvault set-policy --name my-keyvault \
  --object-id $(az webapp identity show --name my-app-123 --resource-group my-app-rg --query principalId -o tsv) \
  --secret-permissions get list
```

### 2. Store Secrets in Key Vault
```powershell
# Create Key Vault
az keyvault create --name my-app-kv --resource-group my-app-rg --location eastus

# Store secret
az keyvault secret set --vault-name my-app-kv --name "DatabasePassword" --value "your-password"

# Reference in app settings
az webapp config appsettings set \
  --name my-app-123 \
  --resource-group my-app-rg \
  --settings "DATABASE_PASSWORD=@Microsoft.KeyVault(VaultName=my-app-kv;SecretName=DatabasePassword)"
```

## 📞 Support Resources

- **Azure CLI Reference**: https://docs.microsoft.com/cli/azure/
- **App Service Documentation**: https://docs.microsoft.com/azure/app-service/
- **Container Registry**: https://docs.microsoft.com/azure/container-registry/
- **Troubleshooting Guide**: See DEPLOYMENT.md in your project

## 🎯 Next Steps After Deployment

1. **Test Application**: Verify all endpoints work
2. **Configure Custom Domain**: If needed
3. **Set Up SSL Certificate**: For custom domains
4. **Configure Alerts**: For monitoring
5. **Set Up CI/CD**: For automated deployments
6. **Backup Strategy**: For data and configuration
7. **Scaling Plan**: For handling increased load

Use this guide as a starting point and customize based on your specific requirements!
