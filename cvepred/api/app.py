from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from cvepred.base.dataset import (
    create_dataset,
    split_datasets,
    RANDOM_STATE,
    create_train_datasets,
)
from cvepred.api.models import CveModels
from pycaret.classification import setup
import pandas as pd

app = FastAPI()

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


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/sample")
def sample() -> CveModels:
    data = samples.sample(n=20).drop(columns=["hasExploit"]).to_dict("records")

    return CveModels.model_validate({"data": data})


@app.post("/predict")
def predict(inputs: CveModels):
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

    predictions_compact.insert(0, "cve_opts", inputs.model_dump()["data"])

    return predictions_compact.to_dict("records")
