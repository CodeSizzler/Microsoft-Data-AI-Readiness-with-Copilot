# Day 1 Lab: Azure AI Foundation
## Exploring Microsoft Foundry and Running Your First Task

**Module covered:** The Azure AI landscape, foundation models and the model catalog, tokens / context / embeddings / inference, grounding and RAG, Copilot / Copilot Studio / custom AI, enterprise use cases.

**Duration:** ~90–120 minutes for Parts 1–5 and 7. Part 6 and the Extension Challenges add ~20–30 minutes; treat them as optional or homework if the group is running long.

**Portal version:** Updated for the new Microsoft Foundry portal (`ai.azure.com` with the New Foundry toggle ON), October 2026.

> **About this edition:** Azure AI Foundry is now Microsoft Foundry. The portal has a new layout: a top navigation bar with **Home, Discover, Build, Operate, Manage** and **Docs**, replacing the long left-hand menu of the classic portal. Every step in this lab uses the new layout. Hub-based projects, the classic Playgrounds page and *Add your data* with Azure AI Search are not used.

## Learning objectives

By the end of this lab, you will be able to:

- Navigate the Microsoft Foundry portal and explain how it relates to Azure AI services (Foundry Tools) and Azure OpenAI.
- Open the Foundry project created for you and explain how a project relates to its Foundry resource.
- Browse the model catalog and inspect the foundation models already deployed for this lab.
- Run inference in the model playground and observe tokens, the context window and instructions (system prompts) in action.
- Give an agent your own document with the File search tool to see grounding / RAG behaviour first-hand.
- Compare the model's raw behaviour with the grounded agent and explain the difference.
- Explain when Microsoft 365 Copilot, Copilot Studio or a custom Foundry solution is the right choice for a business scenario.

## Prerequisites

| Requirement | Notes |
| --- | --- |
| Azure subscription | Training/sandbox subscription with quota for the Foundry models used in this lab. |
| Access to Microsoft Foundry | `https://ai.azure.com`, signed in with your lab credentials. |
| Project access (granted for you) | A Foundry project `proj-<your user name>` is already provisioned. You need at least the **Foundry User** role (formerly Azure AI User) on it. |
| File upload permission (for Part 5) | Uploading a file to File search creates a vector store. See the instructor note below: in the new portal this can need a role at the Foundry resource scope, not only the project. |
| A modern browser | Microsoft Edge or Google Chrome. |
| (Optional) A sample document | A short PDF/Word/TXT file (2–5 pages) about a fictitious product or policy. A ready-made sample is provided in Step 5.2. |

> **Instructor note:** Before the session, confirm that these deployments exist on the shared Foundry resource and show **Succeeded**: `chat-lab-deploy` (gpt-5-mini), `gpt4o-lab-deploy` (gpt-4o) and `embed-lab-deploy` (text-embedding-3-small). Optionally add a DeepSeek deployment for the parameter comparison in Step 4.3. Check the shared tokens-per-minute (TPM) limit is high enough for the class size.
>
> Test a File search upload with a participant account. If it fails with "You don't have permission to upload files in this project… assign the Foundry User role", assign **Foundry User** at the Foundry resource scope (a known behaviour of the new portal when it creates vector stores), or have participants attach a vector store you pre-created.
>
> No Azure AI Search resource is needed. The Foundry Agent Service handles chunking, embedding and indexing for File search.

## Classic portal vs. new portal: where things moved

Use this table if you have used Azure AI Foundry before or are following older material.

| Task | Classic portal (old) | New Microsoft Foundry portal |
| --- | --- | --- |
| Browse the model catalog | Model catalog (left pane) | Discover → Models |
| View model deployments | Models + endpoints (left pane) | Build → Models |
| Chat with a model | Playgrounds → Chat playground | Build → Models → select a deployment (playground opens) |
| Build agents | Agents (left pane) | Build → Agents |
| Ground on your data | Chat playground → Add your data (Azure AI Search) | Agent → Tools → Add → File search |
| Evaluations | Evaluation (left pane) | Build → Evaluations |
| Tracing / monitoring | Tracing, Monitoring (left pane) | Operate |
| Quota, users, connected resources | Management center | Manage |
| Switch project / see all projects | Management center → All resources | Project name (top left) → View all projects |

## Part 1 – Orientation: The Azure AI Landscape

**Goal:** Understand where Microsoft Foundry sits relative to other Azure AI offerings before touching the portal.

### Step 1.1 – Map the landscape (predict, then verify)

Open a blank note (OneNote or Notepad) and, before opening the portal, write one sentence for each term:

- Microsoft Foundry (formerly Azure AI Foundry)
- Azure AI services / Foundry Tools (formerly Cognitive Services)
- Foundation model
- Copilot vs. Copilot Studio vs. a custom AI app

You will revisit and correct these at the end of the lab.

### Step 1.2 – Sign in and find your way around

1. Go to `https://ai.azure.com` and sign in with your lab credentials.
2. In the top banner, make sure the **New Foundry** toggle is ON. If it is off, switch it on; the page reloads into the new experience.
3. Close any welcome tips or quick-start panes. Selecting the Foundry logo (top left) always brings you back to the home page.
4. Look at the top banner from left to right and identify, without clicking yet:
   - **Project selector** (top left): shows the current project; open it to switch projects or select *View all projects*.
   - **Home**: project overview, endpoint and API key, quick actions.
   - **Discover**: the Models catalog (foundation models from OpenAI, Microsoft, Meta, Mistral, DeepSeek and others).
   - **Build**: where you work: Agents, Models (your deployments and playground), Tools, Knowledge, Data, Evaluations, Fine-tuning.
   - **Operate**: monitoring, tracing and compliance across your projects.
   - **Manage**: quota, users and connected resources.

> 📷 **Screenshot:** New Foundry home page with the top navigation (Home / Discover / Build / Operate / Manage / Docs) and the New Foundry toggle ON highlighted.

> ✅ **Checkpoint:** You can explain that a Foundry resource holds shared infrastructure and model deployments, while a project is your own workspace inside it. You can name what lives under Discover, Build and Operate.

## Part 2 – Open Your Project

### Step 2.1 – Open your assigned project

1. Select the project selector at the top left of the banner.
2. Select your project, `proj-<your user name>`. If it is not in the short list, select *View all projects* and pick it from there.
3. Do not select **Create new project**. Participants do not have permission to create projects, and one has already been provisioned for you on the shared Foundry resource.

> 📷 **Screenshot:** Project selector dropdown open, showing proj-<user name>, View all projects and Create new project.

> **Note:** In the new portal every project is a Foundry project that belongs to a Foundry resource. Older hub-based projects only appear in the classic portal; you will not use them in this lab.

### Step 2.2 – Explore your project home page

1. Select **Home** in the top banner. Confirm your project name appears in the project selector.
2. Find the **Project endpoint** (format `https://<resource>.services.ai.azure.com/api/projects/<project>`) and the **API key** on the home page. You would use these to call models or agents from code later. Do not share the key.
3. Select **Build** in the top banner, then **Models** in the left pane. This is the list of model deployments available to your project.

> 📷 **Screenshot:** Project Home page showing Project endpoint and API key, then Build → Models deployment list.

> ✅ **Checkpoint:** You can open your project, find its endpoint, and reach Build → Models.

## Part 3 – Model Catalog and Your Deployments

### Step 3.1 – Browse the model catalog

1. Select **Discover** in the top banner, then **Models** in the left pane.
2. Use the search box and filters to explore the catalog:
   - Filter by collection / provider (for example Azure OpenAI, Microsoft, Meta, Mistral, DeepSeek).
   - Filter by inference task (for example chat completion, embeddings).
   - Note models marked *sold directly by Azure* versus partner and community models.
3. Open the model card for `gpt-5-mini` (or the chat model your instructor names) and read:
   - Context window (input tokens) and maximum output tokens.
   - Modalities: text, image (vision), audio.
   - Supported deployment types (for example Global Standard, Data Zone, Provisioned) and regions.
   - Whether it is a reasoning model. This matters in Step 4.3.
4. Do not select **Deploy**. Deploying models is an administrator task in this course; the deployments you need already exist.

> 📷 **Screenshot:** Discover → Models catalog with filters applied, and the gpt-5-mini model card showing context window and deployment options.

> 💬 **Discussion point:** Why might you choose a smaller model such as gpt-5-mini over gpt-5 for a production use case? (Cost, latency, rate limits, and "good enough" accuracy for the task.)

### Step 3.2 – Review the chat model deployment

1. Select **Build** in the top banner, then **Models** in the left pane.
2. Open the details of `chat-lab-deploy` and note:
   - Model and version: `gpt-5-mini`.
   - Deployment type: Global Standard.
   - Rate limit in tokens per minute (TPM). This limit is shared by everyone on the course.
   - Status / provisioning state: should be **Succeeded**.
3. If the deployment is missing or shows **Failed**, tell your instructor. You cannot create or repair deployments yourself.

> 📷 **Screenshot:** Build → Models with chat-lab-deploy details: model version, Global Standard, TPM limit, Succeeded.

### Step 3.3 – Review the embedding model deployment

1. Return to **Build → Models**.
2. Search for `embed-lab-deploy` (text-embedding-3-small, or the embedding model your instructor names).
3. Open it and note that it is an embedding model: it turns text into vectors for search, and you cannot chat with it in a playground.

> ✅ **Checkpoint:** Under Build → Models you can see chat-lab-deploy, embed-lab-deploy and gpt4o-lab-deploy, all Succeeded.

## Part 4 – Core Concepts in Action: Tokens, Context, Inference

### Step 4.1 – Open the model playground

1. Go to **Build → Models**.
2. Select `chat-lab-deploy`. The model playground opens: a setup pane on the left (model, Instructions, parameters) and a chat pane on the right.
3. Confirm the deployment selector at the top of the setup pane shows `chat-lab-deploy`.

> 📷 **Screenshot:** Model playground for chat-lab-deploy: Instructions box on the left, chat pane on the right.

> **Note:** There is no separate Playgrounds menu in the new portal. You reach the playground for a model by selecting its deployment under Build → Models. The **Code** tab shows how to make the same call from Python, C#, JavaScript or REST.

### Step 4.2 – Observe tokens and context

1. In the **Instructions** box (the system prompt), replace the default text with:

```text
You are a concise assistant. Answer in no more than 2 sentences.
```

2. Apply / save the instructions if the playground asks you to.

3. In the chat box, ask:

```text
Explain what a context window is, using a mailbox analogy.
```

4. Send it, then find the token usage for the exchange (shown with the response details or near the chat box, depending on the current build). Note the input and output token counts.
5. Now send a much longer question: paste 3–4 sentences of filler text, then add your real question. Compare the token count with the first message.

> 📷 **Screenshot:** Chat pane showing the reply and the token usage for the short and the long prompt.

> 💬 **Discussion point:** What happens once a conversation exceeds the model's context window? (The oldest turns are truncated or dropped, or the request fails with an error.) Why does every earlier turn count towards input tokens?

### Step 4.3 – Change inference parameters

1. In the setup pane, open the parameters / model settings section.
2. Check which parameters are offered for `chat-lab-deploy`. Because gpt-5-mini is a reasoning model, you will usually not see Temperature or Top P; instead you may see Reasoning effort and Max output tokens.
3. Switch the deployment selector to `gpt4o-lab-deploy`. Set **Temperature = 0** and ask: "Give me 3 taglines for a coffee shop." Send the same prompt two or three times and notice how similar the answers are.
4. Set **Temperature = 1** and repeat. Compare the creativity and variability of the responses.
5. *(Optional)* If your instructor deployed a DeepSeek model, select it and check which parameters it exposes. If Temperature is available, repeat the 0 vs. 1 test and compare with gpt-4o.
6. Switch back to `chat-lab-deploy`. Lower **Max output tokens** to a small value (for example 100) and ask the tagline question again. The reply will usually be empty, not shortened. This is expected: a reasoning model spends tokens *thinking* before writing, so a small budget runs out before any visible text appears.
7. Switch to `gpt4o-lab-deploy`, set the same small max-token value and repeat. This time you see a genuinely truncated response.
8. Restore the original deployment (`chat-lab-deploy`) and default parameter values.

> 📷 **Screenshot:** Parameters for gpt4o-lab-deploy (Temperature, Top P, Max output tokens) next to the reduced parameters for gpt-5-mini.

> 📷 **Screenshot:** Tagline responses at Temperature 0 vs. Temperature 1, and the empty vs. truncated reply with a small max-token value.

> ✅ **Checkpoint:** You can say which parameters are available for gpt-5-mini, gpt-4o and (if used) DeepSeek, and explain how Temperature and Max output tokens change the output, and why a reasoning model returns an empty reply when the token budget is too small.

## Part 5 – Grounding and RAG: Give the Model Knowledge It Doesn't Have

### Step 5.1 – Establish the baseline (ungrounded) behaviour

1. Stay in the model playground for `chat-lab-deploy` (Build → Models → chat-lab-deploy). Start a new chat so earlier messages do not influence the answer.
2. Ask a question about a fictitious internal policy:

```text
What is Contoso's remote work reimbursement policy for home internet?
```

3. Note that the model either says it does not know, or invents a plausible-sounding answer (a hallucination). Copy or screenshot this response; you will compare it later.

> 📷 **Screenshot:** Ungrounded answer from chat-lab-deploy to the Contoso question.

### Step 5.2 – Create the sample policy document

Open Notepad (or Word), paste the text below and save it as `contoso-remote-work-policy.txt` (`.docx`, `.pdf` and `.md` also work).

```text
Contoso Remote Work Policy (Sample)
- Employees working remotely 3+ days/week receive a $50/month home internet stipend.
- Stipend is paid via monthly expense claim, approved by direct manager.
- Equipment (laptop, monitor) is provided by IT upon request; personal equipment is not reimbursed.
- Policy effective January 2025, reviewed annually by HR.
```

### Step 5.3 – Create an agent with the File search tool

1. Select **Build** in the top banner, then **Agents** in the left pane.
2. Select **New agent** (or **Create agent**). If asked what to build, choose to build a prompt agent in the portal.
3. Enter the agent name `contoso-policy-agent-<your initials>` and select **Create**. The agent editor opens with the agent playground beside it.
4. In the model selector, choose `chat-lab-deploy`.
5. In **Instructions**, enter:

```text
You are an HR assistant. Answer questions using only the uploaded policy documents.
If the answer isn't in the documents, say you don't know rather than guessing.
```

6. In the **Tools** section, check whether Web search is already enabled. If it is, remove or switch it off, so the agent can only use your document and the before/after comparison stays clean.
7. In Tools, select **Add → File search**.
8. Select **Upload files**, browse to `contoso-remote-work-policy.txt` under *Attach files*, and select **Attach**. Foundry creates a vector store: it chunks the file, embeds the chunks with an embedding model and indexes them for you.
9. Wait until the file shows as processed / indexed (a confirmation appears).
10. Select **Save**. Each save creates a new version of the agent.

> 📷 **Screenshot:** Agent editor: model = chat-lab-deploy, Instructions filled in, Tools showing File search with contoso-remote-work-policy.txt attached.

> **Note:** If the upload fails with a permissions message asking for the Foundry User role, stop and tell your instructor; the fix is a role assignment, not something you can change yourself.

### Step 5.4 – Ask the grounded question

1. Use the agent playground chat pane next to the editor.
2. Ask the same question as in Step 5.1:

```text
What is Contoso's remote work reimbursement policy for home internet?
```

3. Compare the answer with your Step 5.1 baseline. It should now state the $50/month stipend for people working remotely 3+ days a week, usually with a citation that points back to the source file.
4. Ask a question the document does not cover, for example: "What is Contoso's travel reimbursement policy?" A well-grounded agent should say it does not know instead of inventing an answer, because the instructions in Step 5.3 told it to.

> 📷 **Screenshot:** Grounded answer with the $50/month figure and file citation, plus the "I don't know" reply to the travel policy question.

> ✅ **Checkpoint:** You have a clear before-RAG / after-RAG comparison and can explain retrieval-augmented generation as: retrieve relevant chunks from your data → add them to the prompt as context → the model writes an answer grounded in that context.

## Part 6 – Where Copilot, Copilot Studio and Custom AI Fit

### Step 6.1 – Scenario mapping exercise

For each scenario, choose Microsoft 365 Copilot, Copilot Studio or Custom Microsoft Foundry solution, and write a one-line justification.

| # | Scenario | Your answer | Justification |
| --- | --- | --- | --- |
| 1 | Employees want AI help summarising Outlook emails and Teams meetings | | |
| 2 | HR wants a no-code chatbot on the intranet answering FAQs from a knowledge base, built by a business analyst | | |
| 3 | Engineering wants a custom RAG app with fine-grained control over retrieval, model choice and evaluation pipelines | | |
| 4 | Support team wants a bot in Teams that can also trigger Power Automate flows | | |
| 5 | Product team wants to embed a domain-specific model in their own external-facing web app | | |

## Wrap-Up and Reflection

1. Return to your Step 1.1 notes. Update your one-sentence definitions now that you have used the portal.
2. Answer these reflection questions in your notes:
   - What is one enterprise use case in your own organisation where RAG would add clear value?
   - What is one risk of grounding a model on your own data (for example stale documents or sensitive data exposure)?
   - If you had to justify choosing Copilot Studio over a custom Foundry build to a stakeholder, what would you say?

## Cleanup

You work in a shared, instructor-provisioned environment, so you only clean up what you created:

1. Go to **Build → Agents**, open the menu (…) for `contoso-policy-agent-<your initials>` and select **Delete**.
2. If the uploaded file or its vector store is still listed under **Build → Data** (or the agent's File search tool), delete it too.
3. Do not delete model deployments, your project or the resource group; they are shared with the rest of the course.

> **Instructor note:** After the course, delete the training resource group in the Azure portal (Resource group → Delete resource group, type the name to confirm). This removes the Foundry resource, projects, deployments, agents and vector stores together.

## Lab Summary Checklist

- [ ] Signed in to the new Microsoft Foundry portal and found Home, Discover, Build, Operate and Manage
- [ ] Opened your assigned Foundry project and found its endpoint
- [ ] Browsed the model catalog and reviewed the chat and embedding deployments
- [ ] Observed token usage and context window effects in the model playground
- [ ] Adjusted temperature and max output tokens, and saw how reasoning models behave differently
- [ ] Compared ungrounded vs. grounded (RAG) answers using an agent with File search
- [ ] Completed the Copilot vs. Copilot Studio vs. custom Foundry mapping exercise
- [ ] Deleted your agent and uploaded file

## Extension Challenges (If Time Permits)

- **Multi-document grounding:** Upload a second document (for example a travel policy) to the same File search tool and ask a question that needs the agent to pick the right source.
- **Prompt engineering:** Rewrite the agent instructions so it always answers with one line plus a "Source:" citation. Save and compare the two agent versions.
- **Compare models:** Switch the agent's model from `chat-lab-deploy` to `gpt4o-lab-deploy`, save a new version and ask the same grounded question. Compare answer quality, latency and cost implications.
- **Look at the code:** In the model playground, open the **Code** tab and identify the endpoint, deployment name and parameters used for the call.
