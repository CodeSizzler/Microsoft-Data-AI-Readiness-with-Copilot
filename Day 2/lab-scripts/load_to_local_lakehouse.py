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
