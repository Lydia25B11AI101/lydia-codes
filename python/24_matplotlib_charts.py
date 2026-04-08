# Python Program 24: Data Visualization with Matplotlib
# Author: Lydia S. Makiwa
# Description: Create bar charts, line plots, and pie charts for AIML data

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Lydia S. Makiwa — Data Visualization Demo", fontsize=14, fontweight="bold")

# ── 1. Bar Chart — Student Scores ────────────────────────
names  = ["Lydia", "Alice", "Bob", "Carol", "David"]
scores = [95, 82, 71, 88, 64]
colors = ["#c084fc" if s >= 80 else "#60a5fa" if s >= 70 else "#f87171" for s in scores]
axes[0,0].bar(names, scores, color=colors, edgecolor="white")
axes[0,0].set_title("Student Scores")
axes[0,0].set_ylabel("Score")
axes[0,0].set_ylim(0, 105)
axes[0,0].axhline(y=80, color="green", linestyle="--", alpha=0.6, label="Pass (80)")
axes[0,0].legend()

# ── 2. Line Plot — Fibonacci Growth ──────────────────────
fib = [0,1,1,2,3,5,8,13,21,34,55,89]
axes[0,1].plot(fib, color="#c084fc", marker="o", linewidth=2)
axes[0,1].set_title("Fibonacci Sequence Growth")
axes[0,1].set_xlabel("Index")
axes[0,1].set_ylabel("Value")
axes[0,1].fill_between(range(len(fib)), fib, alpha=0.2, color="#c084fc")

# ── 3. Pie Chart — Programming Languages ─────────────────
langs  = ["Python", "C", "HTML/CSS", "Java", "Other"]
usage  = [40, 25, 15, 12, 8]
colors3 = ["#c084fc","#60a5fa","#4ade80","#fbbf24","#f87171"]
axes[1,0].pie(usage, labels=langs, colors=colors3, autopct="%1.0f%%", startangle=90)
axes[1,0].set_title("Language Usage in Projects")

# ── 4. Scatter Plot — Score vs Age ───────────────────────
ages   = [20, 22, 21, 23, 19, 24, 20, 22]
scores2= [95, 82, 71, 88, 64, 91, 78, 85]
axes[1,1].scatter(ages, scores2, color="#c084fc", s=100, edgecolors="white", linewidth=1.5)
z = np.polyfit(ages, scores2, 1)
p = np.poly1d(z)
x_line = np.linspace(min(ages), max(ages), 100)
axes[1,1].plot(x_line, p(x_line), "r--", alpha=0.7, label="Trend")
axes[1,1].set_title("Score vs Age")
axes[1,1].set_xlabel("Age"); axes[1,1].set_ylabel("Score")
axes[1,1].legend()

plt.tight_layout()
plt.savefig("data_visualization.png", dpi=120, bbox_inches="tight")
print("✅ Chart saved as data_visualization.png")
print("   (Run locally to see the visualization)")
