# ============================================================
# Program Title : Sentiment Analysis with TextBlob
# Author        : Lydia S. Makiwa
# Date          : 2026-04-09
# Description   : Analyses the sentiment of text (positive,
#                 negative, neutral) using the TextBlob NLP
#                 library. Includes a simple tweet analyser demo.
# ============================================================

# Install if needed: pip install textblob
# python -m textblob.download_corpora

from textblob import TextBlob

def analyse_sentiment(text):
    """
    Returns:
        polarity  : -1.0 (very negative) to +1.0 (very positive)
        subjectivity: 0.0 (objective) to 1.0 (subjective)
        label     : Positive / Neutral / Negative
    """
    blob = TextBlob(text)
    pol  = blob.sentiment.polarity
    subj = blob.sentiment.subjectivity

    if pol > 0.1:
        label = "Positive"
    elif pol < -0.1:
        label = "Negative"
    else:
        label = "Neutral"

    return pol, subj, label

def print_analysis(text):
    pol, subj, label = analyse_sentiment(text)
    bar_len = int(abs(pol) * 20)
    bar = "#" * bar_len
    sign = "+" if pol >= 0 else "-"
    print(f"  Text    : {text[:60]}")
    print(f"  Polarity: {sign}{abs(pol):.3f}  [{bar:<20}]  {label}")
    print(f"  Subj    : {subj:.3f}")
    print()

# -- Demo --------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("  SENTIMENT ANALYSER — Lydia S. Makiwa")
    print("=" * 60)

    sample_texts = [
        "I absolutely love studying machine learning! It is so exciting.",
        "This bug has been giving me headaches all week. I hate it.",
        "The program runs in O(n log n) time.",
        "Artificial intelligence is transforming every industry today!",
        "I am not sure whether this result is correct or not.",
        "Python is an amazing language for data science and AI.",
        "The installation failed and nothing is working properly.",
    ]

    print()
    for text in sample_texts:
        print_analysis(text)

    # Interactive mode
    print("--- Interactive Mode (type 'quit' to exit) ---")
    while True:
        user_input = input("Enter text: ").strip()
        if user_input.lower() in ("quit", "exit", "q", ""):
            break
        print_analysis(user_input)
