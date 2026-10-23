# Lab 4 – Other Ways to Build: a Customer Helpline on the Standard Harness

> **Home page card:** **Other ways to build** (standard harness) · **Time:** about 90 minutes · **Level:** Intermediate

---

## 1. Introduction

Labs 1–3 used the new **GitHub Copilot harness**: you describe the agent and the model plans each turn. Sometimes you need **more control** than that. A customer-facing bot, for example, should collect the same details in the same order every time, validate an asset ID before using it, and expose **only** the tools customers are allowed to use.

That's what **Other ways to build** is for. It opens the **standard harness**: classic Copilot Studio with **topics**, **question nodes**, **entities**, configurable **orchestration**, the **MCP onboarding wizard** with per-tool on/off switches, and the widest choice of **channels**.

You'll build the **Northwind Customer Helpline**, a public website chat where customers can ask questions and report faults.

**What you'll learn to do:**

- Explore the three options behind **Other ways to build**
- Create a standard-harness agent and choose its **orchestration** mode
- Ground it in **public FAQ** knowledge only
- Build a **topic** with **question nodes**, a **regular-expression entity**, a **condition** and an **adaptive card**
- Connect the **same MCP server** from Lab 1 through the **MCP onboarding wizard** and **switch off the tools customers mustn't use**
- Customise **system topics** (greeting, escalation)
- Publish to a **website**
- Decide **which harness to use when**

---

## 2. Prerequisites

- Lab 1's MCP server running and reachable (your tunnel, Azure URL or instructor URL, plus the API key)
- Lab files: `lab-files/knowledge/Customer_FAQ.docx`

---

## 3. Scenario

Customers keep phoning the hotline with simple questions ("Is my repair free?", "How fast will you come?") and with fault reports that miss the asset ID half the time. Northwind wants a **website helpline** that answers FAQs, collects complete fault reports, and tells customers their response time from their service plan. It must **never** reveal stock levels, prices or technician names.

---

## 4. Exercise

### Part A – Tour "Other ways to build" (5 min)

1. In Copilot Studio, on **Home**, select **Other ways to build**.
2. Look at the options:

| Option | What it is | Use it when |
| --- | --- | --- |
| **Customer Assist Agent** | A ready-made customer-service agent template | You want a customer-service starting point quickly, especially alongside Dynamics 365 contact-centre scenarios |
| **Copilot** (describe it) | Describe the agent in natural language; Copilot drafts a standard-harness agent | You want speed but still need standard-harness features |
| **Standard orchestration** | Build from scratch with full control over topics, orchestration and settings | You need predictable, designed conversations, which is today's lab |

3. Choose **standard orchestration** (build from blank / configure).

---

### Part B – Create the agent (10 min)

1. **Name:** `Northwind Customer Helpline`
2. **Description:** `Public helpline for Northwind Field Service customers: answers FAQs, collects fault reports and shares response times.`
3. **Instructions:**

```text
You are the Northwind Customer Helpline, talking to customers on our public website.
- Be warm, brief and clear. Customers are facility managers, not engineers.
- Answer general questions only from the Customer FAQ.
- When a customer wants to report a problem, use the "Report a fault" topic.
- You may look up a customer's asset to tell them its service plan and response time. Never reveal part numbers, prices, stock levels or technician names.
- If anything suggests danger (smoke, fire, burning smell, gas, fuel leak, electric shock, injury), give the safety advice from the FAQ and escalate to a human immediately.
```

4. Select **Create**.
5. Go to **Settings** → **Generative AI** and look at the **Orchestration** choice:
   - **Generative orchestration** (the default for new agents) uses topic and tool *descriptions* to decide what to run.
   - **Classic** orchestration uses topic *trigger phrases* only.
   Keep **generative** on for this lab.
6. In the knowledge settings, turn **off** using the model's general knowledge and **web search**. Customers must only get Northwind's official answers.

---

### Part C – Knowledge: public FAQ only (5 min)

1. **Knowledge** → **Add knowledge** → **Files** → upload `Customer_FAQ.docx`.
2. Give the source a description: `Official answers for Northwind customers: response times, costs, safety advice, servicing, coverage area.`
3. In the **Test** pane, ask: `Is my repair free?`
   ✅ The answer covers warranty, list price and **85 USD/hour labour**, with a citation.

> 🧩 Notice what this agent **doesn't** know: no service manuals and no internal SOP. **Least privilege applies to knowledge too.** The internal Service Desk Agent (Lab 1) and the public Helpline get different sources.

---

### Part D – Connect the MCP server with the onboarding wizard (15 min)

1. Open **Tools** → **Add a tool** → **New tool** → **Model Context Protocol**.
2. Complete the wizard:

| Field | Value |
| --- | --- |
| **Server name** | `Northwind Field Service` |
| **Server description** | `Look up a Northwind customer's installed asset by asset ID (AST-####) to find its service plan and warranty.` |
| **Server URL** | the same `…/mcp` URL as Lab 1 |
| **Authentication** | **API key** → **Type:** Header → **Header name:** `x-api-key` |

3. Select **Create**, then create a **new connection** and enter your API key value.
4. Select **Add and configure**. The server's settings page opens with **Details**, **Tools** and **Resources**.
5. Under **Tools**, turn **off** **Allow all**, then switch on **only** `get_asset`.
   Leave `check_part_stock`, `find_parts_for_model` and `find_technician` **off**.
6. **Save**.

🧩 **Same server, different permissions.** Lab 1's internal agent uses all four tools; the public helpline gets one. You reused the MCP server without changing any code and controlled exposure at the agent. MCP access also follows your **Power Platform data policies**, because it runs through connectors.

**Test it:**

```text
What service plan does AST-2002 have and how fast would you come?
```

✅ **Platinum, 2 hours**.

```text
Do you have a voltage regulator in stock for it?
```

✅ The helpline should say it can't share stock information. Its activity map shows **no** `check_part_stock` call (it isn't available).

---

### Part E – Build the "Report a fault" topic (25 min)

#### Step 1 – A custom entity for asset IDs

1. **Settings** → **Entities** → **New entity** → **Regular expression (Regex)**.
2. **Name:** `Asset ID` · **Pattern:** `AST-\d{4}` · **Save**.

🧩 Custom entities validate input **before** anything else runs. The new harness doesn't support them, so this is one reason to choose the standard harness.

#### Step 2 – Create the topic

1. **Topics** → **Add a topic** → **From blank**. Name it `Report a fault`.
2. In the **Trigger** node, set the description (generative orchestration uses this):
   `The customer wants to report a fault, breakdown, alarm, noise or problem with Northwind equipment.`
   Add a few trigger phrases as well, for example `report a fault`, `my AC is broken`, `generator won't start`, `something is wrong with our cold room`.

#### Step 3 – Ask the questions

Add these nodes in order:

1. **Ask a question:** `What's the asset ID? It's on the silver label inside the service door and looks like AST-1234.`
   - **Identify:** `Asset ID` (your entity) · **Save as:** `varAssetID`
   - Under question behaviour, set a **retry prompt**: `That doesn't look right – asset IDs look like AST-1234. Can you check the label?`
2. **Ask a question:** `What's happening? Please describe the problem, including any code on the display.`
   - **Identify:** **User's entire response** · **Save as:** `varSymptom`
3. **Ask a question:** `What's the best phone number to reach you?`
   - **Identify:** **Phone number** · **Save as:** `varPhone`

#### Step 4 – Safety branch

1. Add a **Condition**: `varSymptom` **contains** `smoke`. Select **+ New condition** with **OR** and add `fire`, `burning`, `gas`, `fuel`, `shock` and `spark`.
2. **True branch:**
   - **Send a message:** `⚠️ Please keep everyone away from the equipment. Only switch off the power if it's safe to do so. If there's fire, call emergency services now. I'm connecting you to our duty team immediately.`
   - **Topic management** → **Go to another topic** → **Escalate**
3. **False branch:** continue below.

#### Step 5 – Summarise with an adaptive card

1. In the False branch: **Send a message** → **Add** → **Adaptive card**, and paste:

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    { "type": "TextBlock", "text": "Fault report received", "weight": "Bolder", "size": "Medium", "color": "Accent" },
    { "type": "FactSet", "facts": [
      { "title": "Asset", "value": "${varAssetID}" },
      { "title": "Problem", "value": "${varSymptom}" },
      { "title": "Call-back number", "value": "${varPhone}" }
    ]},
    { "type": "TextBlock", "text": "Our service desk will call you back within your service plan's response time.", "wrap": true }
  ]
}
```

   *If the card editor uses Power Fx formulas instead of `${…}`, switch the card to **Formula** mode and reference `Topic.varAssetID` and so on.*

2. **Send a message:** `I'll check your service plan for the response time now.` The orchestrator can call `get_asset` here, as your instructions allow it. If your topic editor offers **Add a tool** in the node menu, you can instead call the **Northwind Field Service → get_asset** tool directly with `varAssetID` and display its `service_plan`.
3. **Topic management** → **End current topic**.
4. **Save**.

#### Step 6 – Test

In the **Test** pane, with the **activity map** open:

| Say | Expect |
| --- | --- |
| `Our rooftop AC is making a grinding noise` | Topic starts and asks for the asset ID |
| `It's AST-12` | Retry prompt (fails the regex) |
| `AST-1002` | Asks for the symptom |
| `Grinding from the fan, still cooling` | Asks for a phone number |
| `+971 50 000 2222` | Adaptive card, then a response time from **Silver: next business day** |

Run it again with a symptom of `burning smell and smoke`. ✅ Safety message, then **Escalate**.

---

### Part F – System topics (5 min)

1. Open **Topics** → **System** → **Conversation Start** and change the greeting to:
   `Hi, I'm the Northwind Helpline. I can answer questions about your service, or take a fault report. What can I help with?`
2. Open **Escalate** and change its message to explain how to reach the human team: `I'm passing you to our duty team. You can also call the hotline on your service plan at any time.`
3. Look at **Fallback**: it runs when nothing matches. Leave it as is.

---

### Part G – Publish to a website (10 min)

1. Select **Publish** → **Publish**.
2. Go to **Channels** → **Demo website** (or **Web app** / **Custom website**). Copy the link or the embed code.
3. Open the demo site and run your Part E test conversation as a customer would.
4. Look at the other channels on the list (Teams and Microsoft 365, SharePoint, WhatsApp, mobile and more). The standard harness supports a wider set than the new harness.

> ⚠️ **Authentication:** a public website helpline typically uses **No authentication**. That's exactly why you limited its knowledge and tools. An internal agent should use **Microsoft Entra ID** authentication.

---

## 5. Which harness when? 🧩

| | **GitHub Copilot harness** (Agent / Workflow / App cards) | **Standard harness** (Other ways to build) |
| --- | --- | --- |
| How you author | Describe it; components panel (Instructions, Knowledge, Tools, Skills, Model, Memory) | Topics, nodes, entities, variables, plus generative orchestration |
| Conversation control | The model plans each turn; **Hooks** run workflows at lifecycle points | You design exact paths; topics can be fully deterministic |
| Reusable behaviours | **Skills** | Prompts, topics |
| Custom entities and validation | Not supported | Supported (you used a regex entity) |
| MCP | Add MCP server in **Tools** | **MCP onboarding wizard**, with per-tool on/off switches |
| Channels | Microsoft 365 / Teams, websites | Wider: plus SharePoint, WhatsApp, contact centre and more |
| Authentication | Entra ID or anonymous | Entra ID, anonymous, manual/custom |
| Best for | Knowledge workers, internal copilots, complex reasoning with tools | Customer-facing flows, regulated conversations, specific channels |

**Rule of thumb:** if you can describe *what good looks like* but not *every step*, use the **new harness**. If compliance, data capture or the channel require *specific steps*, use the **standard harness**. Many organisations run both, as Northwind now does.

> Agents can't be moved between harnesses after creation, so choose deliberately.

---

## 6. 🏆 Challenge (optional)

1. **Work order status topic:** add a topic "Check my work order" that asks for a work order number (regex entity `WO-\d+`), reads the `Work Order` row from Dataverse with a connector tool, and shows **Status** and **Created On** on an adaptive card. It must not show the parts cost.
2. **Customer Assist Agent:** create a second agent from the **Customer Assist Agent** option. Compare what it gives you out of the box with what you built by hand. What would you reuse?
3. **Prebuilt MCP:** under **Tools** → **Model Context Protocol**, browse the prebuilt Microsoft MCP servers (for example, Dataverse). Which one could replace your challenge 1 topic, and what would you have to lock down first?

---

## 7. Wrap-up: the whole Northwind solution

| Lab | Card | What it does for Northwind |
| --- | --- | --- |
| 1 | Agent | Internal Service Desk Agent: manuals + MCP live data + skills |
| 2 | Workflow | Fault emails become diagnosed, approved work orders automatically |
| 3 | App | Dispatchers see and act on work orders |
| 4 | Other ways to build | Customers self-serve on the website, with tightly limited tools |

**One MCP server, four tools, two agents, two levels of access.** That's MCP done well.

**Clean up:** stop the MCP server and tunnel; unpublish the demo website if you shared its link.

## 8. Troubleshooting

| Problem | Fix |
| --- | --- |
| Wizard can't connect to the MCP server | Same checks as Lab 1: `/mcp` suffix, tunnel public, server running, header name `x-api-key`. |
| The topic never triggers | Improve the trigger description; check other topics don't overlap; look at the activity map to see what the orchestrator picked. |
| The regex entity rejects valid IDs | The pattern is case-sensitive. Try `(?i)AST-\d{4}`, or ask customers to use capitals. |
| The helpline reveals stock or technicians | In the MCP server's **Tools** settings, check **Allow all** is off and only `get_asset` is on. |
| Adaptive card shows `${varAssetID}` literally | Switch the card to formula mode, or check the variable names match. |
