/* C Program 12: File Input and Output
   Author: Lydia S. Makiwa
   Description: Writes student data to a file and reads it back */

#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *fp;

    /* Write to file */
    fp = fopen("students.txt", "w");
    if (fp == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    fprintf(fp, "Name,Marks\n");
    fprintf(fp, "Lydia Makiwa,95\n");
    fprintf(fp, "Alice Johnson,85\n");
    fprintf(fp, "Bob Smith,72\n");
    fprintf(fp, "Carol White,88\n");
    fclose(fp);
    printf("Data written to students.txt\n\n");

    /* Read from file */
    fp = fopen("students.txt", "r");
    if (fp == NULL) {
        printf("Error reading file!\n");
        return 1;
    }

    printf("=== Reading from students.txt ===\n");
    char line[100];
    while (fgets(line, sizeof(line), fp) != NULL)
        printf("  %s", line);

    fclose(fp);

    /* Append to file */
    fp = fopen("students.txt", "a");
    fprintf(fp, "David Brown,61\n");
    fclose(fp);
    printf("\nAppended David Brown to file.\n");

    return 0;
}
