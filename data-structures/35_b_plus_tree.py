"""
Program Title: B+ Tree Basic Implementation (Insertion & Search)
Author: Lydia S. Makiwa
Date: June 2, 2026

Description:
A simplified, highly educational implementation of a B+ Tree of order 3 (Max 3 keys per node).
B+ Trees are balanced search trees optimal for system storage and database indexing operations.
This implements node-splitting insertion and tree searches.
"""

import math

class BPlusNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = [] # Child nodes if internal, or None/leaf-links if leaf
        self.next = None   # Direct pointer to next leaf node (for range queries)

class BPlusTree:
    def __init__(self, order=3):
        self.root = BPlusNode(is_leaf=True)
        self.order = order # Maximum branches (order)

    def search(self, key):
        """
        Traverse down to leaf node to locate a key.
        """
        current = self.root
        while not current.is_leaf:
            i = 0
            while i < len(current.keys) and key >= current.keys[i]:
                i += 1
            current = current.children[i]
        
        # Check if key is in the leaf node
        return key in current.keys

    def insert(self, key):
        """
        Insert key. Splits recursively from bottom up when nodes exceed size constraints.
        """
        root = self.root
        if len(root.keys) == self.order:
            new_root = BPlusNode(is_leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0, self.root)
            self.root = new_root
            
        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        if node.is_leaf:
            # Insert key in sorted order
            node.keys.append(key)
            node.keys.sort()
        else:
            # Find which child to traverse
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            child = node.children[i]
            if len(child.keys) == self.order:
                self._split_child(node, i, child)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent, i, child):
        mid = len(child.keys) // 2
        split_key = child.keys[mid]
        
        new_node = BPlusNode(is_leaf=child.is_leaf)
        
        # Parent gains a key and child pointer
        parent.keys.insert(i, split_key)
        parent.children.insert(i + 1, new_node)
        
        # Split keys/children
        if child.is_leaf:
            new_node.keys = child.keys[mid:]
            child.keys = child.keys[:mid]
            # Link leaf node pointers
            new_node.next = child.next
            child.next = new_node
        else:
            new_node.keys = child.keys[mid + 1:]
            child.keys = child.keys[:mid]
            new_node.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]

# --- Working Demo ---
if __name__ == "__main__":
    print("--- B+ Tree Data Structure Operations ---")
    
    # Initialize a B+ Tree of order 3
    bptree = BPlusTree(order=3)
    
    # Insert values
    values_to_insert = [5, 15, 25, 35, 45, 10, 20]
    print(f"Inserting numbers: {values_to_insert}")
    for value in values_to_insert:
        bptree.insert(value)
        
    print("\nRoot Node Keys: ", bptree.root.keys)
    
    # Search for specific keys
    queries = [15, 30, 45, 100]
    print("\nSearching B+ Tree:")
    for q in queries:
        found = bptree.search(q)
        print(f"  Key {q:3d} Present: {found}")