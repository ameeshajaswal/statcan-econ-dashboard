import pandas as pd
from prophet import Prophet
from pathlib import Path
import matplotlib.pyplot as plt

# ==========================================
# Load Data
# ==========================================

df = pd.read_csv("clean/labour_force.csv")

# ==========================================
# Filter National Unemployment Rate
# ==========================================

unemployment = df[
    (df["geography"] == "Canada") &
    (df["indicator"] == "Unemployment rate")
].copy()

# ==========================================
# Prepare Data for Prophet
# ==========================================

unemployment = unemployment.rename(
    columns={
        "date": "ds",
        "value": "y"
    }
)

unemployment["ds"] = pd.to_datetime(unemployment["ds"])

unemployment = unemployment[
    unemployment["ds"] >= "2018-01-01"
]

unemployment = unemployment[["ds", "y"]]

print("\nLatest Actual Data:")
print(unemployment.tail())

# ==========================================
# Build Forecast Model
# ==========================================

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    interval_width=0.95
)

model.fit(unemployment)

# ==========================================
# Forecast Next 12 Months
# ==========================================

future = model.make_future_dataframe(
    periods=12,
    freq="MS"
)

forecast = model.predict(future)

# ==========================================
# Output Folder
# ==========================================

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# ==========================================
# Save Full Forecast
# ==========================================

forecast[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
].to_csv(
    output_dir / "unemployment_forecast_all.csv",
    index=False
)

# ==========================================
# Future Forecast Only
# ==========================================

last_actual = unemployment["ds"].max()

future_only = forecast[
    forecast["ds"] > last_actual
][
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
]

future_only.to_csv(
    output_dir / "unemployment_forecast.csv",
    index=False
)

# ==========================================
# Power BI File
# Historical + Projected
# ==========================================

actual = unemployment.copy()
actual["series"] = "Historical"

actual.columns = [
    "date",
    "value",
    "series"
]

forecast_series = future_only.copy()

forecast_series = forecast_series.rename(
    columns={
        "ds": "date",
        "yhat": "value"
    }
)

forecast_series = forecast_series[
    [
        "date",
        "value"
    ]
]

forecast_series["series"] = "Projected"

combined = pd.concat(
    [actual, forecast_series],
    ignore_index=True
)

combined.to_csv(
    output_dir / "unemployment_actual_vs_forecast.csv",
    index=False
)

# ==========================================
# Forecast Summary
# Used for KPI Cards
latest_forecast = future_only.iloc[-1]

pd.DataFrame({
    "current_unemployment": [
        unemployment["y"].iloc[-1]
    ],
    "forecast_unemployment": [
        latest_forecast["yhat"]
    ],
    "forecast_date": [
        latest_forecast["ds"]
    ]
}).to_csv(
    output_dir / "forecast_summary.csv",
    index=False
)
# ==========================================
# Save Forecast Chart
# ==========================================

print("\nFiles Created:")
print("output/unemployment_forecast.csv")
print("output/unemployment_forecast_all.csv")
print("output/unemployment_actual_vs_forecast.csv")
print("output/forecast_summary.csv")
print("output/unemployment_forecast.png")