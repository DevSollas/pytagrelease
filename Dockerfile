FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY pyproject.toml README.md requirements-dev.txt app.py ./
COPY src ./src
COPY tests ./tests
COPY .env.example ./.env.example

RUN python -m pip install --upgrade pip && \
    pip install -e .[dev]

CMD ["sh", "-c", "ruff check . && mypy . && pytest -q"]
