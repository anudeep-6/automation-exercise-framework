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

## Containerising the Automation Framework

### What was built
A production-style Docker setup for the `automation-exercise-framework` project:
- `Dockerfile` — builds a self-contained image with Python 3.12, all dependencies, and Playwright + Chromium
- `.dockerignore` — excludes `.env`, `artifacts/`, `__pycache__`, `.git` from the build context
- `docker-compose.yml` — three named services (`api-tests`, `ui-tests`, `hybrid-tests`) for targeted suite execution

### Dockerfile decisions
```dockerfile
FROM python:3.12-slim                          # matches local runtime exactly
COPY pyproject.toml .                          # copied before source so layer cache survives code changes
RUN pip install --no-cache-dir .               # installs all project deps
RUN playwright install --with-deps chromium    # chromium only — keeps image lean (~500MB vs 1.5GB for all browsers)
COPY . .                                       # source copied last
```

### Why API tests first in Docker
API tests have no display or browser rendering dependency — they run reliably in any
headless Linux environment. UI tests need additional Playwright browser setup and are
better validated locally first before containerising.

### Secrets management
`.env` is in `.dockerignore` — it is never baked into the image layer.
Credentials are injected at runtime only:
```bash
docker run --env-file .env ecommerce-tests pytest tests/api/ -v
```
In `docker-compose.yml` this is handled via `env_file: .env` per service.

### Volume mount for artifacts
Allure results and test artifacts are written to the host machine by mounting `./artifacts`:
```yaml
volumes:
  - ./artifacts:/app/artifacts
```
Without this, artifacts disappear when the container exits.

### Result
17/17 API tests passed inside Docker in 11 seconds.
Environment: `Linux-6.6.87.2-microsoft-standard-WSL2` (Docker Desktop on Windows).

### Useful commands
```bash
# Build the image (run from repo root)
docker build -t ecommerce-tests .

# Run API suite
docker run --env-file .env ecommerce-tests pytest tests/api/ -v

# Run a specific test file
docker run --env-file .env ecommerce-tests pytest tests/api/test_products_api.py -v

# Run via compose (artifacts land in ./artifacts/)
docker-compose run api-tests

# Shell into the container for debugging
docker run --env-file .env -it ecommerce-tests /bin/bash
```