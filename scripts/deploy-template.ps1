# Azure Deployment Script Template
# Use this script as a starting point for deploying any containerized application to Azure

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,
    
    [string]$Location = "eastus",
    [string]$ImageTag = "latest",
    [string]$AppServiceSku = "B1",
    [hashtable]$EnvironmentVariables = @{},
    [int]$Port = 8000,
    [switch]$SkipBuild,
    [switch]$Help
)

function Show-Help {
    Write-Host @"
Azure Deployment Script Template

USAGE:
    .\deploy-template.ps1 -ProjectName <name> [OPTIONS]

REQUIRED PARAMETERS:
    -ProjectName <string>    Name of your project (used for all Azure resources)

OPTIONAL PARAMETERS:
    -Location <string>       Azure region (default: eastus)
    -ImageTag <string>       Docker image tag (default: latest)
    -AppServiceSku <string>  App Service plan SKU (default: B1)
    -Port <int>             Application port (default: 8000)
    -EnvironmentVariables   Hashtable of environment variables
    -SkipBuild              Skip Docker image build
    -Help                   Show this help

EXAMPLES:
    # Basic deployment
    .\deploy-template.ps1 -ProjectName "my-api"
    
    # With custom location and environment variables
    .\deploy-template.ps1 -ProjectName "my-api" -Location "westeurope" -EnvironmentVariables @{
        "DATABASE_URL" = "postgresql://user:pass@host:5432/db"
        "API_KEY" = "your-api-key"
    }
    
    # Skip build (use existing image)
    .\deploy-template.ps1 -ProjectName "my-api" -SkipBuild

PREREQUISITES:
    - Azure CLI installed and logged in (az login)
    - Dockerfile in current directory
    - Docker Desktop (for local builds, optional if using ACR build)
"@
}

function Test-Prerequisites {
    Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow
    
    # Check Azure CLI
    try {
        az --version | Out-Null
        Write-Host "✅ Azure CLI installed" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Azure CLI not found. Please install it first." -ForegroundColor Red
        return $false
    }
    
    # Check Azure login
    try {
        $account = az account show | ConvertFrom-Json
        Write-Host "✅ Logged in to Azure as: $($account.user.name)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Not logged in to Azure. Run 'az login' first." -ForegroundColor Red
        return $false
    }
    
    # Check Dockerfile
    if (Test-Path "Dockerfile") {
        Write-Host "✅ Dockerfile found" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Dockerfile not found in current directory" -ForegroundColor Red
        return $false
    }
    
    return $true
}

function Get-UniqueResourceName {
    param([string]$BaseName, [string]$Suffix = "")
    
    # Add random suffix to ensure uniqueness
    $randomSuffix = Get-Random -Minimum 100 -Maximum 999
    if ($Suffix) {
        return "$BaseName-$Suffix-$randomSuffix"
    }
    return "$BaseName-$randomSuffix"
}

function Deploy-AzureResources {
    param(
        [string]$ProjectName,
        [string]$Location,
        [string]$ImageTag,
        [string]$AppServiceSku,
        [hashtable]$EnvVars,
        [int]$AppPort,
        [bool]$SkipImageBuild
    )
    
    # Generate resource names
    $resourceGroup = "$ProjectName-rg"
    $acrName = Get-UniqueResourceName $ProjectName "acr"
    $imageName = "$ProjectName-api"
    $appPlan = "$ProjectName-plan"
    $webAppName = Get-UniqueResourceName $ProjectName "app"
    
    Write-Host "`n🚀 Starting deployment for: $ProjectName" -ForegroundColor Cyan
    Write-Host "Resource Group: $resourceGroup" -ForegroundColor White
    Write-Host "ACR Name: $acrName" -ForegroundColor White
    Write-Host "Web App Name: $webAppName" -ForegroundColor White
    Write-Host "Location: $Location" -ForegroundColor White
    
    try {
        # Step 1: Create Resource Group
        Write-Host "`n📁 Creating resource group..." -ForegroundColor Yellow
        az group create --name $resourceGroup --location $Location | Out-Null
        Write-Host "✅ Resource group created" -ForegroundColor Green
        
        # Step 2: Create Azure Container Registry
        Write-Host "`n🏗️  Creating Azure Container Registry..." -ForegroundColor Yellow
        az acr create --resource-group $resourceGroup --name $acrName --sku Basic | Out-Null
        az acr update --name $acrName --admin-enabled true | Out-Null
        
        $acrLoginServer = az acr show --name $acrName --query loginServer -o tsv
        Write-Host "✅ ACR created: $acrLoginServer" -ForegroundColor Green
        
        # Step 3: Build and Push Image
        if (-not $SkipImageBuild) {
            Write-Host "`n🐳 Building Docker image..." -ForegroundColor Yellow
            az acr build --registry $acrName --image "$imageName`:$ImageTag" . | Out-Null
            Write-Host "✅ Image built and pushed" -ForegroundColor Green
        }
        else {
            Write-Host "⏭️  Skipping image build" -ForegroundColor Yellow
        }
        
        # Step 4: Create App Service Plan
        Write-Host "`n📋 Creating App Service Plan..." -ForegroundColor Yellow
        az appservice plan create --name $appPlan --resource-group $resourceGroup --sku $AppServiceSku --is-linux | Out-Null
        Write-Host "✅ App Service Plan created" -ForegroundColor Green
        
        # Step 5: Create Web App
        Write-Host "`n🌐 Creating Web App..." -ForegroundColor Yellow
        az webapp create --resource-group $resourceGroup --plan $appPlan --name $webAppName --deployment-container-image-name "$acrLoginServer/$imageName`:$ImageTag" | Out-Null
        Write-Host "✅ Web App created" -ForegroundColor Green
        
        # Step 6: Configure Container Access
        Write-Host "`n🔐 Configuring container access..." -ForegroundColor Yellow
        $acrUser = az acr credential show --name $acrName --query username -o tsv
        $acrPass = az acr credential show --name $acrName --query "passwords[0].value" -o tsv
        
        az webapp config container set --name $webAppName --resource-group $resourceGroup --docker-custom-image-name "$acrLoginServer/$imageName`:$ImageTag" --docker-registry-server-url "https://$acrLoginServer" --docker-registry-server-user $acrUser --docker-registry-server-password $acrPass | Out-Null
        Write-Host "✅ Container access configured" -ForegroundColor Green
        
        # Step 7: Configure App Settings
        Write-Host "`n⚙️  Configuring app settings..." -ForegroundColor Yellow
        
        # Set port
        az webapp config appsettings set --name $webAppName --resource-group $resourceGroup --settings "WEBSITES_PORT=$AppPort" | Out-Null
        
        # Set custom environment variables
        if ($EnvVars.Count -gt 0) {
            foreach ($key in $EnvVars.Keys) {
                Write-Host "Setting $key..." -ForegroundColor Gray
                az webapp config appsettings set --name $webAppName --resource-group $resourceGroup --settings "$key=$($EnvVars[$key])" | Out-Null
            }
        }
        
        Write-Host "✅ App settings configured" -ForegroundColor Green
        
        # Step 8: Configure Production Settings
        Write-Host "`n🏭 Configuring production settings..." -ForegroundColor Yellow
        az webapp config set --name $webAppName --resource-group $resourceGroup --always-on true | Out-Null
        az webapp log config --name $webAppName --resource-group $resourceGroup --docker-container-logging filesystem | Out-Null
        Write-Host "✅ Production settings configured" -ForegroundColor Green
        
        # Step 9: Restart App
        Write-Host "`n🔄 Restarting application..." -ForegroundColor Yellow
        az webapp restart --name $webAppName --resource-group $resourceGroup | Out-Null
        Write-Host "✅ Application restarted" -ForegroundColor Green
        
        # Success Summary
        Write-Host "`n🎉 Deployment completed successfully!" -ForegroundColor Green
        Write-Host "`n📊 Deployment Summary:" -ForegroundColor Cyan
        Write-Host "  Resource Group: $resourceGroup" -ForegroundColor White
        Write-Host "  Container Registry: $acrLoginServer" -ForegroundColor White
        Write-Host "  Web App URL: https://$webAppName.azurewebsites.net" -ForegroundColor Yellow
        Write-Host "  Image: $acrLoginServer/$imageName`:$ImageTag" -ForegroundColor White
        
        # Save deployment info
        $deploymentInfo = @{
            ProjectName = $ProjectName
            ResourceGroup = $resourceGroup
            ACRName = $acrName
            ACRLoginServer = $acrLoginServer
            WebAppName = $webAppName
            WebAppURL = "https://$webAppName.azurewebsites.net"
            ImageName = "$acrLoginServer/$imageName`:$ImageTag"
            Location = $Location
            DeployedAt = Get-Date
        }
        
        $deploymentInfo | ConvertTo-Json | Out-File "deployment-info.json"
        Write-Host "`n💾 Deployment info saved to deployment-info.json" -ForegroundColor Cyan
        
        return $deploymentInfo
    }
    catch {
        Write-Host "`n❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Check the error above and try again." -ForegroundColor Yellow
        return $null
    }
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

# Validate parameters
if ([string]::IsNullOrEmpty($ProjectName)) {
    Write-Host "❌ ProjectName is required. Use -Help for usage information." -ForegroundColor Red
    exit 1
}

# Validate project name (Azure naming requirements)
if ($ProjectName -notmatch '^[a-zA-Z0-9\-]{3,24}$') {
    Write-Host "❌ ProjectName must be 3-24 characters, alphanumeric and hyphens only." -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Azure Deployment Script" -ForegroundColor Cyan
Write-Host "Project: $ProjectName" -ForegroundColor White

# Check prerequisites
if (-not (Test-Prerequisites)) {
    Write-Host "`n❌ Prerequisites not met. Please resolve issues above." -ForegroundColor Red
    exit 1
}

# Confirm deployment
Write-Host "`n📋 Deployment Configuration:" -ForegroundColor Cyan
Write-Host "  Project: $ProjectName" -ForegroundColor White
Write-Host "  Location: $Location" -ForegroundColor White
Write-Host "  Image Tag: $ImageTag" -ForegroundColor White
Write-Host "  App Service SKU: $AppServiceSku" -ForegroundColor White
Write-Host "  Port: $Port" -ForegroundColor White
Write-Host "  Environment Variables: $($EnvironmentVariables.Count) items" -ForegroundColor White
Write-Host "  Skip Build: $SkipBuild" -ForegroundColor White

$confirm = Read-Host "`nProceed with deployment? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y" -and $confirm -ne "yes") {
    Write-Host "❌ Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

# Start deployment
$result = Deploy-AzureResources -ProjectName $ProjectName -Location $Location -ImageTag $ImageTag -AppServiceSku $AppServiceSku -EnvVars $EnvironmentVariables -AppPort $Port -SkipImageBuild $SkipBuild

if ($result) {
    Write-Host "`n🌐 Test your application:" -ForegroundColor Cyan
    Write-Host "  $($result.WebAppURL)" -ForegroundColor Yellow
    Write-Host "  $($result.WebAppURL)/docs (if FastAPI)" -ForegroundColor Yellow
    
    Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Test your application at the URL above" -ForegroundColor White
    Write-Host "  2. Configure any additional environment variables" -ForegroundColor White
    Write-Host "  3. Set up monitoring and alerts" -ForegroundColor White
    Write-Host "  4. Configure custom domain (if needed)" -ForegroundColor White
}
else {
    Write-Host "`n❌ Deployment failed. Check errors above." -ForegroundColor Red
    exit 1
}
