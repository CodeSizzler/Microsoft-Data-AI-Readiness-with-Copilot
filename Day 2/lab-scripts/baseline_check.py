import pandas as pd

df = pd.read_csv("raw_customer_data_large.csv")

print("Row count:", len(df))
print("Average AnnualSpend (raw):", df["AnnualSpend"].mean())
print("\nCustomer count by Country (raw, unstandardized):")
print(df["Country"].value_counts())
