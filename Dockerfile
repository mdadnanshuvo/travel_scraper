# Use an official Python image
FROM python:3.12-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory for your project
WORKDIR /app

# Install system dependencies for Playwright and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    libevent-dev \
    libgstreamer-plugins-bad1.0-0 \
    libflite1 \
    gstreamer1.0-libav \
    libx11-xcb1 \
    libdbus-1-3 \
    libxtst6 \
    libnss3 \
    libatk1.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libatk-bridge2.0-0 \
    libnspr4 \
    && rm -rf /var/lib/apt/lists/*  # Clean apt cache to reduce image size

# Install Playwright (installs required browsers)
RUN pip install playwright && python -m playwright install --with-deps

# Install Twisted and select reactor
RUN pip install twisted[select]

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Scrapy is installed explicitly
RUN pip install scrapy

# Install scrapy-playwright for Playwright support in Scrapy
RUN pip install scrapy-playwright

# Copy project files into the container
COPY . .

# Expose port for Playwright or any service your app needs (e.g., port 8050 for Splash)
EXPOSE 8050  

# Set up the default command to run Scrapy crawl command (or any other necessary command)
CMD ["scrapy"]  # Update with your actual spider name
