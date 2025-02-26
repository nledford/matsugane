#!/usr/bin/env just --justfile

# List all available commands
default:
    @just -l

[group('Tailwind')]
tailwind-build:
    bunx @tailwindcss/cli -i ./matsugane/Styles/tailwind.css -o ./matsugane/wwwroot/lib/css/styles.css

[group('Tailwind')]
tailwind-watch:
    bunx @tailwindcss/cli --cwd ./matsugane -i ./Styles/tailwind.css -o ./wwwroot/app.css --watch --minify
