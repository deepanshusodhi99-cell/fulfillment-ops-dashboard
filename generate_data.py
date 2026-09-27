"""
generate_data.py

Generates a SYNTHETIC dataset for the Fulfillment & Transportation Operations
Dashboard portfolio project. This data is randomly generated to reflect
realistic distributions based on general domain knowledge of distribution
center / carrier operations -- it is NOT real company data from any employer.

Run: python generate_data.py
Output: data.json (consumed by index.html)
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(seed=42)

# ---- Config ----
DAYS = 60
CARRIERS = ["FedEx", "Day & Ross", "Purolator", "TForce", "Canpar"]
END_DATE = datetime(2026, 9, 26)
START_DATE = END_DATE - timedelta(days=DAYS - 1)
dates = [START_DATE + timedelta(days=i) for i in range(DAYS)]

# ---- Daily operational metrics ----
daily_rows = []
base_inbound = 850
base_outbound = 780

for i, d in enumerate(dates):
    weekday = d.weekday()
    weekend_factor = 0.55 if weekday >= 5 else 1.0
    seasonal_drift = 1.0 + 0.15 * np.sin(i / DAYS * np.pi)  # gentle ramp mid-period

    inbound = max(0, int(rng.normal(base_inbound * weekend_factor * seasonal_drift, 45)))
    outbound = max(0, int(rng.normal(base_outbound * weekend_factor * seasonal_drift, 50)))

    on_time_pct = np.clip(rng.normal(92.5, 3.2), 78, 99.5)
    trailer_utilization = np.clip(rng.normal(74, 8), 45, 98)
    inventory_accuracy = np.clip(rng.normal(97.2, 1.4), 90, 100)

    daily_rows.append({
        "date": d.strftime("%Y-%m-%d"),
        "inbound_volume": inbound,
        "outbound_volume": outbound,
        "on_time_pct": round(float(on_time_pct), 1),
        "trailer_utilization_pct": round(float(trailer_utilization), 1),
        "inventory_accuracy_pct": round(float(inventory_accuracy), 1),
    })

df_daily = pd.DataFrame(daily_rows)

# ---- Carrier performance (aggregated) ----
carrier_rows = []
for c in CARRIERS:
    base_rate = rng.uniform(88, 97)
    volume_share = rng.uniform(0.12, 0.28)
    carrier_rows.append({
        "carrier": c,
        "on_time_pct": round(float(np.clip(base_rate + rng.normal(0, 1.5), 80, 99)), 1),
        "shipments": int(rng.integers(900, 4200)),
        "avg_transit_days": round(float(rng.uniform(1.2, 3.4)), 1),
    })

df_carrier = pd.DataFrame(carrier_rows).sort_values("on_time_pct", ascending=False)

# ---- Trailer status distribution (snapshot) ----
trailer_status = {
    "In Transit": int(rng.integers(120, 180)),
    "At Dock (Loading)": int(rng.integers(40, 70)),
    "At Dock (Unloading)": int(rng.integers(35, 65)),
    "Staged / Ready": int(rng.integers(60, 100)),
    "Idle / Empty": int(rng.integers(20, 45)),
}

# ---- Summary KPIs (derived) ----
summary = {
    "avg_on_time_pct": round(float(df_daily["on_time_pct"].mean()), 1),
    "avg_trailer_utilization_pct": round(float(df_daily["trailer_utilization_pct"].mean()), 1),
    "avg_inventory_accuracy_pct": round(float(df_daily["inventory_accuracy_pct"].mean()), 1),
    "total_volume_last_7d": int(
        df_daily.tail(7)["inbound_volume"].sum() + df_daily.tail(7)["outbound_volume"].sum()
    ),
    "total_assets_tracked": sum(trailer_status.values()),
}

output = {
    "meta": {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "note": "Synthetic demo dataset for portfolio purposes. Not real company data.",
        "date_range": {"start": dates[0].strftime("%Y-%m-%d"), "end": dates[-1].strftime("%Y-%m-%d")},
    },
    "summary": summary,
    "daily": df_daily.to_dict(orient="records"),
    "carriers": df_carrier.to_dict(orient="records"),
    "trailer_status": trailer_status,
}

with open("data.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Wrote data.json with {len(df_daily)} daily records and {len(df_carrier)} carriers.")
