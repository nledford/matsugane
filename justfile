#!/usr/bin/env just --justfile

set dotenv-load

venv:
    source .venv/bin/activate

lint:
    uv run pyright
    uvx ruff check --fix
    uvx ruff format

test: lint
    pytest -v

run:
    #uv run lastfm_stats
    uvx textual run --dev ./src/matsugane/main.py

# updates dependecies using `uv`
# SOURCE: https://gist.github.com/yhoiseth/c80c1e44a7036307e424fce616eed25e
update:
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

lock-sync:
    uv lock --upgrade
    uv sync --all-groups

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

act:
    act -s GITHUB_TOKEN="$(gh auth token)"