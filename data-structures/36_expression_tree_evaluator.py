# ==============================================================================
# Title: Expression Tree Evaluator (Postfix Expression)
# Author: Lydia S. Makiwa
# Date: June 3, 2026
# Description: Constructs a binary expression tree from a postfix expression
#              and evaluates the tree to compute the numeric result. Also includes
#              tree traversal methods (inorder, preorder, postorder).
#              Designed for DSA students learning tree construction and tree recursion.
# ==============================================================================

class Node:
    """Class representing a node in the expression tree."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def is_operator(c):
    """Utility function to check if character is an operator."""
    return c in ['+', '-', '*', '/', '^']

def construct_tree(postfix_expr):
    """
    Constructs an expression tree from a postfix expression.
    postfix_expr: a list of tokens/strings (e.g. ['4', '5', '+', '3', '*'])
    """
    stack = []
    
    for token in postfix_expr:
        # If token is operand, push to stack
        if not is_operator(token):
            stack.append(Node(token))
        # If token is operator, pop two elements, make them children, push parent
        else:
            node = Node(token)
            # The first popped is right child, second popped is left child
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
            
    return stack.pop()

def evaluate(root):
    """Recursively evaluates the expression tree and returns numerical value."""
    # Base Case: Empty Tree
    if root is None:
        return 0
        
    # Base Case: Leaf Node (Operand)
    if root.left is None and root.right is None:
        return float(root.value)
        
    # Evaluate left and right subtrees
    left_val = evaluate(root.left)
    right_val = evaluate(root.right)
    
    # Perform math operation based on parent operator
    if root.value == '+':
        return left_val + right_val
    elif root.value == '-':
        return left_val - right_val
    elif root.value == '*':
        return left_val * right_val
    elif root.value == '/':
        if right_val == 0:
            raise ZeroDivisionError("Division by zero in expression tree evaluation!")
        return left_val / right_val
    elif root.value == '^':
        return left_val ** right_val

def inorder_traversal(root, result=None):
    """Inorder Traversal (Left, Root, Right) -> Infix form"""
    if result is None:
        result = []
    if root:
        if is_operator(root.value):
            result.append('(')
        inorder_traversal(root.left, result)
        result.append(root.value)
        inorder_traversal(root.right, result)
        if is_operator(root.value):
            result.append(')')
    return "".join(result)

# --- Demo & Example ---
if __name__ == "__main__":
    print("--- Binary Expression Tree Evaluator Demo ---")
    
    # Postfix notation for: (4 + 5) * 3 - 8 / 2
    # Equivalent Postfix: 4 5 + 3 * 8 2 / -
    postfix_expression = ["4", "5", "+", "3", "*", "8", "2", "/", "-"]
    print(f"\nPostfix expression input: {' '.join(postfix_expression)}")
    
    # Construct tree
    root = construct_tree(postfix_expression)
    print("Expression tree successfully constructed.")
    
    # Traversal representation
    infix_expr = inorder_traversal(root)
    print(f"Reconstructed Infix expression: {infix_expr}")
    
    # Evaluate tree
    try:
        ans = evaluate(root)
        print(f"Evaluation Result: {ans}")
    except Exception as e:
        print(f"Error during evaluation: {e}")
