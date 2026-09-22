import requests
import zipfile
import os
import io

tables={
    "labour_force": "14100287",
    "job_vacancies":"14100371",
    "weekly_earnings":"14100223",
    "cpi_inflation":"18100004",
    "gdp_by_industry":"36100104",
    "population":"17100009"
}
metadata_url="https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV"

os.makedirs("data",exist_ok=True)

for name,pid in tables.items():
    print(f"\nFetching {name} (table {pid})...")
    #ask for download link
    request_url=f"{metadata_url}/{pid}/en"
    resp=requests.get(request_url)
    download_info=resp.json()

    if download_info.get("status")!="SUCCESS":
        print(f"Failed to get download link for :{download_info})")
        continue

    zip_url=download_info["object"]
    print(f"Download link received.")

    #download zip file
    zip_resp=requests.get(zip_url)

    #unzip data into data folder
    target_folder=os.path.join("data",name)
    os.makedirs(target_folder,exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(zip_resp.content)) as z:
        z.extractall(target_folder)

    print(f"Saved to {target_folder}/")
print("\nDone. Check the data folder.")