import kagglehub
import pandas as pd


def create_dataset(raw=False):
    dataset_path = kagglehub.dataset_download("fedesoriano/stroke-prediction-dataset")

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
