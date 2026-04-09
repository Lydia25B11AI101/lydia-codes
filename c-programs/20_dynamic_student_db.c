/*
 * Program Title : Dynamic Student Database (malloc / realloc)
 * Author        : Lydia S. Makiwa
 * Date          : 2026-04-09
 * Description   : Builds a resizable student database using
 *                 dynamic memory allocation (malloc, realloc,
 *                 free). Covers: structs, pointers, heap memory.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NAME_LEN 50

typedef struct {
    int    id;
    char   name[NAME_LEN];
    float  mark;
} Student;

typedef struct {
    Student* data;
    int      size;
    int      capacity;
} StudentDB;

/* Initialise the database */
void db_init(StudentDB* db, int initial_cap) {
    db->data     = (Student*)malloc(initial_cap * sizeof(Student));
    db->size     = 0;
    db->capacity = initial_cap;
}

/* Add a student (auto-resizes) */
void db_add(StudentDB* db, int id, const char* name, float mark) {
    if (db->size == db->capacity) {
        db->capacity *= 2;
        db->data = (Student*)realloc(db->data, db->capacity * sizeof(Student));
        printf("  [DB resized to capacity %d]\n", db->capacity);
    }
    db->data[db->size].id   = id;
    strncpy(db->data[db->size].name, name, NAME_LEN - 1);
    db->data[db->size].mark = mark;
    db->size++;
}

/* Print all students */
void db_print(StudentDB* db) {
    printf("\n%-5s  %-20s  %s\n", "ID", "Name", "Mark");
    printf("%-5s  %-20s  %s\n", "---", "----", "----");
    for (int i = 0; i < db->size; i++) {
        Student* s = &db->data[i];
        printf("%-5d  %-20s  %.1f\n", s->id, s->name, s->mark);
    }
}

/* Find top student */
Student* db_top(StudentDB* db) {
    if (db->size == 0) return NULL;
    Student* top = &db->data[0];
    for (int i = 1; i < db->size; i++)
        if (db->data[i].mark > top->mark) top = &db->data[i];
    return top;
}

/* Free memory */
void db_free(StudentDB* db) { free(db->data); db->size = db->capacity = 0; }

int main() {
    StudentDB db;
    db_init(&db, 2);  /* start small so we see resize */

    printf("=== Dynamic Student Database ===\n");
    db_add(&db, 1, "Lydia Makiwa",    88.5);
    db_add(&db, 2, "Aisha Nkosi",     76.0);
    db_add(&db, 3, "Themba Dlamini",  92.3);
    db_add(&db, 4, "Zanele Mokoena",  81.0);
    db_add(&db, 5, "Sipho Khumalo",   67.5);

    db_print(&db);

    Student* top = db_top(&db);
    printf("\nTop student: %s with %.1f%%\n", top->name, top->mark);

    db_free(&db);
    printf("Memory freed. Done!\n");
    return 0;
}
