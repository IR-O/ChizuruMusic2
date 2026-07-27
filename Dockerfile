FROM python:3.10.4-slim-buster

# Update system and install dependencies
RUN apt update && apt upgrade -y
RUN apt-get install -y \
    git \
    curl \
    python3-pip \
    ffmpeg \
    wget \
    bash \
    neofetch \
    software-properties-common

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install wheel
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Run bot
CMD python3 -m Chizuru
