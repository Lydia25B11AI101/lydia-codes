/*
 * Program Title: Fractional Knapsack Solver (Greedy Approach)
 * Author: Lydia S. Makiwa
 * Date: June 5, 2026
 * Description: Implements the classic Fractional Knapsack problem using a greedy strategy.
 *              Items are sorted in descending order of value-to-weight ratio using bubble sort,
 *              and greedily added to maximize profits in the knapsack capacity constraint.
 *              Familiarizes AIML students with structural representations and sorting in C.
 */

#include <stdio.h>

struct Item {
    char id;
    double weight;
    double value;
    double ratio; // value/weight
};

// Sort items based on value-to-weight ratio in descending order
void sortItems(struct Item items[], int n) {
    int i, j;
    struct Item temp;
    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - i - 1; j++) {
            if (items[j].ratio < items[j + 1].ratio) {
                temp = items[j];
                items[j] = items[j + 1];
                items[j + 1] = temp;
            }
        }
    }
}

// Solve Fractional Knapsack
double fractionalKnapsack(struct Item items[], int n, double capacity) {
    sortItems(items, n);

    double totalProfit = 0.0;
    double currentWeight = 0.0;

    printf("\n--- Greedy Allocation Process ---\n");
    for (int i = 0; i < n; i++) {
        if (currentWeight + items[i].weight <= capacity) {
            currentWeight += items[i].weight;
            totalProfit += items[i].value;
            printf("Packed Item %c fully: weight = %.1f, value = %.1f. Current load = %.1f / %.1f\n",
                   items[i].id, items[i].weight, items[i].value, currentWeight, capacity);
        } else {
            // Take fraction of next item to top up the knapsack
            double remainingCapacity = capacity - currentWeight;
            double fraction = remainingCapacity / items[i].weight;
            totalProfit += items[i].value * fraction;
            currentWeight += remainingCapacity;
            printf("Packed Item %c partially (%.1f%%): weight = %.1f, added value = %.1f. Current load = %.1f / %.1f\n",
                   items[i].id, fraction * 100, remainingCapacity, items[i].value * fraction, currentWeight, capacity);
            break; // Knapsack is full
        }
    }
    return totalProfit;
}

int main() {
    printf("=== Fractional Knapsack Problem (Greedy Method) ===\n");

    struct Item items[] = {
        {'A', 10.0, 60.0, 60.0/10.0},
        {'B', 20.0, 100.0, 100.0/20.0},
        {'C', 30.0, 120.0, 120.0/30.0}
    };
    int n = sizeof(items) / sizeof(items[0]);
    double capacity = 50.0;

    printf("\nTotal items available: %d\n", n);
    for (int i = 0; i < n; i++) {
        printf("Item %c: Value = $%.2f, Weight = %.2f kg, Ratio = %.2f\n",
               items[i].id, items[i].value, items[i].weight, items[i].ratio);
    }
    printf("Knapsack Max Capacity: %.2f kg\n", capacity);

    double maxProfit = fractionalKnapsack(items, n, capacity);
    printf("\nMaximum profit that can be achieved: $%.2f\n", maxProfit);

    return 0;
}
