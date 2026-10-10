import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


conn = sqlite3.connect("data/gas.db")
df = pd.read_sql("SELECT * FROM imports", conn)
conn.close()

df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year

mix = df.groupby(["year", "type"])["gwh"].sum().unstack()

full = mix[mix.index <= 2025]

plt.figure(figsize=(10, 5))
plt.plot(full.index, full["pipeline"], label="Pipeline")
plt.plot(full.index, full["LNG"], label="LNG")
plt.axvline(2011.17, color="green", linestyle="--", label="Medgaz pipeline opens")
plt.axvline(2021.83, color="red", linestyle="--", label="Maghreb-Europe pipeline closes")
plt.legend()
plt.ylim(0)
plt.title("Spain's gas imports by pipeline and by ship")
plt.ylabel("GWh per year")
plt.savefig("charts/lng_vs_pipeline.png")
