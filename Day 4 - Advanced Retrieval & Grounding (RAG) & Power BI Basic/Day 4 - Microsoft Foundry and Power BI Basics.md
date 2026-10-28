  

**Comparision of AI services on Microsoft:**

| ** ** | **M365 Copilot** | **Copilot Studio** | **Microsoft Foundry** |
| --- | --- | --- | --- |
| What? | This runs on M365 environment, its bounded to your SharePoint tenant, we cannot have third party connectors, knoweledge is limited to your SharePoint data, web-search (bing) | Build your autonomous Agents - low code, zero code, your data can be from third-party, web-search, pre-trained data (models) | Advanced - core coding, hard code your agent. All matured compared to Copilot Studio. |
| When? Usecase | - To develop an agent which can work for HR roles, with the data that is on SharePoint.  - Summarizing, design a presentation, do a calculation on excel, schedule a meeting with calendar, prepare for a meeting, etc., anything with M365 apps. | - HR agent which can call the data from 3rd party (D365) which can do on-boarding, employee information, NDA, laptop agreements, etc., (MCP server, low code environment) | - Pro developer who can build the same HR agent, you can write your MCP server, host your own models, any connectors (8000) to go with MCP server. |
| Multi - agents? | Yes - M365 environment (if your data is within SharePoint) | Yes | Yes |

| MCP? | No | yes | Yes |
| --- | --- | --- | --- |
| RAG? | Yes - its not managed by you | Yes | Yes |
| Model selection? | very limited - Gpt and claude (auto) | Yes - OpenAI & Claude | Yes (12000) |
| Evaluation? | No | Monitoring (view) | Yes |
| Channel? | No - My apps (portal.office.com) | Yes | Yes |
| SDK? | Cloud based (portal.office.com) | copilotstudio.microsoft.com | ai.azure.com  VS Code  Foundry Toolkit |

Lab - Developing an agent with VS Code for Foundry

\- VS Code

\- Foundry Toolkit

\- Python

\- Git

\- Azure CLI

Step 1 - Model (gpt or claude)

Foundry -> Existing project -> Model

API key - 5dpzgrHue4C15uNmOizFgogNmwv7Hvxo91AK8QqBqXjUWQ5e0GCiJQQJ99CJAC1i4TkXJ3w3AAAAACOGFvoO

Project endpoint - https://aif-p1-sbx-centralus.services.ai.azure.com/api/projects/sbx-labinstructor-01

Azure OpenAI endpoint - https://aif-p1-sbx-centralus.openai.azure.com/openai/v1

Model name -

# gpt-5.2
**Step by step execution:**

> \- Model on an existing project (model name, endpoint, azure openai endpoint, api key)
> 
> \- VS code - Foundry Toolkit, Python
> 
> \- virtual environment (python lib)
> 
> \- activate this vent
> 
> \- env file (prject endpoint, model name)
> 
> \- Knowledge source (.md)
> 
> \- create-agent.py - vector indexing, call the model, project endpoint, published your agent
> 
> \- chat.py - to get the response
> 
> \- Publish and versioning
