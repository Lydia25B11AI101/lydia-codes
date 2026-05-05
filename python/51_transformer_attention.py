# Program Title: Transformer Self-Attention Mechanism (NumPy)
# Author: Lydia S. Makiwa
# Date: 2026-05-05
# Description: Implements Scaled Dot-Product Attention from scratch —
#              the building block of GPT, BERT, and all modern LLMs.
#              Understanding this is key to working in AI/NLP.

import numpy as np

np.random.seed(42)

def softmax(x, axis=-1):
    e = np.exp(x - x.max(axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: queries  (seq_len, d_k)
    K: keys     (seq_len, d_k)
    V: values   (seq_len, d_v)
    Returns: output (seq_len, d_v), attention weights (seq_len, seq_len)
    """
    d_k = Q.shape[-1]
    # Compute attention scores
    scores = Q @ K.T / np.sqrt(d_k)   # scale to prevent vanishing gradients

    # Apply mask (e.g. causal mask for GPT)
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)

    attn_weights = softmax(scores, axis=-1)
    output = attn_weights @ V
    return output, attn_weights

def multi_head_attention(X, num_heads, d_model):
    """
    X: input sequence (seq_len, d_model)
    Splits d_model into num_heads and runs attention in parallel.
    """
    d_k = d_model // num_heads
    seq_len = X.shape[0]
    outputs = []

    for h in range(num_heads):
        # Random learned projections (in practice, these are trained)
        Wq = np.random.randn(d_model, d_k) * 0.1
        Wk = np.random.randn(d_model, d_k) * 0.1
        Wv = np.random.randn(d_model, d_k) * 0.1
        Q, K, V = X @ Wq, X @ Wk, X @ Wv
        out, _ = scaled_dot_product_attention(Q, K, V)
        outputs.append(out)

    # Concatenate all heads
    multi_head_out = np.concatenate(outputs, axis=-1)
    # Final linear projection
    Wo = np.random.randn(d_model, d_model) * 0.1
    return multi_head_out @ Wo

# ─── Demo ───
seq_len = 5    # 5 tokens (e.g. words in a sentence)
d_model = 8    # embedding dimension

# Simulate token embeddings
X = np.random.randn(seq_len, d_model)

print("=== Scaled Dot-Product Attention ===")
Q = X @ np.random.randn(d_model, 4)
K = X @ np.random.randn(d_model, 4)
V = X @ np.random.randn(d_model, 4)
out, attn = scaled_dot_product_attention(Q, K, V)
print(f"Input shape:       {X.shape}")
print(f"Output shape:      {out.shape}")
print(f"Attention weights:\n{np.round(attn, 3)}")

print("\n=== Causal (Masked) Self-Attention (GPT-style) ===")
mask = np.tril(np.ones((seq_len, seq_len)))  # lower triangular
out_masked, attn_masked = scaled_dot_product_attention(Q, K, V, mask=mask)
print(f"Masked attention weights (each token only sees past tokens):")
print(np.round(attn_masked, 3))

print("\n=== Multi-Head Attention ===")
mha_out = multi_head_attention(X, num_heads=2, d_model=d_model)
print(f"Multi-head output shape: {mha_out.shape}")
print("Multi-head output (first 2 tokens):")
print(np.round(mha_out[:2], 4))
