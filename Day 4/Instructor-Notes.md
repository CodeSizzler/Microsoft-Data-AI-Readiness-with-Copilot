# Instructor Notes – Copilot Studio Agent Lab Series

> For trainers only.

## Before the class (do a full dry run)

Several features in this series are **preview** and roll out by environment. Do one full dry run in the **exact environment** learners will use, 48 hours before the session.

| Check | Why |
| --- | --- |
| The Home page shows **Agent**, **Workflow**, **App (preview)** and **Other ways to build** | App (preview) is rolling out by environment |
| Copilot Credits are allocated to the lab environment | GitHub Copilot harness agents, workflows and apps are usage-based |
| Learners have the **Environment Maker** role (or higher) and Dataverse | Needed to create tables, agents, workflows and apps |
| Outlook mailboxes are licensed | Lab 2 trigger |
| Your tenant's DLP policy allows the **MCP**, **Office 365 Outlook** and **Dataverse** connectors in the same group | Otherwise tools and workflows are blocked |
| Exact labels for **Extract**, **Classify**, **Human review** and the **Agent** node in the workflow designer | Names may differ slightly; update the lab text if needed |
| Whether skills can be **uploaded** (zip) in your tenant, or only created | Lab 1 Part E covers both paths |

## Host one shared MCP server (recommended)

Tunnels on corporate laptops are the most common blocker. Host one server for the whole class:

```bash
cd lab-files/mcp-server
az containerapp up --name northwind-mcp-class --resource-group rg-copilot-labs \
  --location centralindia --source . --ingress external --target-port 8000 \
  --env-vars MCP_API_KEY=<class-key>
```

Give learners the URL (ending in `/mcp`) and the key. The tools are read-only, so sharing is safe. Strong learners can still run their own copy (Option B) to explore the code.

**Verify it:**

```bash
curl -s -X POST https://<app>.azurecontainerapps.io/mcp -H "x-api-key: <class-key>" \
  -H "content-type: application/json" -H "accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-06-18" -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

The server uses the official MCP Python SDK v2 (`mcp>=2.2`, `MCPServer`) over **Streamable HTTP**, stateless, with an optional `x-api-key` check. It was tested locally: unauthenticated calls return 401, and all four tools list and run.

## Suggested agenda (2 days)

| Day | Session | Lab | Time |
| --- | --- | --- | --- |
| 1 AM | Concepts: harnesses, agents vs workflows vs apps, MCP | – | 45 min |
| 1 AM–PM | Agent + MCP + skills | Lab 1 | 120 min |
| 1 PM | Workflows | Lab 2 | 90 min |
| 2 AM | Apps | Lab 3 | 60 min |
| 2 AM–PM | Standard harness, harness decision | Lab 4 | 90 min |
| 2 PM | Showcase and Q&A | – | 45 min |

## Answer key – data you can check against

**Assets** (`data/assets.json`; "today" is October 2026)

| Asset | Model | Customer / city | Warranty | Plan |
| --- | --- | --- | --- | --- |
| AST-1001 | HX-200 | Lakeside Medical, Pune | **Expired** 2026-04-12 | Gold, 4 h |
| AST-1002 | HX-200 | Bluewater Mall, Dubai | Until 2028-01-20 | Silver, next business day |
| AST-2001 | PG-50 | Lakeside Medical, Pune | **Expired** 2025-09-01 | Gold, 4 h |
| AST-2002 | PG-50 | Northgate Data Hub, Riyadh | Until 2028-11-05 | Platinum, 2 h |
| AST-3001 | CX-10 | FreshBite Foods, Chennai | **Expired** 2026-06-18 | None |

**Lab 1 Part E – expected Fault Diagnosis Report (AST-1001, E09):**
HX-FAN-07, 2 in Pune · out of warranty · 420 + 2.5 h × 85 = **632.50 USD** · **approval required** (part > 500) · Gold, 4 h · **P2** (P1 only if the agent treats total cooling loss at a hospital as critical; accept either with a reason) · Arjun Mehta, today 14:00.

**Lab 1 safety test:** any troubleshooting step in the answer = fail.

**Lab 2 expected runs:**

| Email | Extract AssetID | Classify | Path |
| --- | --- | --- | --- |
| 1 Generator (AST-2001, G11) | AST-2001 | P1 (hospital generator fails to start) | Human review → Dataverse → reply |
| 2 Grinding (AST-1002) | AST-1002 | P3 (still cooling) | Dataverse → reply |
| 3 Cold room | *(empty)* | – | Ask-for-asset-ID email |

Agent report for email 1: G11 → **PG-BAT-12** (3 in Pune) · out of warranty · 180 + 0.5 h × 85 = **222.50 USD** · Arjun Mehta.

**Lab 3:** P1 tile = 2 (WO-5004, WO-5008) + any new P1s from Lab 2. Awaiting approval = WO-5003, WO-5008. Approval banner only on WO-5008 (610 USD).

**Lab 4:** AST-2002 → Platinum, 2 hours. Stock questions must be refused. Check the activity map shows no stock tool call.

## Discussion prompts

- Lab 1: "Your tool descriptions are prompts. Who in your organisation should own them?"
- Lab 2: "Which steps in your processes must stay human-approved, even if the AI is 99% right?"
- Lab 3: "You didn't write the code but you're publishing it. What do you check before you do?"
- Lab 4: "Same MCP server, different permissions per agent. Where does that pattern apply in your company?"

## Known risks

| Risk | Mitigation |
| --- | --- |
| Tunnels blocked by corporate policy | Use the shared Azure-hosted server |
| Free tunnel URL changes on restart | Edit the MCP server entry; use the shared server |
| Preview UI labels change | Dry run; tell learners to "pick the closest match" |
| Credits run out mid-class | Allocate enough credits per learner; avoid re-running whole evaluations repeatedly |
| Generated apps differ between learners | Mark against the checklist, not the screen |
