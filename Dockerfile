# Stage 1: Base image setup with Poetry installation
FROM python:3.11-slim AS base

# Set Poetry installation path
ENV POETRY_HOME=/opt/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}

# Install curl for Poetry installation and essential build dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && poetry --version

# Stage 2: Builder for installing dependencies with Poetry
FROM base AS builder

WORKDIR /app

# Copy Poetry lock files
COPY poetry.lock pyproject.toml ./

# Configure Poetry to use an in-project virtual environment
RUN poetry config virtualenvs.in-project true

# Install dependencies using Poetry
RUN poetry install --no-root

# Stage 3: Runner for final application
FROM base AS runner

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv/ /app/.venv/

# Copy application code into the container
COPY . /app

# Create database directory (or mount a volume if needed)
RUN mkdir -p /db

# Expose the necessary port
EXPOSE 8000

# Ensure entrypoint script is executable
RUN chmod +x /app/src/entrypoint.sh

# Stage 4: Development environment (optional)
FROM runner AS development

WORKDIR /app/src
ENTRYPOINT [ "/app/src/entrypoint.sh" ]

# Stage 5: Production environment (set user/group for production deployment)
FROM runner AS production

# Set user and group for security purposes
ARG user=django
ARG group=django
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user}

# Set ownership to the specified user/group
RUN chown -R ${uid}:${gid} /app
RUN chown -R ${uid}:${gid} /db

USER ${uid}:${gid}

WORKDIR /app/src
ENTRYPOINT [ "/app/src/entrypoint.sh" ]