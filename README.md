# 3D Gaussian Splatting using sterolabs ZED2i Camera
This repository is focused on creating Gaussian splatting based on the Stereolab ZED2i camera. It provides a Docker setup for the ZED SDK on Ubuntu 24.04, enabling efficient development and deployment.

## Automatic Image Processing Pipeline

This project includes an automatic pipeline for processing images from a ZED2i SVO file. The pipeline performs the following steps:

1. **Image Extraction**: Extracts images from the ZED2i SVO file.
2. **Image Selection**: Automatically selects the best images based on high sharpness and uniqueness.
3. **COLMAP Initialization**: Initializes COLMAP for Gaussian splatting.
4. **Gaussian Splatting**: Performs 3D Gaussian splatting using the gsplat library to generate a high-quality 3D reconstruction.

This automated process streamlines the workflow, ensuring that only the most relevant and high-quality images are used for further processing. 
## Requirements

- Docker installed on your system
- NVIDIA graphics card

## Quick Start

1. Clone the repository, build the Docker image, and run the container:
   ```bash
   https://github.com/Funktiona/sterolabs-gaussian-splatting
   sudo docker build -t stereolabs-gaussian-splatting .
   sudo docker run -it --rm --name zed-container stereolabs-gaussian-splatting
   ```


## Additional Resources

- [Stereolab ZED SDK Documentation](https://www.stereolabs.com/docs/)
- [Docker Documentation](https://docs.docker.com/)
