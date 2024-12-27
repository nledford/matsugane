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
#    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.5

RUN apt-get update && apt-get install -y nala
RUN nala install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry self add poetry-plugin-bundle

WORKDIR /app
COPY . .
RUN poetry bundle venv /venv


FROM gcr.io/distroless/python3-debian12
COPY --from=builder /venv /venv
ENTRYPOINT ["/venv/bin/charts"]