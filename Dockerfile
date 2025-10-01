FROM python:3.12-slim AS base

ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    git \
 && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Copier uniquement les fichiers de gestion des dépendances pour profiter du cache Docker
COPY pyproject.toml poetry.lock* /app/

RUN /opt/poetry/bin/poetry install --no-root --only main

COPY . /app

EXPOSE 5000

CMD ["/opt/poetry/bin/poetry", "run", "python", "app.py"]
