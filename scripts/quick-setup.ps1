# Quick Environment Setup Script for ARYA API
# This script helps you quickly set up environment variables for the Azure deployment

param(
    [switch]$Interactive,
    [switch]$Help
)

function Show-Help {
    Write-Host @"
ARYA API - Quick Environment Setup Script

DESCRIPTION:
    This script helps you set up environment variables for the ARYA API Azure deployment.
    It provides an interactive mode to collect and validate all required values.

USAGE:
    .\quick-setup.ps1 [OPTIONS]

OPTIONS:
    -Interactive    Run in interactive mode (recommended for first-time setup)
    -Help          Show this help message

EXAMPLES:
    # Interactive setup
    .\quick-setup.ps1 -Interactive
    
    # Show help
    .\quick-setup.ps1 -Help

REQUIRED ENVIRONMENT VARIABLES:
    - DATABASE_URL: PostgreSQL connection string
    - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
    - AZURE_OPENAI_API_BASE: Azure OpenAI endpoint URL
    - AZURE_OPENAI_API_VERSION: API version (usually 2024-12-01-preview)
    - AZURE_OPENAI_DEPLOYMENT_NAME: Model deployment name (e.g., gpt-4o)
"@
}

function Get-DatabaseUrl {
    Write-Host "`n📊 Database Configuration" -ForegroundColor Cyan
    Write-Host "Format: postgresql://username:password@host:5432/database?sslmode=require" -ForegroundColor Gray
    
    $username = Read-Host "Database Username"
    $password = Read-Host "Database Password" -AsSecureString
    $passwordText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
    $host = Read-Host "Database Host (e.g., server.postgres.database.azure.com)"
    $database = Read-Host "Database Name"
    
    # URL encode special characters in password
    $encodedPassword = [System.Web.HttpUtility]::UrlEncode($passwordText)
    
    return "postgresql://$username`:$encodedPassword@$host`:5432/$database`?sslmode=require"
}

function Get-AzureOpenAIConfig {
    Write-Host "`n🤖 Azure OpenAI Configuration" -ForegroundColor Cyan
    
    $apiKey = Read-Host "Azure OpenAI API Key" -AsSecureString
    $apiKeyText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey))
    
    $apiBase = Read-Host "Azure OpenAI Endpoint (e.g., https://your-resource.cognitiveservices.azure.com/)"
    if (-not $apiBase.EndsWith("/")) {
        $apiBase += "/"
    }
    
    Write-Host "Common API versions: 2024-12-01-preview, 2024-10-21, 2024-08-01-preview" -ForegroundColor Gray
    $apiVersion = Read-Host "API Version [2024-12-01-preview]"
    if ([string]::IsNullOrEmpty($apiVersion)) {
        $apiVersion = "2024-12-01-preview"
    }
    
    Write-Host "Common deployments: gpt-4o, gpt-4, gpt-35-turbo" -ForegroundColor Gray
    $deploymentName = Read-Host "Deployment Name [gpt-4o]"
    if ([string]::IsNullOrEmpty($deploymentName)) {
        $deploymentName = "gpt-4o"
    }
    
    return @{
        ApiKey = $apiKeyText
        ApiBase = $apiBase
        ApiVersion = $apiVersion
        DeploymentName = $deploymentName
    }
}

function Confirm-Settings {
    param(
        $DatabaseUrl,
        $OpenAIConfig
    )
    
    Write-Host "`n📋 Configuration Summary" -ForegroundColor Cyan
    Write-Host "Database URL: $($DatabaseUrl -replace ':([^:@]+)@', ':[REDACTED]@')" -ForegroundColor White
    Write-Host "OpenAI API Key: [REDACTED]" -ForegroundColor White
    Write-Host "OpenAI Endpoint: $($OpenAIConfig.ApiBase)" -ForegroundColor White
    Write-Host "API Version: $($OpenAIConfig.ApiVersion)" -ForegroundColor White
    Write-Host "Deployment: $($OpenAIConfig.DeploymentName)" -ForegroundColor White
    
    $confirm = Read-Host "`nDo you want to apply these settings? (y/N)"
    return $confirm -eq "y" -or $confirm -eq "Y" -or $confirm -eq "yes"
}

function Test-Prerequisites {
    # Check if Azure CLI is installed
    try {
        az --version | Out-Null
        Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Azure CLI is not installed. Please install it first." -ForegroundColor Red
        Write-Host "Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
        return $false
    }
    
    # Check if logged in to Azure
    try {
        $account = az account show | ConvertFrom-Json
        Write-Host "✅ Logged in to Azure as: $($account.user.name)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Not logged in to Azure. Please run 'az login' first." -ForegroundColor Red
        return $false
    }
    
    # Check if update-env.ps1 exists
    $updateScriptPath = Join-Path $PSScriptRoot "update-env.ps1"
    if (Test-Path $updateScriptPath) {
        Write-Host "✅ Update script found" -ForegroundColor Green
    }
    else {
        Write-Host "❌ update-env.ps1 not found. Please ensure it's in the same directory." -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Load System.Web for URL encoding
Add-Type -AssemblyName System.Web

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

Write-Host "🚀 ARYA API - Quick Environment Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Test prerequisites
Write-Host "`n🔍 Checking prerequisites..." -ForegroundColor Yellow
if (-not (Test-Prerequisites)) {
    Write-Host "`n❌ Prerequisites not met. Please resolve the issues above and try again." -ForegroundColor Red
    exit 1
}

if (-not $Interactive) {
    Write-Host "`n💡 Run with -Interactive flag for guided setup" -ForegroundColor Yellow
    Write-Host "   .\quick-setup.ps1 -Interactive" -ForegroundColor Gray
    exit 0
}

Write-Host "`n🎯 Interactive Setup Mode" -ForegroundColor Green
Write-Host "This will help you configure all required environment variables." -ForegroundColor White

# Collect database configuration
$databaseUrl = Get-DatabaseUrl

# Collect Azure OpenAI configuration
$openAIConfig = Get-AzureOpenAIConfig

# Confirm settings
if (-not (Confirm-Settings -DatabaseUrl $databaseUrl -OpenAIConfig $openAIConfig)) {
    Write-Host "`n❌ Setup cancelled by user." -ForegroundColor Yellow
    exit 0
}

# Apply settings using the update-env.ps1 script
Write-Host "`n🔧 Applying configuration..." -ForegroundColor Cyan

$updateScriptPath = Join-Path $PSScriptRoot "update-env.ps1"
try {
    & $updateScriptPath -DatabaseUrl $databaseUrl -OpenAIApiKey $openAIConfig.ApiKey -OpenAIApiBase $openAIConfig.ApiBase -OpenAIApiVersion $openAIConfig.ApiVersion -OpenAIDeploymentName $openAIConfig.DeploymentName
    
    Write-Host "`n🎉 Setup completed successfully!" -ForegroundColor Green
    Write-Host "Your ARYA API is now configured and ready to use." -ForegroundColor White
    Write-Host "`n🌐 Access your API at:" -ForegroundColor Cyan
    Write-Host "   https://arya-recruitment-api-v2.azurewebsites.net" -ForegroundColor Yellow
    Write-Host "   https://arya-recruitment-api-v2.azurewebsites.net/docs" -ForegroundColor Yellow
}
catch {
    Write-Host "`n❌ Error during setup: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please check the error and try again." -ForegroundColor Yellow
}
