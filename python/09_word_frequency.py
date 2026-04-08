# Python Program 9: Word Frequency Counter
# Author: Lydia S. Makiwa
# Description: Counts word frequency in a piece of text

import re
from collections import Counter

def word_frequency(text):
    """Returns a sorted word frequency dictionary."""
    words = re.findall(r'\b[a-z]+\b', text.lower())
    return Counter(words)

sample_text = """
Artificial intelligence is transforming the world. Machine learning and deep learning
are subsets of artificial intelligence. Python is the most popular language for
machine learning and data science. Data science uses Python extensively.
"""

freq = word_frequency(sample_text)
top_10 = freq.most_common(10)

print("=== Word Frequency Counter ===")
print(f"Total words: {sum(freq.values())}")
print(f"Unique words: {len(freq)}")
print("\nTop 10 most common words:")
print(f"{'Word':<15} {'Count':>5} {'Bar'}")
print("-" * 35)
for word, count in top_10:
    bar = "█" * count
    print(f"{word:<15} {count:>5}  {bar}")
