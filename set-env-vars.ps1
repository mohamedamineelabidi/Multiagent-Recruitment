# Environment Variables Setup Script for Azure Web App
# Run this script after updating the values below

# === UPDATE THESE VALUES ===
$DATABASE_URL = "postgresql://<username>:<password>@<host>:5432/<database>?sslmode=require"
$AZURE_OPENAI_API_KEY = "<your-azure-openai-api-key>"
$AZURE_OPENAI_API_BASE = "https://<your-resource-name>.openai.azure.com/"
$AZURE_OPENAI_API_VERSION = "2025-01-01-preview"
$AZURE_OPENAI_DEPLOYMENT_NAME = "<your-deployment-name>"

# === AZURE DEPLOYMENT VARIABLES ===
$RESOURCE_GROUP = "Arya-v2-recruitment-API"
$WEBAPP_NAME = "arya-recruitment-api-v2"

Write-Host "Setting environment variables for $WEBAPP_NAME..." -ForegroundColor Cyan

# Set all environment variables at once
az webapp config appsettings set `
  --name $WEBAPP_NAME `
  --resource-group $RESOURCE_GROUP `
  --settings `
  DATABASE_URL="$DATABASE_URL" `
  AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" `
  AZURE_OPENAI_API_BASE="$AZURE_OPENAI_API_BASE" `
  AZURE_OPENAI_API_VERSION="$AZURE_OPENAI_API_VERSION" `
  AZURE_OPENAI_DEPLOYMENT_NAME="$AZURE_OPENAI_DEPLOYMENT_NAME"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Environment variables set successfully!" -ForegroundColor Green
    Write-Host "`n🔄 Restarting web app..." -ForegroundColor Cyan
    az webapp restart --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP
    
    Write-Host "`n🌐 Your API is now ready:" -ForegroundColor Green
    Write-Host "Main URL: https://$WEBAPP_NAME.azurewebsites.net" -ForegroundColor Yellow
    Write-Host "Swagger UI: https://$WEBAPP_NAME.azurewebsites.net/docs" -ForegroundColor Yellow
    
    Write-Host "`n📋 To view logs:" -ForegroundColor Cyan
    Write-Host "az webapp log tail --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP" -ForegroundColor Gray
} else {
    Write-Host "`n❌ Failed to set environment variables. Please check your values." -ForegroundColor Red
}
