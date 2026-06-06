"""
Title: Hybrid Least Recently Used (LRU) and Least Frequently Used (LFU) Cache
Author: Lydia S. Makiwa
Date: June 06, 2026

Description:
This program implements a hybrid LRU-LFU cache policy from scratch in Python.
Normal caches use LRU (evicting the oldest items) or LFU (evicting the least 
frequently used items). This hybrid cache balances both strategies by weighting
the frequency of access and the recency of access. 

Teaches: Doubly linked lists, custom hashing, cache eviction strategies, and 
advanced object design.
"""

import time

class CacheNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1
        self.last_accessed = time.time()
        self.prev = None
        self.next = None

class HybridCache:
    def __init__(self, capacity=4):
        self.capacity = capacity
        self.cache = {} # maps key to CacheNode
        self.head = CacheNode(None, None) # Dummy head
        self.tail = CacheNode(None, None) # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node):
        # Removes a node from the doubly linked list.
        prev = node.prev
        next_node = node.next
        prev.next = next_node
        next_node.prev = prev

    def _add_to_head(self, node):
        # Adds a node directly behind the dummy head (most recently used position).
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _update_recency(self, node):
        # Moves an accessed node to the head of the list and updates metadata.
        self._remove_node(node)
        self._add_to_head(node)
        node.freq += 1
        node.last_accessed = time.time()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._update_recency(node)
            return node.value
        return -1

    def put(self, key, value):
        if self.capacity <= 0:
            return

        # If key already exists, update its value and recency
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._update_recency(node)
            return

        # Cache is full - run Hybrid eviction
        if len(self.cache) >= self.capacity:
            # Hybrid Cost Function: Cost = (Frequency * Weight_F) + (Recency_Age * Weight_R)
            # To simplify, we evict the node with the lowest overall score = Freq - (Current_Time - Last_Accessed)*10
            # A node with high freq but very old accesses might still be evicted.
            current_time = time.time()
            least_valuable_node = None
            min_score = float('inf')

            # Scan the list from tail (oldest recency) to find best victim
            curr = self.tail.prev
            while curr != self.head:
                recency_age = current_time - curr.last_accessed
                # Score = Frequency - (Age factor)
                # Lower score means older or less used.
                score = curr.freq - (recency_age * 0.1)
                
                if score < min_score:
                    min_score = score
                    least_valuable_node = curr
                curr = curr.prev

            if least_valuable_node:
                # Evict selected node
                self._remove_node(least_valuable_node)
                del self.cache[least_valuable_node.key]
                print(f"Cache Eviction: Removed key '{least_valuable_node.key}' (Freq: {least_valuable_node.freq})")

        # Insert new node
        new_node = CacheNode(key, value)
        self.cache[key] = new_node
        self._add_to_head(new_node)
        print(f"Inserted: {key} -> {value}")

    def print_cache_state(self):
        print("Current Cache (Most Recent -> Oldest):")
        curr = self.head.next
        while curr != self.tail:
            print(f"  [{curr.key}: {curr.value} (Freq: {curr.freq})]", end="")
            curr = curr.next
        print("\n")

def run_cache_demo():
    print("=== Hybrid LRU-LFU Cache Demonstration ===")
    cache = HybridCache(capacity=3)
    
    cache.put("A", "Apple")
    cache.put("B", "Banana")
    cache.put("C", "Cherry")
    cache.print_cache_state()
    
    # Access "A" and "B" to raise their frequencies
    cache.get("A")
    cache.get("A")
    cache.get("B")
    cache.print_cache_state()
    
    # Put "D" which triggers eviction of "C" because "C" has freq=1 and is older than D
    cache.put("D", "Dragonfruit")
    cache.print_cache_state()

if __name__ == "__main__":
    run_cache_demo()
