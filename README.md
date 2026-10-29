# Microsoft Data & AI Readiness

Handouts, architecture references, and hands-on lab artifacts for the *Microsoft Data & AI Readiness Program.*

## 📌 Program Overview

This repository provides structured learning modules, code samples, step-by-step lab guides, and production-ready architecture patterns to accelerate enterprise adoption of Microsoft Cloud Data & AI platforms. The curriculum spans foundation models, enterprise retrieval (RAG), multi-agent orchestration, agentic operations, SAP & OpenText system integrations, and real-time operational analytics tailored to enterprise scenarios.

## 📂 Repository Structure & Day-wise Curriculum

| Folder / Module | Focus & Core Highlights | Key Hands-on Labs & Deliverables |
| :--- | :--- | :--- |
| **Day 1** | **Agentic Workflows & Multi-Agent Orchestration**<br>• Autonomous and semi-autonomous agent design principles<br>• Tool integration, function calling, and structured reasoning pipelines<br>• Frameworks: Semantic Kernel, LangChain/LangGraph, and AutoGen | • Implementing tool/plugin calling for enterprise schemas<br>• Multi-agent workflows with supervisor/worker patterns<br>• Dynamic task execution with structured outputs and guardrails |
| **Day 2** | **Copilot Studio & Low-Code / Pro-Code Conversational AI**<br>• Microsoft Copilot Studio architecture and classic/modern authoring portal<br>• Generative answers, topic triggers, entities, and flow orchestration<br>• Enterprise connectors and Power Platform integration | • Lab: Building a Q&A agent in Copilot Studio<br>• Connecting external APIs and secure enterprise knowledge sources<br>• Fallback handling and conversational flow design |
| **Day 3** | **Microsoft Foundry - Azure AI Foundation & Core Concepts**<br>• Introduction to Azure AI Foundry and Azure OpenAI Service<br>• Model catalog exploration, parameter tuning, and prompt engineering patterns<br>• Foundation architectures and enterprise security boundaries | • Setting up Azure AI Foundry workspaces & model deployments<br>• Prompt flow basics and few-shot/system prompt optimization<br>• Securing endpoints via Managed Identities & RBAC |
| **Day 4** | **Advanced Retrieval & Grounding (RAG) & Power BI Basics**<br>• Retrieval-Augmented Generation (RAG) architectural patterns and vector indexing<br>• Azure AI Search: hybrid search, semantic ranking, and chunking strategies<br>• Power BI fundamentals: data ingestion, modeling, DAX, and report visualization | • Chunking and indexing technical refinery/operations specs in Azure AI Search<br>• Enterprise knowledge Q&A backend with grounded citations<br>• Building interactive Power BI operational dashboards connected to curated data |
| **Day 5** | **Microsoft Fabric & Enterprise Analytics**<br>• Unified analytics architecture with OneLake, Lakehouse, and Warehouse<br>• End-to-end data engineering with Fabric Notebooks and Data Pipelines<br>• Real-time intelligence, Direct Lake connectivity, and governance via Microsoft Purview | • End-to-end Lakehouse ingestion and transformation pipeline<br>• Direct Lake reporting integration with Power BI<br>• Implementing enterprise security, data lineage, and Purview governance policies |
| **Artifacts** | **Production Design & Enterprise Solution Accelerators**<br>• Architectural blueprints and decision matrices tailored<br>• Enterprise integration guides (Azure AI Foundry agent orchestration with SAP & OpenText)<br>• Reusable container configurations (`Dockerfile`), IaC templates, and integration utilities | • Platform Architecture Decision Guide<br>• SAP & OpenText connector reference patterns<br>• Production deployment manifests and environment setups |

## 🛠️ Technology Stack

- **Cloud & AI Platform:** Microsoft Azure (Azure AI Foundry, Azure OpenAI Service, Azure AI Search, Azure Container Apps, Azure API Management)
- **Agentic & AI Frameworks:** Semantic Kernel, LangChain / LangGraph, AutoGen, Microsoft Copilot Studio
- **Data & Business Intelligence:** Microsoft Fabric (OneLake, Lakehouse, Data Factory), Power BI
- **Enterprise Systems Integration:** SAP ERP / Core Workloads, OpenText Content Suite
- **Governance & Monitoring:** Azure AI Content Safety, Microsoft Purview, Azure Monitor & Application Insights
- **Runtime & Deployment:** Python 3.10+, Docker

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) authenticated with your enterprise subscription (`az login`)
- Azure subscription access with configured permissions for:
  - Azure OpenAI Service (with quota for GPT-4o / text-embedding models)
  - Azure AI Search (Basic tier or above recommended for vector/hybrid search)
  - Azure AI Foundry workspace
  - Microsoft Copilot Studio environment
  - Microsoft Fabric-enabled workspace capacity
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for containerized deployments and local evaluation runners)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/CodeSizzler/Microsoft-Data-AI-Readiness.git](https://github.com/CodeSizzler/Microsoft-Data-AI-Readiness.git)
   cd Microsoft-Data-AI-Readiness
