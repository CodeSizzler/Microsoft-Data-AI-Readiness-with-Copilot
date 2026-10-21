# Lab 2 – Copilot in Fabric: From Data to Insight in Plain English

> **Time:** about 50 minutes · **Level:** Beginner · **Coding:** none required. Copilot writes it, you review it.

---

## 1. Introduction

**Copilot in Fabric** is built into each Fabric experience. In this lab you'll use it in two places:

| Where | What Copilot does |
| --- | --- |
| **Notebooks** (Data Engineering) | Writes and explains PySpark/SQL code from your prompts, and helps fix errors |
| **Power BI** | Builds report pages and summarises insights from a semantic model |

You'll also create a **semantic model** in between. That's the business layer Power BI, Copilot and (in Lab 3) Fabric IQ all build on.

> ⚠️ **Copilot needs a paid capacity (F2 or higher, or Power BI Premium P1+)**, plus the Copilot tenant settings listed in the [README](README.md). It doesn't work on trial capacities.
>
> 💡 Copilot's output varies from run to run. **Always read the code or visual before trusting it.** Compare your numbers with the answer key.

---

## 2. Prerequisites

- **Lab 1 complete**: `Refinery_LH` with tables `units`, `equipment`, `production_daily`, `work_orders` and the `downtime_events` shortcut

---

## 3. Exercise

### Part A – Copilot in a notebook (20 min)

1. Open **Refinery_LH** → on the ribbon select **Open notebook** → **New notebook**.
   ✅ The notebook opens with `Refinery_LH` attached in the left **Explorer**.
2. Select **Copilot** on the notebook ribbon. The Copilot chat pane opens on the right.
3. Send each prompt below, one at a time. For each answer: **read the code**, **insert it** into a new cell, then **run** the cell.

**Prompt 1 – Explore**

```text
Load the production_daily table from the attached lakehouse and show the first 10 rows and the column data types.
```

**Prompt 2 – Analyse**

```text
Calculate throughput attainment percent (actual divided by planned) per UnitId for September 2026, join with the units table to show UnitName, and sort from lowest to highest.
```

✅ The **Fluid Catalytic Cracker** should be lowest, at **~86.7 %**.

**Prompt 3 – Visualise**

```text
Plot daily Throughput_kbbl and PlannedThroughput_kbbl for UnitId U400 as a line chart.
```

✅ You should see a sharp **dip on 11–13 September**.

**Prompt 4 – Find the cause**

```text
From downtime_events, show unplanned events (Planned = 'No') for UnitId U400 in September 2026 with EquipmentId, cause and duration.
```

✅ A **62-hour "Catalyst issue"** event starting **12 September** explains the dip.

**Prompt 5 – Save a result for others**

```text
Write the attainment result from prompt 2 to a new Delta table called unit_attainment in the attached lakehouse, overwriting it if it exists.
```

Refresh **Tables** in the Explorer. ✅ `unit_attainment` appears.

4. **Explain code:** select any generated cell and ask Copilot:
   `Explain what this cell does in simple terms.`
5. **Fix an error:** in a new cell, type and run
   `spark.table("production_dailyy").show()`
   (note the typo). When the error appears, use **Fix with Copilot** (preview) or ask in the chat pane: `Fix the error in the last cell.`
6. Rename the notebook `Refinery Copilot Analysis` (top left) and save it.

> 🧩 **Copilot doesn't replace understanding.** It writes the first draft fast, and you still check joins, filters and units. A wrong join in a refinery KPI is still wrong, however fast it was written.

---

### Part B – Build a semantic model (15 min)

1. Open **Refinery_LH** (Lakehouse view) → on the ribbon select **New semantic model**.
2. **Name:** `Refinery Reliability Model`. Select the tables:
   - `units`
   - `equipment`
   - `production_daily`
   - `downtime_events`
   - `work_orders`
3. Select **Confirm**. The model opens in the web modelling view.
4. **Create relationships**: drag from the first column to the second (many-to-one):

| From (many) | To (one) |
| --- | --- |
| `production_daily[UnitId]` | `units[UnitId]` |
| `equipment[UnitId]` | `units[UnitId]` |
| `downtime_events[EquipmentId]` | `equipment[EquipmentId]` |
| `work_orders[EquipmentId]` | `equipment[EquipmentId]` |

5. **Add measures:** select the `production_daily` table → **New measure**, and add each line below as its own measure. Put the downtime and work order measures on their own tables.

```DAX
Actual Throughput (kbbl) = SUM ( production_daily[Throughput_kbbl] )
Planned Throughput (kbbl) = SUM ( production_daily[PlannedThroughput_kbbl] )
Attainment % = DIVIDE ( [Actual Throughput (kbbl)], [Planned Throughput (kbbl)] )
Unplanned Downtime (h) = CALCULATE ( SUM ( downtime_events[DurationHours] ), downtime_events[Planned] = "No" )
Open Work Orders = CALCULATE ( COUNTROWS ( work_orders ), work_orders[Status] <> "Completed" )
```

6. Format **Attainment %** as a percentage with 1 decimal place.

> 💡 Prefer not to type DAX? If **Copilot** is available in the modelling view, ask it: `Create a measure for unplanned downtime hours where Planned is "No"`, then review what it writes.

> 🧩 **Why a semantic model?** It's where SATORP defines *once* what "attainment" or "unplanned downtime" means. Power BI, Copilot and Fabric IQ then all use the same definitions.

---

### Part C – Copilot in Power BI (15 min)

1. From the semantic model, select **Create report** (or **New report** → **Create from scratch**).
2. Open the **Copilot** pane in the report editor.
3. Send:

```text
Create a report page for refinery reliability showing: Attainment % by unit name, Unplanned Downtime (h) by cause, and Open Work Orders by priority.
```

4. Review the page Copilot builds. Ask for changes in plain English, for example:
   `Sort attainment from lowest to highest and highlight units below 90%.`
5. Ask questions about the data:
   - `Which unit has the lowest attainment and what is its value?`
   - `Summarise the main reliability issues on this page in three bullet points.`
6. **Save** the report as `Refinery Reliability Report` in your workspace.

✅ **Checkpoint:** FCC lowest (~86.7 %). The top unplanned cause is **Fouling (~184.5 h)**, with Catalyst issue a close second. Open work orders split by P1/P2/P3.

---

## 4. Checkpoint

- [ ] A notebook with Copilot-generated analysis and a saved `unit_attainment` table
- [ ] `Refinery Reliability Model` with 4 relationships and 5 measures
- [ ] A Copilot-built report page whose numbers match the answer key

## 5. Challenge (optional)

- **Copilot in Data Factory:** create a **Dataflow Gen2**, connect to `work_orders`, and ask Copilot to `keep only P1 and P2 work orders that are not completed and add a column AgeDays since CreatedDate`.
- **Narrative:** add a **Narrative** visual with Copilot to the report and compare it with your own reading of the data.

## 6. Troubleshooting

| Problem | Fix |
| --- | --- |
| No **Copilot** button | Capacity is trial or below F2, or the tenant settings are off. Ask your admin. |
| Copilot code fails | Ask Copilot to fix it, or check table names in the Explorer (`dbo.` prefix with schema-enabled lakehouses). |
| Report visuals look wrong | Check the relationships in the semantic model first. Most "wrong numbers" come from a missing relationship. |
