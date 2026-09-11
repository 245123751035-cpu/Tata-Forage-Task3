import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

RAW = r"C:\Users\kshit\Downloads\Online Retail.xlsx"
OUT_DATA = r"C:\Users\kshit\Tata-Forage-Task3\data\cleaned_data.xlsx"
OUT_VIS = r"C:\Users\kshit\Tata-Forage-Task3\visuals"

NAVY = "#0B3D61"
TEAL = "#15A085"
ACCENT = "#F0A202"
GRAY = "#5B6B79"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "Arial"],
    "axes.edgecolor": "#CBD5DE",
    "axes.linewidth": 0.8,
    "axes.titlesize": 15,
    "axes.titleweight": "bold",
    "axes.titlecolor": NAVY,
    "axes.labelsize": 11,
    "axes.labelcolor": GRAY,
    "xtick.color": GRAY,
    "ytick.color": GRAY,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "grid.color": "#E3E9EE",
    "grid.linewidth": 0.8,
})

# ----------------------------------------------------------------------------
# 1. LOAD & CLEAN
# ----------------------------------------------------------------------------
df = pd.read_excel(RAW)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("Raw rows:", len(df))
print("Duplicated rows:", int(df.duplicated().sum()))

df = df.drop_duplicates()

df = df[~df["InvoiceNo"].astype(str).str.startswith("C", na=False)]
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]
df = df[df["CustomerID"].notna()]
df = df[df["StockCode"].astype(str).str.strip() != ""]
df = df[df["Description"].astype(str).str.strip() != ""]

df["Revenue"] = df["Quantity"] * df["UnitPrice"]
df["Month"] = df["InvoiceDate"].dt.to_period("M")

df.to_excel(OUT_DATA, index=False)
print("Saved cleaned data -> data/cleaned_data.xlsx")

print("Cleaned rows:", len(df))
print("UK rows:", int((df["Country"] == "United Kingdom").sum()))
print("Countries:", df["Country"].nunique())


def money(x):
    return f"\u00a3{int(x):,}"


def save(fig, name):
    fig.savefig(f"{OUT_VIS}\\{name}", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


# ----------------------------------------------------------------------------
# 2. Q1 - CEO: 2011 monthly revenue time series
# ----------------------------------------------------------------------------
q1 = (
    df[df["InvoiceDate"].dt.year == 2011]
    .groupby(df["InvoiceDate"].dt.to_period("M"))
    .agg(Revenue=("Revenue", "sum"))
    .reindex(pd.period_range("2011-01", "2011-12", freq="M"))
)
q1["Revenue"] = q1["Revenue"].fillna(0)

fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(q1.index.astype(str), q1["Revenue"].values / 1000, marker="o",
        color=TEAL, linewidth=2.6, markersize=7, markerfacecolor="white",
        markeredgecolor=TEAL, markeredgewidth=2)
ax.fill_between(range(len(q1)), q1["Revenue"].values / 1000, color=TEAL, alpha=0.08)
ax.set_title("Monthly Revenue Trend for 2011", pad=14)
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (thousands \u00a3)")
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.0f"))
ax.text(-0.08, 1.04, "VISUAL 1 \u00b7 CEO QUESTION 1", transform=ax.transAxes,
        fontsize=8.5, color=GRAY, alpha=0.0)
for i, v in enumerate(q1["Revenue"].values / 1000):
    ax.annotate(f"{v:,.0f}", (i, v), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=8.5, color=NAVY)
ax.margins(x=0.04, y=0.18)
save(fig, "Q1_2011_monthly_revenue.png")

print("Q1 total 2011 revenue:", money(q1["Revenue"].sum()))
print("Q1 best month:", q1["Revenue"].idxmax(), money(q1["Revenue"].max()))

# ----------------------------------------------------------------------------
# 3. Q2 - CMO: Top 10 countries by revenue + quantity (excl UK)
# ----------------------------------------------------------------------------
q2 = (
    df[df["Country"] != "United Kingdom"]
    .groupby("Country")
    .agg(Revenue=("Revenue", "sum"), Quantity=("Quantity", "sum"))
    .sort_values("Revenue", ascending=False)
    .head(10)
    .sort_values("Revenue", ascending=True)
)

fig, ax = plt.subplots(figsize=(9.5, 6))
labels = q2.index.tolist()
revenue = (q2["Revenue"] / 1000).tolist()
bar = ax.barh(labels, revenue, color=NAVY, height=0.62)
for i, p in enumerate(bar):
    ax.text(p.get_width() + 4, p.get_y() + p.get_height() / 2,
            f"\u00a3{q2['Revenue'].iloc[i]:,.0f}", va="center", fontsize=8.5, color=NAVY)
    ax.text(p.get_width() + 4, p.get_y() + p.get_height() / 2 - 0.32,
            f"Qty {q2['Quantity'].iloc[i]:,.0f}", va="center", fontsize=7.5, color=GRAY)
ax.set_title("Top 10 Countries by Revenue (United Kingdom Excluded)", pad=14)
ax.set_xlabel("Revenue (thousands \u00a3)")
ax.margins(x=0.42)
save(fig, "Q2_top10_countries_revenue.png")

print("Q2 top revenue country:", df[df["Country"] != "United Kingdom"]["Revenue"].groupby(df["Country"]).sum().idxmax())

# ----------------------------------------------------------------------------
# 4. Q3 - CMO: Top 10 customers by revenue (descending)
# ----------------------------------------------------------------------------
q3 = (
    df.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 5.4))
bar = ax.bar(q3["CustomerID"].astype(int).astype(str), q3["Revenue"] / 1000,
             color=[NAVY] + [TEAL] * (len(q3) - 1), width=0.62)
for i, p in enumerate(bar):
    ax.text(p.get_x() + p.get_width() / 2, p.get_height() + 1.5,
            f"\u00a3{q3['Revenue'].iloc[i]:,.0f}", ha="center", fontsize=8.5, color=NAVY)
ax.set_title("Top 10 Customers by Revenue Generated", pad=14)
ax.set_xlabel("Customer ID")
ax.set_ylabel("Revenue (thousands \u00a3)")
ax.grid(axis="y")
ax.set_axisbelow(True)
ax.margins(y=0.16)
save(fig, "Q3_top10_customers.png")

print("Q3 top customer:", int(q3["CustomerID"].iloc[0]), money(q3["Revenue"].iloc[0]))
print("Q3 top-10 share of revenue:", round(q3["Revenue"].sum() / df["Revenue"].sum() * 100, 1), "%")

# ----------------------------------------------------------------------------
# 5. Q4 - CEO: Demand across all countries (excl UK)
# ----------------------------------------------------------------------------
q4 = df[df["Country"] != "United Kingdom"].groupby("Country").agg(
    Quantity=("Quantity", "sum"), Revenue=("Revenue", "sum")
).sort_values("Quantity", ascending=False)

import plotly.graph_objects as go

fig = go.Figure(go.Choropleth(
    locations=q4.index,
    z=q4["Quantity"],
    locationmode="country names",
    colorscale="Blues",
    showscale=True,
    colorbar=dict(title="Units Sold", thickness=16, outlinewidth=0),
    marker_line_color="white",
    marker_line_width=0.5,
))
fig.update_layout(
    title="Product Demand Across Countries (United Kingdom Excluded)",
    title_font=dict(size=20, color=NAVY, family="Segoe UI, Arial"),
    geo=dict(showframe=False, showcoastlines=True, coastlinecolor="#B9C6D2",
             showcountries=True, countrycolor="#B9C6D2", projection_type="natural earth",
             bgcolor="white"),
    margin=dict(l=0, r=20, t=70, b=10),
    paper_bgcolor="white",
)
fig.write_image(f"{OUT_VIS}\\Q4_global_demand_map.png", width=1500, height=750, scale=2)
print("saved Q4_global_demand_map.png")

print("\nQ4 top demand:", q4.head(5).to_string())
print("\nDone.")