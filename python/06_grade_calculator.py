# Python Program 6: Simple Student Grade Calculator
# Author: Lydia S. Makiwa

def get_grade(score):
    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"

students = {
    "Alice": [85, 90, 78],
    "Bob": [60, 55, 70],
    "Lydia": [95, 98, 100],
}

print(f"{'Name':<10} {'Average':>8} {'Grade':>6}")
print("-" * 28)
for name, scores in students.items():
    avg = sum(scores) / len(scores)
    print(f"{name:<10} {avg:>8.1f} {get_grade(avg):>6}")
