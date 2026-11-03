# Multi-stage production Dockerfile for Flask Backend

FROM python:3.13-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy backend and database seed scripts
COPY backend /app/backend
COPY database /app/database

WORKDIR /app/backend

RUN chmod +x entrypoint.sh

EXPOSE 10000

ENTRYPOINT ["./entrypoint.sh"]