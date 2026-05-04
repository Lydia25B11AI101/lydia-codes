# ============================================================
# Program Title : Red-Black Tree (Insertion)
# Author        : Lydia S. Makiwa
# Date          : 2026-05-04
# Description   : Implement a Red-Black BST with insertion
#                 and in-order traversal. Balancing is done
#                 via rotations and re-colouring.
# ============================================================

RED, BLACK = 'R', 'B'

class Node:
    def __init__(self, key):
        self.key    = key
        self.color  = RED
        self.left   = None
        self.right  = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.NIL  = Node(0)
        self.NIL.color = BLACK
        self.root = self.NIL

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL: y.left.parent = x
        y.parent = x.parent
        if x.parent is None: self.root = y
        elif x == x.parent.left: x.parent.left = y
        else: x.parent.right = y
        y.left = x; x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL: y.right.parent = x
        y.parent = x.parent
        if x.parent is None: self.root = y
        elif x == x.parent.right: x.parent.right = y
        else: x.parent.left = y
        y.right = x; x.parent = y

    def insert(self, key):
        z = Node(key)
        z.left = z.right = self.NIL
        y, x = None, self.root
        while x != self.NIL:
            y = x
            x = x.left if z.key < x.key else x.right
        z.parent = y
        if y is None: self.root = z
        elif z.key < y.key: y.left = z
        else: y.right = z
        self._fix_insert(z)

    def _fix_insert(self, z):
        while z.parent and z.parent.color == RED:
            gp = z.parent.parent
            if z.parent == gp.left:
                uncle = gp.right
                if uncle.color == RED:
                    z.parent.color = uncle.color = BLACK
                    gp.color = RED; z = gp
                else:
                    if z == z.parent.right:
                        z = z.parent; self._left_rotate(z)
                    z.parent.color = BLACK; gp.color = RED
                    self._right_rotate(gp)
            else:
                uncle = gp.left
                if uncle.color == RED:
                    z.parent.color = uncle.color = BLACK
                    gp.color = RED; z = gp
                else:
                    if z == z.parent.left:
                        z = z.parent; self._right_rotate(z)
                    z.parent.color = BLACK; gp.color = RED
                    self._left_rotate(gp)
        self.root.color = BLACK

    def inorder(self, node=None):
        if node is None: node = self.root
        result = []
        def _in(n):
            if n != self.NIL:
                _in(n.left)
                result.append(f'{n.key}({n.color})')
                _in(n.right)
        _in(node)
        return result

# Demo
rbt = RedBlackTree()
for k in [10, 20, 30, 15, 5, 25, 35, 1]:
    rbt.insert(k)
print('In-order traversal (key(colour)):')
print(' -> '.join(rbt.inorder()))
print('Root is always BLACK:', rbt.root.color == 'B')
print('Red-Black Tree insertion demo complete!')
