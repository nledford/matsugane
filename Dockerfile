#FROM python:3.13.1-bookworm AS builder
FROM coatldev/six:latest AS builder
LABEL authors="nledford"

# Python
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.5

RUN apt-get update && apt-get install -y nala
RUN nala install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-ansi --only=main

COPY . /app
CMD ["poetry", "run", "python", "main.py"]

#RUN pipx install --python python3.13 poetry
#RUN pipx inject poetry poetry-plugin-bundle
#WORKDIR /src
#COPY . .
#RUN poetry bundle venv --python=/usr/bin/python3 --only=main /venv


#FROM gcr.io/distroless/python3-debian12
#COPY --from=builder /venv /venv
#ENTRYPOINT ["/venv/bin/charts"]