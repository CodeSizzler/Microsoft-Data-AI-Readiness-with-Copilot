# Lab 1 – OneLake Foundations

> **Time:** about 45 minutes · **Level:** Beginner · **No coding needed** (a little SQL is provided)

---

## 1. Introduction

**OneLake** is the single, organisation-wide data lake that comes with every Microsoft Fabric tenant. Think of it as **"OneDrive for data"**: every lakehouse, warehouse and database in Fabric stores its data in OneLake, in open **Delta Parquet** format.

In this lab you'll:

- create two **lakehouses**, one for production data and one for the reliability team
- **upload** refinery CSV files and **load them into tables**
- create a **shortcut** so one lakehouse can use the other team's data **without copying it**
- query everything with **SQL**
- find your data in the **OneLake catalog**

### Three ideas to remember 🧩

| Idea | What it means for SATORP |
| --- | --- |
| **One lake** | All Fabric data in one governed place, not dozens of copies in different tools |
| **One copy** | Shortcuts let teams reuse data where it already lives: in OneLake, ADLS Gen2, Amazon S3, Google Cloud Storage, Dataverse and more |
| **Open format** | Delta Parquet tables can be read by Spark, SQL, Power BI and KQL engines alike |

---

## 2. Prerequisites

- A Fabric workspace on **F2 or higher** capacity, where you are a **Contributor** or above
- From `lab-files/`: `units.csv`, `equipment.csv`, `production_daily.csv`, `work_orders.csv`, `downtime_events.csv`

---

## 3. Exercise

### Part A – Create your workspace (5 min)

1. Go to **https://app.fabric.microsoft.com** and sign in.
2. Select **Workspaces** → **+ New workspace**.
3. **Name:** `SATORP-Fabric-Lab-<your initials>`.
4. Under **Advanced**, choose the **Fabric capacity** your instructor gave you (not Trial). Select **Apply**.

---

### Part B – Create the Refinery lakehouse and load data (15 min)

1. In your workspace, select **+ New item** → search **Lakehouse** → select it.
2. **Name:** `Refinery_LH` → **Create**. Leave other options at their defaults.
3. In the **Explorer** on the left, select the **…** next to **Files** → **Upload** → **Upload files**.
4. Upload these four files:
   - `units.csv`
   - `equipment.csv`
   - `production_daily.csv`
   - `work_orders.csv`
5. Expand **Files**. For **each** file: select **…** → **Load to Tables** → **New table** → keep the suggested name (for example `units`) → **Load**.
6. Expand **Tables**. ✅ You should see **4 tables**. Select `production_daily` to preview its rows.

> 💡 **What just happened?** The CSV files stay in **Files** (raw zone). **Load to Tables** created **Delta tables** in **Tables**, which every Fabric engine can read.

---

### Part C – Create the Reliability lakehouse (5 min)

Imagine the reliability team owns downtime data in **their own** lakehouse.

1. Back in the workspace: **+ New item** → **Lakehouse** → **Name:** `Reliability_LH` → **Create**.
2. Upload `downtime_events.csv` to **Files**, then **Load to Tables** → **New table** → `downtime_events`.

---

### Part D – Create a shortcut: use data without copying it (10 min)

The production team wants downtime data in **their** lakehouse, but the reliability team must stay the owner, so it shouldn't be copied.

1. Open **Refinery_LH**.
2. Select the **…** next to **Tables** → **New shortcut**.
3. Choose **Microsoft OneLake** as the source.
4. Select **Reliability_LH** → **Next**.
5. Expand **Tables** and tick `downtime_events` → **Next** → **Create**.
6. ✅ `downtime_events` now appears under **Tables** in Refinery_LH with a **shortcut (link) icon**.

**Prove it's one copy:**

- Open the `downtime_events` shortcut in Refinery_LH: it shows **37 rows**.
- No data was copied. If the reliability team adds rows in Reliability_LH, they appear here immediately.

> 🧩 **Why it matters for SATORP:** the same pattern connects data that already lives elsewhere, such as ADLS Gen2, Amazon S3 or Dataverse, through **external shortcuts**. Fewer copies means one version of the truth, lower storage cost and simpler governance.

---

### Part E – Query OneLake with SQL (10 min)

Every lakehouse gets a free **SQL analytics endpoint**.

1. In **Refinery_LH**, use the switcher in the top-right corner to change from **Lakehouse** to **SQL analytics endpoint**.
2. Select **New SQL query**.
3. Paste and **Run** each query:

**Query 1 – Throughput attainment by unit (September 2026)**

```sql
SELECT  u.UnitName,
        ROUND(SUM(p.Throughput_kbbl) * 100.0 / SUM(p.PlannedThroughput_kbbl), 1) AS Attainment_pct
FROM    dbo.production_daily AS p
JOIN    dbo.units AS u ON p.UnitId = u.UnitId
GROUP BY u.UnitName
ORDER BY Attainment_pct;
```

✅ The lowest unit should be the **Fluid Catalytic Cracker (~86.7 %)**.

**Query 2 – Unplanned downtime hours by unit (uses the shortcut!)**

```sql
SELECT  u.UnitName,
        ROUND(SUM(d.DurationHours), 1) AS UnplannedHours
FROM    dbo.downtime_events AS d
JOIN    dbo.units AS u ON d.UnitId = u.UnitId
WHERE   d.Planned = 'No'
GROUP BY u.UnitName
ORDER BY UnplannedHours DESC;
```

✅ **Fluid Catalytic Cracker** is top again, with about **192.5 hours**.

> 💡 If a query says a table isn't found, remove the `dbo.` prefix. That depends on whether your lakehouse has schemas enabled.

---

### Part F – Find your data in the OneLake catalog (5 min)

1. In the left navigation, select **OneLake catalog**.
2. On the **Explore** tab, search for `Refinery_LH`. Open it to see its tables, owner and details.
3. Look at the **Govern** tab (what you can see depends on your role). This is where admins and data owners check sensitivity labels, endorsement and data health.

> 🧩 The OneLake catalog is how people across SATORP **discover** trusted data instead of asking around for "the latest spreadsheet".

---

## 4. Checkpoint

- [ ] Two lakehouses: `Refinery_LH` (4 tables + 1 shortcut) and `Reliability_LH` (1 table)
- [ ] Query 1 shows the FCC as the lowest attainment
- [ ] Query 2 runs across the shortcut, with no copied data
- [ ] You found `Refinery_LH` in the OneLake catalog

## 5. Challenge (optional)

- Install **OneLake file explorer** (Windows) and browse your lakehouse files like a OneDrive folder.
- If you have an Azure Data Lake Storage Gen2 account, create an **external shortcut** to a folder in it.

## 6. Troubleshooting

| Problem | Fix |
| --- | --- |
| **Load to Tables** is greyed out | The file is still uploading. Refresh the Explorer. |
| Shortcut can't see Reliability_LH | Both lakehouses must be in a workspace you can access. Refresh and try again. |
| Numbers differ slightly from the answer key | Check you loaded the right files and didn't load one twice. |
