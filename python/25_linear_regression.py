# Python Program 25: Simple Linear Regression (from scratch)
# Author: Lydia S. Makiwa
# Description: Implements linear regression without scikit-learn — core AIML concept

import numpy as np

class LinearRegression:
    """Simple linear regression using gradient descent."""

    def __init__(self, lr=0.01, epochs=1000):
        self.lr     = lr
        self.epochs = epochs
        self.m = self.b = 0  # slope and intercept

    def fit(self, X, y):
        n = len(X)
        for epoch in range(self.epochs):
            y_pred = self.m * X + self.b
            loss   = np.mean((y_pred - y) ** 2)
            dm = (2/n) * np.sum((y_pred - y) * X)
            db = (2/n) * np.sum(y_pred - y)
            self.m -= self.lr * dm
            self.b -= self.lr * db
            if epoch % 200 == 0:
                print(f"  Epoch {epoch:4d} | Loss: {loss:.4f} | m={self.m:.3f} b={self.b:.3f}")

    def predict(self, X):
        return self.m * X + self.b

    def r_squared(self, X, y):
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - ss_res / ss_tot


# Dataset: Study hours → Exam score
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
y = np.array([52, 58, 62, 68, 75, 79, 85, 88, 92, 96], dtype=float)

# Normalise X
X_norm = (X - X.mean()) / X.std()

model = LinearRegression(lr=0.1, epochs=1000)
print("Training LinearRegression...\n")
model.fit(X_norm, y)

r2 = model.r_squared(X_norm, y)
print(f"\nR² Score: {r2:.4f} ({'Excellent' if r2 > 0.95 else 'Good' if r2 > 0.8 else 'Fair'})")
print(f"\nPredictions:")
for hrs in [3, 5, 8, 10]:
    x_n = (hrs - X.mean()) / X.std()
    pred = model.predict(x_n)
    print(f"  {hrs} study hours → predicted score: {pred:.1f}")
