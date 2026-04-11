# building
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# runtime
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app
RUN useradd -u 1000 -m appuser

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/assets /app/assets
COPY --from=builder /app/alembic.ini /app/alembic.ini
COPY --from=builder /app/src/marionette/infrastructure/database/alembic /app/src/marionette/infrastructure/database/alembic

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONBUFFERED=1

USER appuser

CMD ["python", "-OO", "-m", "marionette"]