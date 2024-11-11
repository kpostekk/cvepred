import kagglehub
import pandas as pd
from pathlib import Path


def create_dataset(raw=False):
    """
    Returns the stroke prediction dataset.

    """
    dataset_path = kagglehub.dataset_download("fedesoriano/stroke-prediction-dataset")

    dataset_path = Path(dataset_path) / "healthcare-dataset-stroke-data.csv"

    df = pd.read_csv(dataset_path)

    if raw:
        return df

    df["bmi"] = df["bmi"].fillna(df["bmi"].median())

    return df


def sample_dataset():
    df = create_dataset()
    rs = 3267189
    train_df = df.sample(frac=0.7, random_state=rs)
    tune_df = df.drop(train_df.index)

    return train_df, tune_df
