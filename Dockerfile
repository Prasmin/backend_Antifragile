# syntax=docker/dockerfile:1

FROM python:3.13-slim

# Keep logs visible immediately in Docker
ENV PYTHONUNBUFFERED=1

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Compile bytecode at build time for faster container startup
ENV UV_COMPILE_BYTECODE=1
# Use copy mode — hardlinks are unreliable across Docker layers
ENV UV_LINK_MODE=copy

WORKDIR /app

# Add the virtual environment to PATH so uv-installed tools are available
ENV PATH="/app/.venv/bin:$PATH"

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Stage 1: install dependencies only.
# This layer is cached separately — rebuilds only when pyproject.toml or uv.lock changes.
COPY pyproject.toml uv.lock .python-version ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Stage 2: copy application code, then install the project itself.
COPY ./app /app/app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Switch to the non-privileged user to run the application.
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application using uvicorn directly.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
