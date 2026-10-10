import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("data/gas.db")
df = pd.read_sql("SELECT * FROM imports", conn)
conn.close()

df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year

last12 = df[df["date"] > df["date"].max() - pd.DateOffset(months=12)]
russia_gap = last12[last12["country"] == "Rusia"]["gwh"].sum()

complete = df[df["year"] <= 2025]
yearly = complete.groupby(["year", "country"])["gwh"].sum().unstack().fillna(0)
change = yearly.diff()

biggest = change.stack().sort_values(ascending=False).head(5)

english = {"Argelia": "Algeria", "Estados Unidos": "United States", "Egipto": "Egypt"}

names = []
values = []
colors = []
for (year, country), value in biggest.items():
	names.append(f"{english.get(country, country)}\n{year}")
	values.append(value)
	colors.append("grey")

names.append("Russia's supply\n(last 12 months)")
values.append(russia_gap)
colors.append("red")

bars = pd.DataFrame({"name": names, "value": values, "color": colors})
bars = bars.sort_values("value", ascending=False)

plt.figure(figsize=(10, 5))
plt.bar(bars["name"], bars["value"], color=bars["color"])
plt.title("Largest one-year increases in gas supply to Spain\ncompared with Russia's supply over the last 12 months")
plt.ylabel("GWh")
plt.tight_layout()
plt.savefig("charts/stress_test.png")
