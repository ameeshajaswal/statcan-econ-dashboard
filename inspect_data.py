import pandas as pd
import os
'''
tables={
    "labour_force": "14100287",
    "job_vacancies":"14100371",
    "weekly_earnings":"14100223",
    "cpi_inflation":"18100004",
    "gdp_by_industry":"36100104",
    "population":"17100009"
}

for name, pid in tables.items():
    path= f"data/{name}/{pid}.csv"
    if os.path.exists(path):
        df=pd.read_csv(path, nrows=2)
        print(f"\n{name} ({pid})")
        print(df.columns.tolist())

    else:
        print(f"\n{name}: file not found at {path}")
'''
'''
checks={
    "labour_force": ("data/labour_force/14100287.csv",["Labour force characteristics","Gender","Age group"]),
    "job_vacancies":("data/job_vacancies/14100371.csv",["Statistics"]),
    "weekly_earnings":("data/weekly_earnings/14100223.csv",["Estimate","North American Industry Classification System (NAICS)"]),
    "cpi_inflation":("data/cpi_inflation/18100004.csv",["Products and product groups"]),
    "gdp_by_industry":("data/gdp_by_industry/36100104.csv",["Prices","Seasonal adjustment","Estimates"]),
    "population":("data/population/17100009.csv",["GEO"])
}

for name, (path, cols) in checks.items():
    print(f"\n====={name}=====")
    df=pd.read_csv(path,usecols=cols+["GEO"] if "GEO" not in cols else cols)
    for col in cols:
        uniques=df[col].dropna().unique()
        print(f"\n{col} ({len(uniques)} unique values):")
        print(f" ",list(uniques)[:8],"..." if len(uniques)>8 else "")

import pandas as pd
df=pd.read_csv("data/labour_force/14100287.csv",usecols=["Statistics","Data type"])
print("Statistics:",df["Statistics"].dropna().unique())
print("Data type:",df["Data type"].dropna().unique())
'''
import pandas as pd

headline = pd.read_csv("clean/labour_force.csv")
youth = pd.read_csv("clean/labour_force_youth.csv")

#compare the two dataframes
sample_h=headline[(headline["geography"]=="Canada") & (headline["indicator"]=="Unemployment rate")].tail(5)
sample_y=youth[(youth["geography"]=="Canada") & (youth["indicator"]=="Unemployment rate")].tail(5)
print("Headline(should be ~overall unemployment rate, roughly 5-7%):")
print(sample_h)
print("\nYouth (should be ~youth unemployment rate, roughly 10-15%):")
print(sample_y)

print(headline.head(15))