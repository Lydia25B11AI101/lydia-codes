# Python Program 14: Matrix Operations (without NumPy)
# Author: Lydia S. Makiwa
# Description: Add, subtract, transpose, and multiply matrices manually

def print_matrix(matrix, label=""):
    if label: print(f"{label}:")
    for row in matrix:
        print("  " + "  ".join(f"{x:5}" for x in row))
    print()

def add_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def subtract_matrices(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def multiply_matrices(A, B):
    rows_A, cols_A = len(A), len(A[0])
    cols_B = len(B[0])
    result = [[0]*cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]

print_matrix(A, "Matrix A")
print_matrix(B, "Matrix B")
print_matrix(add_matrices(A, B),      "A + B")
print_matrix(subtract_matrices(A, B), "A - B")
print_matrix(transpose(A),            "Transpose of A")
print_matrix(multiply_matrices(A, B), "A × B")
