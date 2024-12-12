from pycaret.classification import setup

from cvepred.base.dataset import RANDOM_STATE, create_train_datasets

# print("Datasets loading...")

(df_train, df_test) = create_train_datasets()

# print("Datasets loaded")

s = setup(
    data=df_train,
    test_data=df_test,
    target="hasExploit",
    session_id=RANDOM_STATE,
    # verbose=False,
    preprocess=False,
)

best_models = s.compare_models(
    # Following models are not Turbo comp
    # exclude=["rbfsvm", "gpc", "mlp", "et", "lda", "gbc"]
    # Choosing lightweight models
    include=[
        # "catboost",
        "lr",
        # "knn",
        "nb",
        "dt",
        "svm",
        "ridge",
        "rf",
        "qda",
        "ada",
        "gbc",
        "lda",
        "et",
    ],
    # verbose=False,
    # n_select=3,
)

model_comparison = s.pull()

if __name__ == "__main__":
    print(model_comparison)
