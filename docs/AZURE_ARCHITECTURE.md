# Azure Architecture - ARYA Recruitment Platform

**Version:** 1.0  
**Last Updated:** February 2026  
**Author:** Mohamed Amine Elabidi

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Azure Services](#2-azure-services)
3. [Network Architecture](#3-network-architecture)
4. [Data Flow](#4-data-flow)
5. [Security Architecture](#5-security-architecture)
6. [Cost Estimation](#6-cost-estimation)
7. [Scaling Strategy](#7-scaling-strategy)

---

## 1. Architecture Overview

### High-Level Azure Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    INTERNET                                          │
│                                                                                      │
│                              ┌─────────────────┐                                     │
│                              │   End Users     │                                     │
│                              │  (HR, Candidates)│                                    │
│                              └────────┬────────┘                                     │
└───────────────────────────────────────┼─────────────────────────────────────────────┘
                                        │ HTTPS (443)
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           AZURE CLOUD - FRANCE CENTRAL                               │
│                                                                                      │
│  ┌───────────────────────────────────────────────────────────────────────────────┐  │
│  │                           RESOURCE GROUP: arya-recruitment-rg                  │  │
│  │                                                                                │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │                        COMPUTE SERVICES                                  │  │  │
│  │  │                                                                          │  │  │
│  │  │   ┌─────────────────────────────────────────────────────────────────┐   │  │  │
│  │  │   │              AZURE APP SERVICE PLAN (Linux B1)                  │   │  │  │
│  │  │   │                                                                  │   │  │  │
│  │  │   │   ┌─────────────────────────────────────────────────────────┐   │   │  │  │
│  │  │   │   │           APP SERVICE: arya-recruitment-api-v2          │   │   │  │  │
│  │  │   │   │                                                          │   │   │  │  │
│  │  │   │   │   ┌─────────────────────────────────────────────────┐   │   │   │  │  │
│  │  │   │   │   │              DOCKER CONTAINER                   │   │   │   │  │  │
│  │  │   │   │   │                                                  │   │   │   │  │  │
│  │  │   │   │   │   ┌───────────────────────────────────────┐     │   │   │   │  │  │
│  │  │   │   │   │   │         ARYA FastAPI App              │     │   │   │   │  │  │
│  │  │   │   │   │   │         Python 3.11                   │     │   │   │   │  │  │
│  │  │   │   │   │   │         Uvicorn Server                │     │   │   │   │  │  │
│  │  │   │   │   │   │         Port: 8000                    │     │   │   │   │  │  │
│  │  │   │   │   │   └───────────────────────────────────────┘     │   │   │   │  │  │
│  │  │   │   │   │                                                  │   │   │   │  │  │
│  │  │   │   │   └─────────────────────────────────────────────────┘   │   │   │  │  │
│  │  │   │   │                                                          │   │   │  │  │
│  │  │   │   └─────────────────────────────────────────────────────────┘   │   │  │  │
│  │  │   │                                                                  │   │  │  │
│  │  │   └─────────────────────────────────────────────────────────────────┘   │  │  │
│  │  │                                                                          │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────┘  │  │
│  │                                      │                                         │  │
│  │                    ┌─────────────────┼─────────────────┐                       │  │
│  │                    │                 │                 │                       │  │
│  │                    ▼                 ▼                 ▼                       │  │
│  │  ┌─────────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐  │  │
│  │  │   CONTAINER         │  │    DATABASE      │  │      AI SERVICES         │  │  │
│  │  │   SERVICES          │  │    SERVICES      │  │                          │  │  │
│  │  │                     │  │                  │  │  ┌────────────────────┐  │  │  │
│  │  │ ┌─────────────────┐ │  │ ┌──────────────┐ │  │  │  AZURE OPENAI      │  │  │  │
│  │  │ │ AZURE CONTAINER │ │  │ │ POSTGRESQL   │ │  │  │                    │  │  │  │
│  │  │ │ REGISTRY        │ │  │ │ FLEXIBLE     │ │  │  │  Deployment:       │  │  │  │
│  │  │ │                 │ │  │ │ SERVER       │ │  │  │  gpt-4o            │  │  │  │
│  │  │ │ aryaregistryv2  │ │  │ │              │ │  │  │                    │  │  │  │
│  │  │ │                 │ │  │ │ SKU: B1ms    │ │  │  │  Capabilities:     │  │  │  │
│  │  │ │ Images:         │ │  │ │ Storage: 32GB│ │  │  │  - Job Analysis    │  │  │  │
│  │  │ │ - arya-api:v1   │ │  │ │              │ │  │  │  - CV Evaluation   │  │  │  │
│  │  │ │ - arya-api:v2   │ │  │ │ Database:    │ │  │  │  - Project Gen     │  │  │  │
│  │  │ │ - arya-api:latest│ │  │ │ arya_db     │ │  │  │  - Scoring         │  │  │  │
│  │  │ └─────────────────┘ │  │ └──────────────┘ │  │  └────────────────────┘  │  │  │
│  │  │                     │  │                  │  │                          │  │  │
│  │  └─────────────────────┘  └──────────────────┘  └──────────────────────────┘  │  │
│  │                                                                                │  │
│  └───────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Mermaid Architecture Diagram

```mermaid
graph TB
    subgraph "Internet"
        USERS[End Users<br/>HR Managers, Candidates]
    end

    subgraph "Azure Cloud - France Central"
        subgraph "Resource Group: arya-recruitment-rg"
            subgraph "Compute"
                ASP[App Service Plan<br/>Linux B1]
                APP[App Service<br/>arya-recruitment-api-v2]
            end
            
            subgraph "Container Services"
                ACR[Azure Container Registry<br/>aryaregistryv2]
            end
            
            subgraph "Database"
                PG[(PostgreSQL<br/>Flexible Server<br/>B1ms)]
            end
            
            subgraph "AI Services"
                AOAI[Azure OpenAI<br/>GPT-4o Model]
            end
        end
    end

    USERS -->|HTTPS :443| APP
    ACR -->|Pull Image| APP
    APP -->|TCP :5432| PG
    APP -->|HTTPS API| AOAI
    ASP --- APP
```

---

## 2. Azure Services

### 2.1 Azure App Service

| Property | Value |
|----------|-------|
| **Name** | arya-recruitment-api-v2 |
| **Type** | Web App for Containers |
| **OS** | Linux |
| **Plan** | B1 (Basic) |
| **Region** | France Central |
| **Runtime** | Docker Container |
| **URL** | https://arya-recruitment-api-v2.azurewebsites.net |

**Configuration:**
- Always On: Enabled
- HTTPS Only: Enabled
- Minimum TLS Version: 1.2
- HTTP/2: Enabled

**Environment Variables:**
```
DATABASE_URL=postgresql://user:pass@host:5432/arya_db
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<key>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 2.2 Azure Container Registry

| Property | Value |
|----------|-------|
| **Name** | aryaregistryv2 |
| **SKU** | Basic |
| **Region** | France Central |
| **Admin User** | Enabled |
| **Login Server** | aryaregistryv2.azurecr.io |

**Repositories:**
- `arya-api:latest`
- `arya-api:v1.0`
- `arya-api:v2.0`

### 2.3 Azure Database for PostgreSQL

| Property | Value |
|----------|-------|
| **Type** | Flexible Server |
| **SKU** | Burstable B1ms |
| **vCores** | 1 |
| **Memory** | 2 GB |
| **Storage** | 32 GB |
| **Region** | France Central |
| **PostgreSQL Version** | 14 |
| **Backup Retention** | 7 days |
| **High Availability** | Disabled (Dev/Test) |

**Database Configuration:**
```
Database Name: arya_db
Port: 5432
SSL Mode: Require
Connection Pooling: Enabled
Max Connections: 100
```

### 2.4 Azure OpenAI Service

| Property | Value |
|----------|-------|
| **Resource Name** | arya-openai |
| **Region** | France Central |
| **Model** | GPT-4o |
| **Deployment Name** | gpt-4o |
| **API Version** | 2024-02-15-preview |

**Model Capabilities:**
| Function | Description |
|----------|-------------|
| Job Analysis | Extract skills and requirements from job descriptions |
| Project Generation | Create role-specific assessment projects |
| CV Evaluation | Score candidates against job criteria |
| Submission Scoring | Evaluate project submissions |

**Rate Limits:**
- Tokens per minute: 30,000
- Requests per minute: 60

---

## 3. Network Architecture

### 3.1 Network Flow Diagram

```mermaid
flowchart LR
    subgraph "Public Internet"
        CLIENT[Client]
    end
    
    subgraph "Azure"
        subgraph "App Service"
            FE[Frontend<br/>HTTPS :443]
            BE[Backend<br/>Uvicorn :8000]
        end
        
        subgraph "Private Endpoints"
            PG_EP[PostgreSQL<br/>:5432]
            AOAI_EP[OpenAI API<br/>:443]
        end
    end
    
    CLIENT -->|TLS 1.2+| FE
    FE --> BE
    BE -->|SSL| PG_EP
    BE -->|HTTPS| AOAI_EP
```

### 3.2 Security Groups and Firewall Rules

**App Service:**
- Inbound: HTTPS (443) from Internet
- Outbound: PostgreSQL (5432), HTTPS (443)

**PostgreSQL Flexible Server:**
- Inbound: TCP 5432 from App Service IP range
- SSL/TLS: Required

**Azure OpenAI:**
- Authentication: API Key
- Network: Public endpoint with key authentication

---

## 4. Data Flow

### 4.1 Request Processing Flow

```mermaid
sequenceDiagram
    participant User
    participant AppService as App Service
    participant OpenAI as Azure OpenAI
    participant DB as PostgreSQL

    User->>AppService: HTTPS Request
    AppService->>AppService: Validate Request
    
    alt AI Processing Required
        AppService->>OpenAI: API Call (GPT-4o)
        OpenAI-->>AppService: AI Response
    end
    
    AppService->>DB: Query/Insert Data
    DB-->>AppService: Data Response
    
    AppService-->>User: JSON Response
```

### 4.2 CI/CD Pipeline Flow

```mermaid
flowchart LR
    subgraph "Development"
        DEV[Developer]
        CODE[Source Code]
    end
    
    subgraph "GitHub"
        REPO[Repository]
        ACTIONS[GitHub Actions]
    end
    
    subgraph "Azure"
        ACR[Container Registry]
        APP[App Service]
    end
    
    DEV --> CODE
    CODE --> REPO
    REPO --> ACTIONS
    ACTIONS -->|Build & Push| ACR
    ACR -->|Deploy| APP
```

---

## 5. Security Architecture

### 5.1 Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 1: Network Security                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - HTTPS Only (TLS 1.2+)                                     ││
│  │ - Azure Firewall Rules                                      ││
│  │ - IP Restrictions (optional)                                ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Layer 2: Application Security                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - Input Validation (Pydantic)                               ││
│  │ - CORS Configuration                                        ││
│  │ - Rate Limiting                                             ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Layer 3: Data Security                                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - PostgreSQL SSL Connections                                ││
│  │ - Encrypted Storage (Azure managed)                         ││
│  │ - Environment Variables for Secrets                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Layer 4: Identity & Access                                      │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - Azure RBAC for Resources                                  ││
│  │ - API Key for OpenAI                                        ││
│  │ - Container Registry Authentication                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Secrets Management

| Secret | Storage | Rotation |
|--------|---------|----------|
| Database Password | App Service Configuration | Manual |
| OpenAI API Key | App Service Configuration | Manual |
| ACR Credentials | App Service Configuration | Auto (Managed Identity) |

---

## 6. Cost Estimation

### 6.1 Monthly Cost Breakdown (EUR)

| Service | SKU | Estimated Cost |
|---------|-----|----------------|
| **App Service Plan** | B1 (Linux) | ~13 EUR |
| **Azure Container Registry** | Basic | ~5 EUR |
| **PostgreSQL Flexible Server** | B1ms | ~15 EUR |
| **Azure OpenAI** | Pay-per-use | ~20-50 EUR* |
| **Data Transfer** | Outbound | ~5 EUR |
| **Total** | | **~58-88 EUR/month** |

*OpenAI costs vary based on usage (tokens processed)

### 6.2 Cost Optimization Recommendations

| Recommendation | Potential Savings |
|----------------|-------------------|
| Use Reserved Instances (1 year) | 30-40% |
| Enable auto-scaling during off-hours | 20-30% |
| Optimize OpenAI prompts | Variable |
| Use Spot instances for dev/test | 60-90% |

---

## 7. Scaling Strategy

### 7.1 Horizontal Scaling

```mermaid
graph TB
    subgraph "Current: Single Instance"
        A1[App Service Instance 1]
    end
    
    subgraph "Scaled: Multiple Instances"
        LB[Load Balancer]
        B1[Instance 1]
        B2[Instance 2]
        B3[Instance 3]
    end
    
    A1 -.->|Scale Out| LB
    LB --> B1
    LB --> B2
    LB --> B3
```

### 7.2 Scaling Tiers

| Tier | Plan | Instances | Use Case |
|------|------|-----------|----------|
| **Development** | B1 | 1 | Testing, Development |
| **Production** | S1 | 2-3 | Normal traffic |
| **Enterprise** | P1v2 | 3-10 | High availability |

### 7.3 Database Scaling Path

| Current | Next Tier | Trigger |
|---------|-----------|---------|
| B1ms (1 vCore) | B2ms (2 vCores) | CPU > 80% |
| B2ms (2 vCores) | GP_Gen5_4 | High IOPS needed |
| GP_Gen5_4 | Read Replicas | Read-heavy workload |

---

## Azure Resource Summary

```
Resource Group: arya-recruitment-rg
Region: France Central
├── App Service Plan (Linux B1)
│   └── App Service: arya-recruitment-api-v2
│       └── Docker Container: aryaregistryv2.azurecr.io/arya-api:latest
├── Container Registry: aryaregistryv2 (Basic)
├── PostgreSQL Flexible Server (B1ms)
│   └── Database: arya_db
└── Azure OpenAI Service
    └── Deployment: gpt-4o
```

---

## Quick Reference

### Service Endpoints

| Service | Endpoint |
|---------|----------|
| **API** | https://arya-recruitment-api-v2.azurewebsites.net |
| **Swagger UI** | https://arya-recruitment-api-v2.azurewebsites.net/docs |
| **ReDoc** | https://arya-recruitment-api-v2.azurewebsites.net/redoc |
| **Health Check** | https://arya-recruitment-api-v2.azurewebsites.net/health |
| **Container Registry** | aryaregistryv2.azurecr.io |

### Azure CLI Commands

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "<subscription-id>"

# View App Service logs
az webapp log tail --name arya-recruitment-api-v2 --resource-group arya-recruitment-rg

# Restart App Service
az webapp restart --name arya-recruitment-api-v2 --resource-group arya-recruitment-rg

# Deploy new image
az webapp config container set \
  --name arya-recruitment-api-v2 \
  --resource-group arya-recruitment-rg \
  --docker-custom-image-name aryaregistryv2.azurecr.io/arya-api:latest
```

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | February 2026 | Mohamed Amine Elabidi | Initial version |

---

*This document is part of the ARYA Multi-Agent Recruitment System technical documentation.*
