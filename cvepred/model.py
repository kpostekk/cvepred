from pycaret.classification import setup

from .dataset import create_train_dataset, RANDOM_STATE

(df_train, df_test) = create_train_dataset()

s = setup(
    data=df_train,
    test_data=df_test,
    target="stroke",
    session_id=RANDOM_STATE,
    verbose=False,
    preprocess=False,
)

cvepred_model = s.create_model("rf", verbose=False)
