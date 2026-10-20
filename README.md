# Microsoft Data & AI Readiness for SATORP

Handouts, architecture references, and hands-on lab artifacts for the **Microsoft Data & AI Readiness Program** conducted for **SATORP (Saudi Aramco Total Refining and Petrochemical Company)**.

---

## 📌 Program Overview

This repository provides structured learning modules, code samples, lab guides, and production-ready architecture patterns to accelerate enterprise adoption of Microsoft Cloud Data & AI platforms. The focus spans foundation models, enterprise agentic workflows, integration with core systems (SAP, OpenText), and real-time operational analytics.

---

## 📂 Repository Structure

| Folder / Module | Focus & Core Highlights |
| :--- | :--- |
| **[Day 1](./Day%201)** | **Azure AI Foundation**<br>• Introduction to Azure AI Foundry and OpenAI service foundations<br>• Core capabilities, model selection, prompt engineering basics, and foundational patterns |
| **[Day 2](./Day%202)** | **Advanced Retrieval & Grounding**<br>• Retrieval-Augmented Generation (RAG) architectures<br>• Vector indexing with Azure AI Search, chunking strategies, and knowledge grounding |
| **[Day 3](./Day%203)** | **Agentic Workflows & Multi-Agent Orchestration**<br>• Agent development with Semantic Kernel, LangChain/LangGraph, or Microsoft Copilot Studio<br>• Tool integration, function calling, and structured reasoning pipelines |
| **[Day 4](./Day%204)** | **Enterprise Operations & Production Deployment**<br>• Model evaluation, safety filters, content moderation, and LLM governance<br>• Deployment options (Azure Container Apps, endpoints, monitoring, and observability) |
| **[Artifacts](./Artifacts)** | **Production Design & Enterprise Solution Accelerators**<br>• Enterprise integration blueprints (e.g., Azure AI Foundry agent orchestration with SAP & OpenText)<br>• Reusable scripts, container definitions (`Dockerfile`), and integration utilities |

---

## 🛠️ Technology Stack

- **Cloud Platform:** Microsoft Azure (Azure AI Foundry, Azure OpenAI Service, Azure AI Search, Azure Container Apps)
- **Frameworks & Orchestration:** Python, Semantic Kernel / LangChain / AutoGen / Microsoft Copilot Studio
- **Enterprise Integrations:** SAP ERP / Core Workloads, OpenText Content Suite
- **Containerization:** Docker

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) configured with your subscription
- Access to an Azure subscription with Azure OpenAI and Azure AI Search permissions
- Docker Desktop (for containerized deployments)

### Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/CodeSizzler/SATORP-Microsoft-Data-AI-Readiness.git](https://github.com/CodeSizzler/SATORP-Microsoft-Data-AI-Readiness.git)
   cd SATORP-Microsoft-Data-AI-Readiness
