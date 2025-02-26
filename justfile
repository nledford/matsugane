#!/usr/bin/env just --justfile

# List all available commands
default:
    @just -l

[group('dotnet')]
build: tailwind-build
    dotnet build

[group('dotnet')]
watch:
    dotnet watch --project matsugane

[group('Tailwind')]
tailwind-build:
    bun update --cwd ./matsugane
    bunx @tailwindcss/cli --cwd ./matsugane -i ./Styles/tailwind.css -o ./wwwroot/app.css --minify

[group('Tailwind')]
tailwind-watch:
    bunx @tailwindcss/cli --cwd ./matsugane -i ./Styles/tailwind.css -o ./wwwroot/app.css --watch --minify
