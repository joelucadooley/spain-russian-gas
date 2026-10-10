import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("data/gas.db")
df = pd.read_sql("SELECT * FROM imports", conn)
conn.close()

df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year

names =	{
	"Argelia": "Algeria",
	"Estados Unidos": "United States",
	"Rusia": "Russia",
	"Nigeria": "Nigeria",
}

df["supplier"] = df["country"].map(names).fillna("Other")


mix = df.groupby(["year", "supplier"])["gwh"].sum().unstack()
share = mix.div(mix.sum(axis=1), axis=0) * 100
share = share[["Algeria", "United States", "Russia", "Nigeria", "Other"]]

recent = share[share.index >= 2015]
recent = recent.rename(index={2026: "2026 (Jan-Jul)"})

recent.plot(kind="bar", stacked=True, figsize=(10, 5))
plt.title("Who supplies Spain's gas?")
plt.ylabel("% of annual imports")
plt.tight_layout()
plt.savefig("charts/supplier_mix.png")
