"""
analysis.py
"Global Threads" Sales Performance — Data Visualization Portfolio Project

Loads data/sales.csv and produces six polished, presentation-ready charts
that tell a coherent story: growth trend -> seasonality -> category mix ->
regional performance -> channel economics -> the discount/satisfaction tradeoff.

Run: python analysis.py
Output: charts/01_revenue_trend.png ... charts/06_discount_vs_satisfaction.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ---------------------------------------------------------------
# Style setup — consistent, presentation-grade look across all charts
# ---------------------------------------------------------------
sns.set_theme(style="whitegrid", context="talk")
PALETTE = ["#2E5EAA", "#E8702A", "#3FA796", "#C44569", "#8E7CC3", "#F4A300"]
sns.set_palette(PALETTE)
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#444444",
    "axes.titleweight": "bold",
    "axes.titlesize": 18,
    "axes.titlepad": 16,
    "font.family": "DejaVu Sans",
    "figure.dpi": 150,
})

df = pd.read_csv("data/sales.csv", parse_dates=["date"])
df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
df["year"] = df["date"].dt.year
df["month_name"] = df["date"].dt.strftime("%b")

def money(x, pos):
    return f"${x/1000:,.0f}K" if x >= 1000 else f"${x:,.0f}"

MONEY_FMT = mticker.FuncFormatter(money)


# ---------------------------------------------------------------
# 1. Monthly revenue trend (line) — the headline growth story
# ---------------------------------------------------------------
monthly = df.groupby("month")["net_revenue"].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly["month"], monthly["net_revenue"], color=PALETTE[0], linewidth=2.8,
        marker="o", markersize=5)
ax.fill_between(monthly["month"], monthly["net_revenue"], color=PALETTE[0], alpha=0.08)
ax.yaxis.set_major_formatter(MONEY_FMT)
ax.set_title("Monthly Net Revenue Shows Steady Growth Into Year Two")
ax.set_xlabel("")
ax.set_ylabel("Net Revenue")
# annotate holiday peaks
for yr in [2024, 2025]:
    peak = monthly[monthly["month"].dt.year == yr].nlargest(1, "net_revenue").iloc[0]
    ax.annotate(f"Holiday peak\n{money(peak['net_revenue'], None)}",
                xy=(peak["month"], peak["net_revenue"]),
                xytext=(10, 18), textcoords="offset points",
                fontsize=11, color="#333333",
                arrowprops=dict(arrowstyle="->", color="#888888"))
fig.tight_layout()
fig.savefig("charts/01_revenue_trend.png", bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------
# 2. Seasonality heatmap — month x weekday order volume
# ---------------------------------------------------------------
df["weekday"] = df["date"].dt.day_name()
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

pivot = df.pivot_table(index="weekday", columns="month_name", values="order_id",
                        aggfunc="count").reindex(index=weekday_order, columns=month_order)

fig, ax = plt.subplots(figsize=(13, 6))
sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.5, linecolor="white",
            cbar_kws={"label": "Orders"}, ax=ax, annot=False)
ax.set_title("Weekends and Holiday Months Drive Order Volume")
ax.set_xlabel("")
ax.set_ylabel("")
fig.tight_layout()
fig.savefig("charts/02_seasonality_heatmap.png", bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------
# 3. Category revenue mix (horizontal bar, sorted)
# ---------------------------------------------------------------
cat_rev = df.groupby("category")["net_revenue"].sum().sort_values()

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(cat_rev.index, cat_rev.values, color=PALETTE[1])
ax.xaxis.set_major_formatter(MONEY_FMT)
ax.set_title("Apparel Leads the Category Mix, Electronics Punches Above Its Share")
ax.set_xlabel("Net Revenue")
for bar, val in zip(bars, cat_rev.values):
    ax.text(val + cat_rev.max() * 0.01, bar.get_y() + bar.get_height() / 2,
            money(val, None), va="center", fontsize=12, color="#333333")
fig.tight_layout()
fig.savefig("charts/03_category_mix.png", bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------
# 4. Regional performance over time (small multiples / stacked area)
# ---------------------------------------------------------------
reg_month = df.pivot_table(index="month", columns="region", values="net_revenue",
                            aggfunc="sum").fillna(0)
reg_month = reg_month[df.groupby("region")["net_revenue"].sum().sort_values(ascending=False).index]

fig, ax = plt.subplots(figsize=(12, 6.5))
ax.stackplot(reg_month.index, reg_month.T.values, labels=reg_month.columns,
             colors=PALETTE, alpha=0.9)
ax.yaxis.set_major_formatter(MONEY_FMT)
ax.set_title("North America and Europe Anchor Revenue Across Every Region")
ax.set_xlabel("")
ax.set_ylabel("Net Revenue")
ax.legend(loc="upper left", frameon=True, fontsize=11, ncol=2)
fig.tight_layout()
fig.savefig("charts/04_regional_performance.png", bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------
# 5. Channel economics — average order value by channel (box plot)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6.5))
sns.boxplot(data=df, x="channel", y="net_revenue", hue="channel",
            palette=PALETTE[2:5], showfliers=False, ax=ax, legend=False)
ax.yaxis.set_major_formatter(MONEY_FMT)
ax.set_title("Retail Stores Generate the Highest and Most Consistent Order Values")
ax.set_xlabel("")
ax.set_ylabel("Net Revenue per Order")
fig.tight_layout()
fig.savefig("charts/05_channel_order_value.png", bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------
# 6. Discount depth vs. customer satisfaction (scatter + trend)
# ---------------------------------------------------------------
disc_summary = df.groupby("discount_pct").agg(
    avg_satisfaction=("satisfaction_score", "mean"),
    orders=("order_id", "count"),
).reset_index()

fig, ax = plt.subplots(figsize=(10, 6.5))
sizes = disc_summary["orders"] / disc_summary["orders"].max() * 1200 + 100
sc = ax.scatter(disc_summary["discount_pct"] * 100, disc_summary["avg_satisfaction"],
                 s=sizes, color=PALETTE[3], alpha=0.75, edgecolor="white", linewidth=1.5)
z = np.polyfit(disc_summary["discount_pct"], disc_summary["avg_satisfaction"], 1)
trend_x = np.linspace(0, 30, 50)
ax.plot(trend_x, np.poly1d(z)(trend_x / 100), "--", color="#555555", linewidth=2)
ax.set_title("Deeper Discounts Correlate With Lower Satisfaction Scores")
ax.set_xlabel("Discount Depth (%)")
ax.set_ylabel("Avg. Satisfaction Score (1–5)")
ax.set_ylim(3.5, 5.0)
for _, row in disc_summary.iterrows():
    ax.annotate(f"{int(row['discount_pct']*100)}%",
                (row["discount_pct"] * 100, row["avg_satisfaction"]),
                textcoords="offset points", xytext=(0, 14), ha="center", fontsize=10)
fig.tight_layout()
fig.savefig("charts/06_discount_vs_satisfaction.png", bbox_inches="tight")
plt.close(fig)

print("All 6 charts saved to charts/")
