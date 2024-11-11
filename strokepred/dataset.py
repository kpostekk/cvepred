from pathlib import Path

import kagglehub
import pandas as pd
from imblearn.over_sampling import SMOTE

RANDOM_STATE = 455612378


def sanitize_dataset(df: pd.DataFrame):
    """
    Removes outliers and fills missing values in the dataset.
    Also perform remaps on int values to boolean values (if possible).
    Based on results from the EDA notebook.
    """
    # Drop id
    df = df.drop(columns=["id"])

    # Fill missing bmi values
    df["bmi"] = df["bmi"].fillna(df["bmi"].median())

    # Remove "Other"
    df = df[df["gender"] != "Other"]
    # df["gender"] = df["gender"].isin(["Male", "Female"])

    # Remove bmi outliers
    df = df[df["bmi"] < 65]

    # Remap ever married into boolean values
    df["ever_married"] = df["ever_married"] == "Yes"

    # Remap hypertension into boolean values
    df["hypertension"] = df["hypertension"] == 1

    # Remap heart_disease into boolean values
    df["heart_disease"] = df["heart_disease"] == 1

    # Remap stroke into boolean values
    df["stroke"] = df["stroke"] == 1

    return df


def create_dataset(raw=False):
    """
    Returns the stroke prediction dataset.
    """
    dataset_path = kagglehub.dataset_download("fedesoriano/stroke-prediction-dataset")

    dataset_path = Path(dataset_path) / "healthcare-dataset-stroke-data.csv"

    df = pd.read_csv(dataset_path)

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


def preprocess_dataset():
    """
    Performs SMOTE on the dataset and returns a training and testing set.
    """
    (train_df, _) = split_encoded_dataset()

    # balance the dataset
    smote = SMOTE(random_state=RANDOM_STATE)
    X = train_df.drop("stroke", axis=1)
    y = train_df["stroke"]
    X_balanced, y_balanced = smote.fit_resample(X, y)
    df_balanced = pd.concat(
        [
            pd.DataFrame(X_balanced, columns=X.columns),
            pd.Series(y_balanced, name="stroke"),
        ],
        axis=1,
    )

    return df_balanced


def create_train_dataset():
    df_balanced = preprocess_dataset()
    df_balanced_train = df_balanced.sample(frac=0.7, random_state=RANDOM_STATE)
    df_balanced_test = df_balanced.drop(df_balanced_train.index)

    return df_balanced_train, df_balanced_test
