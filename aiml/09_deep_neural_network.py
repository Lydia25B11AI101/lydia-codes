# AIML Program 09: Deep Neural Network (Multi-Layer) from Scratch
# Author: Lydia S. Makiwa
# Description: Implements a fully connected deep neural network with:
#              - Multiple hidden layers
#              - ReLU + Sigmoid activations
#              - Backpropagation
#              - Mini-batch gradient descent
#              Trained to classify students into performance tiers

import numpy as np

# ── Activation Functions ──────────────────────────────────
def relu(z):          return np.maximum(0, z)
def relu_deriv(z):    return (z > 0).astype(float)
def sigmoid(z):       return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
def sigmoid_deriv(z): return sigmoid(z) * (1 - sigmoid(z))
def softmax(z):
    e = np.exp(z - np.max(z, axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)

def cross_entropy_loss(y_hat, y):
    m = y.shape[0]
    log_p = -np.log(y_hat[range(m), y.argmax(axis=1)] + 1e-9)
    return np.mean(log_p)

# ── Deep Neural Network Class ─────────────────────────────
class DeepNeuralNetwork:
    """
    Architecture: input → [hidden layers with ReLU] → output with Softmax
    """
    def __init__(self, layer_sizes, lr=0.01):
        self.lr     = lr
        self.layers = layer_sizes
        self.params = {}
        np.random.seed(42)

        for l in range(1, len(layer_sizes)):
            n_in  = layer_sizes[l-1]
            n_out = layer_sizes[l]
            # He initialisation for ReLU layers
            self.params[f"W{l}"] = np.random.randn(n_in, n_out) * np.sqrt(2/n_in)
            self.params[f"b{l}"] = np.zeros((1, n_out))

    def forward(self, X):
        self.cache = {"A0": X}
        A = X
        L = len(self.layers) - 1

        for l in range(1, L):           # Hidden layers → ReLU
            Z = A @ self.params[f"W{l}"] + self.params[f"b{l}"]
            A = relu(Z)
            self.cache[f"Z{l}"] = Z
            self.cache[f"A{l}"] = A

        # Output layer → Softmax
        Z = A @ self.params[f"W{L}"] + self.params[f"b{L}"]
        A = softmax(Z)
        self.cache[f"Z{L}"] = Z
        self.cache[f"A{L}"] = A
        return A

    def backward(self, y):
        m = y.shape[0]
        L = len(self.layers) - 1
        grads = {}

        # Output layer gradient
        dZ = self.cache[f"A{L}"] - y
        grads[f"dW{L}"] = self.cache[f"A{L-1}"].T @ dZ / m
        grads[f"db{L}"] = dZ.mean(axis=0, keepdims=True)

        # Hidden layer gradients (backprop)
        for l in range(L-1, 0, -1):
            dA  = dZ @ self.params[f"W{l+1}"].T
            dZ  = dA * relu_deriv(self.cache[f"Z{l}"])
            grads[f"dW{l}"] = self.cache[f"A{l-1}"].T @ dZ / m
            grads[f"db{l}"] = dZ.mean(axis=0, keepdims=True)

        # Update weights
        for l in range(1, L+1):
            self.params[f"W{l}"] -= self.lr * grads[f"dW{l}"]
            self.params[f"b{l}"] -= self.lr * grads[f"db{l}"]

    def train(self, X, y, epochs=2000, batch_size=16):
        m = X.shape[0]
        history = []
        for epoch in range(epochs):
            # Mini-batch
            idx = np.random.permutation(m)
            X_s, y_s = X[idx], y[idx]
            for start in range(0, m, batch_size):
                Xb = X_s[start:start+batch_size]
                yb = y_s[start:start+batch_size]
                self.forward(Xb)
                self.backward(yb)

            if epoch % 400 == 0:
                y_hat = self.forward(X)
                loss  = cross_entropy_loss(y_hat, y)
                acc   = self.accuracy(X, y)
                history.append((epoch, loss, acc))
                print(f"  Epoch {epoch:5d} | Loss: {loss:.4f} | Acc: {acc*100:.1f}%")
        return history

    def predict(self, X):
        y_hat = self.forward(X)
        return np.argmax(y_hat, axis=1)

    def accuracy(self, X, y):
        return np.mean(self.predict(X) == np.argmax(y, axis=1))


# ── Dataset: Student features → Performance tier ──────────
# Features: [study_hours, sleep_hours, assignments_done%, attendance%]
# Classes:  0=Struggling  1=Average  2=High Performer
np.random.seed(0)

def make_students(n, study_mu, sleep_mu, assign_mu, attend_mu, label):
    X = np.column_stack([
        np.random.normal(study_mu,  1.0, n),
        np.random.normal(sleep_mu,  0.8, n),
        np.random.normal(assign_mu, 5.0, n),
        np.random.normal(attend_mu, 5.0, n),
    ])
    y = np.full(n, label)
    return X, y

X0, y0 = make_students(40, study_mu=2, sleep_mu=4, assign_mu=50, attend_mu=60, label=0)
X1, y1 = make_students(40, study_mu=5, sleep_mu=6, assign_mu=75, attend_mu=80, label=1)
X2, y2 = make_students(40, study_mu=9, sleep_mu=8, assign_mu=95, attend_mu=95, label=2)

X_raw = np.vstack([X0, X1, X2])
y_raw = np.concatenate([y0, y1, y2])

# Normalise
X = (X_raw - X_raw.mean(axis=0)) / X_raw.std(axis=0)

# One-hot encode labels
n_classes = 3
Y = np.eye(n_classes)[y_raw.astype(int)]

# Shuffle
idx = np.random.permutation(len(X))
X, Y = X[idx], Y[idx]

print("=== Deep Neural Network — Student Performance Classifier ===")
print(f"Architecture: 4 → 16 → 8 → 3  (input → hidden → hidden → output)")
print(f"Dataset: {len(X)} students, 4 features, 3 classes\n")

dnn = DeepNeuralNetwork(layer_sizes=[4, 16, 8, 3], lr=0.05)
dnn.train(X, Y, epochs=2001, batch_size=20)

print(f"\nFinal Training Accuracy: {dnn.accuracy(X, Y)*100:.1f}%")

print("\nSample Predictions:")
class_names = ["Struggling", "Average", "High Performer"]
features = ["Study hrs", "Sleep hrs", "Assignments%", "Attendance%"]
test_raw = np.array([
    [2, 4, 48, 58],
    [5, 6, 77, 82],
    [9, 8, 96, 97],
    [3, 5, 60, 70],
])
test_norm = (test_raw - X_raw.mean(axis=0)) / X_raw.std(axis=0)
preds = dnn.predict(test_norm)
for i, (row, pred) in enumerate(zip(test_raw, preds)):
    print(f"  Student {i+1}: Study={row[0]}h Sleep={row[1]}h "
          f"Assign={row[2]}% Attend={row[3]}% → {class_names[pred]}")
