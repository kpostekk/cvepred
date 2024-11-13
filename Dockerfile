FROM python:3.11.10 AS base

ENV USER=app-cvepred

# Make a user to run the app
RUN useradd -m ${USER}

USER ${USER}

ENV PATH="/home/${USER}/.local/bin:${PATH}"

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry install

COPY cvepred /app/cvepred

FROM base AS jupyter

RUN poetry install --with notebook

COPY eda.ipynb strokrepred.ipynb /app/

CMD ["poetry", "run", "jupyter", "notebook", "--ip=0.0.0.0"]
