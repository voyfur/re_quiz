FROM python:3.12-slim

# Prevent python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Kyiv \
    PORT=8000 \
    BIND_HOST=0.0.0.0

WORKDIR /app

# Install system utilities if needed for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and JSON catalogs
COPY server.py runner_box_engine.py multi_sport_engine.py stock_checker.py luna_box_consultant.py ./
COPY *.json ./
COPY public/ ./public/

# Expose standard application port
EXPOSE 8000

# Container healthcheck using fast JSON health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/api/health || exit 1

CMD ["python3", "server.py"]
