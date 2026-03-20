import os
from functools import reduce


base_folder = os.path.dirname(__file__)
scores_folder = os.path.join(base_folder, "scores")
report_file = os.path.join(base_folder, "report.txt")


# step 1. directory handling
all_files = os.listdir(scores_folder)
txt_files = []

for file_name in all_files:
    if file_name.endswith(".txt"):
        txt_files.append(file_name)

print("Files found in scores folder:")
for file_name in txt_files:
    print(file_name)


# step 2. file handling
students = []

for file_name in txt_files:
    file_path = os.path.join(scores_folder, file_name)
    file = open(file_path, "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        line = line.strip()

        if line != "":
            parts = line.split(",")
            name = parts[0]
            score = int(parts[1])
            students.append((name, score))

print("\nAll student records:")
print(students)


# step 3.1. count total students
total_students = len(students)
print("\nTotal students:", total_students)


# step 3.2. calculate total score
scores = []
for student in students:
    scores.append(student[1])

total_score = sum(scores)
print("Total score:", total_score)


# step 3.3. find highest and lowest score
highest_score = max(scores)
lowest_score = min(scores)
print("Highest score:", highest_score)
print("Lowest score:", lowest_score)


# step 3.4. increase all score by 5 points
increased_scores = list(map(lambda x: x + 5, scores))
print("Scores increased by 5:", increased_scores)


# step 3.5. find students with score > 85
top_students = list(filter(lambda student: student[1] > 85, students))
print("\nTop students (>85):")
for student in top_students:
    print(student[0], student[1])


# step 3.6. calculate product of all scores
product_of_scores = reduce(lambda x, y: x * y, scores)
print("\nProduct of all scores:", product_of_scores)


# step 3.7. print students with index numbers
print("\nStudents with index numbers:")
for index, student in enumerate(students, start=1):
    print(index, student[0], student[1])


# step 3.8. combine names and scores using zip
names = []
for student in students:
    names.append(student[0])

combined_data = list(zip(names, scores))
print("\nCombined names and scores:")
print(combined_data)


# step 3.9. sort students by score
sorted_students = sorted(students, key=lambda student: student[1], reverse=True)
print("\nStudents sorted by score:")
for student in sorted_students:
    print(student[0], student[1])


# step 4. save results to file
average_score = total_score / total_students

report = open(report_file, "w")
report.write("Total students: " + str(total_students) + "\n")
report.write("Average score: " + str(round(average_score, 2)) + "\n")
report.write("Highest score: " + str(highest_score) + "\n")
report.write("Lowest score: " + str(lowest_score) + "\n")
report.write("Top students:\n")

for student in top_students:
    report.write(student[0] + " " + str(student[1]) + "\n")

report.close()

print("\nReport saved to report.txt")
