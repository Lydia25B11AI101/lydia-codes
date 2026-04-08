# Data Structure 5: Binary Search Tree (BST)
# Author: Lydia S. Makiwa
# Description: Insert, search, and traverse a BST

class Node:
    def __init__(self, data):
        self.data  = data
        self.left  = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        self.root = self._insert(self.root, data)

    def _insert(self, node, data):
        if node is None:
            return Node(data)
        if data < node.data:
            node.left  = self._insert(node.left, data)
        elif data > node.data:
            node.right = self._insert(node.right, data)
        return node

    def search(self, data):
        return self._search(self.root, data)

    def _search(self, node, data):
        if node is None:          return False
        if node.data == data:     return True
        if data < node.data:      return self._search(node.left, data)
        return self._search(node.right, data)

    def inorder(self, node=None, first=True):
        if first: node = self.root
        if node:
            self.inorder(node.left,  False)
            print(node.data, end=" ")
            self.inorder(node.right, False)

    def preorder(self, node=None, first=True):
        if first: node = self.root
        if node:
            print(node.data, end=" ")
            self.preorder(node.left,  False)
            self.preorder(node.right, False)

# Demo
bst = BST()
for val in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(val)

print("Inorder  (sorted):", end=" "); bst.inorder();  print()
print("Preorder (root first):", end=" "); bst.preorder(); print()
print(f"Search 40: {'Found ✅' if bst.search(40) else 'Not found ❌'}")
print(f"Search 99: {'Found ✅' if bst.search(99) else 'Not found ❌'}")
