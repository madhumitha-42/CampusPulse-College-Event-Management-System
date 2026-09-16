# Multi-stage Dockerfile for CampusPulse Fullstack Deployment

# -----------------------------------------------------------------------------
# Stage 1: Build Frontend
# -----------------------------------------------------------------------------
FROM node:22-alpine AS frontend-builder
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY frontend/package.json ./frontend/
COPY lib/ ./lib/
COPY scripts/ ./scripts/
COPY artifacts-api-server/ ./artifacts-api-server/
RUN pnpm install --frozen-lockfile || pnpm install
COPY frontend/ ./frontend/
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN pnpm --filter @workspace/college-events run build

# -----------------------------------------------------------------------------
# Stage 2: Django Backend & Production Server
# -----------------------------------------------------------------------------
FROM python:3.11-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ ./backend/
COPY --from=frontend-builder /app/frontend/dist/public ./backend/staticfiles/frontend

WORKDIR /app/backend
EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
