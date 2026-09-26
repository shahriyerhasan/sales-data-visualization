"""
generate_data.py
Creates a synthetic, realistic e-commerce sales dataset for the
"Global Threads" data visualization portfolio project.

Run: python generate_data.py
Output: data/sales.csv
"""

import numpy as np
import pandas as pd

np.random.seed(42)

# ---- Dimensions ----
start_date = "2024-01-01"
end_date = "2025-12-31"
dates = pd.date_range(start_date, end_date, freq="D")

categories = {
    "Apparel": 1.0,
    "Footwear": 0.8,
    "Accessories": 0.5,
    "Home & Living": 0.7,
    "Electronics": 1.3,
}

regions = {
    "North America": 1.2,
    "Europe": 1.0,
    "Asia Pacific": 1.1,
    "Latin America": 0.6,
    "Middle East & Africa": 0.5,
}

channels = ["Online", "Retail Store", "Marketplace"]
channel_weights = [0.55, 0.30, 0.15]

rows = []
order_id = 100000

for date in dates:
    # Seasonality: more orders on weekends, holiday bump in Nov/Dec, dip in Feb
    dow_factor = 1.25 if date.weekday() >= 5 else 1.0
    month_factor = 1.0
    if date.month in (11, 12):
        month_factor = 1.6
    elif date.month == 2:
        month_factor = 0.85
    elif date.month == 7:
        month_factor = 1.1  # summer sale

    # Slight year-over-year growth
    year_factor = 1.0 if date.year == 2024 else 1.18

    base_orders = np.random.poisson(lam=14 * dow_factor * month_factor * year_factor)

    for _ in range(base_orders):
        category = np.random.choice(list(categories.keys()),
                                     p=[0.32, 0.20, 0.18, 0.18, 0.12])
        region = np.random.choice(list(regions.keys()),
                                   p=[0.30, 0.26, 0.22, 0.13, 0.09])
        channel = np.random.choice(channels, p=channel_weights)

        cat_mult = categories[category]
        reg_mult = regions[region]

        units = max(1, int(np.random.gamma(shape=2.0, scale=1.5)))
        unit_price = np.round(np.random.uniform(15, 120) * cat_mult, 2)
        discount_pct = np.random.choice([0, 0, 0, 0.1, 0.15, 0.2, 0.3],
                                         p=[0.45, 0.1, 0.1, 0.15, 0.1, 0.06, 0.04])

        gross_revenue = round(units * unit_price * reg_mult, 2)
        net_revenue = round(gross_revenue * (1 - discount_pct), 2)

        # Customer satisfaction score, slightly lower when heavy discounting
        # (proxy for clearance / lower-quality batches) plus noise
        satisfaction = np.clip(
            np.random.normal(loc=4.3 - discount_pct * 0.8, scale=0.5), 1, 5
        )

        order_id += 1
        rows.append({
            "order_id": order_id,
            "date": date,
            "category": category,
            "region": region,
            "channel": channel,
            "units": units,
            "unit_price": unit_price,
            "discount_pct": discount_pct,
            "gross_revenue": gross_revenue,
            "net_revenue": net_revenue,
            "satisfaction_score": round(satisfaction, 2),
        })

df = pd.DataFrame(rows)
df.sort_values("date", inplace=True)
df.to_csv("data/sales.csv", index=False)

print(f"Generated {len(df):,} orders from {start_date} to {end_date}")
print(f"Total net revenue: ${df['net_revenue'].sum():,.0f}")
print("Saved to data/sales.csv")
