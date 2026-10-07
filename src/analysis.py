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
plt.plot(recent.index, recent.values, label="Monthly")
plt.plot(smooth.index, smooth.values, linewidth=3, label="12-month average")
plt.title("Russia's share of Spain's gas imports")
plt.ylabel("% of monthly imports ")
plt.axvline(pd.Timestamp("2022-02-24"), color="grey", linestyle="--", label="Invasion of Ukraine")
plt.axvline(pd.Timestamp("2026-04-25"), color="red", linestyle="--", label="EU short-term contract ban")
plt.legend()
plt.savefig("charts/russia_share.png")
