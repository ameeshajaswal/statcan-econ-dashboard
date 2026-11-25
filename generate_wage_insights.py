import pandas as pd
from pathlib import Path

# ==========================================
# Load Data
# ==========================================

inflation_df = pd.read_csv("clean/cpi_inflation.csv")
earnings_df = pd.read_csv("clean/weekly_earnings.csv")

# ==========================================
# Canada CPI
# ==========================================

canada_cpi = inflation_df[
    inflation_df["geography"] == "Canada"
].copy()

canada_cpi["date"] = pd.to_datetime(
    canada_cpi["date"]
)

canada_cpi = canada_cpi.sort_values(
    "date"
)

current_cpi = canada_cpi["value"].iloc[-1]

previous_cpi = canada_cpi["value"].iloc[-13]

inflation_rate = (
    (
        current_cpi -
        previous_cpi
    ) /
    previous_cpi
) * 100

# ==========================================
# Canada Average Weekly Earnings
# ==========================================

canada_earnings = earnings_df[
    earnings_df["geography"] == "Canada"
].copy()

canada_earnings["date"] = pd.to_datetime(
    canada_earnings["date"]
)

canada_earnings = canada_earnings.sort_values(
    "date"
)

current_earnings = (
    canada_earnings["value"].iloc[-1]
)

previous_year_earnings = (
    canada_earnings["value"].iloc[-13]
)

wage_growth = (
    (
        current_earnings -
        previous_year_earnings
    ) /
    previous_year_earnings
) * 100

# ==========================================
# Real Wage Growth
# ==========================================

real_wage_growth = (
    wage_growth -
    inflation_rate
)

# ==========================================
# Purchasing Power Status
# ==========================================

if real_wage_growth > 0:

    purchasing_power_status = "Improving"

elif real_wage_growth < 0:

    purchasing_power_status = "Declining"

else:

    purchasing_power_status = "Stable"

# ==========================================
# Executive Insight
# ==========================================

if real_wage_growth > 0:

    insight = f"""
Wages continue to outpace inflation, resulting in positive real wage growth of {real_wage_growth:.1f}%.

Average weekly earnings have reached ${current_earnings:,.0f}, supporting modest improvements in household purchasing power.

Overall, wage growth remains sufficient to offset current inflationary pressures, indicating an improving consumer income outlook.
"""

else:

    insight = f"""
Inflation continues to outpace wage growth, resulting in real wage growth of {real_wage_growth:.1f}%.

Average weekly earnings have reached ${current_earnings:,.0f}; however, purchasing power remains under pressure from elevated price growth.

Overall, household purchasing power remains constrained despite ongoing wage increases.
"""

# ==========================================
# Save Output
# ==========================================

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

pd.DataFrame({
    "Category": ["Earnings & Inflation Outlook"],
    "Insight": [insight.strip()]
}).to_csv(
    output_dir / "wage_insights.csv",
    index=False
)

# ==========================================
# Debug Output
# ==========================================

print("\nWage Insight Generated\n")

print(f"Current CPI: {current_cpi:.1f}")
print(f"Previous CPI: {previous_cpi:.1f}")
print(f"Inflation Rate: {inflation_rate:.1f}%")

print(f"Current Earnings: {current_earnings:.2f}")
print(f"Previous Earnings: {previous_year_earnings:.2f}")
print(f"Wage Growth: {wage_growth:.1f}%")

print(f"Real Wage Growth: {real_wage_growth:.1f}%")

print(f"Purchasing Power: {purchasing_power_status}")

print("\nInsight:\n")
print(insight)

print("\nSaved:")
print("output/wage_insights.csv")