#!/usr/bin/env just --justfile

test:
    # -v flag to produce verbose output
    pytest -v

update:
    poetry update

docker-build:
    docker build -t nledford/matsugane:latest .

docker-run: docker-build
    docker run -p 8077:8077 --rm -it --name matsugane nledford/matsugane:latest