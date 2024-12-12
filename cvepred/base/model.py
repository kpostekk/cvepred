from pycaret.classification import setup

from cvepred.base.dataset import RANDOM_STATE, create_train_datasets
from pathlib import Path

(df_train, df_test) = create_train_datasets()

s = setup(
    data=df_train,
    test_data=df_test,
    target="hasExploit",
    session_id=RANDOM_STATE,
    verbose=False,
    preprocess=False,
)

cvepred_model = s.create_model("rf", verbose=False)

if __name__ == "__main__":
    _, save_path = s.save_model(cvepred_model, "cvepred_model")
    print(f"Model saved to {Path(save_path).resolve()}")
    print(s.pull())
