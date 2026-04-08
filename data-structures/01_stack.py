# Data Structure 1: Stack Implementation
# Author: Lydia S. Makiwa

class Stack:
    """A simple stack using a Python list (LIFO)."""

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
        print(f"Pushed: {item}")

    def pop(self):
        if self.is_empty():
            print("Stack Underflow! Stack is empty.")
            return None
        item = self.items.pop()
        print(f"Popped: {item}")
        return item

    def peek(self):
        return self.items[-1] if not self.is_empty() else None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def display(self):
        print(f"Stack (top → bottom): {self.items[::-1]}")


# Demo
s = Stack()
s.push(10)
s.push(20)
s.push(30)
s.display()
s.pop()
s.display()
print(f"Top element: {s.peek()}")
