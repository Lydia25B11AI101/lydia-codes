# AIML Program 04: Naive Bayes Classifier
# Author: Lydia S. Makiwa
# Description: Text classification using Naive Bayes — email spam detector

import re
from collections import defaultdict, Counter
import math

class NaiveBayesClassifier:
    """Multinomial Naive Bayes for text classification."""

    def fit(self, texts, labels):
        self.classes    = list(set(labels))
        self.class_prob = {}
        self.word_prob  = {}
        total = len(labels)

        for cls in self.classes:
            class_texts = [t for t, l in zip(texts, labels) if l == cls]
            self.class_prob[cls] = len(class_texts) / total

            all_words  = [w for t in class_texts for w in self._tokenize(t)]
            word_count = Counter(all_words)
            vocab_size = len(set(all_words))
            total_words= sum(word_count.values())

            self.word_prob[cls] = {
                w: (c + 1) / (total_words + vocab_size)   # Laplace smoothing
                for w, c in word_count.items()
            }
            self.word_prob[cls]["_unk_"] = 1 / (total_words + vocab_size)

    def _tokenize(self, text):
        return re.findall(r'\b[a-z]+\b', text.lower())

    def predict(self, text):
        words = self._tokenize(text)
        scores = {}
        for cls in self.classes:
            log_prob = math.log(self.class_prob[cls])
            for w in words:
                log_prob += math.log(self.word_prob[cls].get(w, self.word_prob[cls]["_unk_"]))
            scores[cls] = log_prob
        return max(scores, key=scores.get)


# Email dataset
emails = [
    ("win free money now click here prize lottery", "spam"),
    ("free gift winner congratulations claim now",  "spam"),
    ("buy cheap pills online discount offer today", "spam"),
    ("urgent account verify password immediately",  "spam"),
    ("meeting tomorrow 10am project update needed", "ham"),
    ("please review the attached report by friday", "ham"),
    ("team lunch next tuesday rsvp by wednesday",   "ham"),
    ("your order has been shipped tracking number", "ham"),
    ("can we reschedule the interview to thursday", "ham"),
]

texts  = [e[0] for e in emails]
labels = [e[1] for e in emails]

nb = NaiveBayesClassifier()
nb.fit(texts, labels)

print("=== Naive Bayes Spam Classifier ===\n")
test_emails = [
    "free money win prize click now",
    "project meeting schedule update team",
    "congratulations you have won lottery",
    "interview rescheduled to next monday",
]

for email in test_emails:
    pred = nb.predict(email)
    icon = "🚫 SPAM" if pred == "spam" else "✅ HAM"
    print(f"  {icon} | {email[:45]}")
