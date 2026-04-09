# AIML Program 11: Recurrent Neural Network (RNN) for Text Generation
# Author: Lydia S. Makiwa
# Description: Character-level RNN from scratch using numpy
#              Trains on a short text and generates new characters one at a time
#              Core concept behind GPT, LSTM, and language models

import numpy as np

# ── Helper Functions ──────────────────────────────────────
def softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum()

# ── Character-Level RNN ───────────────────────────────────
class CharRNN:
    """
    Vanilla RNN: h_t = tanh(W_xh * x_t + W_hh * h_{t-1} + b_h)
                 y_t = W_hy * h_t + b_y
    """
    def __init__(self, vocab_size, hidden_size=64, lr=0.01):
        self.vocab_size  = vocab_size
        self.hidden_size = hidden_size
        self.lr          = lr

        # Initialise weights (small random values)
        scale = 0.01
        self.W_xh = np.random.randn(hidden_size, vocab_size)  * scale
        self.W_hh = np.random.randn(hidden_size, hidden_size) * scale
        self.W_hy = np.random.randn(vocab_size,  hidden_size) * scale
        self.b_h  = np.zeros((hidden_size, 1))
        self.b_y  = np.zeros((vocab_size,  1))

        # Adagrad memory
        self.m_Wxh = np.zeros_like(self.W_xh)
        self.m_Whh = np.zeros_like(self.W_hh)
        self.m_Why = np.zeros_like(self.W_hy)
        self.m_bh  = np.zeros_like(self.b_h)
        self.m_by  = np.zeros_like(self.b_y)

    def forward(self, inputs, h_prev):
        """Forward pass — returns outputs, hidden states, loss components."""
        xs, hs, ys, ps = {}, {}, {}, {}
        hs[-1] = h_prev.copy()

        for t, ix in enumerate(inputs):
            xs[t]  = np.zeros((self.vocab_size, 1))
            xs[t][ix] = 1
            hs[t]  = np.tanh(self.W_xh @ xs[t] + self.W_hh @ hs[t-1] + self.b_h)
            ys[t]  = self.W_hy @ hs[t] + self.b_y
            ps[t]  = softmax(ys[t])

        return xs, hs, ys, ps

    def backward(self, inputs, targets, xs, hs, ps):
        """Backpropagation through time (BPTT)."""
        dW_xh = np.zeros_like(self.W_xh)
        dW_hh = np.zeros_like(self.W_hh)
        dW_hy = np.zeros_like(self.W_hy)
        db_h  = np.zeros_like(self.b_h)
        db_y  = np.zeros_like(self.b_y)
        dh_next = np.zeros((self.hidden_size, 1))
        loss  = 0.0

        for t in reversed(range(len(inputs))):
            dy = ps[t].copy()
            dy[targets[t]] -= 1          # softmax + cross-entropy gradient

            dW_hy += dy @ hs[t].T
            db_y  += dy
            loss  -= np.log(ps[t][targets[t], 0] + 1e-9)

            dh = self.W_hy.T @ dy + dh_next
            dh_raw = (1 - hs[t]**2) * dh  # tanh derivative

            db_h  += dh_raw
            dW_xh += dh_raw @ xs[t].T
            dW_hh += dh_raw @ hs[t-1].T
            dh_next = self.W_hh.T @ dh_raw

        # Clip gradients (prevent exploding)
        for d in [dW_xh, dW_hh, dW_hy, db_h, db_y]:
            np.clip(d, -5, 5, out=d)

        return dW_xh, dW_hh, dW_hy, db_h, db_y, loss

    def update(self, dW_xh, dW_hh, dW_hy, db_h, db_y):
        """Adagrad update."""
        for param, dparam, mem in [
            (self.W_xh, dW_xh, self.m_Wxh),
            (self.W_hh, dW_hh, self.m_Whh),
            (self.W_hy, dW_hy, self.m_Why),
            (self.b_h,  db_h,  self.m_bh),
            (self.b_y,  db_y,  self.m_by),
        ]:
            mem += dparam * dparam
            param -= self.lr * dparam / (np.sqrt(mem) + 1e-8)

    def sample(self, h, seed_ix, n):
        """Generate n characters starting from seed character."""
        x = np.zeros((self.vocab_size, 1))
        x[seed_ix] = 1
        result = []
        for _ in range(n):
            h = np.tanh(self.W_xh @ x + self.W_hh @ h + self.b_h)
            y = self.W_hy @ h + self.b_y
            p = softmax(y).ravel()
            ix = np.random.choice(range(self.vocab_size), p=p)
            x  = np.zeros((self.vocab_size, 1))
            x[ix] = 1
            result.append(ix)
        return result

    def train(self, text, char_to_ix, ix_to_char, seq_len=25, epochs=3000):
        h_prev  = np.zeros((self.hidden_size, 1))
        pointer = 0
        smooth_loss = -np.log(1.0/self.vocab_size) * seq_len

        for epoch in range(epochs):
            if pointer + seq_len + 1 >= len(text):
                pointer = 0
                h_prev  = np.zeros((self.hidden_size, 1))

            inputs  = [char_to_ix[c] for c in text[pointer:pointer+seq_len]]
            targets = [char_to_ix[c] for c in text[pointer+1:pointer+seq_len+1]]

            xs, hs, ys, ps = self.forward(inputs, h_prev)
            dW_xh, dW_hh, dW_hy, db_h, db_y, loss = self.backward(inputs, targets, xs, hs, ps)
            self.update(dW_xh, dW_hh, dW_hy, db_h, db_y)

            smooth_loss = smooth_loss * 0.999 + loss * 0.001
            h_prev = hs[seq_len - 1]
            pointer += seq_len

            if epoch % 1000 == 0:
                print(f"  Epoch {epoch:5d} | Smooth Loss: {smooth_loss:.4f}")
                sample_ix  = self.sample(h_prev, inputs[0], 60)
                sample_txt = ''.join([ix_to_char[ix] for ix in sample_ix])
                print(f"  Sample: \"{sample_txt}\"\n")


# ── Training Data ─────────────────────────────────────────
text = (
    "the quick brown fox jumps over the lazy dog "
    "artificial intelligence machine learning deep learning "
    "python data science neural network algorithm "
    "lydia codes every day to become a great ai engineer "
    "the quick brown fox jumps over the lazy dog "
    "learning python is fun and powerful for ai projects "
)

chars      = sorted(set(text))
vocab_size = len(chars)
char_to_ix = {c: i for i, c in enumerate(chars)}
ix_to_char = {i: c for i, c in enumerate(chars)}

print("=== Character-Level RNN Text Generator ===\n")
print(f"Text length: {len(text)} chars | Vocabulary: {vocab_size} unique chars")
print(f"Chars: {repr(''.join(chars))}\n")
print("Training RNN...\n")

rnn = CharRNN(vocab_size=vocab_size, hidden_size=64, lr=0.05)
rnn.train(text, char_to_ix, ix_to_char, seq_len=20, epochs=3001)

# Final generation
print("\n" + "="*55)
print("Final Generated Text Samples:")
h = np.zeros((rnn.hidden_size, 1))
for seed_char in ["t", "a", "l", "p"]:
    seed_ix  = char_to_ix.get(seed_char, 0)
    sample   = rnn.sample(h, seed_ix, 80)
    txt      = seed_char + ''.join([ix_to_char[ix] for ix in sample])
    print(f"  Seed='{seed_char}': {txt}")

print("\nThis is how language models like GPT work at a fundamental level!")
