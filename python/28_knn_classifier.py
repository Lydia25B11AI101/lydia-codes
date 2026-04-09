# ============================================================
# Program Title : K-Nearest Neighbours Classifier (from scratch)
# Author        : Lydia S. Makiwa
# Date          : 2026-04-09
# Description   : Implements KNN using only numpy.
#                 Covers: distance metrics, majority vote, accuracy.
# ============================================================

import numpy as np
from collections import Counter

def euclidean_distance(a, b):
    """Euclidean distance between two 1-D vectors."""
    return np.sqrt(np.sum((np.array(a) - np.array(b)) ** 2))

class KNNClassifier:
    def __init__(self, k=3):
        self.k = k
        self.X_train = []
        self.y_train = []

    def fit(self, X, y):
        """Store training data — KNN is a lazy learner."""
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        return [self._predict_one(x) for x in X]

    def _predict_one(self, x):
        distances = [euclidean_distance(x, xt) for xt in self.X_train]
        k_indices = np.argsort(distances)[:self.k]
        k_labels  = [self.y_train[i] for i in k_indices]
        return Counter(k_labels).most_common(1)[0][0]

    def accuracy(self, X_test, y_test):
        preds = self.predict(X_test)
        return sum(p == t for p, t in zip(preds, y_test)) / len(y_test) * 100

# -- Demo --------------------------------------------------
if __name__ == "__main__":
    X_train = [
        [1.4, 0.2], [1.5, 0.1], [1.7, 0.3],
        [4.7, 1.4], [4.5, 1.5], [4.9, 1.5],
        [6.3, 1.8], [5.8, 1.6], [7.1, 1.8],
    ]
    y_train = ["setosa"]*3 + ["versicolor"]*3 + ["virginica"]*3
    X_test  = [[1.6, 0.2], [4.8, 1.4], [6.5, 1.9]]
    y_test  = ["setosa", "versicolor", "virginica"]

    knn = KNNClassifier(k=3)
    knn.fit(X_train, y_train)
    preds = knn.predict(X_test)

    print("KNN Predictions:")
    for sample, pred, actual in zip(X_test, preds, y_test):
        mark = "OK" if pred == actual else "XX"
        print(f"  [{mark}]  {sample}  ->  Predicted: {pred}  Actual: {actual}")
    print(f"Accuracy: {knn.accuracy(X_test, y_test):.1f}%")
