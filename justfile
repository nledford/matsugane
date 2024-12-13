#!/usr/bin/env just --justfile

test:
    # -v flag to produce verbose output
    pytest -v

update:
    poetry update