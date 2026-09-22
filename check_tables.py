import requests

tables={
    "Labour force (unemployment/employment)": "14100287",
    "Job vacancies":"14100371",
    "Average weekly earnings":"14100223",
    "CPI /inflation":"18100004",
    "GDP by industry":"36100104",
    "Population estimates":"17100009",

}
url="https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata"

for name,pid in tables.items():
    payload=[{"productId":pid}]
    resp=requests.post(url,json=payload)
    data=resp.json()[0]["object"]
    print(f"\n{name} (table {pid})")
    print("Frequency:",data.get("frequencyCode"))
    print("Start:",data.get("cubeStartDate"))
    print("End:",data.get("cubeEndDate"))