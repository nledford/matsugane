#FROM python:3.13.1-slim-bookworm AS builder
#FROM coatldev/six:latest AS builder
#LABEL authors="nledford"
#
## Python
#ENV PYTHONFAULTHANDLER=1 \
#    PYTHONUNBUFFERED=1 \
#    PYTHONHASHSEED=random \
#    PIP_NO_CACHE_DIR=off \
#    PIP_DISABLE_PIP_VERSION_CHECK=on \
#    PIP_DEFAULT_TIMEOUT=100
#
## Poetry
#ENV POETRY_NO_INTERACTION=1 \
#    POETRY_VIRTUALENVS_CREATE=false \
#    POETRY_CACHE_DIR='/var/cache/pypoetry' \
#    POETRY_HOME='/usr/local' \
#    POETRY_VERSION=1.8.5
#
## Install dependencies
#RUN apt-get update && apt-get install -y nala
#RUN nala install -y curl build-essential
#
## Install Poetry
#RUN curl -sSL https://install.python-poetry.org | python3 -
#RUN poetry self add poetry-plugin-bundle
#
## Bundle app
#WORKDIR /app
#COPY . .
#RUN poetry bundle venv --python=/usr/bin/python3 --only=main ./venv
#
#
#FROM gcr.io/distroless/python3-debian12
#COPY --from=builder /venv /venv
#ENTRYPOINT ["/venv/bin/charts"]

FROM python:3.13.1 AS builder

# Configure Poetry
ENV POETRY_VERSION=1.8.5
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-ansi

# Run your app
COPY . /app
#CMD [ "poetry", "run", "python", "-c", "print('Hello, World!')" ]

CMD ["poetry", "run", "python", "./app/main.py"]