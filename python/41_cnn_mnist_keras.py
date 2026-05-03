# ============================================================
# Program Title : CNN Digit Classifier – MNIST with Keras
# Author        : Lydia S. Makiwa
# Date          : 2026-05-03
# Description   : Trains a Convolutional Neural Network on the
#                 MNIST handwritten digits dataset — a key AIML
#                 milestone. Achieves ~99% test accuracy.
# ============================================================

import numpy as np
# TensorFlow / Keras
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

# ── 1. Load & preprocess MNIST ────────────────────────────────
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Normalise pixel values to [0, 1] and reshape for Conv2D
X_train = X_train.astype("float32") / 255.0
X_test  = X_test.astype("float32")  / 255.0
X_train = X_train[..., np.newaxis]  # (60000, 28, 28, 1)
X_test  = X_test[...,  np.newaxis]

# One-hot encode labels
num_classes = 10
y_train_oh  = keras.utils.to_categorical(y_train, num_classes)
y_test_oh   = keras.utils.to_categorical(y_test,  num_classes)

# ── 2. Build the CNN ──────────────────────────────────────────
model = keras.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax'),
], name="MNIST_CNN")

model.summary()

# ── 3. Compile & train ────────────────────────────────────────
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    X_train, y_train_oh,
    validation_split=0.1,
    epochs=5,
    batch_size=128,
    verbose=1
)

# ── 4. Evaluate ───────────────────────────────────────────────
test_loss, test_acc = model.evaluate(X_test, y_test_oh, verbose=0)
print(f"\nTest accuracy : {test_acc:.4f}")
print(f"Test loss     : {test_loss:.4f}")

# ── 5. Predict first 5 test images ───────────────────────────
preds = np.argmax(model.predict(X_test[:5]), axis=1)
print("\nSample predictions vs true labels:")
for i, (p, t) in enumerate(zip(preds, y_test[:5])):
    status = "✅" if p == t else "❌"
    print(f"  Image {i}: predicted={p}, actual={t} {status}")

# Save the model
model.save("mnist_cnn.keras")
print("\nModel saved to mnist_cnn.keras")
