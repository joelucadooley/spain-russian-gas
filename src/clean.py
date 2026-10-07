import pandas as pd
import sqlite3

df = pd.read_excel("data/raw/importaciones-gas.xlsx", sheet_name="Todos", header=5)

keep = []
for col in df.columns:
	name = str(col).lower()
	if not name.startswith("total") and not name.startswith("unnamed"):
		keep.append(col)

df = df[keep]
df = df.rename(columns={df.columns[0]: "year", df.columns[1]: "month"})
df = df.dropna(subset=["year", "month"])
df = df[df["month"].str.strip().str.lower() !="total"]

months = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}

df["month"] = df["month"].str.strip().str.lower().map(months)
df["year"] = df["year"].astype(int)
df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
df = df.drop(columns=["year", "month"])

long = df.melt(id_vars="date", var_name="source", value_name="gwh")
long["gwh"] = pd.to_numeric(long["gwh"], errors="coerce").fillna(0)

def get_type(source):
	source = source.strip()
	if source.endswith("GNL"):
		return "LNG"
	if source.endswith("GN"):
		return "pipeline"
	return "subtotal"

long["type"] = long["source"].apply(get_type)
long = long[long["type"] != "subtotal"]
long["country"] = long["source"].str.strip().str.removesuffix("GNL").str.removesuffix("GN")
long = long[~long["country"].str.contains("Europa")]
long = long[["date", "country", "type", "gwh"]]
long["date"] = long["date"].dt.strftime("%Y-%m-%d")

conn = sqlite3.connect("data/gas.db")
long.to_sql("imports", conn, if_exists="replace", index=False)
conn.close()

print("Saved", len(long), "rows")
