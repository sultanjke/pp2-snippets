# =============================================================
# Working with JSON Data (using sample-data.json)
# =============================================================

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "sample-data.json")

# Load the dataset
with open(DATA_PATH, "r") as file:
    data = json.load(file)

university = data["university"]
department = data["department"]
students = data["students"]

print(f"--- {university} / {department} ---")
print(f"  Semester: {data['semester']}")
print(f"  Total students: {len(students)}\n")


# List all students with their GPA
print("--- All Students ---")
for student in students:
    status = "Active" if student["is_active"] else "Inactive"
    print(f"  {student['name']:<20} GPA: {student['gpa']}  ({status})")


# Filter: active students only
active_students = [s for s in students if s["is_active"]]
print(f"\n--- Active Students ({len(active_students)}/{len(students)}) ---")
for student in active_students:
    print(f"  {student['name']} — {student['address']['city']}")


# Find the student with the highest GPA
top_student = max(students, key=lambda s: s["gpa"])
print(f"\n--- Highest GPA ---")
print(f"  {top_student['name']}: {top_student['gpa']}")


# Calculate the average GPA
average_gpa = sum(s["gpa"] for s in students) / len(students)
print(f"\n--- Average GPA: {average_gpa:.2f} ---")


# Students above average
above_avg = [s for s in students if s["gpa"] > average_gpa]
print(f"  Above average ({len(above_avg)}):")
for student in above_avg:
    print(f"    {student['name']}: {student['gpa']}")


# Count students per city
print(f"\n--- Students by City ---")
city_counts = {}
for student in students:
    city = student["address"]["city"]
    city_counts[city] = city_counts.get(city, 0) + 1

for city, count in city_counts.items():
    print(f"  {city}: {count} student(s)")


# Collect all unique courses across students
all_courses = set()
for student in students:
    all_courses.update(student["courses"])

print(f"\n--- All Courses ({len(all_courses)}) ---")
for course in sorted(all_courses):
    print(f"  {course}")


# Find students enrolled in a specific course
target_course = "Data Structures"
enrolled = [s["name"] for s in students if target_course in s["courses"]]
print(f"\n--- Enrolled in '{target_course}' ---")
for name in enrolled:
    print(f"  {name}")


# Build a summary report and save it as a new JSON file
report = {
    "total_students": len(students),
    "active_count": len(active_students),
    "average_gpa": round(average_gpa, 2),
    "top_student": top_student["name"],
    "cities": city_counts,
    "total_courses": len(all_courses),
}

report_path = os.path.join(SCRIPT_DIR, "report.json")

with open(report_path, "w") as file:
    json.dump(report, file, indent=2)

print(f"\n--- Summary report saved to report.json ---")
print(json.dumps(report, indent=2))

# Clean up
os.remove(report_path)
