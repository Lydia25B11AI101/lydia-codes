"""
Title: B-Tree Multi-way Search Tree (Insertion and Search)
Author: Lydia S. Makiwa
Date: June 06, 2026

Description:
This program implements a B-Tree from scratch in Python. A B-Tree is a self-balancing 
search tree data structure that maintains sorted data and allows searches, sequential 
access, insertions, and deletions in logarithmic time. B-Trees are widely used in 
databases and file systems to optimize read/write operations on large blocks of data.

Teaches: Multi-way node splitting, tree traversals, and disk-aware structures.
"""

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.child = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t # Minimum degree of the tree

    def search(self, k, x=None):
        # Search for a key in the B-Tree.
        if x is None:
            x = self.root
            
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
            
        if i < len(x.keys) and k == x.keys[i]:
            return (x, i)
        elif x.leaf:
            return None
        else:
            return self.search(k, x.child[i])

    def insert(self, k):
        # Insert a new key into the B-Tree.
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            # Root is full, split it and create a new root
            temp = BTreeNode(False)
            self.root = temp
            temp.child.insert(0, root)
            self._split_child(temp, 0, root)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            # Insert the key in the correct position
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            # Find which child is going to have the new key
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                # Child is full, split it
                self._split_child(x, i, x.child[i])
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.child[i], k)

    def _split_child(self, x, i, y):
        # Create a new node to store (t-1) keys of y
        z = BTreeNode(y.leaf)
        t = self.t
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t]

    def display(self, node=None, indent=""):
        # Recursively prints the structure of the B-Tree.
        if node is None:
            node = self.root
        print(indent + str(node.keys))
        if not node.leaf:
            for child in node.child:
                self.display(child, indent + "    ")

def run_btree_demo():
    print("=== Multi-way B-Tree Demonstration ===")
    # Create a B-Tree with minimum degree t=3
    # Every node (except root) must contain between 2 and 5 keys.
    btree = BTree(t=3)
    
    keys = [10, 20, 5, 6, 12, 30, 7, 17]
    for key in keys:
        print(f"Inserting {key}...")
        btree.insert(key)
        
    print("\nB-Tree structure hierarchy:")
    btree.display()
    
    # Search for keys
    print("\nSearching B-Tree:")
    for search_key in [12, 100]:
        res = btree.search(search_key)
        print(f"Key {search_key:3d}: {'FOUND' if res else 'NOT FOUND'}")

if __name__ == "__main__":
    run_btree_demo()
