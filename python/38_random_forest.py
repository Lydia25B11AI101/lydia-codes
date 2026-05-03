# ============================================================
# Program Title : Random Forest Classifier
# Author        : Lydia S. Makiwa
# Date          : 2026-05-03
# Description   : Ensemble learning with Random Forest on the
#                 Wine dataset — compare with single Decision Tree.
# ============================================================

from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
import numpy as np

wine = load_wine()
X, y = wine.data, wine.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=7
)

# ── Train both models ─────────────────────────────────────────
dt  = DecisionTreeClassifier(random_state=7)
rf  = RandomForestClassifier(n_estimators=100, random_state=7)

dt.fit(X_train, y_train)
rf.fit(X_train, y_train)

# ── Compare accuracy ──────────────────────────────────────────
dt_acc = accuracy_score(y_test, dt.predict(X_test))
rf_acc = accuracy_score(y_test, rf.predict(X_test))

print("Random Forest vs Decision Tree – Wine Dataset")
print("=" * 48)
print(f"Decision Tree accuracy : {dt_acc:.2%}")
print(f"Random Forest accuracy : {rf_acc:.2%}")

# ── 5-fold cross-validation ───────────────────────────────────
rf_cv = cross_val_score(rf, X, y, cv=5)
print(f"\nRF 5-fold CV mean: {rf_cv.mean():.2%} ± {rf_cv.std():.2%}")

# ── Feature importances ───────────────────────────────────────
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]
print("\nTop 5 most important features:")
for rank, idx in enumerate(indices[:5], 1):
    print(f"  {rank}. {wine.feature_names[idx]:30s} {importances[idx]:.4f}")
