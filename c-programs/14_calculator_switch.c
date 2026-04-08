/* C Program 14: Calculator using Switch-Case
   Author: Lydia S. Makiwa
   Description: Menu-driven calculator with switch statement */

#include <stdio.h>
#include <math.h>

void print_menu() {
    printf("\n=== Calculator ===\n");
    printf("1. Addition\n");
    printf("2. Subtraction\n");
    printf("3. Multiplication\n");
    printf("4. Division\n");
    printf("5. Power (a^b)\n");
    printf("6. Square Root\n");
    printf("7. Exit\n");
    printf("Choice: ");
}

int main() {
    int choice;
    double a, b, result;

    while (1) {
        print_menu();
        scanf("%d", &choice);

        if (choice == 7) {
            printf("Goodbye! 👋\n");
            break;
        }

        if (choice != 6) {
            printf("Enter two numbers: ");
            scanf("%lf %lf", &a, &b);
        } else {
            printf("Enter a number: ");
            scanf("%lf", &a);
        }

        switch (choice) {
            case 1: result = a + b; printf("Result: %.2f\n", result); break;
            case 2: result = a - b; printf("Result: %.2f\n", result); break;
            case 3: result = a * b; printf("Result: %.2f\n", result); break;
            case 4:
                if (b == 0) printf("Error: Division by zero!\n");
                else { result = a / b; printf("Result: %.2f\n", result); }
                break;
            case 5: result = pow(a, b); printf("Result: %.2f\n", result); break;
            case 6:
                if (a < 0) printf("Error: Cannot take sqrt of negative!\n");
                else { result = sqrt(a); printf("Result: %.4f\n", result); }
                break;
            default: printf("Invalid choice!\n");
        }
    }
    return 0;
}
