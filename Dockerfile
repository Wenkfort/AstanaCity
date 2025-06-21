# Use ARMv7 compatible base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV TYPE=TELEGRAM
ENV DATABASE_TYPE=JSON
ENV DATA_FILE=data.json

# Command to run the application
# CMD ["python", "launcher.py"] 
