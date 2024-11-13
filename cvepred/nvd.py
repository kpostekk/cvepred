from glob import glob
import gzip
import json
from pathlib import Path
import httpx
import pandas as pd

CACHE_PATH = Path.home() / ".cache" / "cvepred"


def create_sources():
    if not CACHE_PATH.exists():
        CACHE_PATH.mkdir(parents=True)

    # Download cisa kev csv
    cisa_kev_path = CACHE_PATH / "cisa_kev.csv"

    if not cisa_kev_path.exists():
        response = httpx.get(
            "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv"
        )

        with open(cisa_kev_path, "wb") as f:
            f.write(response.content)

    # Download nvds
    for year in range(2010, 2025):
        nvd_path = CACHE_PATH / f"nvdcve-1.1-{year}.json.gz"

        if not nvd_path.exists():
            print(f"Downloading NVD for {year}")
            response = httpx.get(
                f"https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.gz"
            )

            with open(nvd_path, "wb") as f:
                f.write(response.content)

    # Merge nvds
    downloaded_nvds = glob(str(CACHE_PATH / "nvdcve-1.1-*.json.gz"))

    nvds_records = []

    for downloaded_nvd in downloaded_nvds:
        with gzip.open(downloaded_nvd, "rb") as f:
            payload = json.load(f)

        nvds_records.extend(payload["CVE_Items"])

    def filter_nvd_v3(row):
        try:
            return row["impact"]["baseMetricV3"]["cvssV3"]["baseScore"] > 0
        except KeyError:
            return False

    nvds_records = list(filter(filter_nvd_v3, nvds_records))

    def map_nvd_v3(record):
        cve_id = record["cve"]["CVE_data_meta"]["ID"]
        cvss3 = record["impact"]["baseMetricV3"]["cvssV3"]
        mapped_record = {
            "cve_nvd_id": cve_id,
            **cvss3,
        }

        del mapped_record["version"]

        return mapped_record

    nvds_records = list(map(map_nvd_v3, nvds_records))

    df = pd.DataFrame(nvds_records)

    df.to_csv(CACHE_PATH / "nvds.csv", index=False)

if __name__ == "__main__":
    create_sources()
