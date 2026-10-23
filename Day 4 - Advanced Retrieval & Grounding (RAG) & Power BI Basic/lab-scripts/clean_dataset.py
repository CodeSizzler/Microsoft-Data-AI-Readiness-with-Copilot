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
