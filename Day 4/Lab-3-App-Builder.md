# Lab 3 – Build the Work Order Console App

> **Home page card:** **App (preview)** (GitHub Copilot harness) · **Time:** about 60 minutes · **Level:** Beginner

---

## 1. Introduction

Your workflow from Lab 2 is now filling Dataverse with work orders. Dispatchers still need somewhere to **see, filter and act** on them. In this lab you'll describe that app in plain language and let Copilot Studio **generate a full working app**, then refine it by chatting, look at the code it wrote, and publish it to your team.

**What you'll learn to do:**

- Create an app from the **App (preview)** card with a natural-language brief
- Connect it to your **Dataverse** `Work Order` table
- Improve it with follow-up prompts: layout, filters, actions, branding
- **Preview** the app and **review the generated code**
- **Publish** and **share** it, and know where users and IT find it

### Why this matters 🧩

Agents **reason**, workflows **run processes**, and apps give people a **screen to work on**. The App builder writes a real, full-stack app (with source control and versioning) from your description. You stay in charge of *what* it should do and *whether it's right*.

> ⚠️ **Preview feature:** App building is rolling out by environment and uses Copilot Credits. Generated apps differ from run to run, so judge your app against the **checklist**, not your neighbour's screen.

---

## 2. Prerequisites

- Lab 2 complete, with the **Work Order** Dataverse table containing at least 8 rows
- **App (preview)** visible on your Copilot Studio Home page
- Your **Northwind Service Desk Agent** published (for the optional challenge)

---

## 3. Scenario

Huda, the dispatch lead in Dubai, starts every shift asking three questions: *What's critical? What's waiting for me to approve? Who's assigned to what?* Right now she answers them by scrolling a spreadsheet. Build her the **Work Order Console**.

---

## 4. Exercise

### Part A – Write the brief (5 min)

Good apps start with a good brief. Before you open the builder, read this one and notice its four parts: **users**, **data**, **screens**, **actions**.

```text
Build an app called "Work Order Console" for Northwind Field Service dispatchers.

Users: dispatchers and the dispatch lead.

Data: use the Dataverse table "Work Order" (columns: Work Order Number, Asset ID, Customer, City, Model, Symptom, Priority, Status, Assigned Technician, Parts Needed, Parts Cost USD, Created On).

Screens:
1. A dashboard with 4 summary tiles: Open work orders, P1 - Critical, Awaiting approval, Completed this week.
2. A work order list, newest first, with filters for City, Priority and Status and a search box. Show Priority as a coloured badge: P1 red, P2 amber, P3 grey.
3. A detail panel for the selected work order showing all fields.

Actions on the detail panel:
- "Assign technician": pick a name and set Status to Assigned.
- "Approve" and "Reject" buttons, only visible when Status is "Awaiting approval". Approve sets Status to Approved; Reject asks for a reason and sets Status to Rejected.
- "Mark completed".

Rules: if Parts Cost USD is over 500, show a warning "Service Manager approval required" on the detail panel.
```

---

### Part B – Generate the app (10 min)

1. In Copilot Studio, on **Home**, select **App (preview)**.
2. Paste the brief and send it.
3. Watch Copilot plan and build. It may ask **clarifying questions** (for example, which table, or whether users can edit records). Answer them.
4. When the build finishes, open the **preview** of the app.

✅ **Checkpoint:**

- [ ] The dashboard shows four tiles with **real numbers** from your table (P1 - Critical should be at least 2)
- [ ] The list shows your Dataverse rows, including any your Lab 2 workflow created
- [ ] Filtering by **City = Riyadh** shows only Riyadh rows

> 💡 If the app shows **sample data** instead of your table, prompt: `Connect the app to my Dataverse table "Work Order" instead of sample data.`

---

### Part C – Refine by conversation (15 min)

Send these prompts **one at a time** and preview after each. That's how real app building works: small, testable changes.

1. **Fix what's wrong first.** If anything in the checklist above failed, describe it plainly, for example:
   `The P1 tile shows 0 but there are two P1 - Critical rows. Count rows where Priority starts with "P1".`
2. **The approval rule:**
   `Open WO-5008. It costs 610 USD, so the Service Manager warning should show. Make the warning a red banner at the top of the detail panel.`
3. **Branding:**
   `Apply Northwind branding: primary colour teal #0B5C6B, white background, rounded cards, and the title "Northwind · Work Order Console" in the header.`
4. **A dispatcher's wish:**
   `Add a "My city" setting at the top. When set, every screen shows only that city's work orders. Remember the choice for the user.`
5. **Mobile:**
   `Make the list and detail panel work well on a phone screen: list first, tap to open details.`

✅ **Checkpoint:**

- [ ] Approving **WO-5003** changes its Status to **Approved**, and the change is visible in the Dataverse table in Power Apps
- [ ] The red approval banner shows on **WO-5008** but not on **WO-5004**
- [ ] The app works at phone width

🧩 **Iterate small.** One change per prompt makes it easy to see what broke and to undo it. "Make it better" gives the builder nothing specific to do.

---

### Part D – Look under the hood (10 min)

1. Open the app's **code** view.
2. Find, without changing anything:
   - where the app reads the `Work Order` table
   - the code behind the **Approve** button
   - where the badge colours for P1 / P2 / P3 are set
3. Ask the builder to explain one piece:
   `Explain in plain English what happens when the Approve button is pressed, step by step.`

🧩 **Why read code you didn't write?** You're accountable for what the app does. Being able to check *"does Approve really only update one row?"* is part of responsible app building. Generated apps also support source control and versioning, so changes can be reviewed like any other software.

---

### Part E – Publish and share (10 min)

1. Select **Publish**. Name the version, for example `v1.0 – first dispatcher release`.
2. **Share** the app with a colleague or a test account, as a **user**, not a co-owner.
3. Open the app the way users will: through the share link, or from **managedapps.cloud.microsoft.com**.
4. Make one more change in the builder (for example, add a "Created On" column). Notice that **users keep seeing v1.0** until you publish again. That's version isolation.

> 💡 **For IT:** published apps appear in the **Microsoft 365 admin center** for governance. Your organisation's Entra identity, data policies and connector policies apply automatically.

---

## 5. 🏆 Challenge (optional)

1. **Bring in the agent.** Ask the builder:
   `Add an "Ask the Service Desk Agent" button on the detail panel that opens a chat with the Northwind Service Desk Agent, pre-filled with the asset ID and symptom.`
   If your tenant doesn't support embedding the agent yet, have the button open the agent in Teams instead.
2. **Technician view.** Ask for a second screen showing only the signed-in technician's assigned jobs, with a "Start job" and "Completed" button.
3. **Chart.** Add a bar chart of open work orders by city and priority to the dashboard.

---

## 6. Wrap-up

| You did | Concept |
| --- | --- |
| Wrote a 4-part brief | Users · Data · Screens · Actions |
| Generated an app on Dataverse | **Natural-language app generation** |
| Refined in small prompts | **Iterative building** and testing |
| Reviewed the generated code | **Accountability** for AI-written software |
| Published and shared versions | **Version isolation** and governance |

**You now have the full Northwind solution:** emails become work orders (Lab 2), the agent diagnoses (Lab 1), and dispatchers act in the app (Lab 3). Lab 4 adds the customer-facing channel using the standard harness.

## 7. Troubleshooting

| Problem | Fix |
| --- | --- |
| No **App (preview)** card | It's rolling out by environment. Ask your admin, or try a different environment. |
| App can't find the table | Check the app and the table are in the **same environment**, and the table is named `Work Order`. |
| Buttons don't save changes | Prompt: `Make Approve, Reject, Assign and Mark completed update the Dataverse row and refresh the list.` |
| The builder made an unwanted big change | Ask it to undo the last change, or restore the previous version. |
