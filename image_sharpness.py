import cv2
import os
import numpy as np

def calculate_sharpness(image):
    """Calculate the sharpness of an image using Laplacian variance."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return laplacian.var()

def main():
    # Path to the images folder
    images_folder = "images"
    
    # Check if the folder exists
    if not os.path.exists(images_folder):
        print(f"Error: '{images_folder}' directory not found!")
        return

    # Get all jpg files
    image_files = [f for f in os.listdir(images_folder) 
                  if f.lower().endswith(('.jpg', '.jpeg'))]
    
    if not image_files:
        print("No JPG images found in the images folder!")
        return

    # Process each image and store results
    results = []
    for filename in image_files:
        filepath = os.path.join(images_folder, filename)
        try:
            # Read the image
            img = cv2.imread(filepath)
            if img is None:
                print(f"Warning: Could not read image {filename}")
                continue
                
            # Calculate sharpness
            sharpness = calculate_sharpness(img)
            results.append((filename, sharpness))
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    # Sort results by sharpness (highest to lowest)
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Print results
    print("\nImage Sharpness Analysis Results:")
    print("-" * 50)
    print(f"{'Filename':<30} {'Sharpness Index':>15}")
    print("-" * 50)
    for filename, sharpness in results:
        print(f"{filename:<30} {sharpness:>15.2f}")

if __name__ == "__main__":
    main()
