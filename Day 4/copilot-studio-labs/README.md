# Copilot Studio Agent Lab Series – Northwind Field Service

Four hands-on experiments that cover every way to build in **Microsoft Copilot Studio**: **Agents**, **Workflows** and **Apps** (all powered by the GitHub Copilot harness), and **Other ways to build** (the standard harness). Along the way you'll connect a **custom MCP server**, add **tools**, **skills**, **knowledge**, **memory** and **evaluations**, and keep a **human in the loop**.

> **About the "GitHub Copilot" label on the Home page cards:** it refers to the **GitHub Copilot harness**, the new authoring and runtime framework inside Copilot Studio. It is *not* the GitHub Copilot coding product, and you don't need a GitHub account or a GitHub Copilot license.

---

## The story

**Northwind Field Service** maintains rooftop HVAC units, standby generators and cold rooms for hospitals, malls, data centres and food warehouses in **Pune, Chennai, Dubai and Riyadh**. Every day the service desk gets fault reports by email and chat. They have to work out what's wrong, whether it's under warranty, which part is needed, whether it's in stock and who can go.

Across four labs you'll build the digital team that does this:

```
                 ┌────────────────────────── Lab 4: Other ways to build ──────────────────────────┐
 Customers ────▶ │  Customer Helpline agent (standard harness): topics, FAQ knowledge, MCP tool,   │
 (web chat)      │  publishes to a website                                                        │
                 └─────────────────────────────────────────────────────────────────────────────────┘

 Fault emails ──▶ Lab 2: WORKFLOW ──▶ Extract ▶ Classify ▶ Agent ▶ Human review ▶ Dataverse ▶ Reply
                                            │
                                            ▼
                 Lab 1: AGENT "Service Desk Agent"
                 knowledge (manuals) · skill · memory · model
                 tools: ◀── MCP ──▶  Northwind Field Service MCP server (assets, parts, technicians)
                                            │
                                            ▼  work orders in Dataverse
                 Lab 3: APP "Work Order Console" for dispatchers
```

## The four labs

| Lab | Home page card | You build | Key skills | Time |
| --- | --- | --- | --- | --- |
| [Lab 1](Lab-1-Agent-with-MCP-Skills-Tools.md) | **Agent** | Service Desk Agent + your own MCP server | Instructions, knowledge, **MCP server**, **skills**, model choice, memory, activity trace, **evaluations**, publish | 120 min |
| [Lab 2](Lab-2-Workflow-Automation.md) | **Workflow** | Fault Email Intake workflow, plus a workflow tool for the agent | Triggers, **Extract**, **Classify**, **Agent** node, **Human review**, Dataverse, test runs, workflow as a **tool** | 90 min |
| [Lab 3](Lab-3-App-Builder.md) | **App (preview)** | Work Order Console app | Natural-language app generation, Dataverse data, iterate by prompt, review code, publish and share | 60 min |
| [Lab 4](Lab-4-Other-Ways-to-Build.md) | **Other ways to build** | Customer Helpline agent (standard harness) | Topics, question nodes, generative answers, **MCP onboarding wizard**, tool selection, website channel, harness comparison | 90 min |

Do the labs **in order**. Each lab reuses something from the one before.

---

## Before you start (everyone)

### Accounts and licensing

- [ ] A work or school account with access to **Copilot Studio** (https://copilotstudio.microsoft.com)
- [ ] A **Power Platform environment** with **Dataverse** where you can create agents, workflows and apps (a developer environment is ideal)
- [ ] **Copilot Credits** available in that environment. Building, testing and evaluating GitHub Copilot harness agents, workflows and apps is **usage-based**.
- [ ] **Outlook** (Exchange Online) mailbox, for Lab 2
- [ ] **App (preview)** visible on your Home page, for Lab 3. It's rolling out by environment.

### For the MCP server (Lab 1)

You need **one** of these (your instructor will tell you which):

| Option | You need | Best for |
| --- | --- | --- |
| **A – Instructor-hosted server** | Just the URL and API key from your instructor | Classrooms (fastest) |
| **B – Run it yourself with a dev tunnel** | Python 3.10+, VS Code or the `devtunnel` CLI | Learners who want to see the server code run |
| **C – Deploy it to Azure Container Apps** | Azure subscription, Azure CLI | Production-style hosting |

### Lab files

```
lab-files/
├── knowledge/
│   ├── HX-200_Service_Manual.docx           Lab 1 – agent knowledge
│   ├── PG-50_Service_Manual.docx            Lab 1 – agent knowledge
│   ├── Field_Safety_and_Escalation_SOP.docx Lab 1 – agent knowledge
│   └── Customer_FAQ.docx                    Lab 4 – helpline knowledge
├── mcp-server/                              Lab 1 & 4 – Northwind Field Service MCP server
│   ├── server.py  requirements.txt  Dockerfile
│   └── data/ assets.json  parts.json  technicians.json
├── skills/
│   ├── fault-diagnosis-report/SKILL.md      Lab 1 – custom skill
│   └── fault-diagnosis-report.zip
├── evaluation/service-desk-test-set.csv     Lab 1 – evaluation test set
├── dataverse/WorkOrders.csv                 Lab 2 & 3 – Work Order table seed data
└── emails/                                  Lab 2 – three sample fault emails
```

> All companies, people, assets and phone numbers are **fictional** training data.

---

## Lab conventions

- **Bold** = something you click or a label on screen. `Code` = something you type or paste.
- 💡 = tip · ⚠️ = watch out · 🧩 = the concept behind what you just did · ✅ = checkpoint
- Copilot Studio is updated often, and Agents, Workflows and Apps on the GitHub Copilot harness are partly in **preview**. If a label differs slightly on your screen, pick the closest match.
- AI output varies between runs. Check the **behaviour** (right tool, right rule, right priority), not the exact wording.
