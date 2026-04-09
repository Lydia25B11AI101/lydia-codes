/* C Program 17: Matrix Multiplication
   Author: Lydia S. Makiwa
   Description: Multiplies two matrices and displays the result */

#include <stdio.h>

#define MAX 10

void print_matrix(int mat[][MAX], int rows, int cols, char* label) {
    printf("%s:\n", label);
    for (int i = 0; i < rows; i++) {
        printf("  ");
        for (int j = 0; j < cols; j++)
            printf("%6d", mat[i][j]);
        printf("\n");
    }
    printf("\n");
}

void multiply(int A[][MAX], int B[][MAX], int C[][MAX],
              int rA, int cA, int cB) {
    for (int i = 0; i < rA; i++)
        for (int j = 0; j < cB; j++) {
            C[i][j] = 0;
            for (int k = 0; k < cA; k++)
                C[i][j] += A[i][k] * B[k][j];
        }
}

int main() {
    int A[MAX][MAX] = {{1,2,3},{4,5,6}};
    int B[MAX][MAX] = {{7,8},{9,10},{11,12}};
    int C[MAX][MAX];

    print_matrix(A, 2, 3, "Matrix A (2x3)");
    print_matrix(B, 3, 2, "Matrix B (3x2)");

    multiply(A, B, C, 2, 3, 2);
    print_matrix(C, 2, 2, "A x B (2x2)");

    return 0;
}
