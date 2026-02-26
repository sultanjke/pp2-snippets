# =============================================================
# The random Module: random, randint, choice, shuffle
# =============================================================

import random


# random() — returns a float between 0.0 and 1.0
print("--- random() ---")
for i in range(5):
    print(f"  {random.random():.4f}")


# randint(a, b) — random integer between a and b (inclusive)
print(f"\n--- randint() ---")
print(f"  Dice roll (1-6):  {random.randint(1, 6)}")
print(f"  Random age (1-100): {random.randint(1, 100)}")
print(f"  Random year: {random.randint(2020, 2030)}")


# uniform(a, b) — random float between a and b
print(f"\n--- uniform() ---")
temperature = random.uniform(-10.0, 40.0)
price = random.uniform(5.0, 100.0)
print(f"  Random temperature: {temperature:.1f}°C")
print(f"  Random price: ${price:.2f}")


# randrange(start, stop, step) — like range() but picks one randomly
print(f"\n--- randrange() ---")
print(f"  Random even (0-20):  {random.randrange(0, 21, 2)}")
print(f"  Random multiple of 5 (0-50): {random.randrange(0, 51, 5)}")


# choice() — pick one random element from a sequence
colors = ["red", "blue", "green", "yellow", "purple"]
cities = ["Almaty", "Astana", "Moscow", "Tokyo", "Berlin"]

print(f"\n--- choice() ---")
print(f"  Random color: {random.choice(colors)}")
print(f"  Random city:  {random.choice(cities)}")


# choices() — pick multiple elements (with replacement)
print(f"\n--- choices() (with replacement) ---")
print(f"  3 random colors: {random.choices(colors, k=3)}")


# sample() — pick multiple unique elements (without replacement)
print(f"\n--- sample() (without replacement) ---")
lottery_numbers = random.sample(range(1, 50), 6)
print(f"  Lottery numbers: {sorted(lottery_numbers)}")


# shuffle() — reorder a list in place
deck = list(range(1, 11))
print(f"\n--- shuffle() ---")
print(f"  Before: {deck}")
random.shuffle(deck)
print(f"  After:  {deck}")


# seed() — set a fixed seed for reproducible results
print(f"\n--- seed() for reproducibility ---")
random.seed(42)
run_1 = [random.randint(1, 100) for _ in range(5)]
random.seed(42)
run_2 = [random.randint(1, 100) for _ in range(5)]
print(f"  Run 1: {run_1}")
print(f"  Run 2: {run_2}")
print(f"  Identical? {run_1 == run_2}")


# Practical application: quiz game with random questions
questions = [
    {"q": "Capital of Kazakhstan?", "answer": "Astana"},
    {"q": "2 ** 10 = ?",            "answer": "1024"},
    {"q": "Largest ocean?",         "answer": "Pacific"},
    {"q": "Python creator?",        "answer": "Guido van Rossum"},
    {"q": "Boiling point of water?","answer": "100°C"},
]

num_questions = 3
selected = random.sample(questions, num_questions)

print(f"\n--- Random Quiz ({num_questions} of {len(questions)} questions) ---")
for i, question in enumerate(selected, 1):
    print(f"  Q{i}: {question['q']}")
    print(f"      Answer: {question['answer']}")


# Practical application: password generator
def generate_password(length=12):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"
    return "".join(random.choices(chars, k=length))


print(f"\n--- Random passwords ---")
for i in range(3):
    print(f"  {generate_password(16)}")
