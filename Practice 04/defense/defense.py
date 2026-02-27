import json


with open("instructors.json", "r", encoding="utf-8") as f:
    instructors = json.load(f)

with open("students.json", "r", encoding="utf-8") as f:
    students = json.load(f)


students_under_instructor = {}

for instructor in instructors:
    students_under_instructor[instructor["name"]] = []

for student in students:
    placed = False

    for instructor in instructors:
        if student["year"] == instructor["instructs_year"]:
            students_under_instructor[instructor["name"]].append(student)
            placed = True
            break

    if placed == False:
        if "Unassigned" not in students_under_instructor:
            students_under_instructor["Unassigned"] = []
        students_under_instructor["Unassigned"].append(student)


# output
output = {
    "instructors": instructors,
    "students": students,
    "students_under_instructor": students_under_instructor
}

with open("students_under_instructor.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Done! Created students_under_instructor.json")