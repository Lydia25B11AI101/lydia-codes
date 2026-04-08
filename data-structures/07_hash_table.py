# Data Structure 7: Hash Table (from scratch)
# Author: Lydia S. Makiwa
# Description: Custom hash table with chaining for collision handling

class HashTable:
    def __init__(self, size=10):
        self.size  = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        idx    = self._hash(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                print(f"Updated: {key} → {value}")
                return
        bucket.append((key, value))
        print(f"Inserted: {key} → {value}")

    def get(self, key):
        for k, v in self.table[self._hash(key)]:
            if k == key: return v
        return None

    def delete(self, key):
        idx    = self._hash(key)
        bucket = self.table[idx]
        self.table[idx] = [(k, v) for k, v in bucket if k != key]
        print(f"Deleted: {key}")

    def display(self):
        print("\nHash Table:")
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"  [{i}] {bucket}")

# Demo
ht = HashTable()
ht.insert("name",  "Lydia Makiwa")
ht.insert("major", "AIML")
ht.insert("year",  "1st Year")
ht.insert("lang",  "Python")
ht.display()
print(f"\nGet 'name': {ht.get('name')}")
ht.delete("year")
ht.display()
