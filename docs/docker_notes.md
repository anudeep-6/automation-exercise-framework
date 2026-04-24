# Docker Notes

## What is Docker?
Docker runs applications in isolated containers — lightweight environments that package
code + dependencies together. Containers behave identically on any machine, eliminating
"works on my machine" problems.

## Why it matters for testing
- CI/CD pipelines (GitHub Actions, Jenkins) run tests inside Docker containers
- Guarantees test environment consistency across dev machines and CI
- Lets you reproduce CI failures locally by running the same container

## Key Concepts
- **Image** – a read-only template (e.g. `python:3.12-slim`)
- **Container** – a running instance of an image
- **Volume mount** – maps a host folder into the container (`-v host_path:container_path`)
- **Dockerfile** – a recipe to build a custom image

## Core Commands
```bash
# Pull an image from Docker Hub
docker pull python:3.12-slim

# Run a one-liner inside a container
docker run python:3.12-slim python -c "print('Tests running in Docker')"

# Run a local file inside a container via volume mount
# Must cd into the file's directory first — container paths are Linux paths
cd /path/to/folder
docker run -v ${PWD}:/tests python:3.12-slim python /tests/test_hello.py

# Run pytest inside a container
docker run -v ${PWD}:/tests python:3.12-slim sh -c "pip install pytest -q && pytest /tests/test_hello.py -v"
```

## Windows Gotcha
Container paths are always Linux paths regardless of host OS.
Never pass a Windows path (C:\...) to the container — use the mounted path (/tests/...) instead.