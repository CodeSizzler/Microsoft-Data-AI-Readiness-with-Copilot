# Day 2 Lab: Data Fundamentals for AI

*Preparing a Sample Dataset for Use — fixed, tested, and runnable in VS Code or Microsoft Fabric*

> **What changed in this version — three real bugs, found by actually running the code**
>
> 1. **Dates were silently corrupted.** `pd.to_datetime(..., dayfirst=True)` without `format="mixed"` turned 1,653 of 2,063 rows (80%) into blank dates, because pandas cannot auto-detect five mixed date formats in one column from `dayfirst` alone. Fixed by adding `format="mixed"`, verified 0 blank dates afterward.
>
> 2. **"Duplicate" customers were never actually removed.** The dataset intentionally plants duplicate customers, but each copy gets its own new `CustomerID` — so a full-row duplicate check (and `drop_duplicates()` with no subset) always finds 0, both in profiling and after "cleaning." Fixed by detecting and dropping duplicates on `Email` (the real business key) instead. This is also a legitimate teaching moment, kept in Part 4 on purpose: a surrogate key can hide a duplicate real-world record.
>
> 3. **The VS Code / local path stopped at Part 2.** Parts 3 and 7 only worked inside a provisioned Microsoft Fabric workspace, with no way to complete the lab without one. Added a local, Fabric-free equivalent for both parts using `sqlite3` (built into Python — nothing to install) so the whole lab runs end-to-end in VS Code alone.
>
> Every code block below was actually run against a generated 2,000+ row dataset before this document was written — not just reviewed by eye.

## How to use this lab

This lab has two tracks for Parts 3 and 7, the two steps that originally required a Microsoft Fabric workspace. Everything else (Parts 1, 2, 4, 5, 6, 8) is identical either way and needs only Python.

| Track | Use when | What you need |
| --- | --- | --- |
| **Fabric track** (original) | You have an assigned Fabric workspace for this course | A browser, access to `app.fabric.microsoft.com`, your `ws-p1-<username>` workspace |
| **VS Code / local track** (new) | You don't have Fabric access yet, or want to work offline | Python 3, `pandas`, `faker` — nothing else to install |

Both tracks produce the same two files you need for Part 8: `raw_customer_data_large.csv` and `cleaned_customer_data_large.csv`. Pick one track and stay on it for the whole lab — don't mix Fabric for one part and local for another, or your row counts in Part 5 won't line up.

## Part 1 — Generate the Dataset (Code-Based)

**Where to write this code:** VS Code (or any editor) with Python 3, a Jupyter/Colab notebook, or a Fabric notebook cell — whichever you have. The steps below assume a local editor + terminal; in a notebook, paste the same code into a cell and run the cell instead.

1. Create a new file named `generate_dataset.py` in a folder you can find again, e.g. `Documents/data-fundamentals-lab/`.
2. Paste in the code below.

```python
import random
import csv
from datetime import date, timedelta
from faker import Faker

random.seed(42)
fake = Faker()
Faker.seed(42)

ROW_COUNT = 2000

COUNTRY_VARIANTS = {
    "United States": ["USA", "usa", "United States", "U.S.A.", "United States of America"],
    "Canada": ["Canada", "CANADA", "canada"],
    "Spain": ["Spain", "spain", "SPAIN"],
    "China": ["China", "china", "CHINA"],
    "Egypt": ["Egypt", "egypt", "EGYPT"],
    "Ireland": ["Ireland", "ireland", "IRELAND"],
    "Germany": ["Germany", "germany", "GERMANY"],
    "India": ["India", "india", "INDIA"],
    "Brazil": ["Brazil", "brazil", "BRAZIL"],
    "Australia": ["Australia", "australia", "AUSTRALIA"],
}

DATE_FORMATS = ["%m/%d/%Y", "%d-%m-%Y", "%m/%d/%y", "%Y-%m-%d", "%d/%m/%Y"]

def random_date():
    start = date(2022, 1, 1)
    end = date(2024, 12, 31)
    d = start + timedelta(days=random.randint(0, (end - start).days))
    return d.strftime(random.choice(DATE_FORMATS))

def messy_case(text, chance=0.35):
    r = random.random()
    if r < chance / 2:
        return text.upper()
    elif r < chance:
        return text.lower()
    return text

def random_phone():
    return f"555-{random.randint(1000,9999)}" if random.random() > 0.5 else f"555{random.randint(1000,9999)}"

rows = []
customer_id = 1000

for i in range(ROW_COUNT):
    customer_id += 1
    name = fake.name()
    email = f"{name.lower().replace(' ', '.')}@email.com"
    country_key = random.choice(list(COUNTRY_VARIANTS.keys()))
    country = random.choice(COUNTRY_VARIANTS[country_key])
    spend = round(random.uniform(50, 5000), 2)

    if random.random() < 0.05:
        spend = ""
    elif random.random() < 0.02:
        spend = -abs(spend)

    if random.random() < 0.04:
        name = ""

    phone = random_phone()
    if random.random() < 0.05:
        phone = ""

    row = {
        "CustomerID": customer_id,
        "Name": messy_case(name) if name else "",
        "Email": messy_case(email, chance=0.3) if name else email,
        "SignupDate": random_date(),
        "Country": country,
        "AnnualSpend": spend,
        "Phone": phone,
    }
    rows.append(row)

    if random.random() < 0.03:
        customer_id += 1
        dup = row.copy()
        dup["CustomerID"] = customer_id
        rows.append(dup)

with open("raw_customer_data_large.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["CustomerID", "Name", "Email", "SignupDate", "Country", "AnnualSpend", "Phone"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> raw_customer_data_large.csv")
```

3. Open a terminal in that folder (VS Code: Terminal → New Terminal) and install the one dependency:

```bash
pip install faker --break-system-packages
# or: python3 -m pip install faker --break-system-packages
# Colab: run  !pip install faker  in a cell instead
```

4. Run it:

```bash
python3 generate_dataset.py
```

5. Confirm `raw_customer_data_large.csv` now exists in that folder with 2,000+ rows. Tested output: `Generated 2063 rows -> raw_customer_data_large.csv`.
6. To change the dataset size, edit `ROW_COUNT` near the top and re-run.

## Part 2 — Measure Why Data Quality Matters

**Where to write this code:** same folder, a new file `baseline_check.py` (or a new notebook cell).

Run this on the raw dataset, before touching it:

```python
import pandas as pd

df = pd.read_csv("raw_customer_data_large.csv")

print("Row count:", len(df))
print("Average AnnualSpend (raw):", df["AnnualSpend"].mean())
print("\nCustomer count by Country (raw, unstandardized):")
print(df["Country"].value_counts())
```

Record two numbers in your notes:

- Average `AnnualSpend`
- Number of distinct “Country” labels shown — note how many of them are really the same country (e.g. `USA`, `usa`, `United States` counted separately)

Tested reference output: average `AnnualSpend` ≈ 2402.98, with 32 distinct Country labels for only 10 real countries. Your own numbers may differ slightly — `generate_dataset.py` uses a fixed random seed, but exact figures can still shift a little across Python/Faker versions, so treat these as a sanity check, not an answer key.

Keep this output — you'll re-run the same two calculations in Part 5 on the cleaned data and compare them side by side.

## Part 3 — Load the Dataset into a Queryable Table

Pick the track you chose in “How to use this lab” above.

### Track A — Microsoft Fabric / OneLake

1. Go to `app.fabric.microsoft.com` and sign in.
2. Workspaces → open your assigned workspace, `ws-p1-<your user name>`. Do not create a new workspace — a new one has no capacity and Fabric items will fail to create.
3. **+ New item → Lakehouse** → name it `data_fundamentals_lab`.
4. Open it → Files → upload `raw_customer_data_large.csv`.
5. Open a new Notebook attached to the lakehouse and run:

```python
df = spark.read.option("header", "true").csv("Files/raw_customer_data_large.csv")
df.show(10)
print("Row count:", df.count())
```

6. Confirm the row count matches Part 1.

### Track B — VS Code / local (no Fabric needed)

Same idea — load the CSV into a table you can query with SQL — using `sqlite3`, which ships with Python. Create `load_to_local_lakehouse.py` next to your CSV:

```python
"""
VS Code / local-only stand-in for Part 3 (Set Up OneLake / Fabric).

If you don't have a Fabric workspace yet, this reproduces the same idea -- load a CSV into a
queryable table in a "lakehouse" -- using sqlite3 (built into Python, no install needed) instead
of a Spark/Fabric Lakehouse. Same mental model: Files -> a table you can query with SQL.
When you do have a Fabric workspace, use the real notebook cell from the lab document instead;
this script exists so you aren't blocked while waiting for one.
"""
import sqlite3
import pandas as pd

df = pd.read_csv("raw_customer_data_large.csv")

conn = sqlite3.connect("local_lakehouse.db")
df.to_sql("raw_customers", conn, if_exists="replace", index=False)

row_count = conn.execute("SELECT COUNT(*) FROM raw_customers").fetchone()[0]
print("Row count:", row_count)
print(pd.read_sql("SELECT * FROM raw_customers LIMIT 10", conn))

conn.close()
```

Run it (`python3 load_to_local_lakehouse.py`) and confirm the printed row count matches Part 1. `local_lakehouse.db` is now your stand-in “lakehouse” for the rest of this track.

## Part 4 — Profile and Clean the Dataset

**Where to write this code:** same folder/notebook as Part 1.

### Step 4.1 — Profile the raw data

Create `profile_dataset.py` (or a new cell) and run:

```python
import pandas as pd

df = pd.read_csv("raw_customer_data_large.csv")

print("Total rows:", len(df))
print("\nMissing values per column:\n", df.isnull().sum())

# Exact full-row duplicates -- almost always 0 here, because every row carries its own
# unique CustomerID even when it is a duplicate customer. This is the point, not a mistake:
# a surrogate key can make two rows LOOK unique while the underlying customer is repeated.
print("\nExact duplicate rows (all columns, including CustomerID):", df.duplicated().sum())

# The real check: duplicate on a business key (Email), case-insensitive, ignoring CustomerID.
email_key = df["Email"].str.lower()
print("Duplicate customers by Email (CustomerID ignored):", email_key.duplicated(keep="first").sum())

print("\nUnique Country values:\n", df["Country"].unique())
print("\nRows with negative AnnualSpend:", (df["AnnualSpend"] < 0).sum())
print("\nSample of SignupDate values:\n", df["SignupDate"].sample(10, random_state=1).tolist())
```

Record all output numbers in your notes. You should see two different duplicate counts here — that contrast is deliberate; see the callout at the top of this document.

### Step 4.2 — Clean the data

Create `clean_dataset.py` in the same folder and run:

```python
import pandas as pd

df = pd.read_csv("raw_customer_data_large.csv")

df["Name"] = df["Name"].str.title()
df["Email"] = df["Email"].str.lower()

country_map = {
    "usa": "United States", "u.s.a.": "United States",
    "united states of america": "United States", "united states": "United States",
    "canada": "Canada",
    "spain": "Spain",
    "china": "China",
    "egypt": "Egypt",
    "ireland": "Ireland",
    "germany": "Germany",
    "india": "India",
    "brazil": "Brazil",
    "australia": "Australia",
}
# FIX: match case-insensitively instead of listing every upper/lower/title variant by hand --
# the original dict mapped "canada" and "CANADA" but relied on .map() doing an exact-string
# match, which is correct but brittle: any variant the author didn't think to list (a stray
# "Canada " with trailing space, for example) would silently fall through to fillna() and
# survive uncleaned. Lowering the column first makes the map exhaustive by construction.
df["Country"] = df["Country"].str.strip().str.lower().map(country_map).fillna(df["Country"])

# FIX: the original call -- pd.to_datetime(df["SignupDate"], errors="coerce", dayfirst=True) --
# silently turned 1,653 of 2,063 rows (80%) into NaT. pandas will not auto-detect FIVE
# different mixed date formats in one column from dayfirst alone; it infers a single format
# from the data and coerces everything else to NaT. Adding format="mixed" tells pandas to
# parse every value independently (via dateutil) instead of assuming one shape for the whole
# column. Verified: 0 NaT after this fix, versus 1,653 before it.
df["SignupDate"] = pd.to_datetime(
    df["SignupDate"], errors="coerce", dayfirst=True, format="mixed"
).dt.strftime("%Y-%m-%d")
# NOTE (worth saying out loud in your cleansing log): dayfirst=True is still a best-effort
# guess for the small number of dates where day and month are both <= 12 (e.g. "03/04/2023"
# could mean 3-Apr or 4-Mar depending on which of the five source formats produced it). That
# ambiguity cannot be recovered after the fact from the value alone -- which is exactly why
# "one consistent format, captured at the source" (Slide 34) beats fixing it downstream.

# FIX: drop_duplicates() on the full row (the original approach) removes 0 rows, because the
# planted duplicate copies deliberately carry a different CustomerID. Dedupe on the business
# key (Email, case-insensitive) instead, which is what actually identifies a repeated customer.
df["_email_key"] = df["Email"].str.lower()
before = len(df)
df = df.drop_duplicates(subset="_email_key", keep="first").drop(columns="_email_key")
print(f"Dropped {before - len(df)} duplicate-customer rows (matched on Email, CustomerID ignored)")

df["Flag_MissingName"] = df["Name"].isna() | (df["Name"].astype(str).str.strip() == "")
df["Flag_MissingSpend"] = df["AnnualSpend"].isna()
df["Flag_ReviewSpend"] = df["AnnualSpend"] < 0

def format_phone(p):
    if pd.isna(p) or str(p).strip() == "":
        return ""
    digits = "".join(filter(str.isdigit, str(p)))
    if len(digits) == 7:
        return f"555-{digits[3:]}" if digits.startswith("555") else digits
    return p

df["Phone"] = df["Phone"].apply(format_phone)
df["Flag_MissingPhone"] = df["Phone"] == ""

df.to_csv("cleaned_customer_data_large.csv", index=False)
print("Saved", len(df), "rows")
```

### Step 4.3 — Re-profile the cleaned data

Re-run the Step 4.1 profiling code, pointing it at `cleaned_customer_data_large.csv` instead. Confirm: 0 blank (NaT) dates, one consistent spelling per country, 0 remaining duplicate customers by Email.

### Step 4.4 — Write a cleansing log

Write 4–6 sentences covering: what was changed, how missing values were handled, how the negative `AnnualSpend` value was flagged (not silently altered), and how the duplicate-customer rows were actually found and removed.

## Part 5 — Compare Before vs. After

**Where to write this code:** same folder/notebook. Create `compare_results.py`.

Run the same two calculations from Part 2, this time on the cleaned file:

```python
import pandas as pd

df_clean = pd.read_csv("cleaned_customer_data_large.csv")

print("Average AnnualSpend (cleaned):", df_clean["AnnualSpend"].mean())
print("\nCustomer count by Country (cleaned, standardized):")
print(df_clean["Country"].value_counts())
```

Put the raw and cleaned numbers side by side in your notes:

| Metric | Raw dataset (Part 2) | Cleaned dataset (Part 5) |
| --- | --- | --- |
| Row count | 2,063 (tested) | 1,972 (tested) — 91 duplicate-customer rows removed |
| Average AnnualSpend | ≈ 2402.98 (tested) | ≈ 2411.98 (tested) |
| Distinct Country labels | 32 (tested) | 10 (tested) |

These are reference numbers from one tested run, not an answer key — your own run should land very close to them but may not match to the decimal. Write 2–3 sentences on what caused each number to change, and what would have gone wrong if this dataset had been used for AI/analytics without cleaning first (for example: country-level reporting undercounting a country because its customers were split across several spelling variants, or an average skewed by a negative value or blank cells).

## Part 6 — Governance, Sensitivity, and Handling Data Responsibly

### Step 6.1 — Classify every column

Fill in Yes/No for each column, using your cleaned dataset:

| Column | Personal data? | Sensitive personal data? |
| --- | --- | --- |
| CustomerID | | |
| Name | | |
| Email | | |
| SignupDate | | |
| Country | | |
| AnnualSpend | | |
| Phone | | |

### Step 6.2 — Choose a sensitivity label

Pick one for the whole file: Public / Internal / Confidential / Highly Confidential. Write one sentence justifying your choice.

### Step 6.3 — Handling rule

Write one line stating which columns must be masked or removed before this file is used in any AI training or grounding pipeline.

## Part 7 — Load Cleaned Data Back

Pick the same track you used in Part 3.

### Track A — Microsoft Fabric / OneLake

1. Upload `cleaned_customer_data_large.csv` to the Files section of your Fabric lakehouse.
2. In your Fabric notebook:

```python
df_clean = spark.read.option("header", "true").option("inferSchema", "true").csv("Files/cleaned_customer_data_large.csv")
df_clean.write.mode("overwrite").format("delta").saveAsTable("cleaned_customers")
```

3. Confirm the table appears under Tables, then verify:

```python
spark.sql("SELECT COUNT(*) FROM cleaned_customers").show()
```

### Track B — VS Code / local (no Fabric needed)

Create `load_cleaned_to_local_lakehouse.py`:

```python
"""
VS Code / local-only stand-in for Part 7 (Load Cleaned Data Back into the Lakehouse).

sqlite3 equivalent of:
    df_clean = spark.read...csv("Files/cleaned_customer_data_large.csv")
    df_clean.write.mode("overwrite").format("delta").saveAsTable("cleaned_customers")
    spark.sql("SELECT COUNT(*) FROM cleaned_customers").show()
"""
import sqlite3
import pandas as pd

df_clean = pd.read_csv("cleaned_customer_data_large.csv")

conn = sqlite3.connect("local_lakehouse.db")
df_clean.to_sql("cleaned_customers", conn, if_exists="replace", index=False)

result = conn.execute("SELECT COUNT(*) FROM cleaned_customers").fetchone()[0]
print("cleaned_customers row count:", result)

conn.close()
```

Run it and confirm the printed row count matches the “Cleaned dataset” row count from Part 5 (1,972 in the tested run).

## Part 8 — Package the Final Output

Assemble in one folder:

1. `raw_customer_data_large.csv`
2. `cleaned_customer_data_large.csv`
3. Cleansing log (Part 4.4)
4. Before/after comparison table (Part 5)
5. Sensitivity label + handling rule (Part 6)

This is your completed sample dataset, prepared for use — and, with Track B, it's one you could complete entirely in VS Code without ever touching a Fabric workspace.
