/* Program Title: 0/1 Knapsack Problem (Dynamic Programming)
   Author: Lydia S. Makiwa
   Date: 2026-05-05
   Description: Solves the 0/1 Knapsack problem using a DP table.
                Given items with weights and values, find the max value
                that fits in a knapsack of given capacity.
                Core DP interview question — used in resource allocation. */

#include <stdio.h>
#include <stdlib.h>

#define MAX_ITEMS 20
#define MAX_W 100

int dp[MAX_ITEMS+1][MAX_W+1];
int max(int a, int b){ return a>b?a:b; }

void knapsack(int n, int weights[], int values[], int W) {
    // Build DP table
    for (int i = 0; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            if (i == 0 || w == 0) {
                dp[i][w] = 0;
            } else if (weights[i-1] <= w) {
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w]);
            } else {
                dp[i][w] = dp[i-1][w];
            }
        }
    }
    printf("Maximum value in knapsack (capacity=%d): %d\n\n", W, dp[n][W]);

    // Trace back chosen items
    printf("Items selected:\n");
    int w = W;
    for (int i = n; i > 0 && w > 0; i--) {
        if (dp[i][w] != dp[i-1][w]) {
            printf("  Item %d: weight=%d  value=%d\n", i, weights[i-1], values[i-1]);
            w -= weights[i-1];
        }
    }
}

int main() {
    int weights[] = {2, 3, 4, 5, 1};
    int values[]  = {6, 10, 14, 16, 4};
    int n = 5, W = 8;

    printf("=== 0/1 Knapsack Problem ===\n");
    printf("Capacity: %d\n", W);
    printf("Items:\n");
    for (int i = 0; i < n; i++)
        printf("  Item %d: weight=%d  value=%d\n", i+1, weights[i], values[i]);
    printf("\n");

    knapsack(n, weights, values, W);
    return 0;
}
