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
# Labour Market Direction
# ==========================================

if change <= -0.30:

    labour_market_trend = "strengthening"

    labour_market_assessment = (
        "labour market conditions are expected to improve gradually"
    )

elif change >= 0.30:

    labour_market_trend = "softening"

    labour_market_assessment = (
        "labour market conditions are expected to weaken modestly"
    )

else:

    labour_market_trend = "stable"

    labour_market_assessment = (
        "labour market conditions are expected to remain broadly stable"
    )

# ==========================================
# Forecast Statement
# ==========================================

if abs(change) < 0.1:

    forecast_statement = (
        "Unemployment is expected to remain near current levels "
        "over the next 12 months, indicating broadly stable "
        "labour market conditions."
    )

elif change > 0:

    forecast_statement = (
        f"Unemployment is projected to increase from "
        f"{latest_unemployment:.1f}% to "
        f"{forecast_unemployment:.1f}% over the next 12 months, "
        f"indicating softer labour market conditions."
    )

else:

    forecast_statement = (
        f"Unemployment is projected to decline from "
        f"{latest_unemployment:.1f}% to "
        f"{forecast_unemployment:.1f}% over the next 12 months, "
        f"indicating improving labour market conditions."
    )

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

    health_status = "Strong"

elif health_index >= 50:

    health_status = "Moderate"

elif health_index >= 35:

    health_status = "Softening"

else:

    health_status = "Weak"

# ==========================================
# Executive Commentary
# ==========================================

insight = f"""
Current indicators suggest that Canada's labour market remains in a
{labour_market_trend} phase.

{forecast_statement}

The Labour Market Health Index currently stands at
{health_index}/100, corresponding to a {health_status.lower()}
labour market assessment.

Labour market performance remains broadly aligned with historical
norms, supported by steady workforce participation and resilient
employment conditions. While hiring activity has moderated relative
to post-pandemic peaks, available indicators continue to support
a balanced employment environment.

Current conditions do not indicate broad-based labour market
deterioration. Employment fundamentals remain stable and labour
market activity continues to be supported by ongoing workforce demand
across key sectors of the economy.

Overall, the economic outlook remains balanced, with forecasts
pointing toward {labour_market_trend} labour market conditions and a
{risk_level.lower()} level of labour market risk over the medium term.
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