# Python Program 23: Pandas Basics for Data Analysis
# Author: Lydia S. Makiwa
# Description: Introduction to Pandas DataFrames — essential for AIML

import pandas as pd
import numpy as np

# ── Create a DataFrame ────────────────────────────────────
data = {
    "Name":    ["Lydia", "Alice", "Bob", "Carol", "David", "Eve"],
    "Age":     [20, 22, 21, 23, 19, 24],
    "Score":   [95, 82, 71, 88, 64, 91],
    "Major":   ["AIML", "CS", "IT", "AIML", "CS", "Data Sci"],
    "Passed":  [True, True, True, True, False, True],
}
df = pd.DataFrame(data)

print("=== Student DataFrame ===")
print(df.to_string(index=False))

# ── Basic info ────────────────────────────────────────────
print("\nShape:", df.shape)
print("\nDescribe:\n", df.describe().round(2))

# ── Filtering ─────────────────────────────────────────────
print("\nAIML students:")
print(df[df["Major"] == "AIML"][["Name","Score"]].to_string(index=False))

print("\nStudents with score > 85:")
print(df[df["Score"] > 85][["Name","Score","Major"]].to_string(index=False))

# ── Grouping ──────────────────────────────────────────────
print("\nAverage score by Major:")
print(df.groupby("Major")["Score"].mean().round(1).to_string())

# ── Adding a column ───────────────────────────────────────
df["Grade"] = df["Score"].apply(
    lambda s: "A" if s>=90 else "B" if s>=80 else "C" if s>=70 else "D"
)
print("\nWith Grade column:")
print(df[["Name","Score","Grade"]].to_string(index=False))
