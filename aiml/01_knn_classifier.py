# AIML Program 01: K-Nearest Neighbours (KNN) Classifier
# Author: Lydia S. Makiwa
# Description: Implements KNN from scratch to classify data points

import numpy as np
from collections import Counter

class KNNClassifier:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def _euclidean(self, a, b):
        return np.sqrt(np.sum((a - b) ** 2))

    def predict_one(self, x):
        distances = [(self._euclidean(x, xt), yt)
                     for xt, yt in zip(self.X_train, self.y_train)]
        k_nearest = sorted(distances, key=lambda d: d[0])[:self.k]
        labels = [label for _, label in k_nearest]
        return Counter(labels).most_common(1)[0][0]

    def predict(self, X):
        return [self.predict_one(x) for x in np.array(X)]

    def accuracy(self, X, y):
        preds = self.predict(X)
        return sum(p == t for p, t in zip(preds, y)) / len(y)


# Dataset: [height_cm, weight_kg] → body type
X_train = [
    [150, 45], [160, 55], [170, 65], [180, 75], [190, 90],
    [155, 80], [165, 85], [175, 95], [185, 105],[145, 40],
]
y_train = ["Slim","Slim","Normal","Normal","Athletic",
           "Heavy","Heavy","Heavy","Heavy","Slim"]

knn = KNNClassifier(k=3)
knn.fit(X_train, y_train)

test = [[162, 58], [172, 90], [180, 80]]
print("=== KNN Classifier Demo ===\n")
print(f"{'Height':>8} {'Weight':>8} {'Prediction':>12}")
print("-" * 32)
for point in test:
    pred = knn.predict_one(np.array(point))
    print(f"{point[0]:>8}cm {point[1]:>6}kg {pred:>12}")

acc = knn.accuracy(X_train, y_train)
print(f"\nTraining Accuracy: {acc*100:.1f}%")
print(f"K value used: {knn.k}")
