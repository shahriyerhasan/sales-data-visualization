# Global Threads — Sales Performance Analysis
*A data visualization portfolio project (Python, pandas, Matplotlib, Seaborn)*

## Overview
Two years of synthetic e-commerce order data (2024–2025) for a fictional
apparel & lifestyle retailer, "Global Threads." The project turns 13k+ raw
orders into a six-chart visual narrative covering growth, seasonality,
product mix, regional performance, channel economics, and the hidden cost
of discounting.

## Files
```
dataviz_project/
├── generate_data.py   # builds the synthetic dataset (run first)
├── analysis.py        # builds all 6 charts (run second)
├── data/
│   └── sales.csv       # 13,138 orders, 11 columns
└── charts/
    ├── 01_revenue_trend.png
    ├── 02_seasonality_heatmap.png
    ├── 03_category_mix.png
    ├── 04_regional_performance.png
    ├── 05_channel_order_value.png
    └── 06_discount_vs_satisfaction.png
```

## How to run it
```bash
pip install pandas numpy matplotlib seaborn
python generate_data.py   # -> data/sales.csv
python analysis.py        # -> charts/*.png
```

## The data story

**1. Revenue Trend (line chart)**
Monthly net revenue climbs steadily with two clear holiday spikes
(Nov–Dec each year), and Year 2 outperforms Year 1 at every comparable
point — the headline "things are working" chart.

**2. Seasonality Heatmap (weekday × month)**
Orders cluster on weekends and intensify sharply in November and December,
with a visible dip in February. Useful for staffing and inventory timing.

**3. Category Mix (horizontal bar)**
Apparel is the volume leader, but Electronics — a smaller share of orders —
punches above its weight in revenue per unit, flagging it as a margin
opportunity worth a deeper look.

**4. Regional Performance (stacked area)**
North America and Europe anchor total revenue across the full period,
while Asia Pacific shows the steepest growth trajectory — the region to
watch for future investment.

**5. Channel Economics (box plot)**
Retail Store orders have the highest *and* most consistent order value;
Marketplace orders are cheaper and more variable — a channel-mix insight
that pure revenue totals would hide.

**6. Discount vs. Satisfaction (bubble scatter + trend line)**
Average satisfaction score declines as discount depth increases, with
bubble size showing order volume at each discount tier. It's a gentle
but visible tradeoff: heavier discounting moves volume but costs
satisfaction — a prompt for a pricing/promotions conversation, not a
throwaway correlation.

## Design choices (why it reads as "portfolio," not "default matplotlib")
- One consistent color palette and typographic style applied across all
  six charts via a shared `rcParams`/`seaborn.set_theme` block.
- Every chart has a **conclusion as its title**, not a description of the
  axes ("Apparel Leads the Category Mix" vs. "Revenue by Category").
- Direct data labels/annotations replace legends wherever possible so the
  reader doesn't have to cross-reference.
- Currency formatting (`$120K` not `120000`) and gridlines kept light so
  they support rather than compete with the data.
- Chart types chosen for the story, not habit: a stacked area for
  regional composition over time, a box plot (not a bar of averages) to
  show channel order-value *spread*, a sized-bubble scatter to fold a
  third variable (order volume) into the discount/satisfaction chart.

## Ideas to extend this project
- Rebuild charts 1–4 as a single interactive Plotly or Tableau dashboard
  with region/category filters.
- Add a cohort retention chart using `order_id`/customer-level data.
- Swap the synthetic dataset for a real one (Kaggle's "Online Retail" or
  "Superstore" datasets drop in with minimal column renaming) to make
  this a genuine portfolio piece backed by real data.
