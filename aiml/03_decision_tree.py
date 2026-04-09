# AIML Program 03: Decision Tree Classifier (from scratch)
# Author: Lydia S. Makiwa
# Description: Builds a simple decision tree using Gini impurity

import numpy as np
from collections import Counter

def gini(y):
    counts = Counter(y)
    total = len(y)
    return 1 - sum((c/total)**2 for c in counts.values())

def best_split(X, y):
    best_gain, best_feat, best_thresh = 0, None, None
    parent_gini = gini(y)
    n, n_feats = len(y), X.shape[1]

    for feat in range(n_feats):
        thresholds = np.unique(X[:, feat])
        for thresh in thresholds:
            left  = y[X[:, feat] <= thresh]
            right = y[X[:, feat] >  thresh]
            if len(left) == 0 or len(right) == 0:
                continue
            gain = parent_gini - (len(left)/n)*gini(left) - (len(right)/n)*gini(right)
            if gain > best_gain:
                best_gain, best_feat, best_thresh = gain, feat, thresh

    return best_feat, best_thresh

class DecisionTree:
    def __init__(self, max_depth=4, min_samples=2):
        self.max_depth   = max_depth
        self.min_samples = min_samples

    def fit(self, X, y):
        self.tree = self._build(np.array(X), np.array(y), 0)

    def _build(self, X, y, depth):
        if depth >= self.max_depth or len(y) < self.min_samples or len(set(y)) == 1:
            return Counter(y).most_common(1)[0][0]
        feat, thresh = best_split(X, y)
        if feat is None:
            return Counter(y).most_common(1)[0][0]
        left_mask  = X[:, feat] <= thresh
        right_mask = ~left_mask
        return {
            "feat": feat, "thresh": thresh,
            "left":  self._build(X[left_mask],  y[left_mask],  depth+1),
            "right": self._build(X[right_mask], y[right_mask], depth+1),
        }

    def _predict_one(self, x, node):
        if not isinstance(node, dict):
            return node
        if x[node["feat"]] <= node["thresh"]:
            return self._predict_one(x, node["left"])
        return self._predict_one(x, node["right"])

    def predict(self, X):
        return [self._predict_one(x, self.tree) for x in np.array(X)]

    def accuracy(self, X, y):
        return sum(p == t for p, t in zip(self.predict(X), y)) / len(y)


# Dataset: [study_hours, sleep_hours] → Pass/Fail
X = np.array([[8,7],[6,6],[2,4],[9,8],[1,3],[7,7],[3,5],
              [5,6],[4,4],[10,9],[2,3],[6,7],[8,6],[1,4],[7,8]])
y = np.array(["Pass","Pass","Fail","Pass","Fail","Pass","Fail",
              "Pass","Fail","Pass","Fail","Pass","Pass","Fail","Pass"])

dt = DecisionTree(max_depth=3)
dt.fit(X, y)

print("=== Decision Tree Classifier ===\n")
print(f"Training Accuracy: {dt.accuracy(X, y)*100:.1f}%\n")
print("Predictions:")
tests = [[7, 7], [2, 3], [9, 8], [3, 4]]
for t in tests:
    pred = dt._predict_one(np.array(t), dt.tree)
    print(f"  Study={t[0]}h Sleep={t[1]}h → {pred}")
