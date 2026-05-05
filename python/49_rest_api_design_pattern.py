# Program Title: REST API Design Pattern (Flask Blueprint Simulation)
# Author: Lydia S. Makiwa
# Date: 2026-05-05
# Description: Simulates a Flask-style REST API for a student database
#              using Python dictionaries — great for understanding REST concepts
#              before deploying with Flask or FastAPI.

from datetime import datetime

# ─── In-memory "database" ───
students_db = {
    1: {"id": 1, "name": "Alice Moyo",   "grade": "A", "enrolled": "2024-01-10"},
    2: {"id": 2, "name": "Bob Ncube",    "grade": "B", "enrolled": "2024-01-12"},
    3: {"id": 3, "name": "Carol Dlamini","grade": "A+","enrolled": "2024-02-01"},
}
next_id = 4

def get_all_students():
    """GET /students → list all"""
    return list(students_db.values())

def get_student(student_id):
    """GET /students/{id} → single record"""
    return students_db.get(student_id, {"error": "Student not found"})

def create_student(name, grade):
    """POST /students → create new"""
    global next_id
    new = {"id": next_id, "name": name, "grade": grade,
             "enrolled": datetime.now().strftime("%Y-%m-%d")}
    students_db[next_id] = new
    next_id += 1
    return new

def update_student(student_id, **kwargs):
    """PUT /students/{id} → update fields"""
    if student_id not in students_db:
        return {"error": "Not found"}
    students_db[student_id].update(kwargs)
    return students_db[student_id]

def delete_student(student_id):
    """DELETE /students/{id} → remove"""
    if student_id in students_db:
        removed = students_db.pop(student_id)
        return {"message": f"Deleted student {removed['name']}"}
    return {"error": "Not found"}

# ─── Demo (simulating HTTP calls) ───
print("=== GET /students ===")
for s in get_all_students():
    print(" ", s)

print("\n=== POST /students (new enrolment) ===")
print(create_student("David Osei", "B+"))

print("\n=== GET /students/4 ===")
print(get_student(4))

print("\n=== PUT /students/2 (update grade) ===")
print(update_student(2, grade="A-"))

print("\n=== DELETE /students/3 ===")
print(delete_student(3))

print("\n=== GET /students (after changes) ===")
for s in get_all_students():
    print(" ", s)
