from pathlib import Path

import kagglehub
import pandas as pd
from imblearn.over_sampling import SMOTE

RANDOM_STATE = 455612378


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
    df = df.drop(columns=["id"])

    # Fill missing bmi values
    df["bmi"] = df["bmi"].fillna(df["bmi"].median())

    # Remove "Other"
    df = df[df['gender'] != 'Other']
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


def sample_dataset():
    df = create_dataset()
    df = pd.get_dummies(df)

    train_df = df.sample(frac=0.7, random_state=RANDOM_STATE)
    tune_df = df.drop(train_df.index)

    return train_df, tune_df


def create_train_dataset():
    (train_df, _) = sample_dataset()

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

    df_balanced_train = df_balanced.sample(frac=0.7, random_state=RANDOM_STATE)
    df_balanced_test = df_balanced.drop(df_balanced_train.index)

    return df_balanced_train, df_balanced_test
