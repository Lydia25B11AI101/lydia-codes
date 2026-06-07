/*
 * Program: Strassen's Matrix Multiplication Algorithm
 * Author: Lydia S. Makiwa
 * Date: June 7, 2026
 * Category: Algorithms / C Programming
 *
 * Description:
 * This program implements Strassen's divide-and-conquer matrix multiplication
 * algorithm for 2x2 and 4x4 matrices. Strassen's algorithm reduces the number
 * of recursive scalar multiplications from 8 to 7, bringing the runtime 
 * complexity down to O(n^2.807) compared to the standard O(n^3).
 */
#include <stdio.h>
#include <stdlib.h>

#define SIZE 4

// Function to print a matrix
void printMatrix(int matrix[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf("%4d ", matrix[i][j]);
        }
        printf("\n");
    }
}

// Strassen's matrix multiplication helper for 2x2 matrices
void strassen2x2(int A[2][2], int B[2][2], int C[2][2]) {
    int p1 = (A[0][0] + A[1][1]) * (B[0][0] + B[1][1]);
    int p2 = (A[1][0] + A[1][1]) * B[0][0];
    int p3 = A[0][0] * (B[0][1] - B[1][1]);
    int p4 = A[1][1] * (B[1][0] - B[0][0]);
    int p5 = (A[0][0] + A[0][1]) * B[1][1];
    int p6 = (A[1][0] - A[0][0]) * (B[0][0] + B[0][1]);
    int p7 = (A[0][1] - A[1][1]) * (B[1][0] + B[1][1]);

    C[0][0] = p1 + p4 - p5 + p7;
    C[0][1] = p3 + p5;
    C[1][0] = p2 + p4;
    C[1][1] = p1 - p2 + p3 + p6;
}

// Standard Matrix Multiplication for verification
void standardMultiply(int A[SIZE][SIZE], int B[SIZE][SIZE], int C[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            C[i][j] = 0;
            for (int k = 0; k < SIZE; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

// Standard Strassen for 4x4 matrix split into submatrices
void strassen4x4(int A[SIZE][SIZE], int B[SIZE][SIZE], int C[SIZE][SIZE]) {
    // We partition the 4x4 matrices into 2x2 blocks
    int a11[2][2], a12[2][2], a21[2][2], a22[2][2];
    int b11[2][2], b12[2][2], b21[2][2], b22[2][2];
    int c11[2][2], c12[2][2], c21[2][2], c22[2][2];

    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            a11[i][j] = A[i][j];
            a12[i][j] = A[i][j + 2];
            a21[i][j] = A[i + 2][j];
            a22[i][j] = A[i + 2][j + 2];

            b11[i][j] = B[i][j];
            b12[i][j] = B[i][j + 2];
            b21[i][j] = B[i + 2][j];
            b22[i][j] = B[i + 2][j + 2];
        }
    }

    // Strassen auxiliary 2x2 variables
    int s1[2][2], s2[2][2], s3[2][2], s4[2][2], s5[2][2], s6[2][2], s7[2][2];
    int tempA[2][2], tempB[2][2];

    // p1 = (a11 + a22) * (b11 + b22)
    for (int i=0; i<2; i++) for (int j=0; j<2; j++) {
        tempA[i][j] = a11[i][j] + a22[i][j];
        tempB[i][j] = b11[i][j] + b22[i][j];
    }
    strassen2x2(tempA, tempB, s1);

    // p2 = (a21 + a22) * b11
    for (int i=0; i<2; i++) for (int j=0; j<2; j++) {
        tempA[i][j] = a21[i][j] + a22[i][j];
    }
    strassen2x2(tempA, b11, s2);

    // p3 = a11 * (b12 - b22)
    for (int i=0; i<2; i++) for (int j=0; j<2; j++) {
        tempB[i][j] = b12[i][j] - b22[i][j];
    }
    strassen2x2(a11, tempB, s3);

    // p4 = a22 * (b21 - b11)
    for (int i=0; i<2; i++) for (int j=0; j<2; j++) {
        tempB[i][j] = b21[i][j] - b11[i][j];
    }
    strassen2x2(a22, tempB, s4);

    // p5 = (a11 + a12) * b22
    for (int i=0; i<2; i++) for (int j=0; j<2; j++) {
        tempA[i][j] = a11[i][j] + a12[i][j];
    }
    strassen2x2(tempA, b22, s5);

    // p6 = (a21 - a11) * (b11 + b12)
    for (int i=0; i<2; i++) for (int j=0; j<2; j++) {
        tempA[i][j] = a21[i][j] - a11[i][j];
        tempB[i][j] = b11[i][j] + b12[i][j];
    }
    strassen2x2(tempA, tempB, s6);

    // p7 = (a12 - a22) * (b21 + b22)
    for (int i=0; i<2; i++) for (int j=0; j<2; j++) {
        tempA[i][j] = a12[i][j] - a22[i][j];
        tempB[i][j] = b21[i][j] + b22[i][j];
    }
    strassen2x2(tempA, tempB, s7);

    // Reconstruct C matrices
    // c11 = p1 + p4 - p5 + p7
    // c12 = p3 + p5
    // c21 = p2 + p4
    // c22 = p1 - p2 + p3 + p6
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            c11[i][j] = s1[i][j] + s4[i][j] - s5[i][j] + s7[i][j];
            c12[i][j] = s3[i][j] + s5[i][j];
            c21[i][j] = s2[i][j] + s4[i][j];
            c22[i][j] = s1[i][j] - s2[i][j] + s3[i][j] + s6[i][j];
        }
    }

    // Merge submatrices back to 4x4 matrix C
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            C[i][j] = c11[i][j];
            C[i][j + 2] = c12[i][j];
            C[i + 2][j] = c21[i][j];
            C[i + 2][j + 2] = c22[i][j];
        }
    }
}

int main() {
    printf("=== Strassen\'s Matrix Multiplication ===\n\n");

    int A[SIZE][SIZE] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12},
        {13, 14, 15, 16}
    };

    int B[SIZE][SIZE] = {
        {16, 15, 14, 13},
        {12, 11, 10, 9},
        {8, 7, 6, 5},
        {4, 3, 2, 1}
    };

    int C_strassen[SIZE][SIZE];
    int C_standard[SIZE][SIZE];

    printf("Matrix A:\n");
    printMatrix(A);

    printf("\nMatrix B:\n");
    printMatrix(B);

    // Strassen multiplication
    strassen4x4(A, B, C_strassen);

    // Standard multiplication for confirmation
    standardMultiply(A, B, C_standard);

    printf("\nResult via Strassen\'s Algorithm:\n");
    printMatrix(C_strassen);

    printf("\nResult via Standard O(n^3) Method:\n");
    printMatrix(C_standard);

    // Verify correctness
    int success = 1;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (C_strassen[i][j] != C_standard[i][j]) {
                success = 0;
            }
        }
    }

    if (success) {
        printf("\nSuccess! Strassen\'s results match the standard method perfectly.\n");
    } else {
        printf("\nError! Discrepancy detected in results.\n");
    }

    return 0;
}
