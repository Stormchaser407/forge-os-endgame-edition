# Forge OS Endgame Edition - Build Environment
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV FORGE_VERSION="1.0.0-endgame"
ENV OBSIDIAN_VERSION="1.0.0"

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    debootstrap \
    squashfs-tools \
    genisoimage \
    isolinux \
    syslinux-utils \
    xorriso \
    grub-pc-bin \
    grub-efi-amd64-bin \
    grub-efi-amd64-signed \
    mtools \
    dosfstools \
    wget \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    cryptsetup \
    plymouth-themes \
    gnome-shell \
    gnome-tweaks \
    docker.io \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Install modern Node.js for Obsidian Council frontend
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Set up Python environment for AI agents
RUN python3 -m pip install --upgrade pip && \
    pip3 install \
    fastapi \
    uvicorn \
    websockets \
    asyncio \
    aiohttp \
    openai \
    anthropic \
    google-generativeai \
    pandas \
    numpy \
    sqlalchemy \
    asyncpg \
    redis \
    celery \
    cryptography \
    requests \
    beautifulsoup4 \
    selenium \
    scrapy \
    nltk \
    transformers \
    torch

# Set up build directories
RUN mkdir -p /forge-os/{build,config,scripts,applications,obsidian-council,branding}

WORKDIR /forge-os

# Copy build configuration
COPY scripts/ /forge-os/scripts/
COPY config/ /forge-os/config/
COPY obsidian-council/ /forge-os/obsidian-council/
COPY branding/ /forge-os/branding/
COPY applications/ /forge-os/applications/

# Make scripts executable
RUN chmod +x /forge-os/scripts/*.sh

# Install Obsidian Council dependencies
WORKDIR /forge-os/obsidian-council
RUN npm install

# Build Obsidian Council frontend
RUN npm run build

WORKDIR /forge-os

# Default build command
CMD ["/forge-os/scripts/build-forge-os.sh"]