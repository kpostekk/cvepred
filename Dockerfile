FROM python:3.11.10 AS base

ENV USER=app-cvepred

# Make a user to run the app
RUN useradd -m ${USER}

USER ${USER}

ENV PATH="/home/${USER}/.local/bin:${PATH}"

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

# RUN poetry config virtualenvs.create false

RUN poetry config virtualenvs.in-project true

RUN poetry install --only main

COPY cvepred /app/cvepred

FROM base AS train

RUN poetry run python3 -m cvepred.model

FROM base AS api

RUN poetry install --only main,api

COPY --from=train /app/cvepred/cvepred_model.pkl /app/cvepred/cvepred_model.pkl

CMD ["poetry", "run", "fastapi", "run", "cvepred/api.py"]