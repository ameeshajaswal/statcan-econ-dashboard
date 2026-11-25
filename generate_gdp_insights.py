import pandas as pd
from pathlib import Path

# ==========================================
# Load GDP Data
# ==========================================

gdp_df = pd.read_csv("clean/gdp_by_industry.csv")

# ==========================================
# Canada GDP Only
# ==========================================

gdp_df = gdp_df[
    gdp_df["geography"] == "Canada"
].copy()

gdp_df["date"] = pd.to_datetime(
    gdp_df["date"]
)

gdp_df = gdp_df.sort_values(
    "date"
)

# ==========================================
# Latest GDP
# ==========================================

current_gdp = (
    gdp_df["value"]
    .iloc[-1]
)

# ==========================================
# Same Quarter Previous Year
# Quarterly data = 4 quarters per year
# ==========================================

previous_year_gdp = (
    gdp_df["value"]
    .iloc[-5]
)

# ==========================================
# GDP Growth (YoY)
# ==========================================

gdp_growth = (
    (
        current_gdp -
        previous_year_gdp
    )
    /
    previous_year_gdp
) * 100

# ==========================================
# GDP in Trillions
# Source data is in millions
# ==========================================

gdp_trillion = (
    current_gdp / 1_000_000
)

# ==========================================
# Economic Outlook
# ==========================================

if gdp_growth >= 2:

    outlook = "Strong"

elif gdp_growth > 0:

    outlook = "Stable"

else:

    outlook = "Weakening"

# ==========================================
# Executive Insight
# ==========================================

if gdp_growth >= 2:

    insight = f"""
Canada's economy continues to expand, with GDP growth of {gdp_growth:.1f}% and total economic output exceeding ${gdp_trillion:.1f} trillion.

Economic activity remains above pre-pandemic levels and continues to support business investment and labour market demand.

Overall, economic conditions remain strong, supported by sustained growth across the Canadian economy.
"""

elif gdp_growth > 0:

    insight = f"""
Canada's economy continues to expand, with GDP growth of {gdp_growth:.1f}% and total economic output exceeding ${gdp_trillion:.1f} trillion.

Economic activity remains above pre-pandemic levels despite slower growth compared with the post-pandemic recovery period.

Overall, economic conditions remain stable, although growth has moderated relative to recent expansionary years.
"""

else:

    insight = f"""
Canada's economy has experienced GDP growth of {gdp_growth:.1f}%, reflecting weaker economic momentum.

Economic activity remains above pre-pandemic levels; however, growth conditions have softened compared with previous periods.

Overall, economic conditions remain cautious as slowing growth continues to weigh on the outlook.
"""

# ==========================================
# Save Output
# ==========================================

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

pd.DataFrame({
    "Category": ["Economic Growth Outlook"],
    "Insight": [insight.strip()]
}).to_csv(
    output_dir / "gdp_insights.csv",
    index=False
)

# ==========================================
# Display Results
# ==========================================

print("\nGDP Insight Generated\n")

print(f"Current GDP: {current_gdp:,.0f}")
print(f"Previous Year GDP: {previous_year_gdp:,.0f}")
print(f"GDP Growth: {gdp_growth:.1f}%")
print(f"GDP (Trillions): {gdp_trillion:.1f}T")
print(f"Economic Outlook: {outlook}")

print("\nInsight:\n")
print(insight)

print("\nSaved:")
print("output/gdp_insights.csv")