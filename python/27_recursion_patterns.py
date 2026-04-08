# Python Program 27: Recursion — Classic Problems
# Author: Lydia S. Makiwa
# Description: Solves classic recursion problems step by step

import functools

def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

# ── 1. Factorial ──────────────────────────────────────────
def factorial(n):
    if n == 0: return 1
    return n * factorial(n - 1)

# ── 2. Fibonacci (memoised) ───────────────────────────────
@memoize
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

# ── 3. Sum of digits ──────────────────────────────────────
def sum_digits(n):
    if n == 0: return 0
    return n % 10 + sum_digits(n // 10)

# ── 4. Power ──────────────────────────────────────────────
def power(base, exp):
    if exp == 0: return 1
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    return base * power(base, exp - 1)

# ── 5. Flatten nested list ────────────────────────────────
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

print("=== Recursion Patterns ===\n")
print("Factorials:")
for n in [0, 1, 5, 10, 12]:
    print(f"  {n}! = {factorial(n)}")

print("\nFibonacci (first 15):")
print("  ", [fib(i) for i in range(15)])

print("\nSum of digits:")
for n in [1234, 99999, 100]:
    print(f"  sum_digits({n}) = {sum_digits(n)}")

print("\nPower (fast exponentiation):")
print(f"  2^10 = {power(2,10)}, 3^5 = {power(3,5)}")

print("\nFlatten nested list:")
nested = [1, [2, 3], [4, [5, 6]], 7, [[8, 9], 10]]
print(f"  {nested}")
print(f"  → {flatten(nested)}")
