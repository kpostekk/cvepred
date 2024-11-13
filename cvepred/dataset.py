from pathlib import Path

import kagglehub
import pandas as pd
from imblearn.over_sampling import SMOTE
from .nvd import CACHE_PATH

RANDOM_STATE = 74328


def sanitize_dataset(df: pd.DataFrame):

    return df


def create_dataset(raw=False):
    """
    Returns the cve exploit prediction dataset.
    """
    nvd_path = CACHE_PATH / "nvds.csv"
    nvd_df = pd.read_csv(nvd_path)

    print(nvd_df.columns)

    cisa_kev_path = CACHE_PATH / "cisa_kev.csv"
    cisa_kev_df = pd.read_csv(cisa_kev_path)

    print(cisa_kev_df.columns)

    df = nvd_df.join(cisa_kev_df.set_index("cveID"), on="cve_nvd_id", how="left")

    print(df.columns)

    if raw:
        return df

    # Drop id
    df = sanitize_dataset(df)

    return df


def split_encoded_dataset():
    """
    Splits the dataset into a training and tuning set.
    Performs one-hot encoding on the dataset.
    """
    df = create_dataset()
    df = pd.get_dummies(df)

    train_df = df.sample(frac=0.7, random_state=RANDOM_STATE)
    tune_df = df.drop(train_df.index)

    return train_df, tune_df


def balanced_dataset():
    """
    Performs SMOTE on the dataset and returns a training and testing set.
    """
    (train_df, _) = split_encoded_dataset()

    # balance the dataset
    smote = SMOTE(random_state=RANDOM_STATE)
    X = train_df.drop("hasExploit", axis=1)
    y = train_df["hasExploit"]
    X_balanced, y_balanced = smote.fit_resample(X, y)
    df_balanced = pd.concat(
        [
            pd.DataFrame(X_balanced, columns=X.columns),
            pd.Series(y_balanced, name="hasExploit"),
        ],
        axis=1,
    )

    return df_balanced


def create_train_dataset():
    df_balanced = balanced_dataset()
    df_balanced_train = df_balanced.sample(frac=0.7, random_state=RANDOM_STATE)
    df_balanced_test = df_balanced.drop(df_balanced_train.index)

    return df_balanced_train, df_balanced_test

if __name__ == "__main__":
    x = create_dataset(raw=True)
    print(x)