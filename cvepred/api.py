from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from cvepred.dataset import create_dataset, split_datasets, RANDOM_STATE
from cvepred.api_models import CveModels
from pycaret.classification import setup

app = FastAPI()

samples = create_dataset()
(df_train, df_test) = split_datasets(samples)

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
    # s.predict_model(model, )
    raise Exception("Not implemented yet")
