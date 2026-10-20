# Lab 2 – Automate Fault Intake with a Workflow

> **Home page card:** **Workflow** (GitHub Copilot harness) · **Time:** about 90 minutes · **Level:** Beginner to intermediate

---

## 1. Introduction

In Lab 1 a person **chatted** with the agent. Most fault reports don't arrive in a chat, though. They arrive as **emails at 2 a.m.**, so in this lab nobody has to start the work.

You'll build a **workflow** that runs whenever a fault email arrives. It pulls out the key details, classifies the urgency, asks your **Service Desk Agent** for a diagnosis, stops for **human approval** on critical jobs, creates a **work order in Dataverse**, and replies to the customer. Then you'll turn a workflow into a **tool** the agent can call itself.

**What you'll learn to do:**

- Create a workflow from the **Workflow** card and use a **connector trigger**
- Use AI nodes: **Extract** (pull fields from text), **Classify** (pick a category) and **Agent** (run your Lab 1 agent)
- Add a **condition** and a **human review** step
- Write to **Dataverse** and reply by **email**
- Test individual nodes and full runs, and read the **Activity** panel
- Add a workflow to an agent as a **tool** (*When an agent calls the flow* → *Respond to the agent*)

### Agent vs workflow, in one line 🧩

**Agents decide what to do next. Workflows follow the steps you designed.** The best solutions combine both: a predictable workflow that calls an agent where judgement is needed.

---

## 2. Prerequisites

- Lab 1 complete. The **Northwind Service Desk Agent** must be **published**, with its MCP server running.
- An Outlook mailbox you can send email to and from
- Lab files: `lab-files/dataverse/WorkOrders.csv`, `lab-files/emails/*.txt`

---

## 3. Scenario

Northwind's customers email `service@…` with "[Fault]" in the subject. Today a coordinator reads each one, works out what it's about, looks things up and types a work order, so night-time emails wait until 9 a.m. The hospital whose generator failed at 3 a.m. didn't appreciate that.

Your workflow will process every fault email in about a minute. A **human still approves every critical job** before a truck rolls.

```
 When a new email arrives ("[Fault]")
        │
        ▼
 Extract ─▶ asset ID, customer, contact, phone, city, symptom
        │
        ▼
 Asset ID found? ── no ──▶ Email: "Please send your asset ID"  ■
        │ yes
        ▼
 Classify ─▶ P1 - Critical / P2 - High / P3 - Normal
        │
        ▼
 Agent: Northwind Service Desk Agent ─▶ Fault Diagnosis Report
        │
        ▼
 P1? ── yes ──▶ Human review (dispatcher approves)
        │                │ approved
        ▼                ▼
 Dataverse: add Work Order row ─▶ Email reply to customer  ■
```

---

## 4. Exercise

### Part A – Create the Work Orders table in Dataverse (10 min)

The workflow writes work orders to **Dataverse**, and Lab 3's app reads them.

1. Go to **https://make.powerapps.com** and select the **same environment** you use in Copilot Studio.
2. Select **Tables** → **New table** → **Import** → **Import an Excel file or .CSV**, and choose `WorkOrders.csv`.
3. Check the column types Copilot proposes:
   - **Work Order Number** → primary name column (text)
   - **Parts Cost USD** → number (or currency)
   - **Created On** → date only
   - **Priority** and **Status** → text is fine (choice columns are a bonus)
4. Name the table **`Work Order`** and select **Save and exit**.
5. Open the table. ✅ You should see **8 rows** (WO-5001 to WO-5008).

---

### Part B – Create the workflow and its trigger (10 min)

1. In Copilot Studio, on **Home**, select the **Workflow** card. The designer opens on the **Build** tab.
2. Name it `Fault Email Intake`.
3. Select the trigger card and change it from **manual** to a **connector trigger**: search **Office 365 Outlook** → **When a new email arrives (V3)**.
4. Sign in to create the connection, then set:
   - **Folder:** Inbox
   - **Subject Filter:** `[Fault]`
   - **Include Attachments:** No
5. Select the **Save** icon.

> 💡 For classroom testing, everyone sends the sample emails **to themselves**, so each learner's workflow only sees their own test emails.

---

### Part C – Extract the details (10 min)

1. Below the trigger, select **Add a step** → search **Extract** → add the **Extract** node.
2. **Input:** select the email **Body** from the trigger (use the dynamic content / token picker).
3. Define the fields to extract:

| Field name | Description (helps the AI) |
| --- | --- |
| `AssetID` | Northwind asset ID in the format AST-####. Leave empty if not stated. |
| `Customer` | The customer's organisation name |
| `ContactName` | Person who sent the report |
| `Phone` | Contact phone number |
| `City` | City of the site (Pune, Chennai, Dubai or Riyadh) |
| `Symptom` | One-sentence description of the problem, including any fault code |

4. Open the node's **Test** tab, paste the body of `email-1-urgent.txt` as a sample input, and select **Run**.
   ✅ You should get `AssetID = AST-2001`, `City = Pune`, `Symptom` mentioning **G11**.
5. Test again with `email-3-missing-asset.txt`. ✅ `AssetID` should be **empty**, not invented.

🧩 **Extract** turns unstructured text into named values that every later step can use, just as you'd do for invoices and contracts.

---

### Part D – Handle the missing asset ID (5 min)

1. **Add a step** → **Condition**.
2. Rule: `AssetID` (from Extract) **is equal to** *(empty)*.
3. In the **True** branch, add **Office 365 Outlook → Send an email (V2)**:
   - **To:** the trigger's **From**
   - **Subject:** `Re: ` + trigger **Subject**
   - **Body:**

     ```text
     Hello <ContactName>,
     Thanks for reporting this. To send the right technician, we need the asset ID – it's printed on the silver label inside the service door and looks like AST-1234. Please reply with it and we'll act immediately.
     If anyone is in danger, call your Northwind hotline now.
     – Northwind Field Service
     ```

4. Build the remaining steps in the **False** branch.

---

### Part E – Classify and diagnose (15 min)

#### Classify

1. In the False branch: **Add a step** → **Classify**.
2. **Input:** the `Symptom` and `Customer` values from Extract.
3. **Categories** (name + description):

| Category | Description |
| --- | --- |
| `P1 - Critical` | Safety risk (smoke, fire, burning smell, gas, fuel leak, shock, injury) OR a hospital or data-centre generator that fails to start OR total loss of cooling at a hospital |
| `P2 - High` | Equipment not working, no safety risk |
| `P3 - Normal` | Equipment still working but noisy or degraded, or a general question |

4. Test the node with the symptoms from emails 1 and 2. ✅ Email 1 should be **P1 - Critical** and email 2 **P3 - Normal**.

#### Agent

1. **Add a step** → **Agent** → choose **Northwind Service Desk Agent**.
2. **Prompt / message to the agent:**

```text
Create a Fault Diagnosis Report for this fault email.
Asset ID: <AssetID>
Customer: <Customer>
City: <City>
Reported symptom: <Symptom>
Priority assigned by intake: <Classify category>
Return the report table only.
```

(Insert each `< >` value with the token picker.)

3. Test the node with the values from email 1.
   ✅ The report should mention **PG-BAT-12** (battery) for **G11**, show the asset is **out of warranty since 2025-09-01**, and suggest a Pune technician (**Arjun Mehta**).

🧩 **The workflow owns the process; the agent supplies the judgement.** Every run follows the same steps in the same order, which is what auditors like. The agent is only used where reasoning is needed.

---

### Part F – Human review for critical jobs (10 min)

1. **Add a step** → **Condition**: Classify category **is equal to** `P1 - Critical`.
2. In the **True** branch: **Add a step** → **Human review** (it may be called *Request approval* or *Human in the loop*).
   - **Assigned to:** your own email address (you're the duty dispatcher)
   - **Title:** `P1 approval – <Customer> – <AssetID>`
   - **Details:** the agent's report output
   - **Options:** `Approve dispatch` / `Reject`
3. Continue only if the outcome is **Approve dispatch**. If it's **Reject**, send yourself a note and stop.
4. Make sure **both** branches (P1 approved, and not P1) continue to Part G. Add Part G's steps after the condition, or duplicate them in each branch.

> ⚠️ **Why a person approves P1s:** P1s involve safety or critical infrastructure, and often out-of-hours call-out costs. The AI recommends; a named person decides. The approval record is your audit trail.

---

### Part G – Create the work order and reply (10 min)

1. **Add a step** → **Microsoft Dataverse** → **Add a new row**. **Table:** `Work Orders`.

| Column | Value |
| --- | --- |
| Work Order Number | expression `concat('WO-', formatDateTime(utcNow(),'MMddHHmmss'))` |
| Asset ID | `AssetID` |
| Customer | `Customer` |
| City | `City` |
| Symptom | `Symptom` |
| Priority | Classify category |
| Status | `New` (or `Approved` in the P1-approved path) |
| Created On | `utcNow()` |

2. **Add a step** → **Office 365 Outlook** → **Send an email (V2)** to the trigger's **From**:
   - **Subject:** `Northwind work order <Work Order Number> – <AssetID>`
   - **Body:** a short acknowledgement with the work order number. Add a promise to call within the response time of their service plan, but **no costs and no part numbers**.
3. **Save**, then **Publish**. Fix anything flagged in red in the **health center** first.

---

### Part H – Test end to end (10 min)

1. Open the three files in `lab-files/emails/` and send each one **to yourself** with the subject and body shown.
2. In the workflow, open the **Activity** panel and select **Refresh**. You should see three runs.
3. Open each run and follow its path:

| Email | Expected path |
| --- | --- |
| 1 – Generator failed to start | Extract ✔ → **P1** → Agent → **Human review waits** → approve it → Dataverse row → reply |
| 2 – Grinding noise | Extract ✔ → **P3** → Agent → Dataverse row → reply (no approval) |
| 3 – Cold room, no asset ID | Extract (AssetID empty) → **ask for asset ID** email → stop |

4. Approve the P1 request (in Outlook, Teams or the approvals centre, wherever it arrived). Watch the run change from **Waiting** to **Succeeded**.
5. ✅ Open the **Work Order** table in Power Apps. You should have **2 new rows**.

> 💡 Use **Test this node** with **Load values from previous run** to debug a single step without sending another email.

---

### Part I – Give the agent a workflow as a tool (10 min)

Now the reverse direction: the **agent** calls a **workflow**. Dispatchers chatting with the agent will be able to say *"log that as a work order"*.

1. Open **Northwind Service Desk Agent** → **Build** → **Tools** → **Add a tool** → **Add** → **Workflow**.
2. The designer opens with **When an agent calls the flow** and **Respond to the agent**.
3. On **When an agent calls the flow**, add the inputs `AssetID`, `Symptom`, `Priority` and `PartsNeeded` (all text).
4. In between, add **Dataverse → Add a new row** (Work Orders), mapping the inputs, with Status `New` and the same Work Order Number expression.
5. On **Respond to the agent**, return `WorkOrderNumber` = the new row's Work Order Number.
6. Name the workflow `Create work order` with the description:
   `Creates a new Northwind work order in Dataverse for an asset after a diagnosis. Use when the user asks to log, raise or create a work order or job.`
7. **Save** → **Publish**, and return to the agent.
8. In **Preview**:

```text
Diagnose AST-3001 – the thermostat display is blank. Then raise a work order for it.
```

✅ The activity trace shows the MCP tools, then **Create work order**, with the arguments and the returned **WO-…** number.

---

## 5. 🏆 Challenge (optional)

1. **Copilot node (preview):** after the Agent step, add a **Copilot** node that asks **Researcher** for any public safety notices about the reported equipment type, and include a one-line summary in the human review details.
2. **Attachments:** customers often send a photo or a PDF service sheet. Turn on **Include Attachments** and use **Extract** on a PDF attachment.
3. **Scheduled workflow:** create a second workflow on a **Recurrence** trigger (daily, 07:00) that emails you all **P1** work orders still marked `New`.

---

## 6. Wrap-up

| You built | Concept |
| --- | --- |
| Email trigger with a subject filter | **Event-driven** automation |
| Extract and Classify nodes | AI that turns text into **structured data** |
| Agent node | The workflow **calls an agent** for judgement |
| Condition + Human review | **Human in the loop** for high-risk steps |
| Dataverse row + email | Systems of record and closing the loop with the customer |
| Workflow as a tool | The agent **calls a workflow** for reliable actions |

## 7. Troubleshooting

| Problem | Fix |
| --- | --- |
| Workflow never starts | Check the subject contains exactly `[Fault]`, the workflow is **published**, and the email reached the **Inbox** folder. |
| Agent node fails | The agent must be **published**, and its MCP server must be running and reachable. |
| Extract invents an asset ID | Strengthen the field description: "Leave empty if not stated. Never guess." |
| Can't publish | Open the **health center** banner and fix the red items. |
| Dataverse step errors on Created On | Make sure the column is Date/Time or Date only, and pass `utcNow()`. |
