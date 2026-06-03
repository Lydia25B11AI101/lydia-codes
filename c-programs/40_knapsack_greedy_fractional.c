/* ==============================================================================
 * Title: Greedy Fractional Knapsack Algorithm
 * Author: Lydia S. Makiwa
 * Date: June 3, 2026
 * Description: Solves the Fractional Knapsack Problem using a greedy approach.
 *              Uses custom structures for items, quicksort for sorting by value-to-weight ratio,
 *              and takes fractional parts of items to maximize the total profit.
 * ==============================================================================
 */

#include <stdio.h>
#include <stdlib.h>

// Struct definition for Knapsack Items
typedef struct {
    int id;
    double weight;
    double value;
    double ratio; // Value-to-weight ratio
} Item;

// Comparison function for QuickSort (sorting in descending order of ratio)
int compareItems(const void* a, const void* b) {
    Item* itemA = (Item*)a;
    Item* itemB = (Item*)b;
    if (itemB->ratio > itemA->ratio) return 1;
    if (itemB->ratio < itemA->ratio) return -1;
    return 0;
}

// Function to solve the fractional knapsack problem
double fractionalKnapsack(Item items[], int n, double capacity) {
    // Sort items by ratio descending
    qsort(items, n, sizeof(Item), compareItems);

    double totalValue = 0.0;
    double currentWeight = 0.0;

    printf("\nFilling Knapsack Greedily (Capacity: %.2f kg):\n", capacity);
    for (int i = 0; i < n; i++) {
        if (currentWeight + items[i].weight <= capacity) {
            // Take the whole item
            currentWeight += items[i].weight;
            totalValue += items[i].value;
            printf("  Item %d (Whole): Took %.2f kg | Cumulative Value: $%.2f\n", 
                   items[i].id, items[i].weight, totalValue);
        } else {
            // Take fractional part of item to fill remaining capacity
            double remainCapacity = capacity - currentWeight;
            double fraction = remainCapacity / items[i].weight;
            double valueTaken = items[i].value * fraction;
            
            currentWeight += remainCapacity;
            totalValue += valueTaken;
            printf("  Item %d (Fractional): Took %.2f kg (%.1f%%) | Cumulative Value: $%.2f\n", 
                   items[i].id, remainCapacity, fraction * 100.0, totalValue);
            break; // Knapsack is full
        }
    }
    return totalValue;
}

// Working example
int main() {
    printf("--- Fractional Knapsack Greedy Algorithm Demo ---\n");

    // Define items: {ID, Weight, Value, Ratio}
    Item items[] = {
        {1, 10.0, 60.0, 0.0},
        {2, 20.0, 100.0, 0.0},
        {3, 30.0, 120.0, 0.0}
    };
    int n = sizeof(items) / sizeof(items[0]);
    double capacity = 50.0;

    // Precompute ratio for each item
    for (int i = 0; i < n; i++) {
        items[i].ratio = items[i].value / items[i].weight;
    }

    printf("\nAvailable Items:\n");
    for (int i = 0; i < n; i++) {
        printf("  Item %d: Value = $%.2f, Weight = %.2f kg, Ratio = %.2f $/kg\n", 
               items[i].id, items[i].value, items[i].weight, items[i].ratio);
    }

    double maxVal = fractionalKnapsack(items, n, capacity);
    printf("\nOptimal Total Value in Knapsack: $%.2f\n", maxVal);

    return 0;
}
