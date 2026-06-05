/*
 * Program Title: Matrix Chain Multiplication using Dynamic Programming
 * Author: Lydia S. Makiwa
 * Date: June 5, 2026
 * Description: C program to solve the Matrix Chain Multiplication problem
 *              using a bottom-up Dynamic Programming approach. It computes
 *              the minimum scalar multiplications needed to multiply a chain
 *              of matrices and outputs the DP tables.
 *              Trains student reasoning on nested memoization loops and algorithm analysis.
 */

#include <stdio.h>
#include <limits.h>

#define MAX_MATRICES 10

// Solves matrix chain multiplication and prints dp matrices
void matrixChainOrder(int p[], int n) {
    int m[MAX_MATRICES][MAX_MATRICES] = {0};
    int s[MAX_MATRICES][MAX_MATRICES] = {0};

    // n is the length of p, which means there are n-1 matrices (A1, A2, ... An-1)
    // m[i, j] = Minimum scalar multiplications to multiply matrices Ai...Aj
    int numMatrices = n - 1;

    // l is chain length (from length 2 to numMatrices)
    for (int l = 2; l <= numMatrices; l++) {
        for (int i = 1; i <= numMatrices - l + 1; i++) {
            int j = i + l - 1;
            m[i][j] = INT_MAX;
            for (int k = i; k <= j - 1; k++) {
                // cost = cost of (Ai..Ak) + cost of (Ak+1..Aj) + multiplication dimensions cost
                int q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];
                if (q < m[i][j]) {
                    m[i][j] = q;
                    s[i][j] = k; // Index where the split yields optimal solution
                }
            }
        }
    }

    printf("\n--- Computed DP Cost Table (m) ---\n");
    for (int i = 1; i <= numMatrices; i++) {
        for (int j = 1; j <= numMatrices; j++) {
            if (j < i) {
                printf("   -  ");
            } else {
                printf("%5d ", m[i][j]);
            }
        }
        printf("\n");
    }

    printf("\nMinimum number of multiplications needed: %d\n", m[1][numMatrices]);
}

int main() {
    printf("=== Matrix Chain Multiplication DP Solver ===\n");

    // Matrix dimensions:
    // A1 is 10 x 20
    // A2 is 20 x 30
    // A3 is 30 x 40
    // A4 is 40 x 30
    int arr[] = {10, 20, 30, 40, 30};
    int size = sizeof(arr) / sizeof(arr[0]);

    printf("\nMatrix chain dimensions:\n");
    for (int i = 0; i < size - 1; i++) {
        printf("  Matrix A%d: %d x %d\n", i + 1, arr[i], arr[i + 1]);
    }

    matrixChainOrder(arr, size);

    return 0;
}
