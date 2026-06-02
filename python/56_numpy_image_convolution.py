"""
Program Title: Image Convolution and Filtering using NumPy
Author: Lydia S. Makiwa
Date: June 2, 2026

Description:
This program demonstrates 2D image convolution (edge detection, sharpening, blurring)
from scratch using NumPy. It illustrates the mathematical core of Convolutional Neural
Networks (CNNs) without relying on external computer vision frameworks like OpenCV.
"""

import numpy as np

def convolve2d(image, kernel):
    """
    Performs 2D convolution of an image with a kernel.
    Assumes image is a 2D numpy array and kernel is a 2D square numpy array.
    Uses 'zero padding' and a stride of 1.
    """
    img_height, img_width = image.shape
    kernel_height, kernel_width = kernel.shape
    
    # Calculate padding size to maintain image dimensions (assuming odd kernel size)
    pad_h = kernel_height // 2
    pad_w = kernel_width // 2
    
    # Pad the input image with zeros
    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    
    # Initialize output image
    output = np.zeros_like(image, dtype=np.float32)
    
    # Perform convolution
    for i in range(img_height):
        for j in range(img_width):
            # Extract region of interest (ROI)
            roi = padded_image[i:i + kernel_height, j:j + kernel_width]
            # Element-wise multiplication and sum
            output[i, j] = np.sum(roi * kernel)
            
    return output

# Define common image processing kernels
sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]], dtype=np.float32)

sobel_y = np.array([[-1, -2, -1],
                    [ 0,  0,  0],
                    [ 1,  2,  1]], dtype=np.float32)

blur_kernel = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]], dtype=np.float32) / 9.0

sharpen_kernel = np.array([[ 0, -1,  0],
                           [-1,  5, -1],
                           [ 0, -1,  0]], dtype=np.float32)

# --- Working Demo ---
if __name__ == "__main__":
    print("--- 2D Image Convolution Demo ---")
    
    # Create a simple 10x10 mock image representing a bright square in the center
    mock_image = np.zeros((10, 10), dtype=np.float32)
    mock_image[3:7, 3:7] = 255.0
    
    print("\nOriginal Mock Image (Bright square in the center):")
    # Format print to make it easy to see the shape
    for row in mock_image:
        print(" ".join(f"{int(x):3d}" for x in row))
        
    # Apply Sobel X filter (Horizontal edge detector)
    detected_edges_x = convolve2d(mock_image, sobel_x)
    
    print("\nEdges detected along the X-axis (Sobel X):")
    for row in detected_edges_x:
        print(" ".join(f"{int(x):4d}" for x in row))
        
    # Apply Box Blur filter
    blurred_img = convolve2d(mock_image, blur_kernel)
    print("\nBlurred Image:")
    for row in blurred_img:
        print(" ".join(f"{int(x):3d}" for x in row))