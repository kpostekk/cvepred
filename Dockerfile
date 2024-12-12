FROM python:3.11.10 AS base

ENV USER=app-cvepred

# Make a user to run the app
RUN useradd -m ${USER}

USER ${USER}

ENV PATH="/home/${USER}/.local/bin:${PATH}"
ENV PYTHONPATH="/app"

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

# RUN poetry config virtualenvs.create false

RUN poetry config virtualenvs.in-project true

RUN poetry install --only main

COPY cvepred/__init__.py /app/cvepred/__init__.py

COPY cvepred/base/ /app/cvepred/base/

FROM base AS train

RUN poetry run python3 -m cvepred.base.model

FROM base AS api

RUN poetry install --only main,api

COPY --from=train /home/app-cvepred/.cache/cvepred /home/app-cvepred/.cache/cvepred
COPY --from=train /app/cvepred_model.pkl /app/cvepred_model.pkl

COPY cvepred/api/ /app/cvepred/api/

CMD ["poetry", "run", "fastapi", "run", "cvepred/api/app.py", "--host", "0.0.0.0", "--port", "8000"]