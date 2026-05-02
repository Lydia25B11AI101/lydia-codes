# ============================================================
# Program Title : Neural Network (2-layer) from Scratch
# Author        : Lydia S. Makiwa
# Date          : 2026-05-02
# Description   : Builds a feedforward neural network with one
#                 hidden layer; trains on XOR using backprop.
# ============================================================

import numpy as np

def sigmoid(z):   return 1 / (1 + np.exp(-z))
def relu(z):      return np.maximum(0, z)
def relu_d(z):    return (z > 0).astype(float)

class NeuralNet:
    def __init__(self, layer_sizes, lr=0.1):
        self.lr = lr
        np.random.seed(1)
        self.W, self.b = [], []
        for i in range(len(layer_sizes)-1):
            ni, no = layer_sizes[i], layer_sizes[i+1]
            self.W.append(np.random.randn(ni, no) * np.sqrt(2/ni))
            self.b.append(np.zeros((1, no)))

    def forward(self, X):
        self.cache = [X]
        A = X
        for i, (w, b) in enumerate(zip(self.W, self.b)):
            Z = A @ w + b
            A = sigmoid(Z) if i == len(self.W)-1 else relu(Z)
            self.cache.append(A)
        return A

    def loss(self, y_hat, y):
        eps = 1e-8
        return -np.mean(y*np.log(y_hat+eps) + (1-y)*np.log(1-y_hat+eps))

    def backward(self, y):
        m  = y.shape[0]
        dA = self.cache[-1] - y
        for i in reversed(range(len(self.W))):
            A_prev = self.cache[i]
            dW = (A_prev.T @ dA) / m
            db = dA.mean(axis=0, keepdims=True)
            if i > 0:
                dA = (dA @ self.W[i].T) * relu_d(self.cache[i])
            self.W[i] -= self.lr * dW
            self.b[i] -= self.lr * db

    def fit(self, X, y, epochs=5000):
        for ep in range(1, epochs+1):
            y_hat = self.forward(X)
            self.backward(y)
            if ep % 1000 == 0:
                print(f'  Epoch {ep:>5d}  Loss: {self.loss(y_hat, y):.4f}')

    def predict(self, X, thr=0.5):
        return (self.forward(X) >= thr).astype(int)


# -- Demo: learn XOR -------------------------------------------
if __name__ == '__main__':
    X = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
    y = np.array([[0],[1],[1],[0]],         dtype=float)

    net = NeuralNet([2, 4, 1], lr=0.5)
    print('Training on XOR problem...\n')
    net.fit(X, y, epochs=5000)

    print('\nPredictions after training:')
    preds = net.predict(X)
    for xi, yi, pi in zip(X, y, preds):
        print(f'  {xi} -> true={int(yi[0])} pred={pi[0]}')
