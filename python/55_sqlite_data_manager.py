"""
Program  : 55_sqlite_data_manager.py
Title    : SQLite Database Manager with Python
Author   : Lydia S. Makiwa
Date     : 2026-06-01

Description:
    A practical SQLite database manager demonstrating CRUD operations,
    relationship tables, aggregation queries, and data export.
    Includes a student-course enrolment system.
    Understanding databases is critical for backend roles at
    companies like Google, Meta, and fintech startups.
"""

import sqlite3
import csv
import os
from datetime import datetime, date
from contextlib import contextmanager


class DatabaseManager:
    """
    A reusable SQLite database manager.
    Handles connection, table creation, CRUD, and exports.
    """
    
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self.connection = None
    
    @contextmanager
    def connect(self):
        """Context manager for safe database connections."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield self.connection
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"  ⚠ Database error: {e}")
            raise
        finally:
            self.connection.close()
            self.connection = None
    
    def execute(self, sql, params=None):
        """Execute a single SQL statement."""
        if not self.connection:
            raise RuntimeError("Not connected. Use 'with db.connect():'")
        cursor = self.connection.execute(sql, params or [])
        return cursor
    
    def fetch_all(self, sql, params=None):
        """Execute query and return all rows as list of dicts."""
        cursor = self.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def fetch_one(self, sql, params=None):
        """Execute query and return first row as dict."""
        cursor = self.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def insert(self, table, data):
        """
        Insert a row into table.
        data: dict of {column: value}
        Returns the rowid of the inserted row.
        """
        columns = list(data.keys())
        placeholders = ",".join("?" for _ in columns)
        col_names = ",".join(columns)
        
        sql = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
        cursor = self.execute(sql, [data[col] for col in columns])
        return cursor.lastrowid
    
    def update(self, table, data, where_col, where_val):
        """Update rows matching condition."""
        set_clause = ", ".join(f"{col} = ?" for col in data)
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_col} = ?"
        cursor = self.execute(sql, [*data.values(), where_val])
        return cursor.rowcount
    
    def delete(self, table, where_col, where_val):
        """Delete rows matching condition."""
        sql = f"DELETE FROM {table} WHERE {where_col} = ?"
        cursor = self.execute(sql, [where_val])
        return cursor.rowcount
    
    def export_csv(self, sql, filename, params=None):
        """Export query results to CSV file."""
        rows = self.fetch_all(sql, params)
        if not rows:
            print("  ⚠ No data to export")
            return
        
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"  💾 Exported {len(rows)} rows to {filename}")
        return filename


# ===== DEMO: Student Course Enrolment System =====
if __name__ == "__main__":
    print("=" * 55)
    print("   SQLite DATABASE MANAGER — STUDENT ENROLMENT")
    print("=" * 55)
    
    db = DatabaseManager(":memory:")  # Use file path for persistent storage
    
    with db.connect():
        # Create tables
        print("\n📦 Creating tables...")
        db.execute("""
            CREATE TABLE courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                credits INTEGER NOT NULL,
                instructor TEXT
            )
        """)
        db.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                enrolment_date TEXT DEFAULT (date('now'))
            )
        """)
        db.execute("""
            CREATE TABLE enrolments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER REFERENCES students(id),
                course_id INTEGER REFERENCES courses(id),
                grade REAL,
                semester TEXT,
                UNIQUE(student_id, course_id, semester)
            )
        """)
        print("   ✅ Tables created: courses, students, enrolments")
        
        # Insert courses
        print("\n📚 Inserting courses...")
        courses = [
            ("CSC101", "Intro to Programming", 4, "Dr. Mwangi"),
            ("CSC201", "Data Structures", 4, "Prof. Ochieng"),
            ("CSC301", "Machine Learning", 3, "Dr. Patel"),
            ("MTH101", "Calculus I", 4, "Dr. Kamau"),
            ("STA201", "Probability & Statistics", 3, "Prof. Nyambura"),
        ]
        for code, title, credits, instructor in courses:
            cid = db.insert("courses", {
                "code": code, "title": title,
                "credits": credits, "instructor": instructor
            })
            print(f"   → {code}: {title} ({credits} cr)")
        
        # Insert students
        print("\n👩‍🎓 Inserting students...")
        students = [
            ("Lydia Makiwa", "lydia@example.com"),
            ("James Otieno", "james@example.com"),
            ("Amina Hassan", "amina@example.com"),
            ("Brian Kiprop", "brian@example.com"),
            ("Cynthia Wanjiku", "cynthia@example.com"),
        ]
        for name, email in students:
            sid = db.insert("students", {"name": name, "email": email})
            print(f"   → {name} ({email})")
        
        # Insert enrolments
        print("\n📝 Recording enrolments with grades...")
        enrolments = [
            (1, 1, 85.5, "2026A"), (1, 2, 78.0, "2026A"),
            (1, 3, None, "2026B"),  # Not yet graded
            (2, 1, 92.0, "2026A"), (2, 3, 88.5, "2026A"),
            (2, 4, 75.0, "2026A"),
            (3, 1, 70.0, "2026A"), (3, 4, 81.0, "2026A"),
            (3, 5, 65.5, "2026A"),
            (4, 2, 95.0, "2026A"), (4, 5, 90.0, "2026A"),
            (5, 1, 88.0, "2026A"), (5, 3, None, "2026B"),
        ]
        for s, c, grade, sem in enrolments:
            db.insert("enrolments", {
                "student_id": s, "course_id": c,
                "grade": grade, "semester": sem
            })
        
        # Query 1: Student with their enrolled courses
        print("\n🔍 Query: Students with their courses and grades")
        rows = db.fetch_all("""
            SELECT s.name, c.code, c.title, e.grade, e.semester
            FROM students s
            JOIN enrolments e ON s.id = e.student_id
            JOIN courses c ON e.course_id = c.id
            ORDER BY s.name, c.code
        """)
        for row in rows[:10]:
            grade = f"{row['grade']:.1f}%" if row['grade'] else "In progress"
            print(f"   {row['name']:20s} | {row['code']:8s} | {grade}")
        
        # Query 2: Course averages
        print("\n📊 Query: Average grades per course")
        rows = db.fetch_all("""
            SELECT c.code, c.title, ROUND(AVG(e.grade), 1) as avg_grade,
                   COUNT(e.id) as students, COUNT(CASE WHEN e.grade IS NOT NULL THEN 1 END) as graded
            FROM courses c
            LEFT JOIN enrolments e ON c.id = e.course_id
            GROUP BY c.id
            ORDER BY avg_grade DESC
        """)
        for row in rows:
            avg = f"{row['avg_grade']:.1f}" if row['avg_grade'] else "N/A"
            print(f"   {row['code']:8s} | Avg: {avg:>6s} | Graded: {row['graded']}/{row['students']}")
        
        # Query 3: Top student
        print("\n🏆 Query: Top performing student")
        row = db.fetch_one("""
            SELECT s.name, ROUND(AVG(e.grade), 1) as avg_grade,
                   COUNT(e.id) as courses_completed
            FROM students s
            JOIN enrolments e ON s.id = e.student_id
            WHERE e.grade IS NOT NULL
            GROUP BY s.id
            ORDER BY avg_grade DESC
            LIMIT 1
        """)
        print(f"   {row['name']} — Avg: {row['avg_grade']}% across {row['courses_completed']} courses")
        
        # Demonstrate export
        print("\n💾 Exporting student results to CSV...")
        db.export_csv("""
            SELECT s.name as "Student", c.code as "Course",
                   c.title as "Course Title", e.grade as "Grade"
            FROM students s
            JOIN enrolments e ON s.id = e.student_id
            JOIN courses c ON e.course_id = c.id
            WHERE e.grade IS NOT NULL
            ORDER BY s.name
        """, "student_results.csv")
    
    print("\n💡 SQLite is used by major companies —")
    print("   Django, Android, Chrome, and Dropbox all use it!")
