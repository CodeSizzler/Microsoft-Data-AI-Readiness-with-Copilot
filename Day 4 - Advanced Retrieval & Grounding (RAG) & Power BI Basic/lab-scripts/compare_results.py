import pandas as pd

df_clean = pd.read_csv("cleaned_customer_data_large.csv")

print("Average AnnualSpend (cleaned):", df_clean["AnnualSpend"].mean())
print("\nCustomer count by Country (cleaned, standardized):")
print(df_clean["Country"].value_counts())
