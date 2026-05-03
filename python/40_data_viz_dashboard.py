# ============================================================
# Program Title : Data Visualisation Dashboard (Matplotlib)
# Author        : Lydia S. Makiwa
# Date          : 2026-05-03
# Description   : 4-panel dashboard — bar, pie, line, scatter —
#                 using synthetic student performance data.
# ============================================================

import matplotlib.pyplot as plt
import numpy as np
import random

random.seed(42)
np.random.seed(42)

# ── Synthetic dataset: 50 students ───────────────────────────
n = 50
students   = [f"S{i:02d}" for i in range(1, n+1)]
maths      = np.random.randint(40, 100, n)
science    = np.clip(maths + np.random.randint(-15, 15, n), 0, 100)
english    = np.random.randint(35, 95, n)
hours_study = np.random.uniform(1, 8, n)

grades = []
for m in maths:
    if m >= 75: grades.append("A")
    elif m >= 60: grades.append("B")
    elif m >= 50: grades.append("C")
    else: grades.append("F")

grade_counts = {g: grades.count(g) for g in ["A","B","C","F"]}

# ── Figure setup ─────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Student Performance Dashboard", fontsize=16, fontweight="bold")

# Panel 1 – Bar: average scores per subject
ax1 = axes[0, 0]
subjects = ["Maths", "Science", "English"]
avgs     = [maths.mean(), science.mean(), english.mean()]
bars = ax1.bar(subjects, avgs, color=["#4C72B0","#55A868","#C44E52"], edgecolor="black")
ax1.set_title("Average Score per Subject")
ax1.set_ylabel("Score")
ax1.set_ylim(0, 100)
for bar, avg in zip(bars, avgs):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height()+1, f"{avg:.1f}", ha="center")

# Panel 2 – Pie: grade distribution
ax2 = axes[0, 1]
ax2.pie(grade_counts.values(), labels=grade_counts.keys(), autopct="%1.1f%%",
        colors=["#2ecc71","#3498db","#f39c12","#e74c3c"], startangle=140)
ax2.set_title("Grade Distribution (Maths)")

# Panel 3 – Line: sorted maths scores
ax3 = axes[1, 0]
sorted_m = np.sort(maths)
ax3.plot(sorted_m, color="#4C72B0", linewidth=2, label="Maths")
ax3.axhline(maths.mean(), color="red", linestyle="--", label=f"Mean={maths.mean():.1f}")
ax3.set_title("Sorted Maths Scores")
ax3.set_xlabel("Student rank")
ax3.set_ylabel("Score")
ax3.legend()

# Panel 4 – Scatter: study hours vs maths score
ax4 = axes[1, 1]
sc = ax4.scatter(hours_study, maths, c=maths, cmap="RdYlGn", edgecolors="grey", s=60)
plt.colorbar(sc, ax=ax4, label="Maths score")
ax4.set_title("Study Hours vs Maths Score")
ax4.set_xlabel("Hours studied per day")
ax4.set_ylabel("Maths score")

plt.tight_layout()
plt.savefig("student_dashboard.png", dpi=150)
print("Dashboard saved to student_dashboard.png")
plt.show()
