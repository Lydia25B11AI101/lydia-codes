# AIML Program 06: Logistic Regression from Scratch
# Author: Lydia S. Makiwa
# Description: Binary classifier using sigmoid + gradient descent
#              Classifies whether a student passes or fails based on study hours & sleep

import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def binary_cross_entropy(y, y_hat):
    eps = 1e-9  # avoid log(0)
    return -np.mean(y * np.log(y_hat + eps) + (1 - y) * np.log(1 - y_hat + eps))

class LogisticRegression:
    def __init__(self, lr=0.1, epochs=1000):
        self.lr     = lr
        self.epochs = epochs
        self.W = None
        self.b = 0.0

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.W = np.zeros(n_features)

        for epoch in range(self.epochs):
            z      = X @ self.W + self.b
            y_hat  = sigmoid(z)
            loss   = binary_cross_entropy(y, y_hat)

            dW = (1/n_samples) * X.T @ (y_hat - y)
            db = (1/n_samples) * np.sum(y_hat - y)
            self.W -= self.lr * dW
            self.b -= self.lr * db

            if epoch % 200 == 0:
                print(f"  Epoch {epoch:5d} | Loss: {loss:.4f}")

    def predict_proba(self, X):
        return sigmoid(X @ self.W + self.b)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)

    def accuracy(self, X, y):
        return np.mean(self.predict(X) == y)


# Dataset: [study_hours, sleep_hours] → 0=Fail, 1=Pass
X = np.array([
    [1, 3], [2, 4], [2, 3], [3, 5], [4, 5],
    [5, 6], [6, 7], [7, 7], [8, 8], [9, 8],
    [10,9], [3, 4], [4, 4], [5, 5], [6, 6],
], dtype=float)
y = np.array([0,0,0,0,0, 0,1,1,1,1, 1,0,0,1,1], dtype=float)

# Normalise
X = (X - X.mean(axis=0)) / X.std(axis=0)

print("=== Logistic Regression — Pass/Fail Predictor ===\n")
model = LogisticRegression(lr=0.5, epochs=1001)
model.fit(X, y)

print(f"\nTraining Accuracy: {model.accuracy(X, y)*100:.1f}%")
print(f"Weights: {model.W.round(3)} | Bias: {model.b:.3f}")

print("\nPredictions on new students:")
tests_raw = np.array([[2,3],[5,6],[8,8],[3,4],[9,9]], dtype=float)
tests_norm = (tests_raw - np.array([5.2, 5.73])) / np.array([2.67, 1.87])
for (hrs, slp), prob in zip(tests_raw, model.predict_proba(tests_norm)):
    verdict = "✅ Pass" if prob >= 0.5 else "❌ Fail"
    print(f"  Study={hrs:.0f}h Sleep={slp:.0f}h → P(pass)={prob:.2f} → {verdict}")
