"""
Title: Hyperparameter Optimization (Grid Search & Random Search) from Scratch
Author: Lydia S. Makiwa
Date: June 06, 2026

Description:
This program implements hyperparameter tuning from scratch without relying on 
scikit-learn's built-in tuning functions. It builds a simple K-Nearest 
Neighbors (KNN) classifier and compares Grid Search vs. Random Search to find 
the best hyperparameters (number of neighbors, distance metric) for classifying 
a synthetic 2D dataset.

Highly relevant for understanding foundational machine learning engineering.
"""

import numpy as np

# Generate synthetic dataset
np.random.seed(42)
X_train = np.random.randn(120, 2)
y_train = np.array([1 if x[0] + x[1] > 0 else 0 for x in X_train])

X_test = np.random.randn(30, 2)
y_test = np.array([1 if x[0] + x[1] > 0 else 0 for x in X_test])

class KNNScratch:
    def __init__(self, k=3, metric="euclidean"):
        self.k = k
        self.metric = metric
        
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
        
    def _compute_distance(self, x1, x2):
        if self.metric == "euclidean":
            return np.sqrt(np.sum((x1 - x2) ** 2))
        elif self.metric == "manhattan":
            return np.sum(np.abs(x1 - x2))
        return 0.0

    def predict(self, X):
        predictions = []
        for x in X:
            distances = [self._compute_distance(x, x_t) for x_t in self.X_train]
            k_indices = np.argsort(distances)[:self.k]
            k_nearest_labels = [self.y_train[i] for i in k_indices]
            most_common = max(set(k_nearest_labels), key=k_nearest_labels.count)
            predictions.append(most_common)
        return np.array(predictions)

def evaluate_accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)

def run_tuning():
    print("=== Hyperparameter Tuning Demonstration ===")
    
    # Hyperparameter Grid Definition
    k_options = [1, 3, 5, 7, 9, 11]
    metric_options = ["euclidean", "manhattan"]
    
    print("\n--- 1. Grid Search (Evaluating all combinations) ---")
    best_grid_acc = 0
    best_grid_params = None
    
    for k in k_options:
        for metric in metric_options:
            knn = KNNScratch(k=k, metric=metric)
            knn.fit(X_train, y_train)
            preds = knn.predict(X_test)
            acc = evaluate_accuracy(y_test, preds)
            
            print(f"Tried: K={k:2d}, Metric={metric:<10} | Test Accuracy: {acc*100:.2f}%")
            if acc > best_grid_acc:
                best_grid_acc = acc
                best_grid_params = (k, metric)
                
    print(f"==> Best Grid Search Result: Accuracy = {best_grid_acc*100:.2f}% with params K={best_grid_params[0]}, metric={best_grid_params[1]}")
    
    print("\n--- 2. Random Search (Evaluating a random sample) ---")
    # Define hyperparameter distribution
    import random
    random.seed(101)
    
    num_samples = 4
    evaluated_samples = set()
    best_rand_acc = 0
    best_rand_params = None
    
    while len(evaluated_samples) < num_samples:
        k = random.choice(k_options)
        metric = random.choice(metric_options)
        param_pair = (k, metric)
        
        if param_pair not in evaluated_samples:
            evaluated_samples.add(param_pair)
            
            knn = KNNScratch(k=k, metric=metric)
            knn.fit(X_train, y_train)
            preds = knn.predict(X_test)
            acc = evaluate_accuracy(y_test, preds)
            
            print(f"Randomly Sampled: K={k:2d}, Metric={metric:<10} | Test Accuracy: {acc*100:.2f}%")
            if acc > best_rand_acc:
                best_rand_acc = acc
                best_rand_params = param_pair
                
    print(f"==> Best Random Search Result: Accuracy = {best_rand_acc*100:.2f}% with params K={best_rand_params[0]}, metric={best_rand_params[1]}")

if __name__ == "__main__":
    run_tuning()
