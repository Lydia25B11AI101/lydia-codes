"""
Program Title: K-Means Clustering for Color Quantization
Author: Lydia S. Makiwa
Date: June 2, 2026

Description:
This program implements the K-Means Clustering algorithm from scratch using NumPy
and demonstrates its application in "color quantization" - reducing the number of 
distinct colors in an image. This is a fundamental unsupervised ML concept.
"""

import numpy as np

class KMeansScratch:
    def __init__(self, k=3, max_iters=100, tol=1e-4):
        self.k = k
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None
        
    def fit(self, X):
        # Randomly initialize centroids from data points
        n_samples, n_features = X.shape
        np.random.seed(42)  # For reproducible results
        random_idx = np.random.choice(n_samples, self.k, replace=False)
        self.centroids = X[random_idx]
        
        for _ in range(self.max_iters):
            # 1. Assign each point to the nearest centroid
            distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
            labels = np.argmin(distances, axis=1)
            
            # 2. Recompute centroids
            new_centroids = np.array([
                X[labels == j].mean(axis=0) if len(X[labels == j]) > 0 else self.centroids[j]
                for j in range(self.k)
            ])
            
            # Check for convergence
            if np.linalg.norm(new_centroids - self.centroids) < self.tol:
                self.centroids = new_centroids
                break
                
            self.centroids = new_centroids
            
        return self

    def predict(self, X):
        distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
        return np.argmin(distances, axis=1)

# --- Working Demo ---
if __name__ == "__main__":
    print("--- K-Means Color Quantization Demo ---")
    
    # Define a small 4x4 image with RGB channels (values 0-255)
    # We want to compress it from 16 colors to k=2 colors
    np.random.seed(0)
    mock_rgb_image = np.array([
        [[255, 0, 0], [254, 5, 2], [10, 12, 250], [12, 10, 240]],
        [[250, 10, 5], [245, 12, 8], [5, 5, 255], [8, 12, 245]],
        [[0, 255, 0], [5, 250, 4], [250, 250, 10], [245, 240, 12]],
        [[2, 255, 10], [1, 248, 5], [240, 245, 5], [255, 255, 0]]
    ], dtype=np.uint8)
    
    height, width, channels = mock_rgb_image.shape
    # Flatten image to 2D array of pixels (N, 3)
    pixels = mock_rgb_image.reshape(-1, channels)
    
    print(f"Original unique colors out of 16 pixels: {len(np.unique(pixels, axis=0))}")
    
    # Train K-Means to find k=3 main color clusters
    k = 3
    kmeans = KMeansScratch(k=k, max_iters=50)
    kmeans.fit(pixels)
    
    # Label each pixel
    labels = kmeans.predict(pixels)
    
    # Quantize: Replace each pixel's color with its centroid color
    quantized_pixels = kmeans.centroids[labels].astype(np.uint8)
    quantized_image = quantized_pixels.reshape(height, width, channels)
    
    print("\nDiscovered Centroids (Dominant Colors):")
    for idx, centroid in enumerate(kmeans.centroids):
        print(f"  Cluster {idx + 1}: R={centroid[0]:.1f}, G={centroid[1]:.1f}, B={centroid[2]:.1f}")
        
    print("\nQuantized (Compressed) Image Matrix (RGB):")
    for r in range(height):
        row_str = " | ".join(f"[{p[0]:3d}, {p[1]:3d}, {p[2]:3d}]" for p in quantized_image[r])
        print(row_str)