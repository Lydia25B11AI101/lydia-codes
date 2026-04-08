# Python Program 5: Number Guessing Game
# Author: Lydia S. Makiwa

import random

def guessing_game():
    secret = random.randint(1, 100)
    attempts = 0
    print("🎮 Guess the number between 1 and 100!")

    while True:
        guess = int(input("Your guess: "))
        attempts += 1
        if guess < secret:
            print("📉 Too low! Try again.")
        elif guess > secret:
            print("📈 Too high! Try again.")
        else:
            print(f"🎉 Correct! You got it in {attempts} attempts.")
            break

guessing_game()
