/*
 * Program Title: Banker's Algorithm for Deadlock Avoidance
 * Author: Lydia S. Makiwa
 * Date: June 2, 2026
 *
 * Description:
 * Implements Dijkstra's Banker's Algorithm. It checks if an Operating System's
 * current allocation of resources to processes is in a 'Safe State' or if it
 * faces deadlock risks.
 */

#include <stdio.h>
#include <stdbool.h>

#define P 5 // Number of processes
#define R 3 // Number of resource types

// Function to find if the system is in safe state
bool isSafe(int processes[], int avail[], int max[][R], int allot[][R]) {
    int need[P][R];
    
    // Calculate the Need matrix: Need = Max - Allocation
    for (int i = 0; i < P; i++) {
        for (int j = 0; j < R; j++) {
            need[i][j] = max[i][j] - allot[i][j];
        }
    }
    
    // Track completed processes
    bool finish[P] = {false};
    
    // Array to store safe sequence
    int safeSeq[P];
    
    // Make a copy of available resources
    int work[R];
    for (int i = 0; i < R; i++) {
        work[i] = avail[i];
    }
    
    int count = 0;
    while (count < P) {
        bool found = false;
        for (int p = 0; p < P; p++) {
            // If process is not finished
            if (!finish[p]) {
                // Check if all needed resources are less than or equal to work resources
                int j;
                for (j = 0; j < R; j++) {
                    if (need[p][j] > work[j])
                        break;
                }
                
                // If all resources needed by process 'p' can be allocated
                if (j == R) {
                    // Add the allocated resources of this process back to work
                    for (int k = 0; k < R ; k++) {
                        work[k] += allot[p][k];
                    }
                    
                    // Add this process to safe sequence
                    safeSeq[count++] = p;
                    
                    // Mark finished
                    finish[p] = true;
                    found = true;
                }
            }
        }
        
        // If we couldn't find any process in this iteration, system is not safe
        if (!found) {
            printf("System is NOT in a safe state! Deadlock risk detected.\n");
            return false;
        }
    }
    
    // Print safe sequence
    printf("System is in a SAFE state.\nSafe Sequence is: ");
    for (int i = 0; i < P; i++) {
        printf("P%d", safeSeq[i]);
        if (i < P - 1) printf(" -> ");
    }
    printf("\n");
    return true;
}

int main() {
    printf("--- Banker's Algorithm Deadlock Avoidance ---\n\n");
    
    int processes[] = {0, 1, 2, 3, 4};
    
    // Available instances of resources A, B, C
    int avail[] = {3, 3, 2};
    
    // Maximum resource demand of each process
    int max[P][R] = {
        {7, 5, 3}, // P0
        {3, 2, 2}, // P1
        {9, 0, 2}, // P2
        {2, 2, 2}, // P3
        {4, 3, 3}  // P4
    };
    
    // Resources currently allocated to each process
    int allot[P][R] = {
        {0, 1, 0}, // P0
        {2, 0, 0}, // P1
        {3, 0, 2}, // P2
        {2, 1, 1}, // P3
        {0, 0, 2}  // P4
    };
    
    // Display configuration
    printf("Process\tCurrent Allocation\tMax Demand\n");
    for (int i = 0; i < P; i++) {
        printf("P%d\t[%d, %d, %d]\t\t[%d, %d, %d]\n", 
               i, allot[i][0], allot[i][1], allot[i][2], max[i][0], max[i][1], max[i][2]);
    }
    printf("\nAvailable Resource Vector: [%d, %d, %d]\n\n", avail[0], avail[1], avail[2]);
    
    // Run Banker's Algorithm
    isSafe(processes, avail, max, allot);
    
    return 0;
}