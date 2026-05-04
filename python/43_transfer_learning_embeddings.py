# ============================================================
# Program Title : Transfer Learning with Word Embeddings
# Author        : Lydia S. Makiwa
# Date          : 2026-05-04
# Description   : Simulate transfer learning using pre-built
#                 word vectors for sentiment classification.
# ============================================================

import numpy as np

# Simulated GloVe-style embeddings (50-dim)
np.random.seed(7)
vocab = ['good','great','excellent','bad','terrible','awful',
         'movie','film','story','acting','plot','director']
EMBED_DIM = 50
embeddings = {w: np.random.randn(EMBED_DIM) for w in vocab}

def sentence_vector(sentence):
    tokens = sentence.lower().split()
    vecs = [embeddings[t] for t in tokens if t in embeddings]
    return np.mean(vecs, axis=0) if vecs else np.zeros(EMBED_DIM)

# Labelled dataset: 1=positive, 0=negative
reviews = [
    ('great movie excellent acting', 1),
    ('terrible film awful plot',     0),
    ('good story great director',    1),
    ('bad film terrible acting',     0),
    ('excellent plot good story',    1),
    ('awful movie terrible director',0),
]

X = np.array([sentence_vector(r) for r, _ in reviews])
y = np.array([l for _, l in reviews])

# Logistic regression on frozen embeddings
w = np.zeros(EMBED_DIM)
b = 0.0
for epoch in range(300):
    pred  = 1 / (1 + np.exp(-(X @ w + b)))
    dw    = X.T @ (pred - y) / len(y)
    db    = np.mean(pred - y)
    w    -= 0.1 * dw
    b    -= 0.1 * db

preds = (1 / (1 + np.exp(-(X @ w + b))) > 0.5).astype(int)
acc   = np.mean(preds == y) * 100
print(f'Training Accuracy: {acc:.1f}%')

# Test on unseen sentences
test = ['great acting excellent plot', 'bad story awful film']
for t in test:
    v = sentence_vector(t)
    p = 1 / (1 + np.exp(-(v @ w + b)))
    label = 'Positive' if p > 0.5 else 'Negative'
    print(f"  '{t}' -> {label} ({p:.2f})")
print('Transfer learning demo complete!')
