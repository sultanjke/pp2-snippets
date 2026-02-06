def score_to_gpa(score):
    if 95 <= score <= 100:
        return 4.00
    elif 90 <= score <= 94:
        return 3.67
    elif 85 <= score <= 89:
        return 3.33
    elif 80 <= score <= 84:
        return 3.00
    elif 75 <= score <= 79:
        return 2.67
    elif 70 <= score <= 74:
        return 2.33
    elif 65 <= score <= 69:
        return 2.00
    elif 60 <= score <= 64:
        return 1.67
    else:
        return 0.00


grades_100 = {
    "Sultan": 85,
    "Aruzhan": 92,
    "Dias": 76,
    "Amina": 98
}

print("GPA студентов:\n")

for name, score in grades_100.items():
    gpa = score_to_gpa(score)
    print(f"{name}: {score} баллов - GPA {gpa:.2f}")
