# =============================================================
# Modifying and Deleting Object Properties
# =============================================================
# Once an object is created, you can:
#   - READ    attributes:  obj.attr
#   - MODIFY  attributes:  obj.attr = new_value
#   - ADD     attributes:  obj.new_attr = value
#   - DELETE  attributes:  del obj.attr
#
# You can also use built-in functions:
#   - getattr(obj, 'attr', default)
#   - setattr(obj, 'attr', value)
#   - delattr(obj, 'attr')
#   - hasattr(obj, 'attr')
# =============================================================


# --- Basic modification ---
class Car:
    def __init__(self, make, model, year, mileage=0):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage

    def info(self):
        return f"{self.year} {self.make} {self.model} ({self.mileage:,} km)"


car = Car("Toyota", "Camry", 2022, 15000)
print("Original:", car.info())

# Modify existing attributes directly
car.mileage = 23000
car.year = 2023
print("Modified:", car.info())


# --- Adding new attributes after creation ---
# Python allows adding attributes that weren't in __init__
car.color = "Red"
car.owner = "Sultan"

print(f"\nAdded attributes -> color: {car.color}, owner: {car.owner}")


# --- Deleting attributes ---
# 'del' removes an attribute from the object entirely
del car.owner
print(f"\nAfter deleting 'owner':")
print(f"  hasattr(car, 'owner'): {hasattr(car, 'owner')}")  # False
print(f"  hasattr(car, 'color'): {hasattr(car, 'color')}")  # True


# --- Safe access with getattr ---
# getattr lets you provide a default if the attribute doesn't exist
owner = getattr(car, "owner", "No owner assigned")
color = getattr(car, "color", "Unknown")
print(f"\n  getattr 'owner': {owner}")
print(f"  getattr 'color': {color}")


# --- Using setattr and delattr programmatically ---
# Useful when attribute names come from variables or data
class UserProfile:
    def __init__(self, username):
        self.username = username

    def show(self):
        print(f"\n  Profile for '{self.username}':")
        # vars() returns the object's __dict__ (all attributes)
        for key, value in vars(self).items():
            print(f"    {key}: {value}")


profile = UserProfile("sultan_dev")

# Dynamically set attributes from a dictionary
updates = {"email": "sultan@example.com", "age": 20, "city": "Almaty"}

for key, value in updates.items():
    setattr(profile, key, value)

profile.show()

# Dynamically delete an attribute
delattr(profile, "city")
print("\nAfter delattr('city'):")
profile.show()


# --- Controlling modifications with methods ---
# Instead of letting users modify attributes directly, use
# methods to add validation and logging
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius  # Leading _ signals "use methods"

    def get_celsius(self):
        return self._celsius

    def set_celsius(self, value):
        if value < -273.15:
            print("  Error: temperature below absolute zero!")
            return
        self._celsius = value
        print(f"  Temperature set to {value}°C")

    def get_fahrenheit(self):
        return round(self._celsius * 9 / 5 + 32, 1)


print("\n--- Controlled modification ---")
temp = Temperature(25)
print(f"  Current: {temp.get_celsius()}°C / {temp.get_fahrenheit()}°F")

temp.set_celsius(100)
print(f"  Updated: {temp.get_celsius()}°C / {temp.get_fahrenheit()}°F")

temp.set_celsius(-300)  # Rejected by validation


# =============================================================
# Practical Application: Editable Contact Book
# =============================================================
class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email


class ContactBook:
    def __init__(self):
        self.contacts = {}

    def add(self, name, phone, email):
        self.contacts[name] = Contact(name, phone, email)
        print(f"  Added: {name}")

    def update(self, name, **fields):
        """Update one or more fields of an existing contact."""
        if name not in self.contacts:
            print(f"  '{name}' not found.")
            return
        contact = self.contacts[name]
        for field, value in fields.items():
            if hasattr(contact, field):
                old = getattr(contact, field)
                setattr(contact, field, value)
                print(f"  Updated {name}'s {field}: '{old}' -> '{value}'")
            else:
                print(f"  Warning: '{field}' is not a valid field.")

    def delete(self, name):
        """Remove a contact from the book."""
        if name in self.contacts:
            del self.contacts[name]
            print(f"  Deleted: {name}")
        else:
            print(f"  '{name}' not found.")

    def show_all(self):
        print(f"\n--- Contact Book ({len(self.contacts)} contacts) ---")
        for c in self.contacts.values():
            print(f"  {c.name:<10} | {c.phone:<15} | {c.email}")


book = ContactBook()
book.add("Alice", "+7-701-111-1111", "alice@example.com")
book.add("Bob", "+7-702-222-2222", "bob@example.com")
book.add("Charlie", "+7-703-333-3333", "charlie@example.com")

book.show_all()

# Modify a contact's fields
print()
book.update("Alice", phone="+7-701-999-9999", email="alice.new@example.com")
book.update("Bob", email="bob.updated@example.com")

book.show_all()

# Delete a contact
print()
book.delete("Charlie")
book.show_all()
