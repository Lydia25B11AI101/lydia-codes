# Python Program 20: Exception Handling
# Author: Lydia S. Makiwa
# Description: try/except/else/finally and custom exceptions

class InsufficientFundsError(Exception):
    """Custom exception for bank operations."""
    def __init__(self, amount, balance):
        self.amount  = amount
        self.balance = balance
        super().__init__(f"Cannot withdraw R{amount}. Balance: R{balance}")


def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print(f"  ❌ ZeroDivisionError: Cannot divide {a} by 0")
        return None
    except TypeError as e:
        print(f"  ❌ TypeError: {e}")
        return None
    else:
        print(f"  ✅ {a} / {b} = {result:.4f}")
        return result
    finally:
        print(f"  (division attempt for {a} / {b} completed)")


def read_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"  ❌ File '{filename}' not found.")
    except PermissionError:
        print(f"  ❌ No permission to read '{filename}'.")
    return None


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(amount, balance)
    return balance - amount


print("=== Exception Handling Demo ===\n")

print("1. Division tests:")
safe_divide(10, 2)
safe_divide(10, 0)
safe_divide(10, "x")

print("\n2. File tests:")
read_file("nonexistent.txt")

print("\n3. Custom exception test:")
try:
    new_balance = withdraw(500, 1000)
except InsufficientFundsError as e:
    print(f"  ❌ {e}")

try:
    new_balance = withdraw(500, 200)
    print(f"  ✅ Withdrawal successful. New balance: R{new_balance}")
except InsufficientFundsError as e:
    print(f"  ❌ {e}")
