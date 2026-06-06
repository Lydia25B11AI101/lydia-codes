"""
Title: Outlier and Anomaly Detection using Isolation Forest
Author: Lydia S. Makiwa
Date: June 06, 2026

Description:
This program implements a complete workflow for anomaly detection using the 
Isolation Forest algorithm. It demonstrates how to generate synthetic 2D data
containing inliers (normal instances) and outliers (anomalies), fit an 
Isolation Forest model using scikit-learn, evaluate anomaly scores, and 
visualize/analyze the results.

This is highly useful for AIML applications such as fraud detection, network 
intrusion detection, and equipment failure forecasting.
"""

import numpy as np
from sklearn.ensemble import IsolationForest

def generate_sensor_data():
    """Generates synthetic multi-dimensional normal sensor data and some anomalies."""
    np.random.seed(42)
    
    # Generate normal data points (inliers)
    normal_data = np.random.normal(loc=10.0, scale=1.5, size=(100, 2))
    
    # Generate anomalous data points (outliers)
    anomalous_data = np.random.uniform(low=0.0, high=25.0, size=(10, 2))
    # Ensure they are actually outliers by filtering out points close to normal mean
    anomalous_data = anomalous_data[np.linalg.norm(anomalous_data - 10.0, axis=1) > 4.0]
    
    # Combine the datasets
    X = np.vstack([normal_data, anomalous_data])
    
    # Create true labels (1 for normal, -1 for anomaly)
    y_true = np.array([1] * len(normal_data) + [-1] * len(anomalous_data))
    
    return X, y_true

def run_anomaly_detection():
    print("=== Isolation Forest Anomaly Detection ===")
    
    # 1. Generate synthetic data
    X, y_true = generate_sensor_data()
    print(f"Generated {X.shape[0]} samples (Normal: {np.sum(y_true == 1)}, Anomalies: {np.sum(y_true == -1)})")
    
    # 2. Instantiate and fit Isolation Forest
    # contamination=0.1 means we expect roughly 10% of the dataset to be anomalies
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    iso_forest.fit(X)
    
    # 3. Predict anomalies (1 for inliers, -1 for outliers)
    y_pred = iso_forest.predict(X)
    
    # 4. Compute anomaly scores (lower/more negative score indicates more anomalous)
    anomaly_scores = iso_forest.decision_function(X)
    
    # 5. Evaluate the results
    correct_normal = np.sum((y_true == 1) & (y_pred == 1))
    correct_anomaly = np.sum((y_true == -1) & (y_pred == -1))
    false_positives = np.sum((y_true == -1) & (y_pred == 1))
    false_negatives = np.sum((y_true == 1) & (y_pred == -1))
    
    print("\n--- Model Evaluation Results ---")
    print(f"Correctly identified Normal points: {correct_normal}")
    print(f"Correctly identified Anomalies: {correct_anomaly}")
    print(f"False Positives (Anomalies missed): {false_positives}")
    print(f"False Negatives (Normal points flagged): {false_negatives}")
    
    accuracy = np.mean(y_true == y_pred) * 100
    print(f"Overall Accuracy: {accuracy:.2f}%")
    
    # Print out some details of detected anomalies
    print("\n--- Flagged Anomalies Sample ---")
    anomalies_indices = np.where(y_pred == -1)[0]
    for idx in anomalies_indices[:5]:
        print(f"Index: {idx:3d} | Coordinates: ({X[idx, 0]:5.2f}, {X[idx, 1]:5.2f}) | Anomaly Score: {anomaly_scores[idx]:.4f}")

if __name__ == "__main__":
    run_anomaly_detection()
