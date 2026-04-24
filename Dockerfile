# Dockerfile
FROM python:3.12-slim

# System deps required by Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer cache benefit)
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Install Playwright + Chromium browser + its OS-level deps
RUN playwright install --with-deps chromium

# Copy the rest of the project
COPY . .

# Default: run API tests (no display needed)
CMD ["pytest", "tests/api/", "-v", "--tb=short"]