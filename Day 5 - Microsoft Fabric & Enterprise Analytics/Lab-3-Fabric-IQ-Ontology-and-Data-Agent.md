# Lab 3 – Fabric IQ: Teach Fabric the Language of the Refinery

> **Time:** about 50 minutes · **Level:** Beginner · **No coding needed**
> ⚠️ **Ontology is a preview feature.** Button names and steps may change slightly.

---

## 1. Introduction

Tables like `equipment` and `work_orders` mean something to a data engineer. A reliability engineer thinks in **units, equipment, work orders and downtime**, and in how they connect: *"this FCC compressor has two open P1 work orders and caused 40 hours of downtime."*

**Fabric IQ** adds that business meaning on top of OneLake. Its key item is the **ontology**: a model of your business **entity types** (Unit, Equipment, Work Order…), their **properties**, and the **relationships** between them, **bound** to real data in OneLake. AI agents can then answer questions in business language and stay grounded in governed data.

**In this lab you'll:**

1. Create an **ontology** for the refinery
2. Add **entity types** and **bind** them to your lakehouse tables
3. Connect them with **relationships**
4. Use the **ontology agent** to extend the model in plain English
5. Ask questions through a **Fabric data agent**

```
   Unit ──hasEquipment──▶ Equipment ──hasWorkOrder──▶ Work Order
    ▲                        │
    │ recordedFor            └──hadDowntime──▶ Downtime Event
 Production Record
```

### Fabric IQ in one table 🧩

| Fabric IQ part | What it is | In this lab |
| --- | --- | --- |
| **OneLake** | The unified data foundation | Lab 1 lakehouses |
| **Semantic model** | Measures and business definitions for BI | Lab 2 model |
| **Ontology** (preview) | Business entities, relationships, rules and metrics bound to data | ✅ Built here |
| **Graph** | Optional execution layer to explore connected entities | Optional look |
| **Data agent** | Natural-language Q&A over your sources | ✅ Built here |
| **Operations agent** | Monitors data and acts on conditions (Real-Time Intelligence) | Discussed only |

---

## 2. Prerequisites

- **Lab 1 complete**: `Refinery_LH` with `units`, `equipment`, `production_daily`, `work_orders` and the `downtime_events` shortcut
- Tenant settings enabled by your admin: **Users can create Fabric items**, **Users can create ontology (preview) items**, plus the **data agent** and **Copilot** settings (see the [README](README.md))

---

## 3. Exercise

### Part A – Create the ontology (5 min)

1. In your workspace, select **+ New item** → search **Ontology** → select **Ontology (preview)**.
2. In **New Ontology**: **Name** `RefineryOntology`, location = your workspace → **Create**.

---

### Part B – Add entity types and bind data (15 min)

You'll add five entity types. The steps are the same for each.

**Steps for the first one, Unit:**

1. On the top ribbon, select **+ Add entity type**. **Name:** `Unit` → **Add Entity Type**.
2. Select the **…** next to **Unit** → **Bind data**.
3. Select **Add**, expand **Refinery_LH** → **dbo** → select the `units` table → **Select table**.
4. Select **Entity type properties**. The columns appear automatically as properties.
   If you're asked for a **key** (identifier) property, choose `UnitId`.
5. Select **Create**, then **Cancel** to close the panel.

**Repeat for the other four** (select **Home** → **+ Add entity type** each time):

| Entity type | Bind to table | Key property |
| --- | --- | --- |
| `Equipment` | `equipment` | `EquipmentId` |
| `Work Order` | `work_orders` | `WorkOrderId` |
| `Downtime Event` | `downtime_events` *(your OneLake shortcut, which works for binding)* | `EventId` |
| `Production Record` | `production_daily` | `Date` + `UnitId` (or skip the key if not asked) |

✅ **Checkpoint:** five entity types on the canvas, each with its properties.

> 🧩 **Binding, not copying:** the ontology doesn't store the data. It **points** at the tables in OneLake. Change the data and the ontology reflects it.

---

### Part C – Add relationships (10 min)

1. Select **Unit** → **Add relationship** (ribbon), or **Add relationship type** on the canvas.
2. Fill in:
   - **Relationship type name:** `hasEquipment`
   - **Origin entity type:** `Unit`
   - **Target entity type:** `Equipment`
3. Select **Create**. Map **Origin Property** `UnitId` → **Target Property** `UnitId` → **Save** → **Cancel**.
4. Add the next two relationships the same way:

| Relationship name | Origin → Target | Origin property → Target property |
| --- | --- | --- |
| `hasWorkOrder` | Equipment → Work Order | `EquipmentId` → `EquipmentId` |
| `hadDowntime` | Equipment → Downtime Event | `EquipmentId` → `EquipmentId` |

✅ **Checkpoint:** the canvas shows **Unit → Equipment → Work Order** and **Equipment → Downtime Event**.

---

### Part D – Extend the model with the ontology agent (10 min)

You'll add the last relationship by **describing** it instead of clicking.

1. On the ribbon, select **Ontology agent**. It opens in **Plan** mode.
2. Send:

```text
Create a relationship type called recordedFor from Production Record to Unit, matching Production Record.UnitId to Unit.UnitId.
```

3. Read the **plan** the agent proposes. Does it match what you asked?
4. Switch to **Act** mode and send:

```text
Apply the plan.
```

5. ✅ `recordedFor` appears on the canvas between **Production Record** and **Unit**.

**Try one more (optional):** ask the agent to describe your model:

```text
Summarise this ontology for a reliability engineer: list the entity types, how they are related, and three questions it can help answer.
```

> 🧩 **Plan first, then act.** The agent proposes changes before applying them, the same "human approves" pattern used across Microsoft's agent tools.

> 💡 **Optional – Graph:** if your ontology shows a **graph** view, open it to explore the connected entities visually. Loading instance data into a graph is an opt-in step; you don't need it for this lab.

---

### Part E – Ask questions with a Fabric data agent (10 min)

1. In your workspace: **+ New item** → **Data agent**. **Name:** `Refinery Reliability Agent` → **Create**.
2. Select **Add data** and choose **RefineryOntology** as the data source.
   *If ontology isn't offered as a source in your tenant yet, add **Refinery_LH** and select all five tables instead. Then see the comparison question at the end of this part.*
3. In **Agent instructions**, paste:

```text
You help SATORP reliability and operations teams.
- A "unit" is a process unit (for example the FCC, coker or hydrocrackers). Always show the unit name, not only the ID.
- "Unplanned downtime" means downtime events where Planned = 'No'.
- "Open" work orders are any work orders whose Status is not 'Completed'.
- Attainment % = actual throughput divided by planned throughput.
- Answer with a short table, then one sentence of explanation. Say clearly when the data does not contain the answer.
```

4. Ask these questions in the chat and compare with the answer key:

| Question | Expected (answer key) |
| --- | --- |
| `Which unit had the most unplanned downtime between July and September 2026?` | **Fluid Catalytic Cracker, ~192.5 h** |
| `What was the top cause of unplanned downtime?` | **Fouling, ~184.5 h** |
| `How many open or in-progress P1 work orders are on criticality A equipment?` | **3** |
| `List the equipment in the Fluid Catalytic Cracker with their open work orders.` | A short list from the FCC's 5 equipment items |
| `What is the refinery's profit margin?` | Says the data **doesn't** contain it, with no guessing |

5. Open the agent's answer details to see the **query it generated**. This is how you check it understood "unplanned" and "open" correctly.
6. Select **Publish** so others (and other agents) can use it.

**Discussion:** if you used tables instead of the ontology, which questions needed the instructions to explain terms like "unit" or "open"? That's exactly the gap the ontology fills: business meaning is defined **once**, centrally, rather than re-explained in every agent's instructions.

---

## 4. Where this goes next at SATORP

| Next step | How |
| --- | --- |
| Use the data agent in **Teams / Microsoft 365 Copilot** | Connect the published data agent to **Copilot Studio** or Microsoft 365 Copilot |
| Watch for problems automatically | An **operations agent** (Real-Time Intelligence) monitoring live equipment data and alerting on conditions |
| Grow the ontology | Add Tag, Product, Shift, Permit; bind real (approved) SAP PM and historian data landed in OneLake |

---

## 5. Checkpoint

- [ ] `RefineryOntology` with 5 entity types and 4 relationships (one created by the ontology agent)
- [ ] `Refinery Reliability Agent` answers the test questions correctly and refuses the profit question
- [ ] You can explain the difference between a **table**, a **semantic model** and an **ontology**

## 6. Troubleshooting

| Problem | Fix |
| --- | --- |
| **Ontology (preview)** isn't in **+ New item** | Ask your admin to enable **Users can create ontology (preview) items**. |
| Bind data can't find the table | Expand **Refinery_LH** → **dbo**. Check Lab 1 created the table, not just the file. |
| The data agent gives wrong numbers | Check its generated query, then tighten the **Agent instructions** (e.g. the definition of "unplanned"). |
| The ontology agent changed something unexpected | Stay in **Plan** mode, read the plan, and only switch to **Act** when it's right. |
