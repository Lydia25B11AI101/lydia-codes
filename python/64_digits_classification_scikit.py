# Program Title: Hand-written Digits Classification using SVM
# Author: Lydia S. Makiwa
# Date: June 5, 2026
# Description: This program demonstrates a machine learning pipeline using scikit-learn.
#              It loads the UCI hand-written digits dataset, splits it into training and testing sets,
#              trains a Support Vector Machine (SVM) classifier, evaluates its performance,
#              and renders a text-based ASCII representation of a classified test digit.
#              Perfect for AIML students exploring supervised classification.

from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split

def run_digit_classifier():
    # 1. Load the digits dataset (8x8 pixel images of digits 0-9)
    digits = datasets.load_digits()
    
    # Flatten the images to a 1D vector of 64 pixels (8x8)
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))
    
    # 2. Split dataset into 80% train and 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        data, digits.target, test_size=0.2, shuffle=True, random_state=42
    )
    
    # 3. Create and train a Support Vector Classifier
    classifier = svm.SVC(gamma=0.001, C=100.0)
    classifier.fit(X_train, y_train)
    
    # 4. Predict on test set
    predicted = classifier.predict(X_test)
    
    # 5. Output metrics
    print("=== Digit Classification Performance ===")
    print(f"Classification Report for SVM Classifier:\n")
    print(metrics.classification_report(y_test, predicted))
    
    print("\nConfusion Matrix:")
    print(metrics.confusion_matrix(y_test, predicted))
    
    # 6. Show a text-based ASCII visualization of an example test digit
    example_idx = 15
    example_flat_image = X_test[example_idx]
    example_image = example_flat_image.reshape((8, 8))
    actual_label = y_test[example_idx]
    predicted_label = predicted[example_idx]
    
    print(f"\n--- Visualizing Test Image #{example_idx} ---")
    print(f"Actual Label: {actual_label} | Predicted Label: {predicted_label}")
    print("ASCII Rendering:")
    for row in example_image:
        row_str = ""
        for pixel in row:
            # Scale 0-16 intensity to ASCII character
            if pixel < 4:
                row_str += "  "
            elif pixel < 8:
                row_str += ". "
            elif pixel < 12:
                row_str += "x "
            else:
                row_str += "# "
        print(row_str)

if __name__ == "__main__":
    run_digit_classifier()
