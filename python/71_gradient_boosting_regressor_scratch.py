"""
Program: Gradient Boosting Regressor from Scratch
Author: Lydia S. Makiwa
Date: June 7, 2026
Category: AIML / Python Basics

Description:
This program implements a basic Gradient Boosting Regressor from scratch. It uses 
simple Decision Stumps (1-level decision trees) as base estimators. The algorithm
sequentially builds trees to fit the pseudo-residuals (negative gradients) of 
the loss function (Mean Squared Error), gradually refining overall predictions.
"""
import numpy as np

class DecisionStump:
    """A 1-level decision tree (stump) for regression"""
    def __init__(self):
        self.feature_idx = None
        self.threshold = None
        self.left_value = None
        self.right_value = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        best_mse = float('inf')
        
        # Loop over features and unique split values
        for feat in range(n_features):
            thresholds = np.unique(X[:, feat])
            for threshold in thresholds:
                left_mask = X[:, feat] <= threshold
                right_mask = ~left_mask
                
                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue
                
                # Predict the mean value of targets in each partition
                left_mean = np.mean(y[left_mask])
                right_mean = np.mean(y[right_mask])
                
                # Calculate Mean Squared Error
                y_pred = np.where(left_mask, left_mean, right_mean)
                mse = np.mean((y - y_pred) ** 2)
                
                if mse < best_mse:
                    best_mse = mse
                    self.feature_idx = feat
                    self.threshold = threshold
                    self.left_value = left_mean
                    self.right_value = right_mean

    def predict(self, X):
        left_mask = X[:, self.feature_idx] <= self.threshold
        return np.where(left_mask, self.left_value, self.right_value)


class GradientBoostingRegressorScratch:
    def __init__(self, n_estimators=100, learning_rate=0.1):
        """
        n_estimators: Number of boosting stages (trees)
        learning_rate: Shrinkage parameter to prevent overfitting
        """
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.estimators = []
        self.initial_prediction = None

    def fit(self, X, y):
        # Step 1: Initialize model with a constant prediction (mean of y)
        self.initial_prediction = np.mean(y)
        y_pred = np.full(y.shape, self.initial_prediction, dtype=np.float64)

        # Step 2: Iteratively fit base estimators to residuals
        for i in range(self.n_estimators):
            # Compute pseudo-residuals (negative gradient of MSE loss)
            residuals = y - y_pred
            
            # Fit a decision stump on the residuals
            stump = DecisionStump()
            stump.fit(X, residuals)
            
            # Update predictions
            y_pred += self.learning_rate * stump.predict(X)
            
            # Save the estimator
            self.estimators.append(stump)

    def predict(self, X):
        # Start with the initial constant prediction
        y_pred = np.full(X.shape[0], self.initial_prediction, dtype=np.float64)
        # Add contributions of each booster multiplied by learning rate
        for stump in self.estimators:
            y_pred += self.learning_rate * stump.predict(X)
        return y_pred


# Demo / Working Example
if __name__ == "__main__":
    print("=== Gradient Boosting Regressor from Scratch ===")
    
    # Generate synthetic 1D quadratic data (with noise)
    np.random.seed(42)
    X = np.random.uniform(-3, 3, size=(100, 1))
    # Quadratic curve: y = 0.5 * x^2 + x + 2 + noise
    y = (0.5 * X[:, 0]**2 + X[:, 0] + 2 + np.random.normal(0, 0.5, size=100))

    # Initialize and fit Gradient Boosting Regressor
    gbr = GradientBoostingRegressorScratch(n_estimators=50, learning_rate=0.1)
    gbr.fit(X, y)

    # Make predictions
    X_test = np.linspace(-3, 3, 10).reshape(-1, 1)
    y_test_true = 0.5 * X_test[:, 0]**2 + X_test[:, 0] + 2
    y_pred = gbr.predict(X_test)

    print("\nModel trained successfully. Comparing Predictions on Test Points:")
    print(f"{'X Value':^10} | {'True y (no noise)':^20} | {'Predicted y':^20}")
    print("-" * 58)
    for i in range(len(X_test)):
        print(f"{X_test[i, 0]:^10.2f} | {y_test_true[i]:^20.4f} | {y_pred[i]:^20.4f}")

    mse = np.mean((y_test_true - y_pred) ** 2)
    print(f"\nMean Squared Error on clean test curve: {mse:.4f}")
