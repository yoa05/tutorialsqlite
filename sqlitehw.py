import sqlite3

# Connect to SQLite (in memory for testing)
conn = sqlite3.connect(':memory:')

# this is important because foreign keys are OFF by default in SQLite
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

# Helper function to inspect table contents
def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(" | ".join(columns))
    print("-" * 30)

    for row in rows:
        print(" | ".join(str(value) for value in row))

# Create tables
cursor.execute("""
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")

cursor.execute("""
CREATE TABLE registered_courses (
    student_id INT,
    course_id INT,
    PRIMARY KEY(student_id, course_id),
    FOREIGN KEY(student_id) REFERENCES student(student_id)
)
""")

cursor.execute("""
CREATE TABLE grades (
    student_id INT,
    course_id INT,
    grade INT,
    PRIMARY KEY(student_id, course_id),
    FOREIGN KEY(student_id) REFERENCES student(student_id)
)
""")

students = [
    (1, 'Alice', 20),
    (2, 'Bob', 22),
    (3, 'Charlie', 21),
    (4, 'Yasmine', 24),
    (5, 'Haya', 26)
]

courses = [
    (1, 201),
    (2, 300),
    (3, 400)
]

grade = [
    (1, 201, 80),
    (2, 300, 90),
    (3, 400, 100)
]

# Insert data
cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", students)
cursor.executemany("INSERT INTO registered_courses VALUES (?, ?)", courses)
cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grade)

conn.commit()

print_table(cursor, "student")

print("\nMax grade per student:")
cursor.execute("""
SELECT g.student_id, g.course_id, g.grade
FROM grades g
WHERE g.grade = (
    SELECT MAX(grade)
    FROM grades
    WHERE student_id = g.student_id
)
""")
for row in cursor.fetchall():
    print(row)

print("\nAverage grade per student:")
cursor.execute("""
SELECT student_id, AVG(grade)
FROM grades
GROUP BY student_id
""")
for row in cursor.fetchall():
    print(row)

# Example SELECT query
cursor.execute("SELECT * FROM student")
print("\nResult of: SELECT * FROM student")
for row in cursor.fetchall():
    print(row)

conn.close()