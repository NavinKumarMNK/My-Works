FROM python:3.11.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y curl libpq-dev build-essential
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

WORKDIR /app
COPY pyproject.toml pyproject.toml

RUN uv venv && uv pip install -r pyproject.toml --system

CMD ["fastapi", "dev", "src", "--reload", "--host", "0.0.0.0", "--port", "8000"]
