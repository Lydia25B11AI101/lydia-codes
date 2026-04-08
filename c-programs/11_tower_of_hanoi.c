/* C Program 11: Tower of Hanoi (Recursion)
   Author: Lydia S. Makiwa
   Description: Classic recursion problem — moves n disks from A to C via B */

#include <stdio.h>

int moves = 0;

void hanoi(int n, char from, char to, char via) {
    if (n == 1) {
        printf("  Move disk 1 from %c → %c\n", from, to);
        moves++;
        return;
    }
    hanoi(n - 1, from, via, to);
    printf("  Move disk %d from %c → %c\n", n, from, to);
    moves++;
    hanoi(n - 1, via, to, from);
}

int main() {
    int n;
    printf("=== Tower of Hanoi ===\n");
    printf("Enter number of disks: ");
    scanf("%d", &n);

    printf("\nSteps to move %d disk(s) from A to C:\n", n);
    hanoi(n, 'A', 'C', 'B');
    printf("\nTotal moves: %d (minimum = 2^n - 1 = %d)\n",
           moves, (1 << n) - 1);
    return 0;
}
