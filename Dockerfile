FROM python:3.12-slim

# Install system dependencies for MySQL and general tools
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    git \
    curl \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code (will be overwritten by volume but good for build)
COPY . .

# Default port for Django
EXPOSE 8000

# Command to run (overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
