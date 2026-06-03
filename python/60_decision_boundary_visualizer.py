# ==============================================================================
# Title: 2D Decision Boundary Visualizer from Scratch
# Author: Lydia S. Makiwa
# Date: June 3, 2026
# Description: Generates a synthetic 2D binary classification dataset, trains a
#              simple custom K-Nearest Neighbors (KNN) classifier, and plots the
#              resulting decision boundary using Matplotlib.
#              Helps AIML students visualize how classification models partition feature space.
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

class SimpleKNN:
    """
    A simple K-Nearest Neighbors Classifier implemented from scratch.
    """
    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def _euclidean_distance(self, x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def predict_single(self, x):
        # Calculate distance from point x to all training points
        distances = [self._euclidean_distance(x, x_train) for x_train in self.X_train]
        # Get the indices of the k-nearest neighbors
        k_indices = np.argsort(distances)[:self.k]
        # Get the labels of the k-nearest neighbors
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        # Return the most common label (majority vote)
        most_common = max(set(k_nearest_labels), key=k_nearest_labels.count)
        return most_common

    def predict(self, X):
        return np.array([self.predict_single(x) for x in X])

# --- Generate Synthetic Dataset ---
def generate_dataset(n_samples=60):
    np.random.seed(42)
    # Class 0: centered around [1.5, 1.5]
    class0 = np.random.randn(n_samples // 2, 2) * 0.6 + np.array([1.5, 1.5])
    # Class 1: centered around [3.5, 3.5]
    class1 = np.random.randn(n_samples // 2, 2) * 0.6 + np.array([3.5, 3.5])
    
    X = np.vstack((class0, class1))
    y = np.array([0] * (n_samples // 2) + [1] * (n_samples // 2))
    return X, y

# --- Demo & Plotting ---
if __name__ == "__main__":
    print("--- 2D KNN Decision Boundary Visualizer ---")
    
    # 1. Generate data
    X, y = generate_dataset()
    print(f"Generated {len(X)} data points with 2 features (X1, X2) and binary classes.")
    
    # 2. Fit KNN model
    knn = SimpleKNN(k=5)
    knn.fit(X, y)
    print("Fitted a custom K-Nearest Neighbors (K=5) classifier.")
    
    # 3. Create a meshgrid to plot decision boundary
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                         np.arange(y_min, y_max, 0.1))
    
    # Predict for each point in meshgrid
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    Z = knn.predict(grid_points)
    Z = Z.reshape(xx.shape)
    
    # 4. Plot results
    plt.figure(figsize=(8, 6))
    # Draw decision boundary
    plt.contourf(xx, yy, Z, alpha=0.3, colors=['#FF9999', '#99FF99'])
    
    # Scatter training data points
    plt.scatter(X[y == 0][:, 0], X[y == 0][:, 1], color='red', label='Class 0 (Red)', edgecolors='k')
    plt.scatter(X[y == 1][:, 0], X[y == 1][:, 1], color='green', label='Class 1 (Green)', edgecolors='k')
    
    plt.title("KNN (K=5) Decision Boundary (Custom Implementation)", fontsize=14)
    plt.xlabel("Feature X1", fontsize=12)
    plt.ylabel("Feature X2", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Save the chart
    output_path = "knn_decision_boundary.png"
    plt.savefig(output_path, dpi=150)
    print(f"Plot saved successfully as '{output_path}'.")
    plt.close()
