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
