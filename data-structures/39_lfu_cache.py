# Program Title: Least Frequently Used (LFU) Cache Implementation
# Author: Lydia S. Makiwa
# Date: June 5, 2026
# Description: Implements a Least Frequently Used (LFU) caching system from scratch in Python.
#              This implementation uses a hash map to map keys to values, and another hash map
#              to map frequency values to an OrderedDict of corresponding keys (effectively grouping
#              keys by active frequencies to support O(1) average time complexity for both get and put).
#              Ideal for students looking to learn production-grade system designs.

from collections import OrderedDict, defaultdict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # Maps key to its value
        self.key_to_val = {}
        # Maps key to its frequency
        self.key_to_freq = {}
        # Maps frequency to OrderedDict of keys with that frequency (preserves insertion/update order)
        self.freq_to_keys = defaultdict(OrderedDict)
        self.min_freq = 0

    def _update_frequency(self, key: int):
        # Retrieve the current frequency of the key
        freq = self.key_to_freq[key]
        
        # Remove the key from the old frequency list
        del self.freq_to_keys[freq][key]
        
        # If the old frequency list is empty and was the minimum frequency, increment the minimum frequency
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
                
        # Update frequency and insert key into the new frequency list
        new_freq = freq + 1
        self.key_to_freq[key] = new_freq
        self.freq_to_keys[new_freq][key] = None

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        
        # Access counts as an update to frequency
        self._update_frequency(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        # If the key already exists, update value and access frequency
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._update_frequency(key)
            return

        # If cache is full, evict the least frequently used key (LRU tie-breaker)
        if len(self.key_to_val) >= self.capacity:
            # Pop the first key (least recently used) from the min_freq group
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            
            # Clean up other mappings
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]
            print(f"  [Eviction] Cache full. Evicting key {evict_key} (Min Freq: {self.min_freq})")

        # Insert new key
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.min_freq = 1
        self.freq_to_keys[1][key] = None

    def display(self):
        print(f"  Current cache state: {self.key_to_val}")
        print(f"  Key Frequencies: {self.key_to_freq}")

if __name__ == "__main__":
    print("=== LFU Cache Demo (Capacity = 2) ===")
    cache = LFUCache(2)
    
    print("\n1. putting (1, 10) and (2, 20):")
    cache.put(1, 10)
    cache.put(2, 20)
    cache.display()
    
    print("\n2. getting key 1 (value should be 10):")
    print(f"  get(1) -> {cache.get(1)}")
    cache.display()
    
    print("\n3. putting (3, 30) (should evict key 2 because key 1 frequency is 2 and key 2 frequency is 1):")
    cache.put(3, 30)
    cache.display()
    
    print("\n4. getting key 2 (should return -1):")
    print(f"  get(2) -> {cache.get(2)}")
    
    print("\n5. getting key 3 (value should be 30):")
    print(f"  get(3) -> {cache.get(3)}")
    cache.display()
