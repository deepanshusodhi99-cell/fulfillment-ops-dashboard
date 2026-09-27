# Fulfillment & Transportation Operations Dashboard

An interactive KPI dashboard visualizing distribution-network operations —
inbound/outbound volume, on-time delivery, trailer utilization, inventory
accuracy, and carrier performance.

**⚠️ Data note:** This project uses a **synthetically generated dataset**
(`generate_data.py`), built to reflect realistic patterns based on general
domain knowledge of distribution-center and carrier operations. **It is not
real data from any employer** — it exists purely to demonstrate dashboard
design, data pipeline, and visualization skills for portfolio purposes.

## Live demo

Enable GitHub Pages on this repo (Settings → Pages → deploy from `main`) and
the dashboard will be live at:
`https://github.com/deepanshusodhi99-cell.github.io/fulfillment-ops-dashboard/`

## Why this project

I build automated reporting and KPI dashboards for Walmart Canada's
distribution network using Excel VBA, Power Query, and Tableau — but that
data is proprietary and can't be shared publicly. This project rebuilds the
same category of dashboard (carrier performance, trailer/asset visibility,
volume trends, inventory accuracy) from the ground up with a public,
web-based stack, so the underlying skill set is verifiable outside a
corporate environment.

## Tech stack

- **Python (pandas, numpy)** — synthetic data generation with realistic
  distributions, seasonality, and noise (`generate_data.py`)
- **JavaScript + Chart.js** — interactive bar, line, and doughnut charts
- **HTML/CSS** — responsive, no framework dependency, single static page

## Structure

```
.
├── generate_data.py   # generates data.json (re-run to regenerate the dataset)
├── data.json          # synthetic dataset consumed by the dashboard
├── index.html          # the dashboard itself
└── README.md
```

## Running locally

```bash
python generate_data.py     # optional — regenerate data.json
python -m http.server 8000  # serve locally (fetch() needs http, not file://)
# open http://localhost:8000
```

## Metrics shown

| Metric | Description |
|---|---|
| On-Time Delivery % | Rolling daily on-time performance |
| Trailer Utilization % | Average trailer capacity utilization |
| Inventory Accuracy % | Daily inventory count accuracy |
| Volume (7-day) | Combined inbound + outbound units, trailing week |
| Carrier Performance | On-time %, shipment volume, avg transit days per carrier |
| Trailer Status | Snapshot distribution of asset status (in transit, at dock, staged, idle) |
