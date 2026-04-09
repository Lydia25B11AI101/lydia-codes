# AIML Program 08: Sentiment Analysis (Lexicon-based + ML)
# Author: Lydia S. Makiwa
# Description: Detects positive/negative/neutral sentiment in text reviews
#              Demonstrates both rule-based and bag-of-words approaches

import re
from collections import Counter

# ── 1. Lexicon-based Sentiment Analyser ──────────────────
POSITIVE_WORDS = {
    "great","excellent","amazing","love","fantastic","wonderful","brilliant",
    "outstanding","superb","perfect","happy","enjoy","best","good","nice",
    "awesome","incredible","beautiful","impressive","helpful","recommend",
}
NEGATIVE_WORDS = {
    "terrible","awful","horrible","hate","worst","bad","poor","disappointing",
    "useless","boring","waste","slow","broken","frustrating","ugly","horrible",
    "dreadful","annoying","pathetic","mediocre","failed","wrong","never",
}
INTENSIFIERS = {"very","extremely","really","absolutely","totally","super"}
NEGATIONS    = {"not","never","no","don't","doesn't","didn't","won't","can't"}

def lexicon_sentiment(text):
    words = re.findall(r'\b[a-z]+\b', text.lower())
    score = 0
    i = 0
    while i < len(words):
        word = words[i]
        multiplier = 1
        if i > 0 and words[i-1] in NEGATIONS:
            multiplier = -1
        if i > 0 and words[i-1] in INTENSIFIERS:
            multiplier *= 1.5

        if word in POSITIVE_WORDS: score += 1 * multiplier
        if word in NEGATIVE_WORDS: score -= 1 * multiplier
        i += 1

    if score > 0:   return "Positive 😊", score
    elif score < 0: return "Negative 😞", score
    else:           return "Neutral 😐",  score

# ── 2. Simple Bag-of-Words ML classifier ─────────────────
class BOWSentimentClassifier:
    def fit(self, texts, labels):
        self.vocab     = {}
        self.pos_words = Counter()
        self.neg_words = Counter()
        for text, label in zip(texts, labels):
            words = re.findall(r'\b[a-z]+\b', text.lower())
            if label == "positive":
                self.pos_words.update(words)
            else:
                self.neg_words.update(words)
        self.pos_total = sum(self.pos_words.values()) + 1
        self.neg_total = sum(self.neg_words.values()) + 1

    def predict(self, text):
        words   = re.findall(r'\b[a-z]+\b', text.lower())
        pos_score = sum(self.pos_words.get(w, 0) / self.pos_total for w in words)
        neg_score = sum(self.neg_words.get(w, 0) / self.neg_total for w in words)
        if pos_score > neg_score: return "Positive 😊"
        if neg_score > pos_score: return "Negative 😞"
        return "Neutral 😐"

# ── Demo ─────────────────────────────────────────────────
train_data = [
    ("This product is absolutely amazing and wonderful", "positive"),
    ("I love this, best purchase I have ever made",      "positive"),
    ("Excellent quality, highly recommend to everyone",  "positive"),
    ("Great experience, very helpful and outstanding",   "positive"),
    ("This is terrible, completely broken and useless",  "negative"),
    ("Worst product ever, total waste of money",         "negative"),
    ("Horrible experience, very disappointing quality",  "negative"),
    ("Awful service, never buying from here again",      "negative"),
]
train_texts  = [t[0] for t in train_data]
train_labels = [t[1] for t in train_data]

clf = BOWSentimentClassifier()
clf.fit(train_texts, train_labels)

reviews = [
    "This phone is absolutely fantastic, I love it!",
    "The battery is terrible and the screen is broken",
    "It arrived on time and works as expected",
    "Not bad but not great either, it is mediocre",
    "Incredible performance, best laptop I have ever used",
    "Horrible quality, very disappointed with this product",
]

print("=== Sentiment Analysis Demo ===\n")
print(f"{'Review':<48} {'Lexicon':>12} {'ML (BOW)':>12}")
print("-" * 76)
for review in reviews:
    lex_label, score = lexicon_sentiment(review)
    ml_label         = clf.predict(review)
    short = review[:46] + ".." if len(review) > 46 else review
    print(f"{short:<48} {lex_label:>12} {ml_label:>12}")
