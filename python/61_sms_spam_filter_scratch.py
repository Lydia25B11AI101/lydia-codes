# ==============================================================================
# Title: SMS Spam Filter from Scratch (Naive Bayes Classifier)
# Author: Lydia S. Makiwa
# Date: June 3, 2026
# Description: Implements a text preprocessing pipeline and a Naive Bayes Classifier 
#              from scratch to classify SMS messages as "Spam" or "Ham" (Legitimate).
#              Exposes core Natural Language Processing (NLP) concepts to AIML students.
# ==============================================================================

import re
import math

class NaiveBayesSpamFilter:
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # Laplace Smoothing parameter
        self.spam_word_counts = {}
        self.ham_word_counts = {}
        self.spam_count = 0
        self.ham_count = 0
        self.vocab = set()

    def clean_and_tokenize(self, text):
        """Cleans input text and tokenizes it into a list of words."""
        # Convert to lowercase and remove punctuation
        text = text.lower()
        words = re.findall(r'\b[a-z0-9]+\b', text)
        return words

    def fit(self, training_data):
        """
        Trains the Naive Bayes model.
        training_data is a list of tuples: (message, label) where label is 'spam' or 'ham'
        """
        for message, label in training_data:
            words = self.clean_and_tokenize(message)
            word_set = set(words) # Use set for presence model (or list for frequency model)
            
            if label == 'spam':
                self.spam_count += 1
                for word in word_set:
                    self.spam_word_counts[word] = self.spam_word_counts.get(word, 0) + 1
                    self.vocab.add(word)
            else:
                self.ham_count += 1
                for word in word_set:
                    self.ham_word_counts[word] = self.ham_word_counts.get(word, 0) + 1
                    self.vocab.add(word)

    def predict(self, message):
        """
        Classifies a message as 'spam' or 'ham' using log probabilities.
        """
        words = self.clean_and_tokenize(message)
        
        # Calculate Prior Log Probabilities
        total_messages = self.spam_count + self.ham_count
        p_spam = self.spam_count / total_messages
        p_ham = self.ham_count / total_messages
        
        log_prob_spam = math.log(p_spam)
        log_prob_ham = math.log(p_ham)
        
        # Add Likelihood Log Probabilities with Laplace Smoothing
        for word in self.vocab:
            if word in words:
                # Probability that word is present given class
                prob_word_spam = (self.spam_word_counts.get(word, 0) + self.alpha) / (self.spam_count + 2 * self.alpha)
                prob_word_ham = (self.ham_word_counts.get(word, 0) + self.alpha) / (self.ham_count + 2 * self.alpha)
                
                log_prob_spam += math.log(prob_word_spam)
                log_prob_ham += math.log(prob_word_ham)
            else:
                # Probability that word is absent given class
                prob_word_spam_absent = 1.0 - (self.spam_word_counts.get(word, 0) + self.alpha) / (self.spam_count + 2 * self.alpha)
                prob_word_ham_absent = 1.0 - (self.ham_word_counts.get(word, 0) + self.alpha) / (self.ham_count + 2 * self.alpha)
                
                log_prob_spam += math.log(prob_word_spam_absent)
                log_prob_ham += math.log(prob_word_ham_absent)
                
        return 'spam' if log_prob_spam > log_prob_ham else 'ham'

# --- Demo & Example ---
if __name__ == "__main__":
    print("--- Naive Bayes SMS Spam Filter Demo ---")
    
    # 1. Tiny training dataset of spam and ham SMS
    training_corpus = [
        ("Winner! Claim your free cash prize of $1000 today!", "spam"),
        ("Get cheap medicines online now without prescription.", "spam"),
        ("URGENT: Click here to claim your bonus coupons immediately.", "spam"),
        ("Call this number to win a free vacation package!", "spam"),
        
        ("Hey, are you free to grab coffee this afternoon?", "ham"),
        ("Please remember to bring the lecture notes for the lab session.", "ham"),
        ("Can you call me when you reach home? Thanks.", "ham"),
        ("I will be slightly late for the group study meeting.", "ham")
    ]
    
    # 2. Train model
    filter_model = NaiveBayesSpamFilter(alpha=1.0)
    filter_model.fit(training_corpus)
    print(f"Trained filter on {len(training_corpus)} SMS samples.")
    print(f"Vocabulary size: {len(filter_model.vocab)} unique tokens.")
    
    # 3. Test on unseen messages
    test_messages = [
        "Free cash rewards and prizes waiting for you! Click now.",
        "Hey, are we still meeting up for dinner tonight?",
        "Urgent! You have won a cheap tropical vacation. Call us now.",
        "Don't forget to submit the data structures project before Friday."
    ]
    
    print("\nClassification Results on Unseen Test Messages:")
    for msg in test_messages:
        pred = filter_model.predict(msg)
        print(f"  Message: \"{msg}\"")
        print(f"  ==> Prediction: {pred.upper()}\n")
