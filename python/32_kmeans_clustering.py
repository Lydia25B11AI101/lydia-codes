# ============================================================
# Program Title : K-Means Clustering from Scratch
# Author        : Lydia S. Makiwa
# Date          : 2026-05-02
# Description   : Unsupervised learning -- assigns data points
#                 to k groups based on centroid proximity.
# ============================================================

import numpy as np
import random

class KMeans:
    def __init__(self, k=3, max_iter=100):
        self.k = k
        self.max_iter = max_iter
        self.centroids = None

    def _assign(self, X):
        dists = np.linalg.norm(X[:, None] - self.centroids[None, :], axis=2)
        return np.argmin(dists, axis=1)

    def fit(self, X):
        idx = random.sample(range(len(X)), self.k)
        self.centroids = X[idx].copy()
        for i in range(self.max_iter):
            labels = self._assign(X)
            new_c  = np.array([X[labels==j].mean(axis=0) for j in range(self.k)])
            if np.allclose(self.centroids, new_c):
                print(f"  Converged in {i+1} iterations.")
                break
            self.centroids = new_c
        return labels

    def predict(self, X):
        return self._assign(X)


# -- Demo ------------------------------------------------------
if __name__ == "__main__":
    np.random.seed(0)
    random.seed(0)
    A = np.random.randn(50, 2) + [0, 5]
    B = np.random.randn(50, 2) + [5, -2]
    C = np.random.randn(50, 2) + [-4, -2]
    X = np.vstack([A, B, C])

    model = KMeans(k=3)
    labels = model.fit(X)
    print("\nClusters found:")
    for i in range(model.k):
        cx, cy = model.centroids[i]
        n = int(np.sum(labels == i))
        print(f"  Cluster {i}: centre=({cx:.2f}, {cy:.2f})  size={n}")
