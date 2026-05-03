# ============================================================
# Program Title : Decision Tree Classifier
# Author        : Lydia S. Makiwa
# Date          : 2026-05-03
# Description   : Train & visualise a Decision Tree on the Iris
#                 dataset using scikit-learn — a core AIML skill.
# ============================================================

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ── Load dataset ──────────────────────────────────────────────
iris = load_iris()
X, y = iris.data, iris.target
labels = iris.target_names          # ['setosa', 'versicolor', 'virginica']

# ── Split into train / test (80/20) ───────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Build & train the tree ─────────────────────────────────────
clf = DecisionTreeClassifier(max_depth=4, random_state=42)
clf.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────────
y_pred = clf.predict(X_test)
print("Decision Tree Classifier – Iris Dataset")
print("=" * 45)
print(f"Accuracy : {accuracy_score(y_test, y_pred):.2%}")
print()
print(classification_report(y_test, y_pred, target_names=labels))

# ── Print ASCII tree ──────────────────────────────────────────
print("Tree Structure (max_depth=4):")
print(export_text(clf, feature_names=list(iris.feature_names)))

# ── Predict a new sample ──────────────────────────────────────
sample = [[5.1, 3.5, 1.4, 0.2]]   # likely Setosa
pred   = clf.predict(sample)
print(f"Sample {sample[0]} → Predicted: {labels[pred[0]]}")
