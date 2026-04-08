/* C Program 5: Armstrong Number Checker
   Author: Lydia S. Makiwa
   Description: Checks if a number is an Armstrong (narcissistic) number */

#include <stdio.h>
#include <math.h>

int count_digits(int n) {
    int count = 0;
    while (n != 0) { count++; n /= 10; }
    return count;
}

int is_armstrong(int n) {
    int digits = count_digits(n);
    int temp = n, sum = 0;
    while (temp != 0) {
        int digit = temp % 10;
        sum += (int)pow(digit, digits);
        temp /= 10;
    }
    return sum == n;
}

int main() {
    printf("=== Armstrong Numbers up to 1000 ===\n");
    for (int i = 1; i <= 1000; i++) {
        if (is_armstrong(i))
            printf("%d is an Armstrong number\n", i);
    }

    int num;
    printf("\nEnter a number to check: ");
    scanf("%d", &num);
    if (is_armstrong(num))
        printf("%d IS an Armstrong number ✓\n", num);
    else
        printf("%d is NOT an Armstrong number ✗\n", num);

    return 0;
}
