#!/usr/bin/env just --justfile

set dotenv-load := true

# List all available commands
default:
    @just -l

# Activate virtual environment
[group('Python')]
venv:
    source .venv/bin/activate

# Lint and format code
[group('Python')]
lint:
    uv run pyright
    uvx ruff check --fix
    uvx ruff format

# Run unit tests
[group('Python')]
test: lint
    uv run pytest -v

# Run the application
[group('Python')]
run: test
    uvx textual run --dev ./src/matsugane/main.py

# Upgrades `pyproject.toml` dependencies with `uv`. (SOURCE: https://gist.github.com/yhoiseth/c80c1e44a7036307e424fce616eed25e)
[group('Python')]
upgrade:
    #!/usr/bin/env python
    from typing import Any
    from re import match, Match
    import toml
    import subprocess


    def main() -> None:
        with open("pyproject.toml", "r") as file:
            pyproject: dict[str, Any] = toml.load(file)
        dependencies: list[str] = pyproject["project"]["dependencies"]
        package_name_pattern = r"^[a-zA-Z0-9\-]+"
        for dependency in dependencies:
            package_match = match(package_name_pattern, dependency)
            assert isinstance(package_match, Match)
            package = package_match.group(0)
            uv("remove", package)
            uv("add", package)


    def uv(command: str, package: str) -> None:
        subprocess.run(["uv", command, package])


    if __name__ == "__main__":
        main()

# Update Python packages
[group('Python')]
update: upgrade
    uv lock --upgrade
    uv sync --all-groups

# Build docker image
[group('Docker')]
docker-build:
    docker build -t nledford/matsugane:latest .

# Run docker image
[group('Docker')]
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

# Test Github actions
[group('Github')]
act:
    act -s GITHUB_TOKEN="$(gh auth token)"
