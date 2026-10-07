import sqlite3
import pandas as pd

conn = sqlite3.connect("data/gas.db")
df = pd.read_sql("SELECT * FROM imports", conn)
conn.close()

df["date"] = pd.to_datetime(df["date"])

total = df.groupby("date")["gwh"].sum()
russia = df[df["country"] == "Rusia"].groupby("date")["gwh"].sum()
share = russia / total * 100

print(share.tail(12).round(1))
