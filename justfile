#!/usr/bin/env just --justfile

set dotenv-load

lint:
    pyright

test: lint
    poetry run pytest -v

run: test
    poetry run lastfm_stats

update:
    poetry update

docker-build:
    docker build -t nledford/matsugane:latest .

docker-run: docker-build
    @echo "Running app for $LASTFM_USER..."
    docker run \
      -p 8077:8077 \
      -e TZ=America/New_York \
      -e LASTFM_USER=$LASTFM_USER \
      -e LASTFM_KEY=$LASTFM_KEY \
      -e LASTFM_SECRET=$LASTFM_SECRET \
      -e LASTFM_PASSWORD=$LASTFM_PASSWORD \
      --rm -it --name matsugane nledford/matsugane:latest