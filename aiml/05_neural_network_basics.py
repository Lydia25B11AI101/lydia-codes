# AIML Program 05: Neural Network from Scratch
# Author: Lydia S. Makiwa
# Description: Simple 2-layer neural network — forward pass, backprop, sigmoid

import numpy as np

def sigmoid(x):       return 1 / (1 + np.exp(-x))
def sigmoid_deriv(x): return sigmoid(x) * (1 - sigmoid(x))

class NeuralNetwork:
    """Simple neural network: input → hidden → output"""

    def __init__(self, input_size, hidden_size, output_size, lr=0.1):
        np.random.seed(42)
        self.lr = lr
        # Xavier initialisation
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2 / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2 / hidden_size)
        self.b2 = np.zeros((1, output_size))

    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = sigmoid(self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = sigmoid(self.z2)
        return self.a2

    def backward(self, X, y):
        m = len(X)
        dz2 = self.a2 - y
        dW2 = self.a1.T @ dz2 / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m
        dz1 = (dz2 @ self.W2.T) * sigmoid_deriv(self.z1)
        dW1 = X.T @ dz1 / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1

    def train(self, X, y, epochs=1000):
        for epoch in range(epochs):
            output = self.forward(X)
            loss   = np.mean((y - output) ** 2)
            self.backward(X, y)
            if epoch % 200 == 0:
                print(f"  Epoch {epoch:5d} | Loss: {loss:.6f}")

    def predict(self, X):
        return (self.forward(X) > 0.5).astype(int)


# XOR problem — classic NN test
X = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
y = np.array([[0],[1],[1],[0]], dtype=float)   # XOR truth table

print("=== Neural Network — XOR Problem ===\n")
nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1, lr=0.5)
nn.train(X, y, epochs=1001)

print("\nPredictions:")
preds = nn.predict(X)
print(f"  {'Input':>10} {'Expected':>10} {'Predicted':>10} {'Correct':>10}")
print("  " + "-" * 44)
for xi, yi, pi in zip(X, y, preds):
    correct = "✅" if yi[0] == pi[0] else "❌"
    print(f"  {str(xi.astype(int)):>10} {str(int(yi[0])):>10} {str(pi[0]):>10} {correct:>10}")
acc = np.mean(preds == y.astype(int)) * 100
print(f"\nAccuracy: {acc:.0f}%")
