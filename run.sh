#!/bin/bash

# Build the Docker image
docker build -t zed-sdk-ubuntu24 .

# Run the container in interactive mode with a pseudo-TTY
# and remove it when it exits
docker run -it --rm \
    --name zed-container \
    zed-sdk-ubuntu24 