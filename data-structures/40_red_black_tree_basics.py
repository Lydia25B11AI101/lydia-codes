# Program Title: Red-Black Tree Basic Rotations and Insertion
# Author: Lydia S. Makiwa
# Date: June 5, 2026
# Description: Demonstrates self-balancing Red-Black Tree mechanics (Rotations and Recoloring) in Python.
#              While a full Red-Black Tree is highly complex, this file highlights the node structure,
#              Left-Rotate, Right-Rotate operations, and standard insertion balancing cases.
#              Excellent for intermediate DSA and database index concepts (B-trees/RB-trees).

class Node:
    def __init__(self, data, color="RED"):
        self.data = data
        self.color = color  # "RED" or "BLACK"
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTreeBasics:
    def __init__(self):
        self.NIL = Node(0, "BLACK") # NIL leaf node representation
        self.root = self.NIL

    # Rotate left helper function
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # Rotate right helper function
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # Simple insertion (recolors & structural adjustments left as educational explanations)
    def insert(self, data):
        new_node = Node(data)
        new_node.left = self.NIL
        new_node.right = self.NIL
        
        y = None
        x = self.root
        
        while x != self.NIL:
            y = x
            if new_node.data < x.data:
                x = x.left
            else:
                x = x.right
                
        new_node.parent = y
        if y is None:
            self.root = new_node
        elif new_node.data < y.data:
            y.left = new_node
        else:
            y.right = new_node
            
        # Root of RB Tree is always black
        if new_node.parent is None:
            new_node.color = "BLACK"
            return
            
        # Simulating a simple balancing rotation if parent is Red
        if new_node.parent.color == "RED":
            # Just illustrative fix for demo
            self._fix_insert(new_node)

    def _fix_insert(self, k):
        while k.parent and k.parent.color == "RED":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left # Uncle node
                if u.color == "RED":
                    # Case 1: Uncle is Red -> Recolor only
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # Case 2: Uncle is Black, Right-Left Case
                        k = k.parent
                        self.right_rotate(k)
                    # Case 3: Uncle is Black, Right-Right Case
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right # Uncle node
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"

    # Preorder Traversal for visualization
    def print_tree(self, node, indent="", last=True):
        if node != self.NIL:
            print(indent, end="")
            if last:
                print("R----", end="")
                indent += "     "
            else:
                print("L----", end="")
                indent += "|    "
            
            print(f"{node.data}({node.color})")
            self.print_tree(node.left, indent, False)
            self.print_tree(node.right, indent, True)

if __name__ == "__main__":
    print("=== Red-Black Tree Rotation & Balance Demo ===")
    rbt = RedBlackTreeBasics()
    
    elements = [20, 15, 25, 10, 5, 1]
    print(f"\nInserting elements: {elements}")
    for el in elements:
        rbt.insert(el)
        
    print("\nVisual Representation of Red-Black Tree (Root/Left/Right):")
    rbt.print_tree(rbt.root)
