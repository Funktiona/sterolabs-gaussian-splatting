# ZED SDK Docker Environment

This repository is focused on creating Gaussian splatting based on the Stereolab ZED2i camera. It provides a Docker setup for the ZED SDK on Ubuntu 24.04, enabling efficient development and deployment.

## Requirements

- Docker installed on your system
- Git for version control

## Quick Start

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   ```

2. Build and run the container:
   ```bash
   ./run.sh
   ```

## Contents

- `Dockerfile`: Contains the Docker image configuration with ZED SDK
- `run.sh`: Script to build and run the Docker container

## Project Overview

This project leverages the Stereolab ZED2i camera to perform Gaussian splatting, a technique used in computer vision and graphics for efficient rendering and processing of 3D data. The Docker environment ensures that all dependencies are correctly installed and configured, providing a seamless development experience.

## Additional Resources

- [Stereolab ZED SDK Documentation](https://www.stereolabs.com/docs/)
- [Docker Documentation](https://docs.docker.com/)

## Automatic Image Processing Pipeline

This project includes an automatic pipeline for processing images from a ZED2i SVO file. The pipeline performs the following steps:

1. **Image Extraction**: Extracts images from the ZED2i SVO file.
2. **Image Selection**: Automatically selects the best images based on high sharpness and uniqueness, removing similar images to ensure diversity.
3. **COLMAP Initialization**: Initializes COLMAP for Gaussian splatting, setting up the necessary environment for efficient 3D data processing and rendering.

This automated process streamlines the workflow, ensuring that only the most relevant and high-quality images are used for further processing. 