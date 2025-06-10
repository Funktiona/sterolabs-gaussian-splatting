# Use Ubuntu 24.04 (Noble Numbat) as base image
FROM ubuntu:24.04

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and upgrade existing packages
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y wget gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# # Add NVIDIA package repositories
# RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-ubuntu2404.pin \
#     && mv cuda-ubuntu2404.pin /etc/apt/preferences.d/cuda-repository-pin-600 \
#     && wget https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda-repo-ubuntu2404-12-0-local_12.0.0-1_amd64.deb \
#     && dpkg -i cuda-repo-ubuntu2404-12-0-local_12.0.0-1_amd64.deb \
#     && cp /var/cuda-repo-ubuntu2404-12-0-local/cuda-*-keyring.gpg /usr/share/keyrings/ \
#     && apt-get update \
#     && apt-get -y install cuda

# Set environment variables
ENV PATH=/usr/local/cuda-12.0/bin${PATH:+:${PATH}}
ENV LD_LIBRARY_PATH=/usr/local/cuda-12.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}


# Install ZED SDK
#RUN ./ZED_SDK_Ubuntu24_cuda12.run --quiet --accept

# Clean up
#RUN rm ZED_SDK_Ubuntu24_cuda12.run



RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-ubuntu2404.pin
RUN mv cuda-ubuntu2404.pin /etc/apt/preferences.d/cuda-repository-pin-600
RUN wget https://developer.download.nvidia.com/compute/cuda/12.9.1/local_installers/cuda-repo-ubuntu2404-12-9-local_12.9.1-575.57.08-1_amd64.deb
RUN dpkg -i cuda-repo-ubuntu2404-12-9-local_12.9.1-575.57.08-1_amd64.deb
RUN cp /var/cuda-repo-ubuntu2404-12-9-local/cuda-*-keyring.gpg /usr/share/keyrings/
RUN apt-get update
RUN apt-get -y install cuda-toolkit-12-9
RUN apt install cuda -y

# Set working directory
WORKDIR /app

# Create a non-root user
RUN useradd -ms /bin/bash zeduser

# Change to non-root user
USER zeduser

# Download ZED SDK
RUN wget https://download.stereolabs.com/zedsdk/5.0/cu12/ubuntu24?_gl=1*kandh5*_gcl_au*MTc5MDA3OTA0NS4xNzQ3OTIwODg5 -O ZED_SDK_Ubuntu24_cuda12.run \
    && chmod +x ZED_SDK_Ubuntu24_cuda12.run

# Install ZED SDK
RUN ./ZED_SDK_Ubuntu24_cuda12.run --quiet --accept

# Switch back to root user to clean up
USER root

# Clean up
RUN rm ZED_SDK_Ubuntu24_cuda12.run

# Set default command
CMD ["/bin/bash"]