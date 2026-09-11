# Tata Data Visualisation — Task 3: Creating Effective Visuals

**Role:** Junior Data Analyst  
**Dataset:** Online Retail (UCI) — 541,909 rows, Dec 2010–Dec 2011  
**Business goal:** Provide visuals that help the CEO and CMO make data-driven decisions and build a global expansion strategy.

---

## 2. Data Cleaning Summary

| Step | Description | Rows removed |
|---|---|---|
| Raw rows | Original dataset | 541,909 |
| Duplicates | Exact duplicate transactions | 5,268 |
| Cancellations | Invoice numbers starting with "C" | — |
| Invalid quantity | Negative / zero quantities (returns, errors) | — |
| Invalid price | Negative / zero unit prices | — |
| Missing customer | Blank Customer IDs | — |
| Blank fields | Empty StockCode / Description | — |
| **Final cleaned rows** | Ready for analysis | **392,692** |

A `Revenue` column was added: `Revenue = Quantity × UnitPrice`.

---

## 3. Visuals and Insights

### VISUAL 1 — CEO Question 1: 2011 Monthly Revenue Trend
**Chart type:** Line chart (time series) — best for showing trends over time.

- Revenue moves through a clear **seasonal cycle**.
- Strong growth from October, peaking in **November 2011 at £1,156,205** (total 2011 revenue ≈ £8.3M).
- A dip in December after the November spike, with **August being the weakest month** (~£580K).

**Insight:** Demand concentrates heavily in the pre-holiday period (Oct–Nov). Forecasts for 2012 should account for this ramp and plan stock/inventory ahead of October.

### VISUAL 2 — CMO Question 2: Top 10 Countries by Revenue (UK Excluded)
**Chart type:** Horizontal bar chart — ideal for comparing categories ranked by value.

- **Netherlands** is the largest international market (≈£285K, 200K+ units), followed by **EIRE**, **Germany**, and **France**.
- Western Europe dominates the top 10; the gap from #1 to #2 is large.

**Insight:** Focus expansion and marketing spend in the Netherlands and EIRE first — they already show the highest receptiveness to the product range.

### VISUAL 3 — CMO Question 3: Top 10 Customers by Revenue
**Chart type:** Vertical bar chart, sorted descending — shows rank of biggest revenue contributors.

- Top customer **14646** generated **£280,206** — over 2× the 2nd-ranked customer.
- The **top 10 customers account for 17.3%** of total company revenue.

**Insight:** High-value customers must be retained with loyalty programs and personalised service; losing any single top-10 customer creates a measurable revenue hit.

### VISUAL 4 — CEO Question 4: Global Demand Map (UK Excluded)
**Chart type:** Choropleth world map — shows all countries at once on a single view without scrolling.

- Demand is **concentrated in Western Europe** (Netherlands, EIRE, Germany, France).
- Secondary clusters appear in Australia, Sweden, and Denmark.

**Insight:** The expansion strategy should prioritise these high-demand regions. Australia is a notable long-distance market worth a dedicated shipping/logistics review.

---

## 4. Expansion Strategy Recommendations

1. **Short term:** Consolidate the Netherlands + EIRE markets (highest proven demand).
2. **Seasonal readiness:** Build inventory 6–8 weeks ahead of the October–November peak.
3. **Customer focus:** Protect the top 10 customers (17.3% of revenue) with VIP retention.
4. **Long term:** Use the demand map to pilot new entry in Australia and Nordic countries.

---

## 5. Files

- `clean_data_Forage.csv` — cleaned transactional dataset (392,692 rows)
- `visuals/` — the four full-resolution chart images (also bundled in `visuals.tar`)
- `build_visuals.py` — reproducible analysis script