/* C Program 10: Structures — Student Record System
   Author: Lydia S. Makiwa
   Description: Uses structs to store and display student records */

#include <stdio.h>
#include <string.h>

#define MAX_STUDENTS 5

struct Student {
    char name[50];
    int  roll_no;
    float marks[3];
    float average;
    char grade;
};

char get_grade(float avg) {
    if (avg >= 90) return 'A';
    if (avg >= 80) return 'B';
    if (avg >= 70) return 'C';
    if (avg >= 60) return 'D';
    return 'F';
}

void compute_stats(struct Student *s) {
    float sum = 0;
    for (int i = 0; i < 3; i++) sum += s->marks[i];
    s->average = sum / 3;
    s->grade = get_grade(s->average);
}

int main() {
    struct Student students[MAX_STUDENTS] = {
        {"Lydia Makiwa",  1, {95, 98, 100}},
        {"Alice Johnson", 2, {85, 78, 90}},
        {"Bob Smith",     3, {60, 55, 70}},
        {"Carol White",   4, {72, 80, 68}},
        {"David Brown",   5, {45, 50, 40}},
    };

    for (int i = 0; i < MAX_STUDENTS; i++)
        compute_stats(&students[i]);

    printf("%-20s %6s %8s %8s %8s %6s %6s\n",
           "Name", "Roll", "Sub1", "Sub2", "Sub3", "Avg", "Grade");
    printf("----------------------------------------------------------------------\n");
    for (int i = 0; i < MAX_STUDENTS; i++) {
        struct Student s = students[i];
        printf("%-20s %6d %8.1f %8.1f %8.1f %6.1f %6c\n",
               s.name, s.roll_no,
               s.marks[0], s.marks[1], s.marks[2],
               s.average, s.grade);
    }
    return 0;
}
