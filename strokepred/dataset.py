import httpx
from pathlib import Path
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


def sample_dataset():
    df = create_dataset()
    rs = 3267189
    train_df = df.sample(frac=0.7, random_state=rs)
    tune_df = df.drop(train_df.index)

    return train_df, tune_df
