# Program Title: Frequency-based Extractive Text Summarizer
# Author: Lydia S. Makiwa
# Date: June 5, 2026
# Description: This program implements a frequency-based extractive text summarizer from scratch.
#              It tokenizes text into sentences and words, filters out common stop words,
#              calculates word frequencies, scores sentences, and retrieves the top N sentences
#              as a summary. Perfect for introduction to Natural Language Processing (NLP).

import re
from collections import defaultdict

def clean_and_tokenize_words(text):
    # Convert to lowercase and remove non-alphanumeric characters except spaces
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    return cleaned.split()

def tokenize_sentences(text):
    # Simple sentence tokenization based on period, exclamation, and question mark
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]

def summarize_text(text, num_sentences=2):
    sentences = tokenize_sentences(text)
    if len(sentences) <= num_sentences:
        return text
    
    words = clean_and_tokenize_words(text)
    
    # Standard list of English stop words
    stop_words = set([
        "the", "a", "an", "and", "or", "but", "if", "then", "else", "of", "to", "in", "on", "at", 
        "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", 
        "after", "above", "below", "from", "up", "down", "is", "am", "are", "was", "were", "be", 
        "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "i", "you", 
        "he", "she", "it", "we", "they", "this", "that", "these", "those"
    ])
    
    # Calculate word frequencies
    word_frequencies = defaultdict(int)
    for word in words:
        if word not in stop_words:
            word_frequencies[word] += 1
            
    # Normalize frequencies
    max_frequency = max(word_frequencies.values()) if word_frequencies else 1
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency
        
    # Score sentences based on word frequencies
    sentence_scores = defaultdict(float)
    for sentence in sentences:
        sentence_words = clean_and_tokenize_words(sentence)
        for word in sentence_words:
            if word in word_frequencies:
                sentence_scores[sentence] += word_frequencies[word]
                
    # Sort sentences by score and pick top N
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    top_sentences = sorted_sentences[:num_sentences]
    
    # Re-order the summary sentences to maintain original flow
    summary_sentences = []
    for s in sentences:
        if s in [item[0] for item in top_sentences]:
            summary_sentences.append(s)
            
    return " ".join(summary_sentences)

if __name__ == "__main__":
    sample_text = (
        "Artificial Intelligence is transformational. It is revolutionizing industries such as healthcare, "
        "finance, and transportation. At the core of modern AI is Machine Learning, where models learn "
        "patterns from historical data rather than following explicit rules. Deep Learning, a subfield "
        "of Machine Learning, uses neural networks to simulate the human brain's capability to process "
        "unstructured data like images and text. While NLP (Natural Language Processing) allows systems "
        "to comprehend human language, Computer Vision allows machines to understand visual inputs. "
        "The development of intelligent agents is paving the way for a highly automated future. "
        "Ethical guidelines and safety regulations are crucial to ensuring AI benefits all of humanity."
    )
    
    print("=== Extractive Text Summarizer Demo ===")
    print("\nOriginal Text:")
    print(sample_text)
    
    summary = summarize_text(sample_text, num_sentences=3)
    print("\nGenerated Summary (Top 3 Sentences):")
    print(summary)
