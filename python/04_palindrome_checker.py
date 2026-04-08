# Python Program 4: Palindrome Checker
# Author: Lydia S. Makiwa

def is_palindrome(s):
    """Checks if a string is a palindrome (ignores case and spaces)."""
    cleaned = s.replace(" ", "").lower()
    return cleaned == cleaned[::-1]

words = ["racecar", "hello", "madam", "python", "level"]
for word in words:
    result = "✅ Palindrome" if is_palindrome(word) else "❌ Not a palindrome"
    print(f"{word:10} → {result}")
