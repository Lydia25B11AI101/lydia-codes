# Python Program 22: NumPy Basics for AIML
# Author: Lydia S. Makiwa
# Description: Introduction to NumPy arrays — foundation of AI/ML in Python

import numpy as np

# ── Array Creation ────────────────────────────────────────
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])
zeros  = np.zeros((3, 3))
ones   = np.ones((2, 4))
rng    = np.arange(0, 20, 2)
linsp  = np.linspace(0, 1, 5)

print("Array a:", a)
print("Array b:", b)
print("Zeros 3x3:\n", zeros)
print("Arange 0-20 step 2:", rng)
print("Linspace 0 to 1:", linsp)

# ── Array Operations ──────────────────────────────────────
print("\na + b:", a + b)
print("a * 2: ", a * 2)
print("a ** 2:", a ** 2)
print("dot product a·b:", np.dot(a, b))

# ── Statistics ────────────────────────────────────────────
data = np.array([23, 45, 12, 67, 34, 89, 56, 11, 78, 42])
print("\nData:", data)
print(f"Mean:   {np.mean(data):.2f}")
print(f"Median: {np.median(data):.2f}")
print(f"Std:    {np.std(data):.2f}")
print(f"Min:    {np.min(data)} | Max: {np.max(data)}")

# ── 2D Array / Matrix ─────────────────────────────────────
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\nMatrix:\n", matrix)
print("Transpose:\n", matrix.T)
print("Shape:", matrix.shape, "| Dtype:", matrix.dtype)
print("Row 0:", matrix[0], "| Col 1:", matrix[:, 1])
