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
