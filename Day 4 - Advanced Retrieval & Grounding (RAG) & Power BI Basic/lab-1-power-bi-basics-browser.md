# Lab 1 – Power BI Basics (Browser Alternative)

> **Use this version only if you cannot install Power BI Desktop.**

Power BI Desktop is a Windows-only application. If you are on a Mac, or your laptop does not allow software installation, work through this version instead. It runs entirely in the browser using the Power BI service in Microsoft Fabric, and reaches the same outcome: a cleaned dataset, DAX measures, and two dashboards.

The learning is identical. Only the tool differs: **Power Query Online** replaces the Power Query Editor in Desktop, and you build visuals in the browser rather than in a desktop window.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Part 1 – Connecting and Shaping the Messy Data](#part-1--connecting-and-shaping-the-messy-data)
- [Part 2 – Level 1 Dashboard: The Quick Win](#part-2--level-1-dashboard-the-quick-win)
- [Part 3 – Level 2 Dashboard: The Advanced Deep Dive](#part-3--level-2-dashboard-the-advanced-deep-dive)
- [Part 4 – Sharing](#part-4--sharing)
- [Differences from the Desktop version](#differences-from-the-desktop-version)

---

## Prerequisites

- No software to install.
- Your assigned Fabric workspace, `ws-p1-<your user name>`. **Do not create a new workspace.**
- The provided dataset: `raw_customer_data_large.csv`, downloaded to your machine.
- A Power BI trial. The first time you try to create a report you will see **"Upgrade to a paid Power BI license"**. Click **Try free** to start the free 60-day trial. You only do this once, and it covers the whole course.

---

## Part 1 – Connecting and Shaping the Messy Data

Same data rescue as the Desktop version, using Power Query Online inside a **Dataflow Gen2**.

### Step 1 – Ingest the data

1. Go to [app.fabric.microsoft.com](https://app.fabric.microsoft.com) and open your assigned workspace, `ws-p1-<your user name>`.
2. Select **New item**, then **Dataflow Gen2**. Name it `Customer_Data_Cleanup` and select **Create**.
3. On the start screen choose **Import from a Text/CSV file**.
4. Select **Upload file**, browse to `raw_customer_data_large.csv` on your machine, and select **Next**.
5. Check the preview shows the columns `CustomerID`, `Name`, `Email`, `SignupDate`, `Country`, `AnnualSpend` and `Phone`, then select **Create**.

You are now in the Power Query editor, the same editor as in Desktop with the same ribbon tabs.

### Step 2 – Clean the messy data

#### Standardize country names

1. Select the **Country** column.
2. Go to the **Transform** tab, then **Format**, then **Capitalize Each Word**. This fixes "canada" to "Canada".
3. The United States appears five different ways in this data: `USA`, `usa`, `U.S.A.`, `United States`, and `United States of America`. Capitalize Each Word does not merge them. Right-click the **Country** column header, choose **Replace Values**, and run it once for each variant so they all become `United States`:
   - replace `Usa`
   - then `U.S.A.`
   - then `United States Of America`

   > Note that Capitalize Each Word will have changed "of" to "Of".

4. Check the **Country** filter list afterwards.

> ⚠️ If you skip this, your distinct-country count will be wrong and nothing will warn you.

#### Handle invalid spend data

1. Select the filter arrow on the **AnnualSpend** column and uncheck **(null)** to remove customers with no spend recorded.
2. Select the filter arrow again, choose **Number Filters**, then **Greater Than**, enter `0`, and select **OK**. This removes negative spend values.

#### Eliminate system duplicates

1. On the **Home** tab select **Remove rows**, then **Remove duplicates**. This removes the glitch duplicates left by a double import.
2. Check the row count at the bottom of the editor before and after, so you can see how many were removed.

### Step 3 – Save the cleaned data

1. Select the **+** icon at the bottom right of the editor to add a data destination, and choose **Lakehouse**.
2. Select your `Organizational_Data_Lakehouse` if you created one on Day 4, or create a new Lakehouse named `Customer_Analytics`.
3. Name the destination table `customers_clean` and select **Next**, then **Save settings**.
4. Select **Save and run** at the top left. Wait for the refresh to complete.

> ✅ **Checkpoint:** your Lakehouse now has a `customers_clean` table containing only valid, de-duplicated rows.

---

## Part 2 – Level 1 Dashboard: The Quick Win

### Step 1 – Create the semantic model and measures

1. Return to your workspace. Select **New item**, then **Semantic model**.
2. Select your Lakehouse, tick the `customers_clean` table, and confirm.
3. Open the semantic model and select **New measure**. Create each of these, pressing the tick to commit:

```dax
Total Customers = DISTINCTCOUNT(customers_clean[CustomerID])
```

```dax
Total Spend = SUM(customers_clean[AnnualSpend])
```

```dax
Average Spend = AVERAGE(customers_clean[AnnualSpend])
```

> 💡 These are the same DAX expressions as the Desktop version. DAX does not change between Desktop and the browser.

### Step 2 – Build the executive view

1. From the semantic model select **Create report**, or go to your workspace and select **New item**, then **Report**, then pick this semantic model.
2. Add three **Card** visuals and place **Total Customers**, **Total Spend** and **Average Spend** on them.
3. Add a **Map** or a **Filled map** visual, put **Country** on **Location** and **Total Spend** on **Bubble size**.
4. Add a **Bar chart** with **Country** on the **Y axis** and **Total Spend** on the **X axis**, then sort it descending.
5. Select **File**, then **Save**, and name the report `Executive Overview`.

---

## Part 3 – Level 2 Dashboard: The Advanced Deep Dive

1. Add a new page to the report using the **+** at the bottom of the canvas.
2. Add a **Matrix** visual. Put **Country** on **Rows** and **Total Spend** and **Total Customers** on **Values**.
3. With the matrix selected, open the **Format** pane, find **Cell elements**, and switch on **Background color** for **Total Spend**. This gives you the conditional formatting from the Desktop version.
4. Add a High-Value Customer measure in the semantic model:

   ```dax
   High Value Customers =
   CALCULATE(
       DISTINCTCOUNT(customers_clean[CustomerID]),
       customers_clean[AnnualSpend] > 5000
   )
   ```

5. Add that measure to the matrix as a third value.
6. Add a **Slicer** visual with **Country**, so regional managers can filter the page.
7. Save the report.

---

## Part 4 – Sharing

Your report is already in the Power BI service, so there is no publish step. It lives in your own workspace and only you can see it. In a real deployment you would share it from the **Share** button, but on this course each participant has a private workspace, so there is nobody to share it with.

---

## Differences from the Desktop version

| Area | Browser version |
| --- | --- |
| Publishing | There is no publish step. Work is saved in the service as you go. |
| Power Query | Power Query Online has the same transforms but a slightly different ribbon layout. |
| Measures | Measures are created in the semantic model rather than in the report file. |
| Formatting | Some advanced formatting options available in Desktop are not present in the browser. Where a formatting step cannot be found, note it and move on; it does not affect the learning outcome. |
