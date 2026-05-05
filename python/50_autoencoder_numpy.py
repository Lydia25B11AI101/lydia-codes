# Program Title: Autoencoder Neural Network (NumPy from Scratch)
# Author: Lydia S. Makiwa
# Date: 2026-05-05
# Description: Builds a simple autoencoder (encoder-decoder) using only NumPy.
#              Autoencoders learn compressed representations — a gateway to
#              dimensionality reduction and generative AI.

import numpy as np

np.random.seed(42)

def sigmoid(x): return 1 / (1 + np.exp(-x))
def sigmoid_d(x): return sigmoid(x) * (1 - sigmoid(x))

class Autoencoder:
    def __init__(self, input_dim, encoding_dim, lr=0.1):
        self.lr = lr
        # Encoder weights
        self.W1 = np.random.randn(input_dim,   encoding_dim) * 0.1
        self.b1 = np.zeros((1, encoding_dim))
        # Decoder weights
        self.W2 = np.random.randn(encoding_dim, input_dim)  * 0.1
        self.b2 = np.zeros((1, input_dim))

    def forward(self, X):
        self.z1     = X @ self.W1 + self.b1
        self.encoded = sigmoid(self.z1)          # compressed representation
        self.z2     = self.encoded @ self.W2 + self.b2
        self.decoded = sigmoid(self.z2)          # reconstruction
        return self.decoded

    def backward(self, X):
        m   = X.shape[0]
        # Reconstruction loss gradient (MSE)
        dL  = (self.decoded - X) * sigmoid_d(self.z2) / m
        dW2 = self.encoded.T @ dL
        db2 = dL.sum(axis=0, keepdims=True)
        dEnc = dL @ self.W2.T * sigmoid_d(self.z1)
        dW1 = X.T @ dEnc
        db1 = dEnc.sum(axis=0, keepdims=True)
        # Update
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2

    def train(self, X, epochs=500):
        for e in range(epochs):
            out  = self.forward(X)
            loss = np.mean((X - out) ** 2)
            self.backward(X)
            if (e+1) % 100 == 0:
                print(f"  Epoch {e+1:4d}  Loss: {loss:.6f}")

# ─── Demo ───
# 8-bit identity encoding challenge
X = np.eye(8)   # 8 different patterns

ae = Autoencoder(input_dim=8, encoding_dim=3, lr=0.5)
print("Training autoencoder (8-dim → 3-dim encoding)...")
ae.train(X, epochs=500)

print("\nEncoded representations (3D bottleneck):")
ae.forward(X)
for i, enc in enumerate(ae.encoded):
    print(f"  Input {i}: {np.round(enc, 3)}")

print("\nReconstruction error per sample:")
for i, (orig, rec) in enumerate(zip(X, ae.decoded)):
    err = np.mean((orig - rec)**2)
    print(f"  Sample {i}: MSE = {err:.6f}")
