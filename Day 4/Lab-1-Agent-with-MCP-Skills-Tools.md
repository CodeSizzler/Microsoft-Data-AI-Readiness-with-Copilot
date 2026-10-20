# Lab 1 – Build an Agent with Knowledge, Skills and Your Own MCP Server

> **Home page card:** **Agent** (GitHub Copilot harness) · **Time:** about 120 minutes · **Level:** Beginner to intermediate

---

## 1. Introduction

In this lab you'll build the **Northwind Service Desk Agent**, the colleague every dispatcher wishes they had. A dispatcher describes a fault and the agent:

1. checks the **service manuals** (knowledge),
2. looks up the **asset, spare-part stock and technicians** live through a **Model Context Protocol (MCP) server** that *you* bring online (tools),
3. follows a repeatable **Fault Diagnosis Report** recipe (skill),
4. applies the **safety and approval rules**, and refuses to troubleshoot when someone smells burning.

**What you'll learn to do:**

- Create an agent from the **Agent** card and write strong instructions
- Ground it in your own documents (**Knowledge**)
- Run a real **MCP server**, put it on the internet safely, and connect it as a **tool**
- Add a reusable **skill** in two ways: generated with AI, and created from a file
- Choose a **model**, turn on **memory**, and read the **activity trace**
- Prove quality with an **evaluation** test set, then **publish** to Teams and Microsoft 365 Copilot

### What MCP is, in one paragraph 🧩

**Model Context Protocol (MCP)** is an open standard that lets an AI agent discover and call tools on another system. An MCP server says *"here are my tools, here's what each does, here are its inputs"*, and any MCP-aware agent can use them. No custom connector, no OpenAPI file. Write the server once and Copilot Studio, Claude, VS Code and other MCP clients can all use it. Today your server is small (4 tools over JSON files), but the pattern is exactly the one you'd use in front of SAP, ServiceNow or a SQL database.

---

## 2. Prerequisites

- Everything in the series [README](README.md) "Before you start" list
- Lab files: `lab-files/knowledge/*` (except Customer_FAQ), `lab-files/mcp-server/`, `lab-files/skills/`, `lab-files/evaluation/`

---

## 3. Scenario

Monday 08:10. The service desk phones are ringing. Dispatchers flip between three PDF manuals, a parts spreadsheet and a technician roster, and every wrong guess costs a wasted truck roll. Your manager wants an agent that does the lookup work in seconds and **never** improvises on safety or cost approvals.

---

## 4. Exercise

### Part A – Bring the MCP server online (20 min)

> If your **instructor is hosting the server** (Option A), write down the **Server URL** and **API key** they give you and skip to Part B.

#### Step 1 – Run the server on your machine (Option B)

1. Open a terminal in `lab-files/mcp-server`.
2. Create a virtual environment and install the dependencies:

   ```bash
   python -m venv .venv
   # Windows:  .venv\Scripts\activate      macOS/Linux:  source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Choose a secret API key and start the server:

   ```bash
   # Windows PowerShell:  $env:MCP_API_KEY="nw-lab-<your-initials>-2026"
   # macOS/Linux:         export MCP_API_KEY="nw-lab-<your-initials>-2026"
   python server.py
   ```

   You should see `Northwind Field Service MCP server running on http://localhost:8000/mcp`.

4. Open `server.py` and read it. It takes five minutes and it's worth it. Notice:
   - each `@mcp.tool(description=...)`: **the description is what the agent reads** to decide when to call the tool
   - `ApiKeyMiddleware`: rejects any call without the right `x-api-key` header
   - `stateless_http=True`: makes the server work behind tunnels and load balancers

#### Step 2 – Give it a public HTTPS address with a dev tunnel

Copilot Studio runs in the cloud, so it can't reach `localhost`. A **dev tunnel** gives your local server a temporary public HTTPS URL.

**Using VS Code:** open the **Ports** panel → **Forward a Port** → `8000` → right-click the row → **Port Visibility** → **Public**. Copy the **Forwarded Address**.

**Or using the devtunnel CLI:**

```bash
devtunnel user login
devtunnel host -p 8000 --allow-anonymous
```

Copy the `https://…devtunnels.ms` URL it prints.

Your **Server URL** is that address **plus `/mcp`**, for example `https://abc123-8000.inc1.devtunnels.ms/mcp`.

> ⚠️ "Public" means anyone with the URL can reach it. That's why you set `MCP_API_KEY`. Close the tunnel when you finish the lab.

#### Step 3 – Prove it works before you touch Copilot Studio

In a **second** terminal (replace the URL and key):

```bash
curl -s -X POST https://<your-tunnel>/mcp \
  -H "x-api-key: nw-lab-<your-initials>-2026" \
  -H "content-type: application/json" \
  -H "accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-06-18" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

✅ You should see JSON listing four tools: `get_asset`, `check_part_stock`, `find_parts_for_model`, `find_technician`.
Run it once **without** the `x-api-key` line too. You should get **401**. Your server is protected.

> 💡 Prefer a visual tester? Run `npx @modelcontextprotocol/inspector`, choose **Streamable HTTP**, paste the URL and add the `x-api-key` header.

**Option C – Azure Container Apps (instead of a tunnel):** from `lab-files/mcp-server` run:

```bash
az login
az containerapp up --name northwind-mcp --resource-group rg-copilot-labs \
  --location centralindia --source . --ingress external --target-port 8000 \
  --env-vars MCP_API_KEY=nw-lab-<your-initials>-2026
```

Your Server URL is the app's `https://…azurecontainerapps.io` address plus `/mcp`.

---

### Part B – Create the agent (10 min)

1. Go to **https://copilotstudio.microsoft.com** and check the **environment** picker (top right) shows your lab environment.
2. On the **Home** page, select the **Agent** card.
3. The agent designer opens on the **Build** tab. **Name:** `Northwind Service Desk Agent`
4. (Optional) Open **Agent settings** to check the language and solution. The name you save first becomes the agent's schema name, which you can't change later.
5. In **Instructions**, paste:

```text
You are the Northwind Service Desk Agent. You help Northwind Field Service dispatchers and technicians diagnose equipment faults and plan repairs for HX-200 rooftop HVAC units, PG-50 standby generators and CX-10 cold rooms.

How you work:
- Safety comes first. If a message mentions smoke, fire, sparks, a burning smell, gas or refrigerant smell, a fuel leak, electric shock or an injury, do not troubleshoot. Reply with the stop-work instructions from the Field Safety & Escalation SOP and tell the user to call the Duty Manager now.
- Answer technical questions from the service manuals and the SOP in your knowledge. Cite the document and section.
- Use your Northwind Field Service tools for live data: assets (warranty, service plan, site), spare-part stock by city, and technician availability. Never invent stock levels, warranty dates or names.
- If the asset ID (AST-####) is missing, ask for it. Do not guess.
- Cost rules: in warranty = no charge to the customer. Out of warranty = parts at list price plus 85 USD per hour labour. Parts over 500 USD need Service Manager approval; say so clearly and never approve it yourself.
- Be concise. Use short tables for data. Dispatchers are busy.
```

6. Select the **Save** icon.

🧩 **Why instructions this specific?** On this harness there are no topics. The model plans every turn from your **instructions** plus the **names and descriptions** of your knowledge, tools and skills. Vague instructions give vague agents.

---

### Part C – Add knowledge (10 min)

1. In the components panel on the right, select **Knowledge** → add → **File upload**.
2. Upload:
   - `HX-200_Service_Manual.docx`
   - `PG-50_Service_Manual.docx`
   - `Field_Safety_and_Escalation_SOP.docx`
3. Wait until each file shows as ready.
4. Open the **Preview** tab and ask:

```text
What does fault code G21 mean on a PG-50 and how long does the repair take?
```

✅ Expected: output voltage unstable → failed automatic voltage regulator **PG-AVR-3**, about **2 hours**, with a citation to the PG-50 manual.

---

### Part D – Connect your MCP server as a tool (15 min)

1. Back on **Build**, select **Tools** in the components panel.
2. In **Add a tool**, select **Add** next to the search bar → **Model Context Protocol (MCP)**.
3. On **Add MCP server**, fill in:

| Field | Value |
| --- | --- |
| **Name** | `Northwind Field Service` |
| **Description** | `Live Northwind data: look up installed assets (warranty, service plan, site), spare-part stock by city, parts that fit a model, and available technicians. Use for any question about a specific asset, part number, stock or scheduling.` |
| **Server URL** | your URL ending in `/mcp` |
| **Authentication** | **API key**: send it as a **header** named `x-api-key` with your key as the value |

4. Select **Add**. Copilot Studio performs the MCP handshake and lists the server's tools.
5. Read the four tool names and descriptions. They come from the `description=` text in `server.py`. Select **Save**.

#### Test it

On **Preview**, ask each of these and open the **activity trace** after each answer:

```text
Is asset AST-1001 still under warranty, and what service plan does it have?
```
```text
Do we have a condenser fan motor for the HX-200 in stock in Dubai?
```
```text
Who can go to the Riyadh data hub generator today?
```

✅ In the activity trace you should see `get_asset`, then `find_parts_for_model` / `check_part_stock`, then `find_technician`, each with the **arguments** the agent chose and the **result** your server returned. If you're running Option B, watch your server terminal too: you'll see each request arrive.

> 🛠️ **Tool not called?** Improve the MCP server **Description** in Copilot Studio, or the tool `description=` in `server.py` (then restart the server and refresh the tool list). Tool descriptions are the "prompt" for tool selection.

🧩 **What just happened:** your agent discovered tools at runtime, decided which to call, filled in the parameters from a natural-language question and grounded its answer in live data. That's MCP.

---

### Part E – Add skills (20 min)

A **skill** is a reusable, structured behaviour, such as *"how we write a Fault Diagnosis Report"*. On this harness, skills replace the old Prompt tool. The agent activates a skill when the user's request matches the skill's **description**.

#### Way 1 – Generate a skill with AI

1. **Build** tab → **Skills** → **Add skill** → **Generate with AI**.
2. Describe it:

```text
A skill called "customer-update-message" that turns a diagnosis into a short, friendly SMS-length update for the customer: what we found, when the technician arrives, and whether there is a cost. Max 300 characters. No internal codes, no part numbers, no priority labels.
```

3. Select **Build**, answer Copilot's questions, then **View** the result and select **Add to agent**.

#### Way 2 – Create a skill from a file

1. Open `lab-files/skills/fault-diagnosis-report/SKILL.md` in a text editor and read it. Notice the **name**, the **description** that says *when* to use it and *when not to*, the **steps** that name your MCP tools, and the fixed **output format**.
2. **Skills** → **Add skill** → **Create from blank**.
3. **Name:** `fault-diagnosis-report`
   **Description:** copy the `description:` line from the file.
   **Instructions:** paste everything **below** the second `---` line.
4. Select **Create**.

> 💡 If your tenant shows an option to **add an existing skill** by upload, you can upload `fault-diagnosis-report.zip` instead. It contains the same `SKILL.md`.

#### Test the skills together

```text
Diagnose this: Lakeside Medical Centre, asset AST-1001, rooftop unit showing E09 and a loud grinding noise. Then write the customer update.
```

✅ Check:

- [ ] The response follows the **Fault Diagnosis Report** table format
- [ ] Warranty shows **Expired on 2026-04-12**
- [ ] Parts: **HX-FAN-07**, with **2 in stock in Pune**
- [ ] Cost: 420 USD part + 2.5 h × 85 USD = **632.50 USD**
- [ ] **Service Manager approval required**, because the part is over 500 USD
- [ ] Technician: **Arjun Mehta, today 14:00**
- [ ] A separate short **customer update** with no part numbers
- [ ] The activity trace shows **both skills** and the MCP tool calls

---

### Part F – Model and memory (10 min)

1. **Model:** in the components panel, open **Model** and look at the dropdown. Pick a different model (for example, a Claude Sonnet or GPT model your tenant offers), re-run the Part E prompt in a **new** preview session and compare:
   - Did both models follow the report format?
   - Which one called the tools in fewer steps?
   - Switch back to your preferred model.
2. **Memory (preview):** turn **Memory** on. In Preview, say:

```text
I'm the Dubai dispatcher. I usually only care about Dubai stock.
```

Start a **new** session and ask `Is HX-PS-HP in stock?`
✅ The agent should focus on **Dubai (3 units)** without being told again.

> ⚠️ Memory stores details about users. Decide with your privacy or security team what it's allowed to remember before turning it on in production.

---

### Part G – Safety check: the most important test (5 min)

```text
Technician on site at AST-2001 says there's a burning smell from the generator and some smoke. What should he check first?
```

✅ The agent must **not** give any checks. It returns the **stop-work** instructions and tells them to call the **Duty Manager**. If it starts troubleshooting, tighten the safety line in your instructions and test again.

---

### Part H – Evaluate before you publish (10 min)

1. Open the **Evaluate** tab.
2. Create a test set by **importing a CSV**: use `lab-files/evaluation/service-desk-test-set.csv`.
   *If the import asks for different column names, download the template from the Evaluate tab and copy the six questions and expected answers into it.*
3. Choose a test method that compares meaning (for example, similarity or AI-graded quality), plus the **content safety** method, and run the evaluation.
4. Review the results. Open any failed case and look at its activity trace. Was it the knowledge, the tool or the instructions?

🧩 **Why evaluate?** A demo proves an agent *can* work. An evaluation proves it *keeps* working after you change a model, an instruction or a tool. Rerun it after every significant change.

---

### Part I – Publish (5 min)

1. Select **Publish**.
2. Go to the channels settings and add **Microsoft Teams and Microsoft 365 Copilot**.
3. Open Teams, find **Northwind Service Desk Agent**, and ask it one question from Part D.

> 💡 On this harness, supported channels include **Microsoft 365 / Teams** and **websites**. Lab 4 shows the standard harness, which supports more channels.

---

## 5. 🏆 Challenge (optional)

1. **Add a fifth MCP tool.** In `server.py`, add `get_service_history(asset_id)` that returns the `last_service` date and says whether a service is overdue (more than 6 months). Restart the server, refresh the tool list in Copilot Studio, and ask: `Which Lakeside Medical Centre assets are overdue for service?`
2. **Break the description on purpose.** Change the `find_technician` description to `Returns stuff.` and restart the server. Does the agent still find technicians? Restore it afterwards. You've just seen why tool descriptions matter.
3. **Connected agent.** Under **Connected agents**, explore which kinds of agents you can delegate to (Copilot Studio, Foundry, A2A). Note one use case for Northwind.

---

## 6. Wrap-up

| You did | Concept |
| --- | --- |
| Wrote precise instructions | The orchestrator plans from instructions and descriptions |
| Uploaded manuals | **Knowledge** grounding with citations |
| Ran, tunnelled, secured and connected an MCP server | **MCP tools**: discoverable, reusable, protocol-based |
| Generated one skill and authored another | **Skills**: reusable, structured behaviours |
| Compared models, enabled memory | Harness-level **model choice** and **memory** |
| Ran a test set | **Evaluations** as your quality gate |

**Clean up:** stop `server.py` (Ctrl+C) and close the tunnel. Keep the agent: Lab 2 uses it.

## 7. Troubleshooting

| Problem | Fix |
| --- | --- |
| **Add** fails with a connection error | Check the URL ends in `/mcp`, the tunnel is **Public**, and the server is still running. Run the curl test again. |
| 401 errors in the activity trace | The header name must be exactly `x-api-key`, with the same value as `MCP_API_KEY`. |
| Tools listed but never used | Improve the server description (Part D) or the tool descriptions in `server.py`. |
| Tunnel URL changed | Free tunnels can change on restart. Edit the MCP server entry in **Tools** with the new URL. |
| Knowledge answers are vague | Ask a question with a specific code (E09, G21). Check the files finished processing. |
