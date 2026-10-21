# Microsoft Fabric with Copilot – OneLake & Fabric IQ Labs

### Three simple, hands-on labs built around a refinery reliability scenario for SATORP

| Lab | Title | What you do | Time |
| --- | --- | --- | --- |
| [Lab 1](Lab-1-OneLake-Foundations.md) | **OneLake foundations** | Create lakehouses, load refinery data, make a **shortcut** (one copy, no duplication), query it with SQL and find it in the **OneLake catalog** | 45 min |
| [Lab 2](Lab-2-Copilot-in-Fabric.md) | **Copilot in Fabric** | Use **Copilot in a notebook** to analyse data, build a **semantic model**, and let **Copilot in Power BI** build a report page | 50 min |
| [Lab 3](Lab-3-Fabric-IQ-Ontology-and-Data-Agent.md) | **Fabric IQ** | Build an **ontology** (Unit → Equipment → Work Order) and ask questions in business language with a **Fabric data agent** | 50 min |

Slides for the session: [`slides/Fabric-OneLake-IQ-for-SATORP.pptx`](slides/Fabric-OneLake-IQ-for-SATORP.pptx)

---

## The scenario

SATORP's reliability team wants one place to answer questions like:

- *"Which process unit lost the most production last month, and why?"*
- *"Which critical equipment still has open P1 work orders?"*

Today the answers are spread across production reports, maintenance systems and spreadsheets. In these labs you'll bring the data into **OneLake**, use **Copilot** to analyse it, and use **Fabric IQ** to describe it in the plant's own language (units, equipment, work orders), so anyone can ask questions in plain English.

> ⚠️ **All data in `lab-files/` is fictional sample data** created for training. Unit names follow a generic refinery layout. The numbers are invented and do **not** represent SATORP operations.

```
 lab-files/*.csv ──▶ Lab 1: OneLake ──────────────▶ Lab 2: Copilot ──────────▶ Lab 3: Fabric IQ
                     Refinery_LH (tables)            Notebook + Copilot           Ontology: Unit, Equipment,
                     Reliability_LH ─ shortcut ─▶     Semantic model               Work Order, Downtime
                     SQL endpoint · OneLake catalog   Copilot in Power BI          Data agent: ask in plain English
```

---

## Before you start

### You need

- [ ] A Microsoft Fabric workspace on a **paid Fabric capacity F2 or higher** (or Power BI Premium P1+). **Trial capacities don't support Copilot.**
- [ ] The **Contributor** role (or higher) on that workspace
- [ ] The five CSV files from `lab-files/`

### Ask your Fabric admin to confirm these tenant settings

Admin portal → **Tenant settings** (also reachable from **OneLake catalog → Govern**):

| Setting | Needed for |
| --- | --- |
| Users can create Fabric items | All labs |
| Users can use Copilot and other features powered by Azure OpenAI | Lab 2, Lab 3 |
| Data sent to Azure OpenAI can be processed outside your capacity's geographic region, compliance boundary, or national cloud instance | Lab 2, Lab 3, *only if* your capacity region requires it. Decide with your compliance team. |
| Users can create ontology (preview) items | Lab 3 |
| Data agent tenant settings (see Fabric data agent docs) | Lab 3 |

### Lab files

| File | Rows | Contents |
| --- | --- | --- |
| `units.csv` | 6 | Process units (CDU, hydrocrackers, FCC, coker, aromatics) with design capacity |
| `equipment.csv` | 30 | Equipment per unit, with type, criticality (A/B/C) and install year |
| `production_daily.csv` | 180 | Daily actual vs planned throughput per unit, September 2026 |
| `downtime_events.csv` | 37 | Downtime events July–September 2026, with cause, hours, planned yes/no |
| `work_orders.csv` | 60 | Maintenance work orders with priority, status, type and cost (SAR) |

---

## Status of features (October 2026)

| Feature | Status |
| --- | --- |
| OneLake, lakehouse, shortcuts, SQL analytics endpoint | Generally available |
| Copilot in Fabric (notebooks, Power BI, Data Factory) | Available on F2+; some capabilities are marked **preview** |
| Fabric data agent | Generally available |
| **Fabric IQ – Ontology** | **Preview.** Labels and steps may change |

> Things move fast in Fabric. If a button name on your screen differs slightly from this guide, pick the closest match.

---

## Answer key (for instructors)

| Question | Expected answer |
| --- | --- |
| Unit with the lowest throughput attainment in Sep 2026 | **U400 – Fluid Catalytic Cracker, ~86.7 %** |
| Unit with the most **unplanned** downtime (Jul–Sep) | **U400 – FCC, ~192.5 hours** |
| Top unplanned downtime cause (Jul–Sep) | **Fouling, ~184.5 hours** (Catalyst issue is second, ~174 h) |
| The FCC dip in production | **11–13 Sep 2026**, matching a 62-hour catalyst-issue event starting 12 Sep |
| Work orders by status | Completed 27 · In progress 18 · Open 15 |
| Open/in-progress **P1** work orders on **criticality A** equipment | **3** |
| Equipment by criticality | A 9 · B 13 · C 8 |
