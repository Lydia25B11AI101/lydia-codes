# AIML Program 07: Principal Component Analysis (PCA) from Scratch
# Author: Lydia S. Makiwa
# Description: Reduces high-dimensional data to 2D using eigendecomposition
#              Core technique in AIML for visualisation and dimensionality reduction

import numpy as np

class PCA:
    def __init__(self, n_components=2):
        self.n_components  = n_components
        self.components_   = None
        self.mean_         = None
        self.explained_var = None

    def fit(self, X):
        # 1. Centre the data
        self.mean_ = np.mean(X, axis=0)
        X_centred  = X - self.mean_

        # 2. Covariance matrix
        cov = np.cov(X_centred.T)

        # 3. Eigenvalues & eigenvectors
        eigenvalues, eigenvectors = np.linalg.eigh(cov)

        # 4. Sort descending
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues  = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # 5. Keep top n_components
        self.components_   = eigenvectors[:, :self.n_components].T
        total_var          = np.sum(eigenvalues)
        self.explained_var = eigenvalues[:self.n_components] / total_var

        return self

    def transform(self, X):
        return (X - self.mean_) @ self.components_.T

    def fit_transform(self, X):
        return self.fit(X).transform(X)


# Dataset: 4-feature student scores (Math, Science, English, History)
np.random.seed(42)
n = 30
math    = np.random.normal(75, 10, n)
science = math + np.random.normal(0, 5, n)       # correlated with math
english = np.random.normal(70, 12, n)
history = english + np.random.normal(0, 6, n)    # correlated with english
X = np.column_stack([math, science, english, history])

labels = ["AIML"]*10 + ["CS"]*10 + ["Arts"]*10

print("=== PCA — Dimensionality Reduction Demo ===\n")
print(f"Original data shape: {X.shape}  (30 students, 4 subjects)")

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print(f"Reduced data shape:  {X_reduced.shape}  (30 students, 2 components)")
print(f"\nExplained Variance:")
total = 0
for i, var in enumerate(pca.explained_var):
    total += var
    print(f"  PC{i+1}: {var*100:.1f}%  (cumulative: {total*100:.1f}%)")

print(f"\nFirst 5 transformed data points (PC1, PC2):")
for i in range(5):
    print(f"  Student {i+1} [{labels[i]:5}]: PC1={X_reduced[i,0]:7.2f}  PC2={X_reduced[i,1]:7.2f}")

print("\nUse PC1 and PC2 to plot 4D data in 2D — perfect for visualisation!")
