# ============================================================
# Program Title : Logistic Regression from Scratch
# Author        : Lydia S. Makiwa
# Date          : 2026-05-02
# Description   : Implements logistic regression using only NumPy
#                 -- core concept for binary classification in ML.
# ============================================================

import numpy as np

class LogisticRegression:
    def __init__(self, lr=0.2, epochs=800):
        self.lr = lr
        self.epochs = epochs
        self.w = None
        self.b = 0.0

    def _sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -250, 250)))

    def fit(self, X, y):
        n, f = X.shape
        self.w = np.zeros(f)
        for ep in range(self.epochs):
            y_hat = self._sigmoid(X @ self.w + self.b)
            self.w -= self.lr * (X.T @ (y_hat - y)) / n
            self.b -= self.lr * np.mean(y_hat - y)
            if ep % 200 == 0:
                loss = -np.mean(y*np.log(y_hat+1e-8) + (1-y)*np.log(1-y_hat+1e-8))
                print(f"  Epoch {ep:>4d}  Loss: {loss:.4f}")

    def predict(self, X, thr=0.5):
        return (self._sigmoid(X @ self.w + self.b) >= thr).astype(int)

    def accuracy(self, X, y):
        return np.mean(self.predict(X) == y)


# -- Demo ------------------------------------------------------
if __name__ == "__main__":
    np.random.seed(42)
    X0 = np.random.randn(100, 2) - 1
    X1 = np.random.randn(100, 2) + 1
    X  = np.vstack([X0, X1])
    y  = np.array([0]*100 + [1]*100, dtype=float)

    model = LogisticRegression()
    print("Training logistic regression...\n")
    model.fit(X, y)
    print(f"\nTraining accuracy: {model.accuracy(X, y)*100:.1f}%")
    print(f"Predict [1.5,1.5] -> class {model.predict(np.array([[1.5,1.5]]))[0]}")
