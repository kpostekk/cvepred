import pandas as pd
from imblearn.over_sampling import SMOTE, RandomOverSampler, ADASYN
import typing

from .nvd import create_sources

RANDOM_STATE = 564127


def create_dataset():
    """
    Returns the cve exploit prediction dataset.

    Performs a left join between the NVD and CISA KEV datasets.
    ``cve_id`` is the index. ``hasExploit`` is the target variable.
    """
    nvd_df, cisa_kev_df = create_sources()

    # Select only the cveID column
    cisa_kev_df = cisa_kev_df[["cveID"]].rename(columns={"cveID": "cve_cisa_id"})
    cisa_kev_df["hasExploit"] = True

    df = (
        pd.merge(
            nvd_df,
            cisa_kev_df,
            how="left",
            left_on="cve_nvd_id",
            right_on="cve_cisa_id",
        ).drop(
            columns=[
                "cve_nvd_id",
                "cve_cisa_id",
                "vectorString",
                "baseScore",
                "baseSeverity",
            ]
        )
        # .rename(columns={"cve_nvd_id": "cve_id"})
    )

    df["hasExploit"] = df["hasExploit"].fillna(False)
    # df = df.set_index("cve_id")

    # Categorical columns
    cat_columns_names = [name for name in df.columns if name not in ["hasExploit"]]

    for cat_column_name in cat_columns_names:
        df[cat_column_name] = pd.Categorical(df[cat_column_name])

    # Remove duplicates
    df = df[~df.index.duplicated(keep="first")]

    return df


def balanced_dataset(
    df: pd.DataFrame, method: typing.Literal["oversample", "undersample"] = "oversample"
):
    """
    Performs ASASYN on the dataset and returns a balanced dataset.
    """
    match method:
        case "oversample":
            smote = ADASYN(random_state=RANDOM_STATE)
            X = df.drop(columns=["hasExploit"])
            y = df["hasExploit"]

            X_resampled, y_resampled = smote.fit_resample(X, y)
            df_balanced = pd.concat([X_resampled, y_resampled], axis=1)

            return df_balanced
        case "undersample":
            has_exploit_records = df[df["hasExploit"] == True]
            no_exploit_records = df[df["hasExploit"] == False].sample(
                n=len(has_exploit_records), random_state=RANDOM_STATE
            )

            df_balanced = pd.concat([has_exploit_records, no_exploit_records])

            return df_balanced
        case _:
            raise ValueError("Invalid method")


def split_datasets(df: pd.DataFrame):
    df_test_true = df[df["hasExploit"] == True].sample(
        frac=0.08, random_state=RANDOM_STATE
    )
    df_test_false = df[df["hasExploit"] == False].sample(
        frac=0.12, random_state=RANDOM_STATE
    )

    df_test = pd.concat([df_test_true, df_test_false])

    df_train = df.drop(df_test.index)

    # df_train = df.sample(frac=0.7, random_state=RANDOM_STATE)
    # df_test = df.drop(df_train.index)

    return df_train, df_test


def create_train_datasets():
    print("Creating datasets...")
    df = create_dataset()
    print("Encoding dataset...")
    df_encoded = pd.get_dummies(df, dtype=int)
    print("Balancing dataset...")
    df_balanced = balanced_dataset(df_encoded, method="oversample")
    print("Splitting dataset...")
    df_balanced_train, xdf_balanced_test = split_datasets(df_balanced)
    print("Datasets created")

    return df_balanced_train, xdf_balanced_test
