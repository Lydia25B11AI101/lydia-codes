# Python Program 3: Fibonacci Sequence
# Author: Lydia S. Makiwa

def fibonacci(n):
    """Returns a list of the first n Fibonacci numbers."""
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib[:n]

n = int(input("How many Fibonacci numbers? "))
print(f"First {n} Fibonacci numbers: {fibonacci(n)}")
