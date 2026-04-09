# AIML Program 10: Convolutional Neural Network (CNN) from Scratch
# Author: Lydia S. Makiwa
# Description: Implements CNN building blocks manually:
#              - Convolution (cross-correlation)
#              - ReLU activation
#              - Max Pooling
#              - Flattening
#              - Fully connected layer
#              Demonstrates edge detection and feature extraction

import numpy as np

# ── 1. Convolution Operation ──────────────────────────────
def convolve2d(image, kernel, padding=0, stride=1):
    """
    Applies a 2D convolution (cross-correlation) to an image.
    image:  H x W
    kernel: kH x kW
    """
    if padding > 0:
        image = np.pad(image, padding, mode='constant')

    H, W   = image.shape
    kH, kW = kernel.shape
    out_H  = (H - kH) // stride + 1
    out_W  = (W - kW) // stride + 1
    output = np.zeros((out_H, out_W))

    for i in range(out_H):
        for j in range(out_W):
            region = image[i*stride:i*stride+kH, j*stride:j*stride+kW]
            output[i, j] = np.sum(region * kernel)

    return output

# ── 2. Pooling ────────────────────────────────────────────
def max_pool2d(feature_map, size=2, stride=2):
    """Applies max pooling to reduce spatial dimensions."""
    H, W   = feature_map.shape
    out_H  = (H - size) // stride + 1
    out_W  = (W - size) // stride + 1
    output = np.zeros((out_H, out_W))

    for i in range(out_H):
        for j in range(out_W):
            region = feature_map[i*stride:i*stride+size, j*stride:j*stride+size]
            output[i, j] = np.max(region)

    return output

def avg_pool2d(feature_map, size=2, stride=2):
    """Applies average pooling."""
    H, W   = feature_map.shape
    out_H  = (H - size) // stride + 1
    out_W  = (W - size) // stride + 1
    output = np.zeros((out_H, out_W))

    for i in range(out_H):
        for j in range(out_W):
            region = feature_map[i*stride:i*stride+size, j*stride:j*stride+size]
            output[i, j] = np.mean(region)

    return output

def relu(x): return np.maximum(0, x)

# ── 3. Classic CNN Kernels (Filters) ─────────────────────
kernels = {
    "Edge Detection (Sobel H)": np.array([[-1,-2,-1],[0,0,0],[1,2,1]]),
    "Edge Detection (Sobel V)": np.array([[-1,0,1],[-2,0,2],[-1,0,1]]),
    "Sharpen":                  np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]),
    "Blur (Box)":               np.ones((3,3)) / 9,
    "Emboss":                   np.array([[-2,-1,0],[-1,1,1],[0,1,2]]),
}

# ── 4. Demo: Apply CNN pipeline to a synthetic "image" ────
np.random.seed(42)

# Create a simple 8x8 synthetic grayscale "image"
image = np.array([
    [0,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,0,0],
    [0,1,1,0,0,1,1,0],
    [0,1,0,0,0,0,1,0],
    [0,1,0,0,0,0,1,0],
    [0,1,1,0,0,1,1,0],
    [0,0,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0],
], dtype=float)

print("=== CNN from Scratch — Feature Extraction Demo ===\n")
print("Input Image (8x8 — circle shape):")
for row in image:
    print("  " + " ".join(["█" if v > 0 else "·" for v in row]))

print(f"\nImage shape: {image.shape}")

# Apply each kernel
for name, kernel in kernels.items():
    feature_map  = convolve2d(image, kernel, padding=1)
    activated    = relu(feature_map)
    pooled       = max_pool2d(activated, size=2, stride=2)
    flattened    = pooled.flatten()

    print(f"\n{'─'*50}")
    print(f"Filter: {name}")
    print(f"  After Conv2D:  {feature_map.shape} | min={feature_map.min():.2f} max={feature_map.max():.2f}")
    print(f"  After ReLU:    {activated.shape}  | zeros={(activated==0).sum()}")
    print(f"  After MaxPool: {pooled.shape}     | values={pooled.flatten().round(1)}")
    print(f"  Flattened:     {flattened.shape[0]} features → FC layer input")

print("\n" + "═"*50)
print("CNN Pipeline Summary:")
print("  Input Image (8x8)")
print("  → Conv2D (3x3 kernel, padding=1) → same size")
print("  → ReLU activation → zeros negatives")
print("  → MaxPool (2x2, stride=2) → halves dimensions")
print("  → Flatten → FC layer → class prediction")
print("\nThis is the core building block of image classification!")
print("Real CNNs (VGG, ResNet) stack many such layers.")
