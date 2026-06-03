/* ==============================================================================
 * Title: Dynamic Matrix Transposition using Pointers
 * Author: Lydia S. Makiwa
 * Date: June 3, 2026
 * Description: Dynamically allocates memory for a 2D matrix using double pointers,
 *              populates it, computes its transpose, displays both matrices, and
 *              properly deallocates all allocated memory.
 *              Designed for C programming students learning advanced pointer arithmetic.
 * ==============================================================================
 */

#include <stdio.h>
#include <stdlib.h>

// Function to dynamically allocate memory for an R x C matrix
int** allocateMatrix(int rows, int cols) {
    int** matrix = (int**)malloc(rows * sizeof(int*));
    if (matrix == NULL) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    for (int i = 0; i < rows; i++) {
        matrix[i] = (int*)malloc(cols * sizeof(int));
        if (matrix[i] == NULL) {
            printf("Memory allocation failed!\n");
            exit(1);
        }
    }
    return matrix;
}

// Function to fill matrix with dummy values
void fillMatrix(int** matrix, int rows, int cols) {
    int val = 1;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            *(*(matrix + i) + j) = val++; // equivalent to matrix[i][j]
        }
    }
}

// Function to display an R x C matrix
void displayMatrix(int** matrix, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%4d ", *(*(matrix + i) + j));
        }
        printf("\n");
    }
}

// Function to transpose matrix A (rows x cols) into matrix B (cols x rows) using pointers
void transposeMatrix(int** src, int** dest, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            *(*(dest + j) + i) = *(*(src + i) + j); // dest[j][i] = src[i][j]
        }
    }
}

// Function to deallocate memory of an R x C matrix
void freeMatrix(int** matrix, int rows) {
    for (int i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);
}

// Main execution function (Working Example)
int main() {
    int rows = 3, cols = 4;
    printf("--- Dynamic Matrix Transposition Demo ---\n");
    printf("Initializing a matrix of size %d x %d...\n\n", rows, cols);

    // Allocate memory for original and transposed matrices
    int** original = allocateMatrix(rows, cols);
    int** transposed = allocateMatrix(cols, rows);

    // Fill and display the original matrix
    fillMatrix(original, rows, cols);
    printf("Original Matrix:\n");
    displayMatrix(original, rows, cols);

    // Perform Transposition
    transposeMatrix(original, transposed, rows, cols);

    // Display Transposed Matrix
    printf("\nTransposed Matrix (%d x %d):\n", cols, rows);
    displayMatrix(transposed, cols, rows);

    // Clean up allocated memory
    freeMatrix(original, rows);
    freeMatrix(transposed, cols);
    printf("\nMemory successfully deallocated. Program finished!\n");

    return 0;
}
