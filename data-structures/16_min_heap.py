# ============================================================
# Program Title : Min-Heap Implementation
# Author        : Lydia S. Makiwa
# Date          : 2026-05-02
# Description   : Min-heap (priority queue) built from scratch.
#                 Supports insert, extract-min, and heapify.
# ============================================================

class MinHeap:
    def __init__(self):
        self.data = []

    def _parent(self, i): return (i - 1) // 2
    def _left(self, i):   return 2 * i + 1
    def _right(self, i):  return 2 * i + 2

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def insert(self, val):
        self.data.append(val)
        self._bubble_up(len(self.data) - 1)

    def _bubble_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self.data[i] < self.data[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def extract_min(self):
        if not self.data:
            raise IndexError("Heap is empty")
        if len(self.data) == 1:
            return self.data.pop()
        min_val = self.data[0]
        self.data[0] = self.data.pop()   # move last to root
        self._heapify_down(0)
        return min_val

    def _heapify_down(self, i):
        n = len(self.data)
        while True:
            smallest = i
            l, r = self._left(i), self._right(i)
            if l < n and self.data[l] < self.data[smallest]: smallest = l
            if r < n and self.data[r] < self.data[smallest]: smallest = r
            if smallest == i: break
            self._swap(i, smallest)
            i = smallest

    def peek(self):
        return self.data[0] if self.data else None

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"MinHeap({self.data})"


# -- Demo ------------------------------------------------------
if __name__ == "__main__":
    h = MinHeap()
    for v in [50, 30, 20, 15, 10, 8, 25]:
        h.insert(v)
    print("Heap after inserts:", h)

    print("\nExtracting in sorted order:")
    while h:
        print(f"  {h.extract_min()}", end="")
    print()
