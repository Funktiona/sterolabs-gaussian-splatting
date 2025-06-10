import os
import subprocess
import sqlite3
import numpy as np
from pathlib import Path

def run_colmap_feature_extractor(image_dir, database_path):
    """Run COLMAP feature extraction on images."""
    cmd = [
        'colmap', 'feature_extractor',
        '--database_path', os.path.abspath(database_path),
        '--image_path', os.path.abspath(image_dir),
        '--ImageReader.camera_model', 'SIMPLE_RADIAL',
        '--SiftExtraction.use_gpu', '0'  # Use CPU
    ]
    subprocess.run(cmd, check=True)

def run_colmap_matcher(database_path):
    """Run COLMAP exhaustive matcher."""
    cmd = [
        'colmap', 'exhaustive_matcher',
        '--database_path', os.path.abspath(database_path),
        '--SiftMatching.use_gpu', '0'  # Use CPU
    ]
    subprocess.run(cmd, check=True)

def run_colmap_mapper(database_path, image_dir, output_dir):
    """Run COLMAP mapper to reconstruct scene."""
    cmd = [
        'colmap', 'mapper',
        '--database_path', os.path.abspath(database_path),
        '--image_path', os.path.abspath(image_dir),
        '--output_path', os.path.abspath(output_dir)
    ]
    subprocess.run(cmd, check=True)

def extract_camera_positions(sparse_dir):
    """Extract camera positions from COLMAP reconstruction."""
    cameras = {}
    
    # Read images.txt
    images_file = os.path.join(sparse_dir, '0', 'images.txt')
    if not os.path.exists(images_file):
        raise FileNotFoundError(f"Could not find {images_file}")
    
    with open(images_file, 'r') as f:
        lines = f.readlines()
    
    # Parse camera positions
    for i in range(0, len(lines), 2):
        if lines[i].startswith('#'):
            continue
        
        # Parse image data line
        data = lines[i].strip().split()
        image_id = int(data[0])
        qw, qx, qy, qz = map(float, data[1:5])  # Quaternion
        tx, ty, tz = map(float, data[5:8])  # Translation
        image_name = data[-1]
        
        # Store position and orientation
        cameras[image_name] = {
            'position': np.array([tx, ty, tz]),
            'quaternion': np.array([qw, qx, qy, qz])
        }
    
    return cameras

def main():
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.join(current_dir, 'colmap_workspace')
    image_dir = os.path.join(current_dir, 'images')
    database_path = os.path.join(workspace_dir, 'database.db')
    output_dir = os.path.join(workspace_dir, 'sparse')
    
    # Create workspace directory
    os.makedirs(workspace_dir, exist_ok=True)
    
    # Check if images directory exists
    if not os.path.exists(image_dir):
        print(f"Error: '{image_dir}' directory not found!")
        return
    
    try:
        print("Running COLMAP pipeline...")
        print(f"Using images from: {image_dir}")
        print(f"Workspace directory: {workspace_dir}")
        
        # Run COLMAP pipeline
        print("1. Extracting features (CPU mode)...")
        run_colmap_feature_extractor(image_dir, database_path)
        
        print("2. Matching features (CPU mode)...")
        run_colmap_matcher(database_path)
        
        print("3. Mapping scene...")
        run_colmap_mapper(database_path, image_dir, output_dir)
        
        # Extract and print camera positions
        print("\nCamera Positions:")
        print("-" * 70)
        print(f"{'Image Name':<30} {'Position (X, Y, Z)':<40}")
        print("-" * 70)
        
        cameras = extract_camera_positions(output_dir)
        for image_name, data in cameras.items():
            pos = data['position']
            print(f"{image_name:<30} ({pos[0]:8.3f}, {pos[1]:8.3f}, {pos[2]:8.3f})")
            
    except subprocess.CalledProcessError as e:
        print(f"Error running COLMAP: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 