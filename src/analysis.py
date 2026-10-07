import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("data/gas.db")
df = pd.read_sql("SELECT * FROM imports", conn)
conn.close()

df["date"] = pd.to_datetime(df["date"])

total = df.groupby("date")["gwh"].sum()
russia = df[df["country"] == "Rusia"].groupby("date")["gwh"].sum()
share = russia / total * 100

recent = share[share.index >= "2019-01-01"]
smooth = russia.rolling(12).sum() / total.rolling(12).sum() * 100
smooth = smooth[smooth.index >= "2019-01-01"]

plt.figure(figsize=(10, 5))
plt.plot(recent.index, recent.values)
plt.plot(smooth.index, smooth.values, linewidth=3)
plt.title("Russia's share of Spain's gas imports")
plt.ylabel("% of monthly imports ")
plt.savefig("charts/russia_share.png")
