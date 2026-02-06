
people_ages = {
    "Sultan": 18,
    "Aruzhan": 19,
    "Dias": 20,
    "Amina": 17,
    "Timur": 25
}


test_names = ["Dias", "Timur", "Sultan", "Ali", "Amina"]


for name in test_names:
    if name in people_ages and 18 <= people_ages[name] <= 24:
        print(f"{name} прошёл тест (возраст: {people_ages[name]})")
    elif name in people_ages:
        print(f"{name} найден, но возраст не подходит (возраст: {people_ages[name]})")
    else:
        print(f"{name} не найден в словаре ")
