from pycaret.classification import setup

from .dataset import RANDOM_STATE, create_train_datasets

(df_train, df_test) = create_train_datasets()

s = setup(
    data=df_train,
    test_data=df_test,
    target="hasExploit",
    session_id=RANDOM_STATE,
    verbose=False,
    preprocess=False,
)

cvepred_model = s.create_model("svm", verbose=False)
