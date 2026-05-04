# ============================================================
# Program Title : Naive Bayes Classifier from Scratch
# Author        : Lydia S. Makiwa
# Date          : 2026-05-04
# Description   : Implement Gaussian Naive Bayes without
#                 sklearn, then apply it to the Iris dataset.
# ============================================================

import numpy as np

class GaussianNaiveBayes:
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.means   = {}
        self.stds    = {}
        self.priors  = {}
        for c in self.classes:
            Xc = X[y == c]
            self.means[c]  = Xc.mean(axis=0)
            self.stds[c]   = Xc.std(axis=0) + 1e-9
            self.priors[c] = len(Xc) / len(y)

    def _likelihood(self, x, mean, std):
        exponent = np.exp(-((x-mean)**2) / (2*std**2))
        return (1 / (np.sqrt(2*np.pi) * std)) * exponent

    def predict(self, X):
        preds = []
        for x in X:
            posteriors = {}
            for c in self.classes:
                log_prior = np.log(self.priors[c])
                log_like  = np.sum(np.log(self._likelihood(x, self.means[c], self.stds[c])))
                posteriors[c] = log_prior + log_like
            preds.append(max(posteriors, key=posteriors.get))
        return np.array(preds)

# Iris dataset (4 features, 3 classes, 150 samples)
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X, y = iris.data, iris.target
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)

gnb = GaussianNaiveBayes()
gnb.fit(X_tr, y_tr)
preds = gnb.predict(X_te)
acc   = np.mean(preds == y_te) * 100

print(f'Test Accuracy: {acc:.1f}%')
print('Class names:', iris.target_names.tolist())
print('Sample predictions:', [iris.target_names[p] for p in preds[:5]])
print('Actual labels:     ', [iris.target_names[t] for t in y_te[:5]])
print('Naive Bayes from scratch complete!')
