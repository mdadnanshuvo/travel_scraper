# Use an official Python image
FROM python:3.12-slim

# Set environment variables to avoid interactive prompts and enable DOCKER_ENV for epollreactor
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    DOCKER_ENV=1  

# Set working directory for your project
WORKDIR /app

# Install system dependencies required for PostgreSQL, Scrapy, Selenium, and Chromium
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    libevent-dev \
    wget \
    unzip \
    curl \
    gnupg2 \
    lsb-release \
    ca-certificates \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies: Selenium and Scrapy-Selenium
RUN pip install --no-cache-dir selenium scrapy-selenium twisted[select]

# Copy project files into the container
COPY . .

# Expose port for debugging or services (optional)
EXPOSE 8050

# Set up entry point for running the Scrapy spider
CMD ["scrapy"]
