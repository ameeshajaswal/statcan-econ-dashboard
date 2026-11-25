import pandas as pd
from pathlib import Path

# ==========================================
# Load Latest Labour Force Data
# ==========================================

labour_df = pd.read_csv("clean/labour_force.csv")

latest_unemployment = (
    labour_df[
        (labour_df["geography"] == "Canada")
        & (labour_df["indicator"] == "Unemployment rate")
    ]["value"]
    .iloc[-1]
)

# ==========================================
# Load Forecast Output
# ==========================================

forecast_df = pd.read_csv(
    "output/unemployment_forecast.csv"
)

forecast_unemployment = (
    forecast_df["yhat"]
    .iloc[-1]
)

# ==========================================
# Calculate Forecast Change
# ==========================================

change = (
    forecast_unemployment -
    latest_unemployment
)

# ==========================================
# Labour Market Trend
# ==========================================

if change <= -0.30:

    labour_market_trend = "strengthening"

elif change >= 0.30:

    labour_market_trend = "softening"

else:

    labour_market_trend = "stable"

# ==========================================
# Risk Classification
# ==========================================

if latest_unemployment < 5.5:

    risk_level = "Low"

elif latest_unemployment < 6.5:

    risk_level = "Moderate"

else:

    risk_level = "Elevated"

# ==========================================
# Labour Market Health Index
# ==========================================

participation_rate = (
    labour_df[
        (labour_df["geography"] == "Canada")
        & (labour_df["indicator"] == "Participation rate")
    ]["value"]
    .iloc[-1]
)

health_index = round(
    (
        (100 - (latest_unemployment * 10))
        + participation_rate
    ) / 2
)

if health_index >= 70:
    health_status = "strong"

elif health_index >= 50:
    health_status = "balanced"

elif health_index >= 35:
    health_status = "below target"

else:
    health_status = "weak"
   

# ==========================================
# Executive Commentary
# ==========================================

if labour_market_trend == "strengthening":

    opening = (
        f"Labour market conditions show early signs of improvement, "
        f"with unemployment projected to decline from "
        f"{latest_unemployment:.1f}% to "
        f"{forecast_unemployment:.1f}% over the next 12 months."
    )

    closing = (
        "Overall, the outlook is cautiously optimistic, with "
        "improving employment prospects and continued monitoring "
        "of labour market risks."
    )

elif labour_market_trend == "softening":

    opening = (
        f"Labour market conditions show signs of softening, "
        f"with unemployment projected to increase from "
        f"{latest_unemployment:.1f}% to "
        f"{forecast_unemployment:.1f}% over the next 12 months."
    )

    closing = (
        "Overall, the outlook remains cautious as forecast results "
        "suggest weaker labour market conditions."
    )

else:

    opening = (
        "Labour market conditions remain broadly stable, with "
        "unemployment expected to remain near current levels over "
        "the next 12 months."
    )

    closing = (
        "Overall, the outlook remains balanced, with labour market "
        "conditions expected to remain broadly stable."
    )

insight = f"""
{opening}

The Labour Market Health Index stands at {health_index}/100,
indicating that labour market conditions remain
{health_status}.

{closing}
"""

# ==========================================
# Save for Power BI
# ==========================================

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

insight_df = pd.DataFrame({
    "Category": ["Executive Economic Outlook"],
    "Insight": [insight.strip()]
})

insight_df.to_csv(
    output_dir / "ai_insights.csv",
    index=False
)

# ==========================================
# Display Output
# ==========================================

print("\nAI Insight Generated\n")
print(insight)

print("\nSaved:")
print("output/ai_insights.csv")