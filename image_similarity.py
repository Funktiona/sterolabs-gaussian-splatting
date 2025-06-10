import cv2
import os
import numpy as np
from itertools import combinations

# Set debug mode
DEBUG = True

def calculate_histogram(image):
    """Calculate color histogram for the image."""
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Calculate histogram for HSV channels
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
    # Normalize histogram
    cv2.normalize(hist, hist)
    return hist.flatten()

def compare_images(img1, img2):
    """Compare two images using histogram correlation."""
    hist1 = calculate_histogram(img1)
    hist2 = calculate_histogram(img2)
    # Calculate correlation between histograms
    similarity = cv2.compareHist(hist1.reshape(-1, 1), hist2.reshape(-1, 1), cv2.HISTCMP_CORREL)
    return similarity

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
    
    if len(image_files) < 2:
        print("Need at least 2 JPG images in the images folder!")
        return

    # Store all similarity results
    similarity_results = []

    # Compare each pair of images
    for img1_name, img2_name in combinations(image_files, 2):
        # In debug mode, only process comparisons for the first image
        if DEBUG and img1_name != image_files[0]:
            continue

        img1_path = os.path.join(images_folder, img1_name)
        img2_path = os.path.join(images_folder, img2_name)

        try:
            # Read both images
            img1 = cv2.imread(img1_path)
            img2 = cv2.imread(img2_path)

            if img1 is None or img2 is None:
                print(f"Warning: Could not read one of the images: {img1_name} or {img2_name}")
                continue

            # Calculate similarity
            similarity = compare_images(img1, img2)
            similarity_results.append((img1_name, img2_name, similarity))

        except Exception as e:
            print(f"Error processing {img1_name} and {img2_name}: {str(e)}")

    # Sort results by similarity (highest to lowest)
    similarity_results.sort(key=lambda x: x[2], reverse=True)

    # Print results
    print("\nImage Similarity Analysis Results:")
    print("-" * 70)
    print(f"{'Image 1':<25} {'Image 2':<25} {'Similarity Index':>15}")
    print("-" * 70)
    
    for img1, img2, similarity in similarity_results:
        print(f"{img1:<25} {img2:<25} {similarity:>15.3f}")

    if not DEBUG:
        # Print most similar pairs for each image
        print("\nMost Similar Pair for Each Image:")
        print("-" * 70)
        
        processed_images = set()
        for img1, img2, similarity in similarity_results:
            if img1 not in processed_images:
                print(f"{img1:<25} is most similar to {img2:<25} (similarity: {similarity:.3f})")
                processed_images.add(img1)
            if img2 not in processed_images:
                print(f"{img2:<25} is most similar to {img1:<25} (similarity: {similarity:.3f})")
                processed_images.add(img2)
    else:
        print("\nDebug Mode: Only showing comparisons for the first image:", image_files[0])

if __name__ == "__main__":
    main() 