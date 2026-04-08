# Python Program 8: Random Password Generator
# Author: Lydia S. Makiwa
# Description: Generates secure random passwords with custom settings

import random
import string

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    """Generates a random password based on given criteria."""
    chars = string.ascii_lowercase
    if use_upper:   chars += string.ascii_uppercase
    if use_digits:  chars += string.digits
    if use_symbols: chars += string.punctuation

    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase) if use_upper else '',
        random.choice(string.digits) if use_digits else '',
        random.choice(string.punctuation) if use_symbols else '',
    ]
    password += [random.choice(chars) for _ in range(length - len(password))]
    random.shuffle(password)
    return ''.join(password)

print("=== Password Generator ===")
length = int(input("Password length (default 12): ") or 12)
print("\nGenerated Passwords:")
for i in range(5):
    print(f"  {i+1}. {generate_password(length)}")
