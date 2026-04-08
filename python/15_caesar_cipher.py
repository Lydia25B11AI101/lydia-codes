# Python Program 15: Caesar Cipher — Encrypt & Decrypt
# Author: Lydia S. Makiwa
# Description: Classic encryption using character shifting

def caesar_encrypt(text, shift):
    """Encrypts text using Caesar cipher."""
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def brute_force(ciphertext):
    """Tries all 25 possible shifts."""
    print("\nBrute Force Attack:")
    for shift in range(1, 26):
        print(f"  Shift {shift:2}: {caesar_decrypt(ciphertext, shift)}")

# Demo
message = "Hello Lydia, Python is Amazing!"
shift = 7

encrypted = caesar_encrypt(message, shift)
decrypted = caesar_decrypt(encrypted, shift)

print(f"Original:  {message}")
print(f"Encrypted: {encrypted} (shift={shift})")
print(f"Decrypted: {decrypted}")
print(f"Match: {message == decrypted} ✅")
