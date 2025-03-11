#!/usr/bin/env just --justfile

set dotenv-load := true

# List all available commands
default:
    @just -l

[group('dotnet')]
build: tailwind-build
    dotnet build

[group('dotnet')]
watch:
    ASPNETCORE_ENVIRONMENT=Development LASTFM_KEY=$LASTFM_KEY LASTFM_USER=$LASTFM_USER dotnet watch --project matsugane

[group('Tailwind')]
tailwind-build:
    bun update --cwd ./matsugane
    bunx @tailwindcss/cli --cwd ./matsugane -i ./Styles/tailwind.css -o ./wwwroot/tailwind.css --minify

[group('Tailwind')]
tailwind-watch:
    bunx @tailwindcss/cli --cwd ./matsugane -i ./Styles/tailwind.css -o ./wwwroot/tailwind.css --watch --minify

# Build a docker image
[group('docker')]
docker-build:
    docker build -t nledford/matsugane .

[group('docker')]
docker-run: docker-build
    docker run --rm -it \
      -p 8080:8080 \
      --env-file .env \
      -e TZ=America/New_York \
      --name matsugane nledford/matsugane:latest