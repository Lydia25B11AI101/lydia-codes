/*
 * Program Title: Page Replacement Algorithms Simulator
 * Author: Lydia S. Makiwa
 * Date: June 2, 2026
 *
 * Description:
 * Implements and compares FIFO (First-In-First-Out) and LRU (Least Recently Used)
 * page replacement algorithms. It evaluates how many page faults occur for a given
 * memory reference string and frame capacity.
 */

#include <stdio.h>
#include <stdbool.h>

#define MAX_REFS 20

// Simulates FIFO Page Replacement
int simulateFIFO(int pages[], int n, int capacity) {
    int frames[10];
    int pageFaults = 0;
    int index = 0; // Tracks oldest page location
    
    // Initialize frames with -1
    for (int i = 0; i < capacity; i++) {
        frames[i] = -1;
    }
    
    printf("\n--- FIFO Process Simulation ---\n");
    for (int i = 0; i < n; i++) {
        int page = pages[i];
        bool isHit = false;
        
        // Check if page is already in frames
        for (int j = 0; j < capacity; j++) {
            if (frames[j] == page) {
                isHit = true;
                break;
            }
        }
        
        // If page is not in frames, it's a page fault
        if (!isHit) {
            frames[index] = page;
            index = (index + 1) % capacity; // Round robin index updates oldest
            pageFaults++;
            
            // Output state
            printf("Ref %2d (Fault): ", page);
        } else {
            printf("Ref %2d (Hit  ): ", page);
        }
        
        // Print active frames
        for (int j = 0; j < capacity; j++) {
            if (frames[j] == -1) printf("[ ] ");
            else printf("[%d] ", frames[j]);
        }
        printf("\n");
    }
    
    return pageFaults;
}

// Simulates LRU Page Replacement
int simulateLRU(int pages[], int n, int capacity) {
    int frames[10];
    int recent[10]; // Tracks recency (stores index or counter of use)
    int pageFaults = 0;
    
    for (int i = 0; i < capacity; i++) {
        frames[i] = -1;
        recent[i] = 0;
    }
    
    printf("\n--- LRU Process Simulation ---\n");
    for (int i = 0; i < n; i++) {
        int page = pages[i];
        bool isHit = false;
        int hitIndex = -1;
        
        // Search frames for page
        for (int j = 0; j < capacity; j++) {
            if (frames[j] == page) {
                isHit = true;
                hitIndex = j;
                break;
            }
        }
        
        if (isHit) {
            recent[hitIndex] = i; // Mark index as recently used
            printf("Ref %2d (Hit  ): ", page);
        } else {
            pageFaults++;
            // Check for empty space first
            int spaceIndex = -1;
            for (int j = 0; j < capacity; j++) {
                if (frames[j] == -1) {
                    spaceIndex = j;
                    break;
                }
            }
            
            // If frames are full, find the Least Recently Used
            if (spaceIndex == -1) {
                int min_recent = recent[0];
                spaceIndex = 0;
                for (int j = 1; j < capacity; j++) {
                    if (recent[j] < min_recent) {
                        min_recent = recent[j];
                        spaceIndex = j;
                    }
                }
            }
            
            // Insert page
            frames[spaceIndex] = page;
            recent[spaceIndex] = i;
            printf("Ref %2d (Fault): ", page);
        }
        
        // Print active frames
        for (int j = 0; j < capacity; j++) {
            if (frames[j] == -1) printf("[ ] ");
            else printf("[%d] ", frames[j]);
        }
        printf("\n");
    }
    
    return pageFaults;
}

int main() {
    printf("--- Page Replacement Algorithm Simulator ---\n");
    
    int reference_string[] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1};
    int n = sizeof(reference_string) / sizeof(reference_string[0]);
    int frame_capacity = 3;
    
    printf("Reference String: ");
    for(int i = 0; i < n; i++) {
        printf("%d ", reference_string[i]);
    }
    printf("\nFrame Capacity: %d\n", frame_capacity);
    
    int fifo_faults = simulateFIFO(reference_string, n, frame_capacity);
    int lru_faults = simulateLRU(reference_string, n, frame_capacity);
    
    printf("\n--- Final Performance Comparison ---\n");
    printf("FIFO Page Faults: %d\n", fifo_faults);
    printf("LRU Page Faults:  %d\n", lru_faults);
    printf("Efficiency Gain with LRU: %.1f%%\n", ((double)(fifo_faults - lru_faults)/fifo_faults)*100);
    
    return 0;
}