import httpx
from pathlib import Path
import os
import hashlib
import zipfile
import pandas as pd


def create_dataset():
    dataset_path = Path("healthcare-dataset-stroke-data.csv")

    if dataset_path.exists():
        return pd.read_csv(dataset_path)

    url = "https://www.kaggle.com/api/v1/datasets/download/fedesoriano/stroke-prediction-dataset"
    response = httpx.get(url, follow_redirects=True)

    archive_path = Path("/tmp/stroke-prediction-dataset.zip")

    with open(archive_path, "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        zip_ref.extractall(".")

    return pd.read_csv(dataset_path)


if __name__ == "__main__":
    df = create_dataset()
    print(df)
