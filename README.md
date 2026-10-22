# Microsoft Data & AI Readiness for SATORP

Handouts, architecture references, and hands-on lab artifacts for the **Microsoft Data & AI Readiness Program** conducted for **SATORP (Saudi Aramco Total Refining and Petrochemical Company)**.

---

## 📌 Program Overview

This repository provides structured learning modules, code samples, step-by-step lab guides, and production-ready architecture patterns to accelerate enterprise adoption of Microsoft Cloud Data & AI platforms. The curriculum spans foundation models, enterprise retrieval (RAG), multi-agent orchestration, agentic operations, SAP & OpenText system integrations, and real-time operational analytics tailored to SATORP enterprise scenarios.

---

## 📂 Repository Structure & Day-wise Curriculum

| Folder / Module | Focus & Core Highlights | Key Hands-on Labs & Deliverables |
| :--- | :--- | :--- |
| [**Day 1**](./Day%201) | **Azure AI Foundation & Core Concepts**<br>• Introduction to Azure AI Foundry and Azure OpenAI Service<br>• Model catalog exploration, parameter tuning, and prompt engineering patterns<br>• Foundation architectures and enterprise security boundaries | • Setting up Azure AI Foundry workspaces & model deployments<br>• Prompt flow basics and few-shot/system prompt optimization<br>• Securing endpoints via Managed Identities & RBAC |
| [**Day 2**](./Day%202) | **Advanced Retrieval & Grounding (RAG)**<br>• Retrieval-Augmented Generation (RAG) architectural patterns<br>• Azure AI Search integration: hybrid search, semantic ranking, and vectorization<br>• Data ingestion, chunking strategies, and knowledge grounding pipelines | • Document ingestion and chunking for technical refinery/operations specs<br>• Vector indexing with Azure AI Search<br>• Building an enterprise knowledge Q&A backend with grounded citations |
| [**Day 3**](./Day%203) | **Agentic Workflows & Multi-Agent Orchestration**<br>• Autonomous and semi-autonomous agent design principles<br>• Tool integration, function calling, and structured reasoning pipelines<br>• Frameworks: Semantic Kernel, LangChain/LangGraph, and AutoGen | • Implementing tool/plugin calling for enterprise schemas<br>• Multi-agent workflows with supervisor/worker patterns<br>• Dynamic task execution with structured outputs and guardrails |
| [**Day 4**](./Day%204) | **Copilot Studio & Low-Code / Pro-Code Conversational AI**<br>• Microsoft Copilot Studio architecture and classic/modern authoring portal<br>• Generative answers, topic triggers, entities, and flow orchestration<br>• Enterprise connectors and Power Platform integration | • Lab: Building a Q&A agent in Copilot Studio for SATORP scenarios<br>• Connecting external APIs and secure enterprise knowledge sources<br>• Fallback handling and conversational flow design |
| [**Day 5**](./Day%205) | **Enterprise Operations, Governance & Production Deployment**<br>• Model evaluation, prompt evaluation benchmarks, and continuous testing<br>• LLM safety filters, content moderation, and Purview data governance<br>• Containerized hosting, API management, monitoring, and observability | • End-to-end evaluation with custom ground truth test sets<br>• Configuring Azure Content Safety filters and jailbreak prevention<br>• Deploying agents to Azure Container Apps with Application Insights telemetry |
| [**Artifacts**](./Artifacts) | **Production Design & Enterprise Solution Accelerators**<br>• Architectural blueprints and decision matrices tailored for SATORP<br>• Enterprise integration guides (Azure AI Foundry agent orchestration with SAP & OpenText)<br>• Reusable container configurations (`Dockerfile`), IaC templates, and integration utilities | • SATORP Platform Architecture Decision Guide<br>• SAP & OpenText connector reference patterns<br>• Production deployment manifests and environment setups |

---

## 🛠️ Technology Stack

- **Cloud Platform:** Microsoft Azure (Azure AI Foundry, Azure OpenAI Service, Azure AI Search, Azure Container Apps, Azure API Management)
- **Agentic & AI Frameworks:** Semantic Kernel, LangChain / LangGraph, AutoGen, Microsoft Copilot Studio
- **Enterprise Systems Integration:** SAP ERP / Core Workloads, OpenText Content Suite
- **Governance & Monitoring:** Azure AI Content Safety, Microsoft Purview, Azure Monitor & Application Insights
- **Runtime & Deployment:** Python 3.10+, Docker

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) authenticated with your enterprise subscription (`az login`)
- Azure subscription access with configured permissions for:
  - Azure OpenAI Service (with quota for GPT-4o / text-embedding models)
  - Azure AI Search (Basic tier or above recommended for vector/hybrid search)
  - Azure AI Foundry workspace
  - Microsoft Copilot Studio environment
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for containerized deployments and local evaluation runners)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/CodeSizzler/SATORP-Microsoft-Data-AI-Readiness.git](https://github.com/CodeSizzler/SATORP-Microsoft-Data-AI-Readiness.git)
   cd SATORP-Microsoft-Data-AI-Readiness
