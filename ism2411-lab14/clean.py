#reflection questions: 1.the fill decision feels most ambiguous. I feel quantity_sold with the mean but the 9,999 placeholders inflated it. I'd want to know why values are missing and whether a median per product category would be a better fill.  2.my comments now explain: why dropped rows missing order_id/order_date, filled quantity_sold, dropped 9999, kept negative revenue   3.three typed 9,999 values distorted revenue(max, mean, median) even after removing them the mean is far above the median

import pandas as pd

print("--Exercise 1--")
df = pd.read_csv("data/messy_sales.csv")
df.info()
print(df.isnull().sum())
print((df.isnull().mean() * 100).round(1))
#customer _id has 7.5% missing, region has 2.3% missing, unit_price is dtype str but should be float

print("--Exercise 2--")
df.columns = df.columns.str.lower().str.replace(" ", "_")
print(df.columns.tolist())

print("--Exercise 3--")
print("Shape before:", df.shape)
df = df.dropna(subset=["order_id", "order_date"])
df["quantity_sold"] = df["quantity_sold"].fillna(df["quantity_sold"].mean())
print("Shape after:", df.shape)
print(df.isnull().sum())
#dropped rows missing order_id or order_date, without an indentifier the row can't be tied to an order, and guessing would create fake records
#filled quantity_sold with the mean, only 2% is missing so the mean keeps those rows without notieably changing the columns average

print("--Exercise 4--")
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
print("Dates that become NaT:", df["order_date"].isna().sum())
df["unit_price"] = (
    df["unit_price"].str.replace("$", "", regex=False).str.replace(",", "", regex=False)
).astype(float)
df["quantity_sold"] = df["quantity_sold"].astype(int)
df["revenue"] = (df["unit_price"] * df["quantity_sold"]).round(2)
print(df.dtypes)

print("--Exercise 5--")
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()
print("Shape after:", df.shape)

print("--Exercise 6--")
pd.set_option("display.max_columns", None)
print(df.describe())
#revenue max is 59,994 (9,999 x 6.00), likely the 9,999 placeholder quantity, not a real order
#revenue mean (441) is far above the median (145), skewed by larger orders and that max
#revenue min is -3,268, a return, so i kept it
print("Rows with quantity_sold == 9999:", (df["quantity_sold"] == 9999).sum())
#dropped: 9999 is a placeholder someone typed, not a real order
df = df[df["quantity_sold"] != 9999]
print("Shape after:", df.shape)
print(df["revenue"].describe())

print("--Exercise 7--")
df.to_csv("data/clean_sales.csv", index=False)
check = pd.read_csv("data/clean_sales.csv")
check.info()
check = pd.read_csv("data/clean_sales.csv", parse_dates=["order_date"])
check.info()
