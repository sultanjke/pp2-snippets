# =============================================================
# Parent and Child Class Relationships + super()
# =============================================================


# Parent (base) class — defines shared behavior for all animals
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def speak(self):
        return f"{self.name} makes a sound."

    def describe(self):
        return f"{self.name} is a {self.species}."


# Child class inherits everything from Animal
class Dog(Animal):
    def __init__(self, name, breed):
        # super() calls the parent's __init__, reusing its setup logic
        super().__init__(name, species="Dog")
        self.breed = breed

    def speak(self):
        return f"{self.name} barks! Woof!"

    def fetch(self, item):
        return f"{self.name} fetches the {item}."


class Cat(Animal):
    def __init__(self, name, is_indoor):
        super().__init__(name, species="Cat")
        self.is_indoor = is_indoor

    def speak(self):
        return f"{self.name} meows! Meow!"


# Creating objects from parent and child classes
generic_animal = Animal("Unknown", "Unknown")
dog = Dog("Rex", "German Shepherd")
cat = Cat("Whiskers", is_indoor=True)

print("--- Parent and child objects ---")
print(generic_animal.speak())
print(dog.speak())
print(cat.speak())

# Child objects inherit methods they didn't override
print(f"\n{dog.describe()}")
print(f"{cat.describe()}")

# Child-only methods
print(f"\n{dog.fetch('ball')}")

# isinstance() checks work with inheritance
print(f"\n--- Type checks ---")
print(f"Is dog an Animal? {isinstance(dog, Animal)}")
print(f"Is dog a Dog?     {isinstance(dog, Dog)}")
print(f"Is cat a Dog?     {isinstance(cat, Dog)}")


# ---- Practical Application: University People System ----

class Person:
    def __init__(self, full_name, age):
        self.full_name = full_name
        self.age = age

    def introduce(self):
        return f"I'm {self.full_name}, {self.age} years old."


class Student(Person):
    def __init__(self, full_name, age, student_id, major):
        super().__init__(full_name, age)
        self.student_id = student_id
        self.major = major

    def introduce(self):
        base_intro = super().introduce()
        return f"{base_intro} Student #{self.student_id}, studying {self.major}."


class Professor(Person):
    def __init__(self, full_name, age, department, years_experience):
        super().__init__(full_name, age)
        self.department = department
        self.years_experience = years_experience

    def introduce(self):
        base_intro = super().introduce()
        return f"{base_intro} Professor in {self.department} ({self.years_experience} yrs)."


people = [
    Student("Sultan", 20, "CS-1001", "Computer Science"),
    Student("Alice", 22, "MA-1042", "Mathematics"),
    Professor("Dr. Smith", 45, "Computer Science", 15),
    Professor("Dr. Lee", 38, "Physics", 8),
]

print("\n--- University People ---")
for person in people:
    print(f"  {person.introduce()}")
