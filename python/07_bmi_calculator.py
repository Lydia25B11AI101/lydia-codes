# Python Program 7: BMI Calculator
# Author: Lydia S. Makiwa
# Description: Calculates Body Mass Index and gives health advice

def bmi_category(bmi):
    if bmi < 18.5: return "Underweight 🟡"
    elif bmi < 25:  return "Normal weight ✅"
    elif bmi < 30:  return "Overweight 🟠"
    else:            return "Obese 🔴"

def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

print("=== BMI Calculator ===")
weight = float(input("Enter weight (kg): "))
height = float(input("Enter height (m): "))

bmi = calculate_bmi(weight, height)
category = bmi_category(bmi)

print(f"\nYour BMI: {bmi:.2f}")
print(f"Category: {category}")
print("\nBMI Ranges:")
print("  < 18.5  → Underweight")
print("  18.5–24.9 → Normal")
print("  25–29.9 → Overweight")
print("  ≥ 30    → Obese")
