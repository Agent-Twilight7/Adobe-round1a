# Base image with explicit AMD64 platform specification
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install dependencies (no cache to reduce image size, offline compatible)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Create the expected input/output directories
RUN mkdir -p /app/input /app/output

# Default command can be overridden when running
CMD ["python", "main.py"]
