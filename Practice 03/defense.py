class Animal:
    def __init__(self, name):
        self.name = name
    def sound(self):
        print("This animal makes a sound.")
class Dog(Animal):
    def __init__(self, name, age):
        super().__init__(name) # self.name = name
        self.age = age
    def sound(self):
        print(f"{self.name} says: Woof!")
class Cat(Animal):
    def sound(self):
        print(f"{self.name} says: Meow!")

animal_1 = Animal("Some animal")
dog_1 = Dog("Luna", 3)
cat_1 = Cat("Max")

animal_1.sound()
dog_1.sound()
cat_1.sound()