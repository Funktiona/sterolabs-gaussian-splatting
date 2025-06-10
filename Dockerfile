# Use Ubuntu 24.04 (Noble Numbat) as base image
FROM ubuntu:24.04

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and upgrade existing packages
RUN apt-get update && apt-get upgrade -y \
    # Install wget
    && apt-get install -y wget \
    # Clean up to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Download ZED SDK
RUN wget https://download.stereolabs.com/zedsdk/5.0/cu12/ubuntu24?_gl=1*kandh5*_gcl_au*MTc5MDA3OTA0NS4xNzQ3OTIwODg5 -O ZED_SDK_Ubuntu24_cuda12.run \
    && chmod +x ZED_SDK_Ubuntu24_cuda12.run

RUN apt install zstd

# Install ZED SDK
RUN ./ZED_SDK_Ubuntu24_cuda12.run --quiet --accept

# Clean up
RUN rm ZED_SDK_Ubuntu24_cuda12.run

# Set default command
CMD ["/bin/bash"] 