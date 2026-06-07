/*
 * Program: Boyer-Moore String Matching Algorithm
 * Author: Lydia S. Makiwa
 * Date: June 7, 2026
 * Category: Algorithms / C Programming
 *
 * Description:
 * This program implements the Boyer-Moore pattern matching algorithm using the
 * Bad Character heuristic. The Boyer-Moore algorithm is an extremely efficient
 * string searching algorithm that skips characters during scanning, making it 
 * standard in modern text search implementations.
 */
#include <stdio.h>
#include <string.h>

#define NO_OF_CHARS 256

// Helper function to find maximum of two integers
int max(int a, int b) {
    return (a > b) ? a : b;
}

// Preprocessing step to fill the bad character heuristic array
void badCharHeuristic(char *str, int size, int badchar[NO_OF_CHARS]) {
    // Initialize all occurrences as -1
    for (int i = 0; i < NO_OF_CHARS; i++) {
        badchar[i] = -1;
    }

    // Fill the actual value of last occurrence of a character
    for (int i = 0; i < size; i++) {
        badchar[(int)str[i]] = i;
    }
}

// Search algorithm using the bad character heuristic
void searchBoyerMoore(char *txt, char *pat) {
    int m = strlen(pat);
    int n = strlen(txt);

    int badchar[NO_OF_CHARS];

    // Compute bad character table
    badCharHeuristic(pat, m, badchar);

    int s = 0; // s is shift of the pattern with respect to text
    int matches_found = 0;

    printf("Searching for pattern '%s' in text '%s'...\n", pat, txt);

    while (s <= (n - m)) {
        int j = m - 1;

        /* Keep reducing index j of pattern while characters of
           pattern and text are matching at this shift s */
        while (j >= 0 && pat[j] == txt[s + j]) {
            j--;
        }

        /* If the pattern is present at current shift, then index j
           will become -1 */
        if (j < 0) {
            printf(" -> Pattern found at index %d\n", s);
            matches_found++;

            /* Shift the pattern so that the next character in text
               aligns with the last occurrence of it in pattern.
               The condition s+m < n is necessary for cases when
               pattern occurs at the end of text */
            s += (s + m < n) ? m - badchar[(int)txt[s + m]] : 1;
        } else {
            /* Shift the pattern so that the bad character in text
               aligns with the last occurrence of it in pattern. The
               max function is used to make sure that we get a positive
               shift. We may get a negative shift if the last occurrence
               of bad character in pattern is on the right side of the
               current character. */
            s += max(1, j - badchar[(int)txt[s + j]]);
        }
    }

    if (matches_found == 0) {
        printf("Pattern not found in the given text.\n");
    } else {
        printf("Search completed. Total matches found: %d\n", matches_found);
    }
}

int main() {
    printf("=== Boyer-Moore String Matching Algorithm ===\n\n");

    char text[] = "ABAAABCDABCDABCDCBAAB";
    char pattern[] = "ABCD";

    searchBoyerMoore(text, pattern);

    printf("\n--- Test Case 2 ---\n");
    char text2[] = "Lydia S. Makiwa is an AI and ML Student";
    char pattern2[] = "Makiwa";
    
    searchBoyerMoore(text2, pattern2);

    return 0;
}
