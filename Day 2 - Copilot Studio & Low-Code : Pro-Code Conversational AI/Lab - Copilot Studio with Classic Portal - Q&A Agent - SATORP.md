# Lab – Build and Publish the SATORP Q&A Agent Assistant in Copilot Studio (Classic)

> **Experience:** Copilot Studio **classic / standard** authoring (topics, nodes, knowledge, channels)
> **Time:** about 2 hours · **Level:** Beginner · **No coding needed**
> **Outcome:** a published Q&A assistant with menus, buttons, adaptive cards and grounded answers, live on a website and in Microsoft Teams

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Prerequisites](#2-prerequisites)
3. [Scenario](#3-scenario)
4. [Architecture at a Glance](#4-architecture-at-a-glance)
5. [Exercise](#5-exercise)
   - [Part A – Create the agent in the classic experience](#part-a--create-the-agent-in-the-classic-experience-10-min)
   - [Part B – Add knowledge sources](#part-b--add-knowledge-sources-15-min)
   - [Part C – Interactive welcome menu](#part-c--interactive-welcome-menu-15-min)
   - [Part D – "About SATORP" adaptive card](#part-d--about-satorp-adaptive-card-15-min)
   - [Part E – "Careers" guided conversation](#part-e--careers-guided-conversation-15-min)
   - [Part F – "Ask a workplace question" with generative answers](#part-f--ask-a-workplace-question-with-generative-answers-15-min)
   - [Part G – Fallback, escalation and feedback](#part-g--fallback-escalation-and-feedback-10-min)
   - [Part H – Safety settings](#part-h--safety-settings-5-min)
   - [Part I – Test like a user](#part-i--test-like-a-user-10-min)
   - [Part J – Publish to a website and Microsoft Teams](#part-j--publish-to-a-website-and-microsoft-teams-15-min)
6. [Challenge](#6-challenge-optional)
7. [Wrap-up](#7-wrap-up)
8. [Troubleshooting](#8-troubleshooting)
9. [Appendix A – Sample knowledge document](#appendix-a--sample-knowledge-document-training-content)
10. [Appendix B – Adaptive card JSON](#appendix-b--adaptive-card-json)

---

## 1. Introduction

In this lab you'll build a **Q&A Agent Assistant for SATORP** from a blank agent and publish it, using the **classic (standard) Copilot Studio authoring experience**.

The assistant answers questions about SATORP from **SATORP's public website** and from **internal Q&A content**. It's built to be **interactive**, so users don't just get walls of text:

| Interactive element | Where you build it |
| --- | --- |
| **Quick-reply menu buttons** | Welcome menu (Part C) |
| **Adaptive card** with facts and link buttons | About SATORP (Part D) |
| **Guided, branching questions** | Careers (Part E) |
| **Grounded generative answers** with citations | Ask a workplace question (Part F) |
| **Feedback buttons** and **escalation** | Wrap-up and fallback (Part G) |

**What you'll learn to do:**

- Create an agent in the classic Copilot Studio experience
- Add **public website** and **document** knowledge sources
- Build **topics** with **trigger phrases**, **question nodes**, **conditions** and **variables**
- Send **quick replies** and **adaptive cards**
- Use the **Create generative answers** node and **system topics**
- Configure **content moderation** and knowledge restrictions
- **Publish** to a **demo website**, a **custom website** and **Microsoft Teams**

---

## 2. Prerequisites

- [ ] A Microsoft 365 work account with access to **Copilot Studio** (https://copilotstudio.microsoft.com)
- [ ] A **Power Platform environment** where you can create agents (developer or sandbox environment recommended)
- [ ] Permission to publish to **Microsoft Teams** (some tenants require admin approval)
- [ ] The **sample knowledge document** from [Appendix A](#appendix-a--sample-knowledge-document-training-content), saved as `SATORP_Workplace_QA_Sample.docx`

> ⚠️ **About the content in this lab**
> - Facts about SATORP come from SATORP's and TotalEnergies' **public websites**. Re-check them before any production release.
> - The workplace Q&A document in Appendix A is **training sample content only**. It is **not** an official SATORP policy. For a real deployment, replace it with **SATORP-approved** documents (for example from SharePoint), owned by the right department.
> - Use of the SATORP name and logo in a published agent should be approved by SATORP Corporate Communications.

---

## 3. Scenario

SATORP (Saudi Aramco Total Refining and Petrochemical Company) runs a full-conversion refinery in **Jubail Industrial City**. Every week the communications, HR and IT teams answer the same questions from candidates, contractors, visitors and new employees:

- *"Who owns SATORP?"* · *"Where is the refinery?"*
- *"How do I apply for a job?"*
- *"What do I need to bring on my first day?"* · *"How do I reset my password?"*

Your job is to build a **SATORP Q&A Assistant** that answers these instantly, **only** from approved sources, and **hands over to a human** when it can't help.

---

## 4. Architecture at a Glance

```
  Users                       SATORP Q&A Assistant (Copilot Studio – classic)
  ─────                       ─────────────────────────────────────────────────
  Website visitor ──┐         Conversation Start ─▶ Main Menu (quick replies)
                    ├──────▶      ├─▶ About SATORP  ─▶ adaptive card + link buttons
  Teams employee  ──┘             ├─▶ Careers       ─▶ branching questions + card
                                  ├─▶ Workplace Q&A ─▶ Create generative answers
                                  └─▶ Contact       ─▶ card with contact links
                              System topics: Conversational boosting · Fallback ·
                                             Escalate · End of Conversation (CSAT)
                                              │ grounded on
                              ┌───────────────┴─────────────────────────────────┐
                              │ Knowledge                                       │
                              │  • Public website: https://www.satorp.com/en    │
                              │  • File: SATORP_Workplace_QA_Sample.docx        │
                              └─────────────────────────────────────────────────┘
```

---

## 5. Exercise

### Part A – Create the agent in the classic experience (10 min)

1. Go to **https://copilotstudio.microsoft.com** and sign in.
2. In the top-right **environment** picker, choose your lab environment.
3. On the **Home** page, select **Other ways to build** and choose to build with **standard orchestration** (the classic experience).
   *In older tenants, select **Create** → **New agent** → **Skip to configure**.*
4. Fill in the agent details:

| Field | Value |
| --- | --- |
| **Name** | `SATORP Q&A Assistant` |
| **Description** | `Answers questions about SATORP, careers and workplace topics from approved sources, and guides users to the right page or team.` |
| **Primary language** | English |

5. In **Instructions**, paste:

```text
You are the SATORP Q&A Assistant.
- Answer questions about SATORP (Saudi Aramco Total Refining and Petrochemical Company) using only the knowledge sources configured for this agent.
- Be professional, friendly and concise. Prefer short answers with bullet points.
- Always include the source link when you answer from the website.
- If the answer is not in your knowledge sources, say you don't know and offer the Main Menu or a human contact. Never guess.
- Never share personal data, salaries, internal financial results or confidential operational details.
- For safety emergencies, tell the user to follow site emergency procedures and contact site emergency services immediately.
```

6. Select **Create**. Wait for the agent to be provisioned. You land on the **Overview** page.
7. Go to **Settings** → **Generative AI** and confirm **Orchestration** is set to **generative** (Copilot Studio picks topics, knowledge and tools from their descriptions). Leave it on for this lab.

> 🧩 **Classic topics + generative orchestration:** you still design topics with nodes, exactly as in classic Copilot Studio. Generative orchestration just makes topic selection smarter by reading each topic's description, not only its trigger phrases.

---

### Part B – Add knowledge sources (15 min)

#### 1. SATORP public website

1. Go to the **Knowledge** tab → **Add knowledge** → **Public websites**.
2. Enter `https://www.satorp.com/en` and select **Add**.
   *Copilot Studio searches up to two levels below the URL you enter, so this covers pages such as `/en/about`, `/en/business`, `/en/sustainability`, `/en/careers` and `/en/contact`.*
3. **Name:** `SATORP public website`
   **Description:** `Official public information about SATORP: company overview, shareholders, refinery, business, sustainability, careers, news and contact details.`
4. Select **Add**.

#### 2. Sample workplace Q&A document

1. Create `SATORP_Workplace_QA_Sample.docx` in Word by copying the text in [Appendix A](#appendix-a--sample-knowledge-document-training-content).
2. **Knowledge** → **Add knowledge** → **Files** → upload it.
3. **Name:** `Workplace Q&A (sample)`
   **Description:** `Training sample answers for new joiners and visitors: first day, site access, PPE basics, IT accounts and password reset, working hours, who to contact.`
4. Wait until the status shows **Ready**.

> 💡 **In production**, use **SharePoint** instead of uploaded files (**Add knowledge** → **SharePoint**), so the agent always uses the latest approved version and respects document permissions.

#### 3. Quick test

Open the **Test your agent** pane (top right) and ask:

```text
Where is SATORP located and who are its shareholders?
```

✅ Expected: **Jubail Industrial City**, Eastern Province, Saudi Arabia; shareholders **Saudi Aramco** and **TotalEnergies**, with a **citation link** to satorp.com.

---

### Part C – Interactive welcome menu (15 min)

You'll replace the default greeting with a **Main Menu** of quick-reply buttons.

#### 1. Create the Main Menu topic

1. Go to **Topics** → **Add a topic** → **From blank**.
2. Rename it (top left) to `Main Menu`.
3. In the **Trigger** node, add the description `The user wants to see what the assistant can help with, the menu, or the options.`, and these trigger phrases:
   - `menu`
   - `main menu`
   - `what can you do`
   - `help`
   - `show options`
4. Select **+** → **Ask a question**. Enter:
   `How can I help you today? Choose an option or type your question.`
5. **Identify:** **Multiple choice options**. Add the options:
   - `About SATORP`
   - `Careers`
   - `Workplace questions`
   - `Contact SATORP`
6. **Save user response as:** rename the variable to `varMenuChoice`.
7. The node creates one **condition branch per option**. In each branch, add **Topic management** → **Go to another topic**:

| Branch | Go to topic |
| --- | --- |
| About SATORP | `About SATORP` (create in Part D, then come back and link it) |
| Careers | `Careers` (Part E) |
| Workplace questions | `Workplace Q&A` (Part F) |
| Contact SATORP | `Contact SATORP` (below) |

8. Select **Save**.

#### 2. Make the greeting show the menu

1. **Topics** → **System** → open **Conversation Start**.
2. Edit the message to:

```text
Marhaba! 👋 I'm the SATORP Q&A Assistant.
I can tell you about SATORP, help with careers, and answer common workplace questions.
```

3. Below the message, add **Topic management** → **Go to another topic** → `Main Menu`.
4. **Save**.

#### 3. Contact SATORP topic (quick win)

1. **Add a topic** → **From blank** → name it `Contact SATORP`. Trigger phrases: `contact`, `phone number`, `email SATORP`, `how do I reach SATORP`, `address`.
2. **Send a message** → **Add** → **Adaptive card** and paste the **Contact card** JSON from [Appendix B](#b3-contact-card).
3. **Save**.

✅ **Checkpoint:** in the test pane select **Start over** (↻). The greeting appears, followed by **four buttons**. Click **Contact SATORP**: the contact card appears with an **Open contact page** button.

---

### Part D – "About SATORP" adaptive card (15 min)

1. **Add a topic** → **From blank** → `About SATORP`.
2. **Trigger** description: `The user asks about SATORP as a company: who it is, ownership, shareholders, location, refinery, capacity, history.`
   Trigger phrases:
   - `about SATORP`
   - `who owns SATORP`
   - `tell me about the company`
   - `where is the refinery`
   - `SATORP shareholders`
3. **Send a message** → **Add** → **Adaptive card**. Paste the **About SATORP card** JSON from [Appendix B](#b1-about-satorp-card).
4. Add **Ask a question**: `Would you like to know more?`
   - **Identify:** **Multiple choice options** → `Our business`, `Sustainability`, `Back to menu`
   - **Save as:** `varAboutNext`
5. In the branches:
   - **Our business** → **Advanced** → **Generative answers** (the **Create generative answers** node). **Input:** `What does SATORP's business include? Summarize the refinery and products.` **Data sources:** `SATORP public website`.
   - **Sustainability** → **Create generative answers** node. **Input:** `Summarize SATORP's sustainability and HSE commitments.` **Data sources:** `SATORP public website`.
   - **Back to menu** → **Go to another topic** → `Main Menu`.
6. **Save**, then go back to **Main Menu** and link the **About SATORP** branch.

✅ **Checkpoint:** type `who owns SATORP`. You should see a **card** with a title, key facts and two buttons (**Visit About page**, **Our Business**), then the follow-up choices.

> 🧩 **Why a card instead of plain text?** Cards give **consistent, approved wording** for facts that must not vary (ownership, location), plus **one-click actions**. Generative answers are better for open questions. Good agents mix both.

---

### Part E – "Careers" guided conversation (15 min)

1. **Add a topic** → **From blank** → `Careers`.
2. **Trigger** description: `The user asks about jobs, careers, vacancies, internships, graduate programmes or how to apply to SATORP.`
   Trigger phrases:
   - `jobs at SATORP`
   - `how do I apply`
   - `careers`
   - `internship`
   - `vacancies`
3. **Ask a question:** `Which describes you best?`
   - **Multiple choice options:** `Student or fresh graduate`, `Experienced professional`, `Current employee`
   - **Save as:** `varCandidateType`
4. In the branches, add **Send a message**:

| Branch | Message |
| --- | --- |
| Student or fresh graduate | `Great! SATORP publishes opportunities for students and graduates on its Careers page. Check eligibility, required documents and deadlines there.` |
| Experienced professional | `SATORP lists open positions on its Careers page. Prepare an updated CV and apply directly to the role that matches your experience.` |
| Current employee | `For internal vacancies and transfers, please check the internal HR portal or speak to your HR business partner.` |

5. After the branches merge, add **Send a message** → **Add** → **Adaptive card** → paste the **Careers card** from [Appendix B](#b2-careers-card).
6. Add **Ask a question** → `Anything else?` → options `Back to menu`, `No, thanks`.
   - **Back to menu** → **Go to another topic** → `Main Menu`
   - **No, thanks** → **Go to another topic** → **End of Conversation** (system topic, which asks for feedback)
7. **Save**, then link **Careers** from **Main Menu**.

✅ **Checkpoint:** `I want an internship` → **Careers** starts → choose **Student or fresh graduate** → the tailored message, then the card with the **Open Careers page** button.

> ⚠️ **Don't let the agent invent programmes or deadlines.** The topic only points to the official Careers page. Recruitment details change often and must come from HR.

---

### Part F – "Ask a workplace question" with generative answers (15 min)

1. **Add a topic** → **From blank** → `Workplace Q&A`.
2. **Trigger** description: `The user has a workplace question: first day, site access, safety equipment, IT account, password, working hours, who to contact internally.`
   Trigger phrases:
   - `workplace question`
   - `first day`
   - `reset my password`
   - `what PPE do I need`
   - `working hours`
3. **Ask a question:** `Sure – what's your question?`
   - **Identify:** **User's entire response** · **Save as:** `varQuestion`
4. Add **Advanced** → **Generative answers** (the **Create generative answers** node):
   - **Input:** select the variable `varQuestion`
   - Select **Edit** under **Data sources** → choose **only** `Workplace Q&A (sample)`
   - Turn **off** **Allow the AI to use its own general knowledge**
5. Add **Ask a question:** `Did that answer your question?` → options `Yes`, `No`.
   - **Yes** → **Send a message**: `Glad I could help! Type "menu" anytime to see more options.`
   - **No** → **Go to another topic** → **Escalate**
6. **Save**, then link **Workplace questions** from **Main Menu**.

✅ **Checkpoint:** select **Workplace questions** → ask `I forgot my password, what should I do?` → the answer comes from the sample document, **with a citation**, followed by the Yes/No buttons.

> 🧩 **Topic-level grounding:** this node is limited to the Workplace Q&A document, so a workplace question can't be answered from the public website. Scoping data sources per topic keeps answers accurate and auditable.

---

### Part G – Fallback, escalation and feedback (10 min)

#### Conversational boosting (fallback to knowledge)

1. **Topics** → **System** → open **Conversational boosting**. This is where the agent searches **all** knowledge when no topic matches.
2. Confirm its **Create generative answers** node uses **both** knowledge sources.

#### Fallback

1. Open **System** → **Fallback**.
2. Change the message to:

```text
Sorry, I couldn't find that in SATORP's approved information. 🙏
You can rephrase your question, type "menu" to see options, or ask to speak to a person.
```

#### Escalate

1. Open **System** → **Escalate** and change the message to:

```text
I'll connect you with the right team. Please use the Contact page or contact the SATORP team responsible for your request. For workplace issues, contact your supervisor or HR business partner.
```

2. Add **Go to another topic** → `Contact SATORP` to show the contact card.

#### End of Conversation (feedback)

1. Open **System** → **End of Conversation**. Keep the **satisfaction survey** (CSAT) node. It shows **rating buttons**, and the scores appear in **Analytics**.

---

### Part H – Safety settings (5 min)

1. **Settings** → **Generative AI**:
   - **Content moderation:** set to **High** for a public assistant.
   - Turn **off** **Use general knowledge** (agent-level) and **web search**. The assistant must answer only from SATORP sources.
2. **Settings** → **Security** → **Authentication**:
   - For the **public website** demo: **No authentication**.
   - For **Teams**: **Authenticate with Microsoft**.
   *(One agent can't use both at once. For a real deployment, create two agents, or publish the internal one to Teams only.)*

> ⚠️ **Least privilege:** a public, unauthenticated agent must never be connected to internal documents. In a real rollout, the **Workplace Q&A** content belongs only in the **Teams / authenticated** agent.

---

### Part I – Test like a user (10 min)

Select **Start over** (↻) before each scenario and keep the **activity map** open to see which topic or knowledge source ran.

| # | Type or click | Expected behaviour |
| --- | --- | --- |
| 1 | *(start)* | Greeting + **4 menu buttons** |
| 2 | **About SATORP** | Adaptive card with facts + **Visit About page** button |
| 3 | `What's the refining capacity?` | Answer from the website **with a citation** |
| 4 | `I'm looking for a job` | **Careers** topic → candidate-type buttons |
| 5 | **Workplace questions** → `What should I bring on my first day?` | Grounded answer from the sample doc + Yes/No |
| 6 | `What is the CEO's salary?` | Polite refusal (not in approved sources, confidential) |
| 7 | `What's the weather in Riyadh?` | Fallback: "couldn't find that in SATORP's approved information" |
| 8 | `I want to talk to a person` | **Escalate** → contact card |
| 9 | `No, thanks` at the end | **CSAT rating buttons** appear |

> 💡 If a test fails, open the **activity map**. It shows whether the wrong topic triggered (improve trigger phrases or the description) or the knowledge didn't contain the answer (improve the content).

---

### Part J – Publish to a website and Microsoft Teams (15 min)

#### 1. Publish

1. Select **Publish** (top right) → **Publish**. Wait for the confirmation.

#### 2. Demo website (quick share)

1. **Channels** → **Demo website**.
2. Add a welcome message: `Welcome to the SATORP Q&A Assistant – training demo.`
3. Add conversation starters: `Who owns SATORP?`, `How do I apply for a job?`, `What should I bring on my first day?`
4. **Save**, copy the link and open it in a new browser tab. Run test scenarios 1, 2 and 4.

#### 3. Custom website (embed)

1. **Channels** → **Web app** / **Custom website** → copy the **embed code** (an `<iframe>`).
2. Paste it into any HTML page, for example a test page on an intranet or a GitHub Pages site:

```html
<!-- Example: SATORP Q&A Assistant embedded in a page -->
<iframe src="PASTE-YOUR-COPILOT-STUDIO-URL-HERE"
        style="width:100%; height:600px; border:none;"
        title="SATORP Q&A Assistant"></iframe>
```

#### 4. Microsoft Teams and Microsoft 365 Copilot

1. Switch authentication to **Authenticate with Microsoft** (Part H) and **Publish** again.
2. **Channels** → **Teams and Microsoft 365 Copilot** → **Add channel**.
3. Select **Edit details** to add a short description, an icon (use an approved SATORP icon only) and the developer name.
4. Select **See agent in Teams** and test it in Teams.
5. To make it available to others: **Availability options** → **Share link**, **Show to my teammates and shared users**, or **Show to everyone in my org** (the last one needs Teams admin approval).

✅ **Final checkpoint:** the assistant works in **two channels**, shows the **menu buttons**, the **About card** and the **Careers card**, and answers workplace questions with citations.

#### 5. Monitor

Open **Analytics** after a few test conversations. Review **sessions**, **resolution / escalation rate**, **CSAT** and **topics**, and the **unanswered questions** to find gaps in the knowledge.

---

## 6. Challenge (optional)

1. **Arabic support:** **Settings** → **Languages** → add **Arabic**. Translate the greeting and the menu options (`عن ساتورب`, `الوظائف`, `أسئلة العمل`, `تواصل معنا`) and test with `ما هي ساتورب؟`.
2. **Suggested follow-ups:** after the generative answer in **Workplace Q&A**, add a quick-reply question with `Ask another question` / `Back to menu` so the user never hits a dead end.
3. **News card:** create a `Latest news` topic that uses **Create generative answers** scoped to the website to summarize the latest items from `https://www.satorp.com/en/media`, followed by an adaptive card button that opens the News & Media page.
4. **SharePoint switch:** replace the uploaded sample document with a SharePoint library of approved content, and confirm that answers still cite correctly.

---

## 7. Wrap-up

| You built | Concept |
| --- | --- |
| Agent from scratch in the classic experience | Classic authoring + generative orchestration |
| Website + document knowledge | **Grounded** answers with citations |
| Main Menu with buttons | **Quick replies** (multiple-choice question node) |
| About and Careers cards | **Adaptive cards** for approved facts and actions |
| Careers branching | **Question nodes, variables, conditions** |
| Workplace Q&A topic | **Create generative answers** scoped per topic |
| Fallback, Escalate, CSAT | **System topics** and a graceful hand-off |
| Moderation + authentication | **Safe, least-privilege** design |
| Demo site, embed, Teams | **Publishing** to multiple channels |

---

## 8. Troubleshooting

| Problem | Fix |
| --- | --- |
| Website answers are empty | Check the URL has **no query string** and is at most two levels deep (`https://www.satorp.com/en`). Allow time for indexing, then test with a question whose answer is on the About page. |
| Adaptive card shows an error | Validate the JSON at https://adaptivecards.io/designer, and keep `"version": "1.5"` or lower. |
| Card buttons do nothing in the test pane | `Action.OpenUrl` opens a new tab. Check your browser's pop-up blocker. |
| The wrong topic triggers | Make trigger phrases more distinct, improve topic **descriptions**, and check the activity map. |
| Menu buttons don't route | Check each condition branch in **Main Menu** has a **Go to another topic** node pointing to an existing topic. |
| Teams says "admin approval required" | Your Teams admin must approve the agent in the Teams admin center. Use **Share link** for testing meanwhile. |
| Agent answers from general knowledge | Turn off general knowledge and web search in **Settings** → **Generative AI**, and in each Create generative answers node. |

---

## Appendix A – Sample knowledge document (training content)

> Copy everything between the lines into a Word document and save it as **`SATORP_Workplace_QA_Sample.docx`**.
> **This is fictional training content. It is not an official SATORP policy.** Replace it with SATORP-approved content before any real use.

---

**SATORP Q&A Assistant – Workplace Q&A (TRAINING SAMPLE – NOT OFFICIAL POLICY)**

**1. What should I bring on my first day?**
Bring your national ID or Iqama, your offer letter, and two passport-size photographs. Report to the main reception at 7:00 AM, where the onboarding team will meet you and arrange your site access badge.

**2. How do I get site access?**
All employees, contractors and visitors need a valid access badge. New employees receive a temporary badge on day one and a permanent badge after completing site safety induction. Visitors must be pre-registered by their host at least 24 hours in advance.

**3. What personal protective equipment (PPE) do I need in the plant?**
Minimum PPE in process areas: safety helmet, safety glasses, flame-resistant coveralls, safety shoes and hearing protection where signs require it. Additional PPE depends on the task and is specified in the work permit. PPE is issued by the stores after induction.

**4. When is the safety induction?**
Safety induction is mandatory before entering any process area. It is scheduled during your first week. Your supervisor will confirm the date and time.

**5. How do I reset my password?**
Use the self-service password reset portal from any company computer, or call the IT Service Desk. Never share your password with anyone, including IT staff.

**6. What are the standard office working hours?**
Standard office hours are Sunday to Thursday, 7:00 AM to 4:00 PM. Shift workers follow their published shift roster.

**7. Who do I contact for HR questions?**
Contact your HR business partner, or raise a request in the HR self-service portal.

**8. What do I do in an emergency on site?**
Follow the site emergency procedures, raise the alarm, go to your designated assembly point and call the site emergency number shown on your badge. Never re-enter an area until the all-clear is given.

---

## Appendix B – Adaptive card JSON

> Paste each JSON into **Send a message** → **Add** → **Adaptive card**. You can preview and edit cards at https://adaptivecards.io/designer.
> Facts in the About card come from satorp.com and totalenergies.com (checked October 2026). Re-check them before release.

### B1. About SATORP card

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    {
      "type": "TextBlock",
      "text": "About SATORP",
      "size": "Large",
      "weight": "Bolder",
      "color": "Accent"
    },
    {
      "type": "TextBlock",
      "text": "Saudi Aramco Total Refining and Petrochemical Company",
      "isSubtle": true,
      "wrap": true,
      "spacing": "None"
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "Location", "value": "Jubail Industrial City, Eastern Province, Saudi Arabia" },
        { "title": "Shareholders", "value": "Saudi Aramco (62.5%) and TotalEnergies" },
        { "title": "Processing capacity", "value": "465,000 barrels per day of Arabian Heavy crude" },
        { "title": "Operational since", "value": "2014" }
      ]
    },
    {
      "type": "TextBlock",
      "text": "A full-conversion refining and petrochemical platform producing high-value fuels and petrochemicals.",
      "wrap": true
    }
  ],
  "actions": [
    { "type": "Action.OpenUrl", "title": "Visit About page", "url": "https://www.satorp.com/en/about" },
    { "type": "Action.OpenUrl", "title": "Our Business", "url": "https://www.satorp.com/en/business/" }
  ]
}
```

### B2. Careers card

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    { "type": "TextBlock", "text": "Careers at SATORP", "size": "Large", "weight": "Bolder", "color": "Accent" },
    {
      "type": "TextBlock",
      "text": "All current opportunities and application steps are published on the official Careers page.",
      "wrap": true
    },
    {
      "type": "TextBlock",
      "text": "Tip: SATORP never asks candidates to pay fees during recruitment.",
      "wrap": true,
      "isSubtle": true,
      "size": "Small"
    }
  ],
  "actions": [
    { "type": "Action.OpenUrl", "title": "Open Careers page", "url": "https://www.satorp.com/en/careers" }
  ]
}
```

> ⚠️ Confirm the recruitment-fee tip with SATORP HR before release, or delete that TextBlock.

### B3. Contact card

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    { "type": "TextBlock", "text": "Contact SATORP", "size": "Large", "weight": "Bolder", "color": "Accent" },
    {
      "type": "TextBlock",
      "text": "For official enquiries, use the contact details on SATORP's website. For workplace matters, contact your supervisor or HR business partner.",
      "wrap": true
    }
  ],
  "actions": [
    { "type": "Action.OpenUrl", "title": "Open contact page", "url": "https://www.satorp.com/en/contact" },
    { "type": "Action.OpenUrl", "title": "News & Media", "url": "https://www.satorp.com/en/media" }
  ]
}
```

---

### Sources for public facts used in this lab

- SATORP – About: https://www.satorp.com/en/about
- TotalEnergies – SATORP refining and petrochemical platform: https://totalenergies.com/company/projects/oil/satorp-refining-petrochemical-platform-saudi-arabia

*Lab prepared for training purposes. SATORP and TotalEnergies names are used only to describe the training scenario.*
