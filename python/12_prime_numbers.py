# Python Program 12: Prime Numbers — Checker & Sieve
# Author: Lydia S. Makiwa
# Description: Checks if a number is prime and lists primes up to N

def is_prime(n):
    """Returns True if n is a prime number."""
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def sieve_of_eratosthenes(limit):
    """Returns all primes up to limit using the Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit+1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]

# Demo
print("=== Prime Number Programs ===\n")

# Check individual numbers
test_nums = [1, 2, 7, 15, 97, 100, 113]
for n in test_nums:
    result = "✅ Prime" if is_prime(n) else "❌ Not Prime"
    print(f"  {n:>4} → {result}")

# Sieve
limit = 50
primes = sieve_of_eratosthenes(limit)
print(f"\nAll primes up to {limit} ({len(primes)} total):")
print("  " + ", ".join(map(str, primes)))
