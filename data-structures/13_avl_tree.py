# ============================================================
# Program Title : AVL Tree (Self-Balancing Binary Search Tree)
# Author        : Lydia S. Makiwa
# Date          : 2026-04-09
# Description   : Implements an AVL tree with insert and
#                 rotations (LL, RR, LR, RL). The tree
#                 automatically balances after every insertion.
# ============================================================

class AVLNode:
    """A single node in an AVL tree."""
    def __init__(self, key):
        self.key    = key
        self.left   = None
        self.right  = None
        self.height = 1  # new node is always a leaf

class AVLTree:
    # ── Helpers ───────────────────────────────────────────────
    def height(self, node):
        return node.height if node else 0

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    # ── Rotations ─────────────────────────────────────────────
    def rotate_right(self, y):
        """Right rotation around y (fixes Left-Left imbalance)."""
        x  = y.left
        T2 = x.right
        x.right = y
        y.left  = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x):
        """Left rotation around x (fixes Right-Right imbalance)."""
        y  = x.right
        T2 = y.left
        y.left  = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    # ── Insert ────────────────────────────────────────────────
    def insert(self, root, key):
        """BST insert + rebalance."""
        # Step 1: Normal BST insert
        if not root:
            return AVLNode(key)
        if key < root.key:
            root.left  = self.insert(root.left,  key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root  # duplicates not allowed

        # Step 2: Update height
        self.update_height(root)

        # Step 3: Check balance and rotate if needed
        bf = self.balance_factor(root)

        # Left-Left
        if bf > 1 and key < root.left.key:
            return self.rotate_right(root)
        # Right-Right
        if bf < -1 and key > root.right.key:
            return self.rotate_left(root)
        # Left-Right
        if bf > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        # Right-Left
        if bf < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def inorder(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.inorder(root.left, result)
            result.append(root.key)
            self.inorder(root.right, result)
        return result

    def print_tree(self, root, indent=0, label="Root"):
        if root:
            print(" " * indent + f"[{label}] {root.key} (h={root.height})")
            self.print_tree(root.left,  indent + 6, "L")
            self.print_tree(root.right, indent + 6, "R")

# -- Demo --------------------------------------------------
if __name__ == "__main__":
    tree = AVLTree()
    root = None

    keys = [10, 20, 30, 40, 50, 25, 5, 15]
    print("Inserting:", keys)
    for k in keys:
        root = tree.insert(root, k)

    print("\nTree Structure (indented):")
    tree.print_tree(root)

    print("\nIn-order traversal (should be sorted):")
    print(tree.inorder(root))

    print("\nRoot balance factor:", tree.balance_factor(root))
    print("Tree height:", tree.height(root))
