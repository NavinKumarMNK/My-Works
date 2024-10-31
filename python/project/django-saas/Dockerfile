FROM python:3.12.7-slim-bullseye
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONBUFFERED 1

RUN apt-get update && apt-get install -y curl libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

COPY pyproject.toml pyproject.toml
RUN uv venv && uv pip install -r pyproject.toml --system
COPY src src

WORKDIR /src

RUN python manage.py pull_staticfiles
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD [ "sh", "entrypoint.sh" ]