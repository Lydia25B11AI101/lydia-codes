# ============================================================
# Program Title : LRU Cache (Least Recently Used)
# Author        : Lydia S. Makiwa
# Date          : 2026-05-03
# Description   : O(1) get & put using an OrderedDict-backed
#                 LRU Cache — a classic interview question.
# ============================================================

from collections import OrderedDict

class LRUCache:
    """
    LRU Cache with O(1) get and put.
    Uses Python's OrderedDict to maintain insertion order.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache    = OrderedDict()

    def get(self, key: int) -> int:
        """Return value if key exists (and mark as recently used), else -1."""
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)   # mark as most recently used
        return self.cache[key]

    def put(self, key: int, value: int):
        """Insert or update key. Evict LRU item if capacity exceeded."""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            evicted = self.cache.popitem(last=False)   # remove LRU (front)
            print(f"  [evict] key={evicted[0]}, val={evicted[1]}")

    def __repr__(self):
        items = list(self.cache.items())
        return "LRU→MRU: " + " | ".join(f"{k}:{v}" for k,v in items)


# ── Demo ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("LRU Cache Demo (capacity = 3)")
    print("=" * 40)
    lru = LRUCache(3)

    ops = [
        ("put", 1, 10), ("put", 2, 20), ("put", 3, 30),
        ("get", 1, None),               # access key 1 → moves to MRU
        ("put", 4, 40),                 # evicts key 2 (LRU)
        ("get", 2, None),               # miss → -1
        ("put", 5, 50),                 # evicts key 3
    ]

    for op in ops:
        if op[0] == "put":
            print(f"put({op[1]}, {op[2]})")
            lru.put(op[1], op[2])
        else:
            result = lru.get(op[1])
            print(f"get({op[1]}) → {result}")
        print(f"  {lru}")
