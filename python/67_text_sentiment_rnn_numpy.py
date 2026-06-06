"""
Title: Simple Recurrent Neural Network (RNN) from Scratch for Sentiment Analysis
Author: Lydia S. Makiwa
Date: June 06, 2026

Description:
This program implements a simple Recurrent Neural Network (RNN) from scratch
using only NumPy. It is trained to perform basic text sentiment classification 
(positive vs. negative) on short sentences. 

This helps AIML students understand:
- Tokenization and vocabulary mapping
- Recurrent hidden state dynamics (h_t = tanh(W_hh * h_prev + W_xh * x_t + b_h))
- Backpropagation Through Time (BPTT) mechanisms
"""

import numpy as np

# Sample training dataset
sentences = [
    "i love learning aiml",
    "this is an amazing program",
    "we are happy and excited",
    "i hate slow progress",
    "this algorithm is bad",
    "sad and disappointed results"
]
# 1 = Positive, 0 = Negative
labels = np.array([1, 1, 1, 0, 0, 0])

# Build Vocabulary
words = list(set(" ".join(sentences).split()))
word_to_ix = {word: i for i, word in enumerate(words)}
vocab_size = len(words)

def text_to_vector(sentence):
    """Converts a sentence into a list of one-hot encoded vectors."""
    vectors = []
    for word in sentence.split():
        if word in word_to_ix:
            vec = np.zeros((vocab_size, 1))
            vec[word_to_ix[word]] = 1
            vectors.append(vec)
    return vectors

class SimpleRNN:
    def __init__(self, input_dim, hidden_dim, output_dim=1):
        # Initialize weights
        self.W_xh = np.random.randn(hidden_dim, input_dim) * 0.01
        self.W_hh = np.random.randn(hidden_dim, hidden_dim) * 0.01
        self.W_hy = np.random.randn(output_dim, hidden_dim) * 0.01
        
        # Biases
        self.b_h = np.zeros((hidden_dim, 1))
        self.b_y = np.zeros((output_dim, 1))
        
        self.hidden_dim = hidden_dim

    def forward(self, inputs):
        """Forward pass through the RNN for an entire sequence."""
        h = {}
        h[-1] = np.zeros((self.hidden_dim, 1))
        
        for t, x in enumerate(inputs):
            # Recurrent hidden state equation: h_t = tanh(W_hh * h_(t-1) + W_xh * x_t + b_h)
            h[t] = np.tanh(np.dot(self.W_hh, h[t-1]) + np.dot(self.W_xh, x) + self.b_h)
            
        # Output prediction from the last hidden state
        last_t = len(inputs) - 1
        y = np.dot(self.W_hy, h[last_t]) + self.b_y
        # Sigmoid activation for binary classification
        p = 1 / (1 + np.exp(-y))
        
        return p, h

    def train(self, sentences, labels, lr=0.1, epochs=200):
        """Train the RNN using gradient descent."""
        for epoch in range(epochs):
            loss = 0
            for sentence, label in zip(sentences, labels):
                inputs = text_to_vector(sentence)
                if not inputs:
                    continue
                    
                # 1. Forward pass
                p, h = self.forward(inputs)
                
                # Binary Cross-Entropy Loss
                loss += - (label * np.log(p + 1e-15) + (1 - label) * np.log(1 - p + 1e-15))
                
                # 2. Backpropagation
                dy = p - label # Gradient of loss with respect to output activation y
                
                dW_hy = np.dot(dy, h[len(inputs)-1].T)
                db_y = dy
                
                # Initialize gradients for recurrent weights
                dW_hh = np.zeros_like(self.W_hh)
                dW_xh = np.zeros_like(self.W_xh)
                db_h = np.zeros_like(self.b_h)
                
                dh_next = np.dot(self.W_hy.T, dy)
                
                # Backpropagate through time (BPTT)
                for t in reversed(range(len(inputs))):
                    dtanh = (1 - h[t] * h[t]) * dh_next # Derivative of tanh
                    db_h += dtanh
                    dW_xh += np.dot(dtanh, inputs[t].T)
                    dW_hh += np.dot(dtanh, h[t-1].T)
                    dh_next = np.dot(self.W_hh.T, dtanh)
                
                # 3. Weight Updates (Gradient Descent)
                self.W_xh -= lr * dW_xh
                self.W_hh -= lr * dW_hh
                self.W_hy -= lr * dW_hy
                self.b_h -= lr * db_h
                self.b_y -= lr * db_y
                
            if (epoch + 1) % 50 == 0:
                print(f"Epoch {epoch+1:3d} | Average Loss: {float(loss/len(sentences)):.4f}")

def run_sentiment_demo():
    print("=== Training RNN from Scratch ===")
    rnn = SimpleRNN(input_dim=vocab_size, hidden_dim=8)
    rnn.train(sentences, labels, lr=0.15, epochs=200)
    
    print("\n=== Testing Sentiment Predictions ===")
    test_phrases = [
        "i love aiml",
        "bad results",
        "this program is amazing"
    ]
    
    for phrase in test_phrases:
        inputs = text_to_vector(phrase)
        if inputs:
            prob, _ = rnn.forward(inputs)
            sentiment = "Positive" if prob > 0.5 else "Negative"
            print(f"Phrase: '{phrase}' -> Prob: {prob[0][0]:.4f} ({sentiment})")

if __name__ == "__main__":
    run_sentiment_demo()
