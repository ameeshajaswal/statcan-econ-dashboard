import pandas as pd
import os
os.makedirs("clean", exist_ok=True)
# ---- Labour force: two slices (headline + youth) ----
df = pd.read_csv("data/labour_force/14100287.csv")
headline = df[(df["Gender"] == "Total - Gender") 
              & (df["Age group"] == "15 years and over")
              & (df["Statistics"] == "Estimate") 
              & (df["Data type"] == "Seasonally adjusted")]
headline = headline.rename(columns={"REF_DATE": "date", "GEO": "geography", "Labour force characteristics": "indicator", "VALUE": "value"})
headline = headline[["date", "geography", "indicator", "value"]]
headline.to_csv("clean/labour_force.csv", index=False)
print(f"labour_force: {len(headline)} rows saved")
youth = df[(df["Gender"] == "Total - Gender") 
           & (df["Age group"] == "15 to 24 years")
           & (df["Statistics"] == "Estimate")
           & (df["Data type"] == "Seasonally adjusted")]
youth = youth.rename(columns={"REF_DATE": "date", "GEO": "geography", "Labour force characteristics": "indicator", "VALUE": "value"})
youth = youth[["date", "geography", "indicator", "value"]]
youth.to_csv("clean/labour_force_youth.csv", index=False)
print(f"labour_force_youth: {len(youth)} rows saved")
# ---- Job vacancies: keep everything ----
df = pd.read_csv("data/job_vacancies/14100371.csv")
df = df.rename(columns={"REF_DATE": "date", "GEO": "geography", "Statistics": "indicator", "VALUE": "value"})
df = df[["date", "geography", "indicator", "value"]]
df.to_csv("clean/job_vacancies.csv", index=False)
print(f"job_vacancies: {len(df)} rows saved")
# ---- Weekly earnings ----
df = pd.read_csv("data/weekly_earnings/14100223.csv")
df = df[
    (df["Estimate"] == "Average weekly earnings including overtime for all employees") &
    (df["North American Industry Classification System (NAICS)"] == "Industrial aggregate excluding unclassified businesses [11-91N]")
]
df = df.rename(columns={"REF_DATE": "date", "GEO": "geography", "Estimate": "indicator", "VALUE": "value"})
df = df[["date", "geography", "indicator", "value"]]
df.to_csv("clean/weekly_earnings.csv", index=False)
print(f"weekly_earnings: {len(df)} rows saved")
# ---- CPI / inflation ----
df = pd.read_csv("data/cpi_inflation/18100004.csv")
df = df[df["Products and product groups"] == "All-items"]
df = df.rename(columns={"REF_DATE": "date", "GEO": "geography", "Products and product groups": "indicator", "VALUE": "value"})
df = df[["date", "geography", "indicator", "value"]]
df.to_csv("clean/cpi_inflation.csv", index=False)
print(f"cpi_inflation: {len(df)} rows saved")
# ---- GDP by industry ----
df = pd.read_csv("data/gdp_by_industry/36100104.csv")
df = df[
    (df["Estimates"] == "Gross domestic product at market prices") &
    (df["Prices"] == "Chained (2017) dollars") &
    (df["Seasonal adjustment"] == "Seasonally adjusted at annual rates")
]
df = df.rename(columns={"REF_DATE": "date", "GEO": "geography", "Estimates": "indicator", "VALUE": "value"})
df = df[["date", "geography", "indicator", "value"]]
df.to_csv("clean/gdp_by_industry.csv", index=False)
print(f"gdp_by_industry: {len(df)} rows saved")
# ---- Population ----
df = pd.read_csv("data/population/17100009.csv")
df = df.rename(columns={"REF_DATE": "date", "GEO": "geography", "VALUE": "value"})
df["indicator"] = "Population"
df = df[["date", "geography", "indicator", "value"]]
df.to_csv("clean/population.csv", index=False)
print(f"population: {len(df)} rows saved")
print("\nAll tables cleaned.")
