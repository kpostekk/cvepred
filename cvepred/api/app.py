from fastapi import FastAPI, HTTPException
from cvepred.base.dataset import (
    create_dataset,
    RANDOM_STATE,
    create_train_datasets,
    create_dataset_ids,
)

from cvepred.api.models import CveModels, CveNvdIdsModel, CvePredictions
from pycaret.classification import setup
from scalar_fastapi import get_scalar_api_reference
import pandas as pd

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)

samples_ids = create_dataset_ids()
samples = create_dataset()
(df_train, df_test) = create_train_datasets()

s = setup(
    data=df_train,
    test_data=df_test,
    target="hasExploit",
    session_id=RANDOM_STATE,
    preprocess=False,
)
model = s.load_model("cvepred_model")


@app.get("/docs", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="CVE Prediction API",
    )


@app.get("/sample/{n}")
def sample(n: int) -> CveModels:
    if n > 20:
        raise HTTPException(status_code=400, detail="Sample size too large.")

    data = samples.sample(n=n).drop(columns=["hasExploit"]).to_dict("records")

    return CveModels.model_validate({"data": data})


@app.post("/predict")
def predict(inputs: CveModels) -> CvePredictions:
    df = pd.DataFrame(inputs.model_dump()["data"])

    # patch created df
    for column in df.columns:
        # if column in df_train.columns and is categorical, then convert to category from train set (whole categorical set)
        if column in samples.columns and df[column].dtype.name == "object":
            df[column] = pd.Categorical(df[column], categories=samples[column].unique())

    df_encoded = pd.get_dummies(df, dtype=int)

    predictions = s.predict_model(model, df_encoded)

    predictions_compact = predictions.rename(
        columns={"prediction_label": "label", "prediction_score": "score"}
    )[["label", "score"]]

    predictions_compact.insert(0, "inputModel", inputs.model_dump()["data"])

    return CvePredictions.model_validate(
        {"data": predictions_compact.to_dict("records")}
    )


@app.post("/predict/from-ids")
def predict_from_id(inputs: CveNvdIdsModel) -> CvePredictions:
    data = (
        samples_ids[samples_ids["cve_nvd_id"].isin(inputs.ids)]
        .drop(columns=["hasExploit", "cve_nvd_id"])
        .to_dict("records")
    )

    if len(data) != len(inputs.ids):
        raise HTTPException(status_code=400, detail="CVE ID not found or is invalid.")

    models = CveModels.model_validate({"data": data})

    return predict(models)
