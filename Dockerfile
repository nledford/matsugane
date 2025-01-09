FROM python:3.13.1 AS builder

# Configure Poetry
ENV POETRY_VERSION=2.0.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Python
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION} \
    && $POETRY_VENV/bin/pip install poetry-plugin-bundle

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Bundle app
WORKDIR /app
COPY . .
RUN poetry bundle venv --only=main /venv

## Run app
#FROM gcr.io/distroless/python3-debian12
#COPY --from=builder /venv /venv
ENTRYPOINT ["/venv/bin/lastfm_stats"]
