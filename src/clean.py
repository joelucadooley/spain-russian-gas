import pandas as pd

df = pd.read_excel("data/raw/importaciones-gas.xlsx", sheet_name="Todos", header=5)

keep = []
for col in df.columns:
	name = str(col).lower()
	if not name.startswith("total") and not name.startswith("unnamed"):
		keep.append(col)

df = df[keep]

print(df.head())
print(df.columns.tolist())
