# Python Program 18: OOP — Inheritance & Polymorphism
# Author: Lydia S. Makiwa
# Description: Animal hierarchy showing inheritance, override, and polymorphism

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age  = age

    def speak(self):
        return "..."

    def info(self):
        return f"{self.name} (age {self.age}): {self.speak()}"

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"


class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def speak(self):
        return "Woof! 🐶"

    def fetch(self):
        return f"{self.name} fetches the ball!"


class Cat(Animal):
    def speak(self):
        return "Meow! 🐱"

    def purr(self):
        return f"{self.name} purrs softly..."


class Bird(Animal):
    def __init__(self, name, age, can_fly=True):
        super().__init__(name, age)
        self.can_fly = can_fly

    def speak(self):
        return "Tweet! 🐦"

    def fly(self):
        return f"{self.name} {'soars through the sky!' if self.can_fly else 'cannot fly.'}"


# Demo — Polymorphism
animals = [
    Dog("Rex", 3, "Labrador"),
    Cat("Whiskers", 5),
    Bird("Tweety", 2),
    Bird("Penguin Pete", 4, can_fly=False),
]

print("=== Animal Kingdom ===")
for animal in animals:
    print(f"  {animal.info()}")

print(f"\n{animals[0].fetch()}")
print(animals[1].purr())
print(animals[2].fly())
print(animals[3].fly())
