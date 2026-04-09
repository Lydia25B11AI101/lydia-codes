# AIML Program 02: K-Means Clustering (from scratch)
# Author: Lydia S. Makiwa
# Description: Groups data into K clusters without labels (unsupervised)

import numpy as np
import random

class KMeans:
    def __init__(self, k=3, max_iters=100):
        self.k = k
        self.max_iters = max_iters

    def fit(self, X):
        X = np.array(X)
        # Random initialisation
        idx = random.sample(range(len(X)), self.k)
        self.centroids = X[idx].astype(float)

        for iteration in range(self.max_iters):
            # Assign clusters
            clusters = [[] for _ in range(self.k)]
            labels = []
            for point in X:
                dists = [np.linalg.norm(point - c) for c in self.centroids]
                cluster = np.argmin(dists)
                clusters[cluster].append(point)
                labels.append(cluster)

            # Update centroids
            new_centroids = []
            for i, cluster in enumerate(clusters):
                if cluster:
                    new_centroids.append(np.mean(cluster, axis=0))
                else:
                    new_centroids.append(self.centroids[i])
            new_centroids = np.array(new_centroids)

            if np.allclose(self.centroids, new_centroids):
                print(f"  Converged at iteration {iteration+1}")
                break
            self.centroids = new_centroids

        self.labels_ = labels
        return self

    def predict(self, X):
        return [np.argmin([np.linalg.norm(p - c) for c in self.centroids])
                for p in np.array(X)]


# Demo — cluster student marks into 3 groups
np.random.seed(42)
group_A = np.random.normal(loc=85, scale=5, size=(15, 2))  # High performers
group_B = np.random.normal(loc=65, scale=5, size=(15, 2))  # Average
group_C = np.random.normal(loc=45, scale=5, size=(15, 2))  # Struggling
data = np.vstack([group_A, group_B, group_C])

print("=== K-Means Clustering Demo ===\n")
km = KMeans(k=3)
km.fit(data)

cluster_names = {0: "Group A", 1: "Group B", 2: "Group C"}
counts = {0: 0, 1: 0, 2: 0}
for label in km.labels_:
    counts[label] += 1

print("Cluster centroids (Math Score, Science Score):")
for i, c in enumerate(km.centroids):
    print(f"  Cluster {i+1}: Math={c[0]:.1f}, Science={c[1]:.1f} ({counts[i]} students)")
