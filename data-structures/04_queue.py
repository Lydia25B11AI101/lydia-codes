# Data Structure 4: Queue Implementation
# Author: Lydia S. Makiwa
# Description: Queue using a list (FIFO — First In, First Out)

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)
        print(f"Enqueued: {item}")

    def dequeue(self):
        if self.is_empty():
            print("Queue Underflow! Queue is empty.")
            return None
        item = self.items.pop(0)
        print(f"Dequeued: {item}")
        return item

    def peek(self):
        return self.items[0] if not self.is_empty() else None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def display(self):
        print(f"Queue (front → rear): {self.items}")

# Demo
q = Queue()
for val in [10, 20, 30, 40, 50]:
    q.enqueue(val)
q.display()
q.dequeue()
q.dequeue()
q.display()
print(f"Front element: {q.peek()}")
print(f"Queue size: {q.size()}")
