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
    bunx @tailwindcss/cli --cwd ./matsugane -i ./Styles/tailwind.css -o ./wwwroot/app.css --minify

[group('Tailwind')]
tailwind-watch:
    bunx @tailwindcss/cli --cwd ./matsugane -i ./Styles/tailwind.css -o ./wwwroot/app.css --watch --minify
