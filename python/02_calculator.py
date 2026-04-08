# Python Program 2: Basic Calculator
# Author: Lydia S. Makiwa

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else "Error: Division by zero"

print("=== Basic Calculator ===")
a = float(input("Enter first number: "))
op = input("Enter operator (+, -, *, /): ")
b = float(input("Enter second number: "))

ops = {'+': add, '-': subtract, '*': multiply, '/': divide}
result = ops.get(op, lambda a, b: "Invalid operator")(a, b)
print(f"Result: {a} {op} {b} = {result}")
