# Azure Web App Environment Variables Update Script
# Author: DevOps Team
# Description: Script to update environment variables for ARYA Recruitment API

param(
    [string]$DatabaseUrl,
    [string]$OpenAIApiKey,
    [string]$OpenAIApiBase,
    [string]$OpenAIApiVersion = "2024-12-01-preview",
    [string]$OpenAIDeploymentName = "gpt-4o",
    [switch]$ShowCurrent,
    [switch]$Help
)

# Configuration
$RESOURCE_GROUP = "Arya-v2-recruitment-API"
$WEBAPP_NAME = "arya-recruitment-api-v2"

function Show-Help {
    Write-Host @"
Azure Web App Environment Variables Update Script

USAGE:
    .\update-env.ps1 [OPTIONS]

OPTIONS:
    -DatabaseUrl <string>           PostgreSQL connection string
    -OpenAIApiKey <string>          Azure OpenAI API key
    -OpenAIApiBase <string>         Azure OpenAI endpoint URL
    -OpenAIApiVersion <string>      API version (default: 2024-12-01-preview)
    -OpenAIDeploymentName <string>  Model deployment name (default: gpt-4o)
    -ShowCurrent                    Display current environment variables
    -Help                           Show this help message

EXAMPLES:
    # Update database URL only
    .\update-env.ps1 -DatabaseUrl "postgresql://user:pass@host:5432/db?sslmode=require"
    
    # Update Azure OpenAI settings
    .\update-env.ps1 -OpenAIApiKey "your-key" -OpenAIApiBase "https://your-resource.cognitiveservices.azure.com/"
    
    # Update all variables
    .\update-env.ps1 -DatabaseUrl "postgresql://..." -OpenAIApiKey "key" -OpenAIApiBase "https://..."
    
    # Show current variables
    .\update-env.ps1 -ShowCurrent

NOTES:
    - Special characters in passwords should be URL-encoded (& becomes %26)
    - The application will automatically restart after updates
    - All changes are applied immediately
"@
}

function Show-CurrentSettings {
    Write-Host "`n🔍 Current Environment Variables:" -ForegroundColor Cyan
    Write-Host "Retrieving settings from Azure..." -ForegroundColor Yellow
    
    try {
        $settings = az webapp config appsettings list --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP | ConvertFrom-Json
        
        $envVars = @(
            "DATABASE_URL",
            "AZURE_OPENAI_API_KEY", 
            "AZURE_OPENAI_API_BASE",
            "AZURE_OPENAI_API_VERSION",
            "AZURE_OPENAI_DEPLOYMENT_NAME",
            "WEBSITES_PORT"
        )
        
        foreach ($var in $envVars) {
            $setting = $settings | Where-Object { $_.name -eq $var }
            if ($setting) {
                if ($var -like "*KEY*" -or $var -like "*URL*") {
                    Write-Host "✅ $var = [REDACTED]" -ForegroundColor Green
                } else {
                    Write-Host "✅ $var = $($setting.value)" -ForegroundColor Green
                }
            } else {
                Write-Host "❌ $var = [NOT SET]" -ForegroundColor Red
            }
        }
    }
    catch {
        Write-Host "❌ Error retrieving settings: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Update-EnvironmentVariable {
    param(
        [string]$Name,
        [string]$Value
    )
    
    if ([string]::IsNullOrEmpty($Value)) {
        return
    }
    
    Write-Host "Updating $Name..." -ForegroundColor Yellow
    
    try {
        az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --settings "$Name=$Value" | Out-Null
        Write-Host "✅ $Name updated successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to update $Name : $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Test-AzureLogin {
    try {
        $account = az account show | ConvertFrom-Json
        Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Not logged in to Azure. Please run 'az login' first." -ForegroundColor Red
        return $false
    }
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

Write-Host "`n🚀 Azure Web App Environment Variables Manager" -ForegroundColor Cyan
Write-Host "Target: $WEBAPP_NAME in $RESOURCE_GROUP" -ForegroundColor White

# Check Azure login
if (-not (Test-AzureLogin)) {
    exit 1
}

if ($ShowCurrent) {
    Show-CurrentSettings
    exit 0
}

# Check if any updates are requested
$hasUpdates = $DatabaseUrl -or $OpenAIApiKey -or $OpenAIApiBase -or $OpenAIApiVersion -or $OpenAIDeploymentName

if (-not $hasUpdates) {
    Write-Host "`n⚠️  No updates specified. Use -Help for usage information." -ForegroundColor Yellow
    Show-CurrentSettings
    exit 0
}

Write-Host "`n🔧 Updating Environment Variables..." -ForegroundColor Cyan

# Update variables
Update-EnvironmentVariable -Name "DATABASE_URL" -Value $DatabaseUrl
Update-EnvironmentVariable -Name "AZURE_OPENAI_API_KEY" -Value $OpenAIApiKey
Update-EnvironmentVariable -Name "AZURE_OPENAI_API_BASE" -Value $OpenAIApiBase
Update-EnvironmentVariable -Name "AZURE_OPENAI_API_VERSION" -Value $OpenAIApiVersion
Update-EnvironmentVariable -Name "AZURE_OPENAI_DEPLOYMENT_NAME" -Value $OpenAIDeploymentName

# Restart application
Write-Host "`n🔄 Restarting application..." -ForegroundColor Cyan
try {
    az webapp restart --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP | Out-Null
    Write-Host "✅ Application restarted successfully" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to restart application: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 Environment variables updated successfully!" -ForegroundColor Green
Write-Host "🌐 API URL: https://$WEBAPP_NAME.azurewebsites.net" -ForegroundColor Yellow
Write-Host "📚 Swagger: https://$WEBAPP_NAME.azurewebsites.net/docs" -ForegroundColor Yellow

Write-Host "`n💡 Tip: Use -ShowCurrent to verify the changes" -ForegroundColor Cyan
