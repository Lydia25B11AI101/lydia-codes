"""
Title: Skip List Probabilistic Data Structure in Python
Author: Lydia S. Makiwa
Date: June 06, 2026

Description:
This program implements a Skip List, which is a probabilistic data structure 
that allows fast search, insertion, and deletion within an ordered sequence of 
elements. It achieves O(log n) average time complexity for these operations 
by maintaining a hierarchy of linked lists where each higher level skips over 
elements to act as an express lane.

Highly useful for intermediate/advanced AIML students to study probabilistic data structures.
"""

import random

class Node:
    def __init__(self, key, level):
        self.key = key
        # List of pointers to next nodes at different levels
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=4, p=0.5):
        self.max_level = max_level
        self.p = p
        # Header node initialized with key -1 (representing negative infinity)
        self.header = Node(-1, self.max_level)
        self.level = 0 # Current maximum level of the skip list

    def random_level(self):
        # Coin toss to determine the level of a new node.
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, key):
        # Inserts a key into the skip list.
        # update keeps track of the nodes whose forward pointers will need update
        update = [None] * (self.max_level + 1)
        current = self.header

        # Search for position to insert the key
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        # Move to level 0 (base list)
        current = current.forward[0]

        # If key is not present, insert it
        if current is None or current.key != key:
            r_level = self.random_level()

            # If random level is greater than current max level, update header pointers
            if r_level > self.level:
                for i in range(self.level + 1, r_level + 1):
                    update[i] = self.header
                self.level = r_level

            # Create new node
            new_node = Node(key, r_level)

            # Insert node by updating pointers
            for i in range(r_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node
                
            print(f"Inserted key {key} at level {r_level}")

    def search(self, key):
        # Searches for a key in the skip list. Returns True if found, False otherwise.
        current = self.header

        # Start from top level and move down
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        current = current.forward[0]

        if current and current.key == key:
            return True
        return False

    def display(self):
        # Prints the skip list levels nicely.
        print("\n--- Skip List Representation ---")
        for lvl in range(self.level + 1):
            print(f"Level {lvl}: ", end="")
            node = self.header.forward[lvl]
            while node:
                print(f"{node.key} -> ", end="")
                node = node.forward[lvl]
            print("None")
        print("--------------------------------")

def run_skip_list_demo():
    print("=== Probabilistic Skip List Demonstration ===")
    lst = SkipList()
    
    keys = [3, 9, 12, 19, 17, 26, 21, 25]
    for key in keys:
        lst.insert(key)
        
    lst.display()
    
    # Search for items
    for search_key in [19, 15, 26]:
        found = lst.search(search_key)
        print(f"Searching for {search_key}: {'FOUND' if found else 'NOT FOUND'}")

if __name__ == "__main__":
    run_skip_list_demo()
