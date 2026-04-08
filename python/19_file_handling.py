# Python Program 19: File Handling — Read, Write, Append, CSV
# Author: Lydia S. Makiwa
# Description: Comprehensive file I/O operations in Python

import os
import csv

# ── 1. Write a text file ──────────────────────────────────
with open("notes.txt", "w") as f:
    f.write("AIML Study Notes\n")
    f.write("=" * 30 + "\n")
    f.writelines([
        "1. Python is great for AI/ML\n",
        "2. NumPy handles arrays\n",
        "3. Pandas handles data frames\n",
        "4. Scikit-learn for ML models\n",
    ])
print("✅ Written: notes.txt")

# ── 2. Read a text file ───────────────────────────────────
print("\n📄 Reading notes.txt:")
with open("notes.txt", "r") as f:
    for line in f:
        print(f"  {line}", end="")

# ── 3. Append to a text file ──────────────────────────────
with open("notes.txt", "a") as f:
    f.write("5. TensorFlow/PyTorch for deep learning\n")
print("\n\n✅ Appended new line.")

# ── 4. Write a CSV file ───────────────────────────────────
students = [
    ["Name", "Score", "Grade"],
    ["Lydia",  95, "A"],
    ["Alice",  82, "B"],
    ["Bob",    71, "C"],
    ["Carol",  60, "D"],
]

with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(students)
print("\n✅ Written: students.csv")

# ── 5. Read a CSV file ────────────────────────────────────
print("\n📊 Reading students.csv:")
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['Name']:<10} Score: {row['Score']}  Grade: {row['Grade']}")

# Cleanup
os.remove("notes.txt")
os.remove("students.csv")
print("\n🧹 Temp files cleaned up.")
