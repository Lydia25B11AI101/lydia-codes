/*
 * Title: Longest Common Subsequence (LCS) using Dynamic Programming
 * Author: Lydia S. Makiwa
 * Date: June 06, 2026
 *
 * Description:
 * This program implements the Longest Common Subsequence (LCS) problem using 
 * Dynamic Programming (tabulation method). It finds the length of the longest
 * subsequence common to two sequences and reconstructs and prints the subsequence itself.
 * 
 * Perfect for a first-year student to master 2D array manipulation and DP.
 */

#include <stdio.h>
#include <string.h>

int max(int a, int b) {
    return (a > b) ? a : b;
}

void findLCS(char *X, char *Y, int m, int n) {
    int L[m + 1][n + 1];
    int i, j;

    // Build the LCS table in bottom-up fashion
    for (i = 0; i <= m; i++) {
        for (j = 0; j <= n; j++) {
            if (i == 0 || j == 0)
                L[i][j] = 0;
            else if (X[i - 1] == Y[j - 1])
                L[i][j] = L[i - 1][j - 1] + 1;
            else
                L[i][j] = max(L[i - 1][j], L[i][j - 1]);
        }
    }

    // L[m][n] contains the length of LCS
    int index = L[m][n];
    printf("Length of Longest Common Subsequence: %d\n", index);

    // Create a character array to store the LCS string
    char lcs_str[index + 1];
    lcs_str[index] = '\0'; // Set the terminating character

    // Start from the right-bottom-most corner and store characters in lcs_str
    i = m;
    j = n;
    while (i > 0 && j > 0) {
        // If current character in X[] and Y[] are same, then current character is part of LCS
        if (X[i - 1] == Y[j - 1]) {
            lcs_str[index - 1] = X[i - 1]; // Put current character in result
            i--;
            j--;
            index--;
        }
        // If they are not same, then find the larger of two and go in that direction
        else if (L[i - 1][j] > L[i][j - 1])
            i--;
        else
            j--;
    }

    // Print the reconstructed LCS
    printf("Longest Common Subsequence: %s\n", lcs_str);
}

int main() {
    printf("=== Longest Common Subsequence Demo ===\n");
    char X[] = "LONGESTSUBSEQUENCE";
    char Y[] = "SUBSEQUENCELONGEST";
    int m = strlen(X);
    int n = strlen(Y);

    printf("Sequence 1: %s\n", X);
    printf("Sequence 2: %s\n", Y);
    
    findLCS(X, Y, m, n);

    return 0;
}
