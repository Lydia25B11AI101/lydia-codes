# Python Program 21: List Comprehensions, Lambdas & Functional Tools
# Author: Lydia S. Makiwa
# Description: Pythonic coding using comprehensions, map, filter, reduce

from functools import reduce

# ── List Comprehensions ───────────────────────────────────
squares      = [x**2 for x in range(1, 11)]
evens        = [x for x in range(1, 21) if x % 2 == 0]
matrix       = [[i*j for j in range(1, 4)] for i in range(1, 4)]
words        = ["hello", "world", "python", "aiml"]
upper_long   = [w.upper() for w in words if len(w) > 4]

print("Squares (1–10):", squares)
print("Even numbers:  ", evens)
print("3×3 table:     ", matrix)
print("Long words:    ", upper_long)

# ── Dict & Set Comprehensions ─────────────────────────────
sq_dict = {x: x**2 for x in range(1, 6)}
unique  = {x % 5 for x in range(20)}
print("\nSquares dict:", sq_dict)
print("Unique mods: ", unique)

# ── Lambda Functions ──────────────────────────────────────
double   = lambda x: x * 2
is_even  = lambda x: x % 2 == 0
add      = lambda a, b: a + b

print("\nLambda double(7):", double(7))
print("Lambda is_even(4):", is_even(4))
print("Lambda add(3,5):  ", add(3, 5))

# ── map, filter, reduce ───────────────────────────────────
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("\nmap (x²):     ", list(map(lambda x: x**2, nums)))
print("filter (even):", list(filter(lambda x: x % 2 == 0, nums)))
print("reduce (sum): ", reduce(lambda a, b: a + b, nums))

# ── Sorting with key ──────────────────────────────────────
students = [("Lydia",95),("Alice",82),("Bob",71),("Carol",88)]
by_score  = sorted(students, key=lambda s: s[1], reverse=True)
print("\nRanked students:", by_score)
