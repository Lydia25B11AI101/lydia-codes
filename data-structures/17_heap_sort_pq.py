# ============================================================
# Program Title : Heap Sort & Priority Queue
# Author        : Lydia S. Makiwa
# Date          : 2026-05-02
# Description   : Heap sort using Python's heapq module, plus
#                 a priority queue for task scheduling.
# ============================================================

import heapq

# ---- Heap Sort -----------------------------------------------
def heap_sort(arr):
    heap = arr[:]
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]


# ---- Priority Queue (task scheduler) -------------------------
class Task:
    def __init__(self, name, priority):
        self.name     = name
        self.priority = priority  # lower number = higher priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Task('{self.name}', priority={self.priority})"


class PriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, task):
        heapq.heappush(self._heap, task)
        print(f"  Added: {task}")

    def pop(self):
        return heapq.heappop(self._heap)

    def __len__(self):
        return len(self._heap)


# -- Demo ------------------------------------------------------
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    print("Heap Sort:")
    print(f"  Before: {data}")
    print(f"  After : {heap_sort(data)}")

    print("\nPriority Queue (task scheduler):")
    pq = PriorityQueue()
    pq.push(Task("Send report",     3))
    pq.push(Task("Fix critical bug",1))
    pq.push(Task("Update docs",     5))
    pq.push(Task("Code review",     2))

    print("\nProcessing tasks:")
    while pq:
        t = pq.pop()
        print(f"  Processing: {t}")
