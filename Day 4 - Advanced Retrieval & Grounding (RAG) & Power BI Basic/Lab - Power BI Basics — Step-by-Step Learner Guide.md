# Power BI Basics — Step-by-Step Learner Guide

**SATORP · Microsoft Data & AI Readiness Program** · Prepared by CodeSizzler

By the end of this lab you will turn a raw Excel file into an interactive Power BI report and publish it to share with your team. Plan for about **3 hours**, done step by step at your own pace. No coding experience needed.

## Contents

- [Welcome: what you will build](#welcome-what-you-will-build)
- [Step 1: Install Power BI Desktop and learn the screen](#step-1-install-power-bi-desktop-and-learn-the-screen)
- [Step 2: Create the practice file and get data](#step-2-create-the-practice-file-and-get-data)
- [Step 3: Clean the data in Power Query](#step-3-clean-the-data-in-power-query)
- [Step 4: Link the tables in the data model](#step-4-link-the-tables-in-the-data-model)
- [Step 5: Write your first DAX measures](#step-5-write-your-first-dax-measures)
- [Step 6: Build the report visuals](#step-6-build-the-report-visuals)
- [Step 7: Make the report interactive](#step-7-make-the-report-interactive)
- [Step 8: Publish and share in the Power BI Service](#step-8-publish-and-share-in-the-power-bi-service)
- [Practice, checklist and quick reference](#practice-checklist-and-quick-reference)

---

## Welcome: what you will build

**You will learn to:**

1. Connect Power BI to an Excel file
2. Clean data with Power Query (no code)
3. Link tables in a simple data model
4. Write your first DAX measures
5. Build charts, cards and slicers
6. Publish and share a report in the Power BI Service

**Before you start, you need:**

- A Windows laptop (Power BI Desktop is Windows only; Mac users can use a Windows VM or the browser-based Service)
- Your work Microsoft account (the same one you use for Outlook and Teams)
- Microsoft Excel, to create the practice file in Step 2
- No coding experience — every step is point-and-click unless stated

**The three parts of Power BI:**

| Part | Where it runs | What you use it for |
| --- | --- | --- |
| Power BI Desktop | Free app on your PC | Connect, clean, model and design reports |
| Power BI Service | Browser at app.powerbi.com | Publish, share, schedule refresh, build dashboards |
| Power BI Mobile | Phone or tablet app | View reports on the go |

The normal workflow is: **Get data → Clean → Model → Visualize → Publish → Share**. Each step below follows that order.

---

## Step 1: Install Power BI Desktop and learn the screen

Install the app from the Microsoft Store so it updates itself every month.

1. Open the **Microsoft Store** on your PC and search for **Power BI Desktop**.
2. Click **Get** (or **Install**). It is free.
3. Open Power BI Desktop and click **Sign in** (top right) with your work account.
4. Close the welcome screen. You now see a blank report canvas.

**Find your way around the screen:**

| Area | Where | What it does |
| --- | --- | --- |
| Ribbon | Top | Home, Insert, Modeling, View tabs — like Excel |
| Report view | Left bar, top icon | The canvas where you build charts |
| Table view | Left bar, middle icon | See your data rows, like a spreadsheet |
| Model view | Left bar, bottom icon | See tables and the lines (relationships) between them |
| Visualizations pane | Right | Pick a chart type and drop fields into it |
| Data pane | Far right | Lists your tables and columns |
| Filters pane | Right, next to Visualizations | Filter one visual, one page or the whole report |
| Page tabs | Bottom | Add or rename report pages |

> **Try it:** click each of the three left-bar icons once and notice how the screen changes. Then save the empty file as **SATORP_PowerBI_Basics.pbix** in a folder you can find again.

---

## Step 2: Create the practice file and get data

You will practise on a small, made-up refinery shipments file with two sheets. The data is fictional and for training only.

### 2a. Build the Excel file

1. Open Excel and create a new workbook.
2. Rename the first sheet **Shipments** and paste the data below into cell A1.
3. Add a second sheet named **Products** and paste the second block into A1.
4. If the data lands in one column, select column A, then **Data → Text to Columns → Delimited → Comma → Finish**.
5. Save the workbook as **Refinery_Shipments.xlsx** and close it.

Sheet 1 — Shipments:

```csv
ShipmentID,ShipDate,ProductID,Customer - Country,Volume_bbl,Price_USD_per_bbl,Notes
S001,2026-01-05,P01,Gulf Energy - UAE,12000,92,ok
S002,2026-01-12,P02,Asia Fuels - India,8500,88,ok
S003,2026-01-20,P03,Euro Petro - Germany,6000,105,late
S004,2026-02-03,P01,Asia Fuels - India,15000,90,ok
S005,2026-02-14,P04,Gulf Energy - UAE,4000,70,ok
S006,2026-02-25,P02,Pacific Oil - Japan,9800,87,ok
S007,2026-03-04,P03,Gulf Energy - UAE,7200,104,ok
S008,2026-03-15,P01,Euro Petro - Germany,11000,93,late
S009,2026-03-28,P04,Pacific Oil - Japan,5200,72,ok
S010,2026-04-06,P02,Euro Petro - Germany,10400,89,ok
S011,2026-04-18,P03,Asia Fuels - India,6800,103,ok
S012,2026-04-29,P01,Pacific Oil - Japan,13500,91,ok
```

Sheet 2 — Products:

```csv
ProductID,ProductName,Category
P01,Diesel,Fuels
P02,Gasoline,Fuels
P03,Jet Fuel,Fuels
P04,Propylene,Petrochemicals
```

### 2b. Connect Power BI to the file

1. In Power BI Desktop, click **Home → Get data → Excel workbook**.
2. Browse to **Refinery_Shipments.xlsx** and click **Open**.
3. The **Navigator** window opens. Tick both **Shipments** and **Products**.
4. Look at the preview on the right to check the data looks right.
5. Click **Transform Data** (not Load). This opens Power Query so you can clean the data first.

> **Load vs Transform Data:** *Load* brings the data in as it is. *Transform Data* lets you fix it first. Choose Transform Data whenever you are unsure — it is the safer habit.

---

## Step 3: Clean the data in Power Query

Power Query records every click as an **Applied Step**, so you can undo or change any step later. Nothing changes in your original Excel file.

1. In the **Queries** list on the left, click **Shipments**.
2. **Check the header row.** If the first row shows Column1, Column2…, click **Home → Use First Row as Headers**.
3. **Remove a column you don't need.** Right-click the **Notes** column header → **Remove**.
4. **Split a combined column.** Click **Customer - Country**, then **Home → Split Column → By Delimiter**. Choose **Custom**, type space-dash-space (` - `) and click **OK**.
5. **Rename the new columns.** Double-click each header and rename them **Customer** and **Country**.
6. **Set data types.** Click the small icon left of each header and set:
   - ShipDate → **Date**
   - Volume_bbl → **Whole Number**
   - Price_USD_per_bbl → **Decimal Number**
   - All ID and name columns → **Text**
7. **Add a calculated column.** Click **Add Column → Custom Column**. Name it **Revenue_USD** and enter the formula `[Volume_bbl] * [Price_USD_per_bbl]`. Click **OK**, then set its type to **Decimal Number**.
8. Click **Products** in the Queries list and repeat steps 2 and 6 (all three columns are Text).
9. Look at the **Applied Steps** list on the right. Click any step to see the data at that point.
10. Click **Home → Close & Apply**. Power BI loads the clean tables.

> **Tip:** turn on **View → Column quality** in Power Query. It shows the percentage of valid, error and empty values under each header — a quick health check.

---

## Step 4: Link the tables in the data model

A relationship tells Power BI that **ProductID** in Shipments means the same thing as **ProductID** in Products. Without it, a chart of revenue by product name shows the same total on every bar.

1. Click the **Model view** icon on the left bar.
2. You see two boxes: **Shipments** and **Products**. Power BI may already have drawn a line between them. If so, skip to step 4.
3. If there is no line, drag **ProductID** from Products and drop it on **ProductID** in Shipments.
4. Double-click the line to open **Edit relationship** and check:
   - Cardinality: **Many to one (\*:1)** — many shipments, one product
   - Cross filter direction: **Single**
   - **Make this relationship active** is ticked
5. Click **OK**.

**Key idea — the star schema:**

- **Fact table** (Shipments): many rows, holds the numbers you add up — volume, price, revenue.
- **Dimension table** (Products): few rows, holds the descriptions you slice by — product name, category.
- Keep dimensions on the "one" side and facts on the "many" side. Real reports add more dimensions (Date, Customer, Plant) around the same fact table, like the points of a star.

```
            ┌────────────┐
            │  Products  │  (dimension, "one" side)
            └─────┬──────┘
                  │ 1
                  │
                  │ *
            ┌─────┴──────┐
            │ Shipments  │  (fact, "many" side)
            └────────────┘
```

---

## Step 5: Write your first DAX measures

DAX is Power BI's formula language, similar to Excel formulas. A **measure** is a calculation that recalculates for whatever the user has filtered — always prefer measures for totals and averages.

| | Calculated column | Measure |
| --- | --- | --- |
| Calculated | Once per row, when data loads | On the fly, for each visual and filter |
| Stored | In the table (uses memory) | Not stored |
| Use it for | Labels and categories you slice by | Totals, averages, ratios, KPIs |

**Create a measure:**

1. Go to **Report view**. In the **Data** pane, right-click the **Shipments** table → **New measure**.
2. The formula bar opens at the top. Type the first formula below and press **Enter**.
3. Repeat for each measure. Each one appears in the Data pane with a calculator icon.
4. Select each measure and use **Measure tools → Format** to set currency or a thousands separator.

Copy these five measures one at a time:

```dax
Total Revenue = SUM(Shipments[Revenue_USD])

Total Volume (bbl) = SUM(Shipments[Volume_bbl])

Shipment Count = COUNTROWS(Shipments)

Avg Price per bbl = DIVIDE([Total Revenue], [Total Volume (bbl)])

Fuels Revenue = CALCULATE([Total Revenue], Products[Category] = "Fuels")
```

**What each function does:**

- `SUM` adds up a column.
- `COUNTROWS` counts the rows in a table.
- `DIVIDE` divides safely — it returns blank instead of an error when dividing by zero.
- `CALCULATE` changes the filter before calculating; here it keeps only Fuels products.

> **Check your work:** put each measure in a Card visual (Step 6). You should see:
>
> | Measure | Expected value |
> | --- | --- |
> | Total Revenue | 9,965,300 |
> | Total Volume (bbl) | 109,400 |
> | Shipment Count | 12 |
> | Avg Price per bbl | 91.09 |
> | Fuels Revenue | 9,310,900 |
>
> If a number differs, recheck the data types in Step 3.

---

## Step 6: Build the report visuals

Every visual follows the same three moves: **click an empty spot on the canvas → pick a visual type → drag fields into its wells**. Build these five visuals on Page 1.

| # | Visual (Visualizations pane) | Drag these fields | Answers the question |
| --- | --- | --- | --- |
| 1 | Card | Total Revenue | How much did we sell? |
| 2 | Card | Total Volume (bbl) | How many barrels did we ship? |
| 3 | Clustered bar chart | Y-axis: Products[ProductName] · X-axis: Total Revenue | Which product earns the most? |
| 4 | Line chart | X-axis: Shipments[ShipDate] · Y-axis: Total Revenue | How is revenue trending by month? |
| 5 | Table | Customer, Country, Total Volume (bbl), Total Revenue | Who are our customers and what did they buy? |

**Step-by-step for visual 3 (use the same pattern for the others):**

1. Click an empty area of the canvas so nothing is selected.
2. In **Visualizations**, click the **Clustered bar chart** icon. An empty box appears.
3. In the **Data** pane, drag **ProductName** into the **Y-axis** well.
4. Drag **Total Revenue** into the **X-axis** well. The bars appear.
5. Drag the corners of the box to resize it, and drag its title bar to move it.

**For the line chart:** Power BI turns ShipDate into a Year → Quarter → Month → Day hierarchy. In the X-axis well, click the **x** next to Year, Quarter and Day so only **Month** remains.

**Make it look professional:**

1. Select a visual and click the **paintbrush** icon (Format visual).
2. Under **General → Title**, write a clear title, for example "Revenue by Product (USD)".
3. Under **Visual → Data labels**, switch labels **On** for the bar chart.
4. Use **View → Themes** to apply one colour theme to the whole report.
5. Add a report heading with **Insert → Text box**: "Refinery Shipments — Jan to Apr 2026".
6. Align visuals with **Format → Align** so edges line up.

---

## Step 7: Make the report interactive

Interactivity lets readers answer their own questions without asking you for a new report.

### 7a. Add slicers

1. Click an empty spot, then click the **Slicer** icon in Visualizations.
2. Drag **Products[Category]** into the **Field** well.
3. In Format visual → **Slicer settings → Style**, choose **Tile** to show buttons.
4. Add a second slicer for **Country**, and a third for **ShipDate** (it shows as a date range slider).
5. Click **Petrochemicals** — every visual on the page updates.

### 7b. Cross-filter by clicking

1. Click the **Diesel** bar in the bar chart. The cards, line chart and table now show Diesel only.
2. Click the bar again (or an empty area of the chart) to clear it.
3. To stop one visual affecting another: select the bar chart, then **Format → Edit interactions**, and click the **ø (None)** icon above the visual you want to protect.

### 7c. Use the Filters pane

1. Open the **Filters** pane on the right.
2. Drag **Customer** into **Filters on this page**.
3. Untick a customer to hide it from the whole page. Readers can change this too, unless you lock it with the padlock icon.

### 7d. Drill down in the line chart

1. Put **ShipDate** back as the full Year → Quarter → Month hierarchy in the line chart.
2. Hover over the chart and click the **double down arrow** to go to the next level.
3. Click the **up arrow** to drill back up.

> **Try it:** save your file (Ctrl+S). Answer: which country bought the most Jet Fuel? Use the slicers, not your eyes on the raw data.

---

## Step 8: Publish and share in the Power BI Service

Publishing copies your report to app.powerbi.com so others can view it in a browser, in Teams or on mobile.

### 8a. Publish

1. Save your file, then click **Home → Publish**.
2. Choose a workspace. Use **My workspace** for practice, or the training workspace your instructor gives you.
3. When you see **Success!**, click **Open in Power BI**.

### 8b. Explore the Service

| Item | What it is |
| --- | --- |
| Workspace | A shared folder for a team's reports and data |
| Semantic model | The data and measures you built (formerly called a dataset) |
| Report | Your pages of visuals, interactive in the browser |
| Dashboard | A single page of tiles pinned from one or more reports |
| App | A packaged, read-only bundle of reports for wide audiences |

### 8c. Pin to a dashboard

1. Open your report in the Service and hover over the **Total Revenue** card.
2. Click the **pin** icon → **New dashboard** → name it **Refinery KPIs** → **Pin**.
3. Pin the bar chart to the same dashboard. Open **Refinery KPIs** from the workspace to see both tiles.

### 8d. Share

1. In the report, click **Share** (top bar).
2. Enter a colleague's email, choose whether they can reshare, and click **Send**.
3. For a team, give them a workspace role instead (**Viewer**, **Contributor**, **Member** or **Admin**) under **Manage access**.

> Sharing needs a **Power BI Pro** or **Premium Per User** licence, or a workspace on Premium/Fabric capacity. Check with your IT team which one SATORP uses.

### 8e. Keep data fresh

- A report built on a file on your laptop does not refresh by itself. Store the Excel file in **OneDrive or SharePoint** and connect to it from there, and the Service can refresh it automatically.
- On-premises sources (SQL Server, plant historians) need an **on-premises data gateway**, set up by IT.
- To schedule refresh: workspace → your semantic model → **Settings → Scheduled refresh**.

---

## Practice, checklist and quick reference

### Mini project (30 minutes, on your own)

Add a second report page called **Customer View** that answers three questions:

1. Which customer brought in the most revenue? (bar chart + Total Revenue)
2. What is each country's share of volume? (donut chart + Total Volume)
3. How many shipments were late? Create this measure:

   ```dax
   Late Shipments = CALCULATE([Shipment Count], Shipments[Notes] = "late")
   ```

   Hint: you removed Notes in Step 3 — go back to **Transform data**, delete the **Removed Columns** step, then Close & Apply. Expected answer: **2**.

### Self-check

- [ ] Connected Power BI to an Excel file
- [ ] Removed, split and renamed columns in Power Query
- [ ] Set the correct data types
- [ ] Created a Many-to-one relationship
- [ ] Wrote five DAX measures and matched the expected numbers
- [ ] Built cards, a bar chart, a line chart and a table
- [ ] Added slicers and used cross-filtering
- [ ] Published, pinned to a dashboard and shared

### Common mistakes and fixes

| Problem | Likely cause | Fix |
| --- | --- | --- |
| Same total on every bar | No relationship between tables | Create it in Model view (Step 4) |
| Numbers are left-aligned and won't sum | Column type is Text | Change type to Whole or Decimal Number in Power Query |
| Line chart shows one point | Date column type is Text, or Year level only | Set type to Date; remove Year/Quarter from the axis |
| Measure shows an error | Typo in table or column name | Type `[` or `'` and pick from the autocomplete list |
| Share button greyed out | No Pro/PPU licence | Ask IT for a licence or a capacity workspace |

### Handy shortcuts

| Keys | Action |
| --- | --- |
| Ctrl + S | Save |
| Ctrl + Z | Undo |
| Ctrl + C / Ctrl + V | Copy and paste a visual |
| Ctrl + G | Group selected visuals |
| Ctrl + click | Select several visuals, or several bars to cross-filter |
| Alt + Enter | New line in the DAX formula bar |

### Glossary

| Term | Meaning |
| --- | --- |
| Power Query | The built-in tool to clean and shape data before loading |
| Applied Steps | The recorded list of cleaning actions in Power Query |
| DAX | Data Analysis Expressions, the formula language for measures |
| Measure | A calculation that responds to filters, such as Total Revenue |
| Relationship | A link between two tables on a shared column |
| Slicer | An on-canvas filter readers click |
| Semantic model | The published data, relationships and measures behind a report |
| Workspace | A shared area in the Service for a team's content |

### Keep learning

The free [Microsoft Learn Power BI training](https://learn.microsoft.com/training/powerplatform/power-bi) paths cover each of these topics in more depth, and lead towards the **PL-300 Power BI Data Analyst** certification.

---

*© CodeSizzler · Training material prepared for SATORP. Sample data is fictional.*
