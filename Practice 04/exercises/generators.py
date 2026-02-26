# 1. Generator that generates squares of numbers up to N
def squares_up_to(n):
    for i in range(1, n + 1):
        yield i ** 2


print("1. Squares up to N=5:")
for square in squares_up_to(5):
    print(f"   {square}", end="")
print()


# 2. Generator to print even numbers between 0 and n, comma separated
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i


n = int(input("\n2. Enter a number: "))
print("   " + ", ".join(str(x) for x in even_numbers(n)))


# 3. Generator for numbers divisible by 3 AND 4 between 0 and n
def divisible_by_3_and_4(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


print("\n3. Numbers divisible by 3 and 4 (0 to 100):")
print("   " + ", ".join(str(x) for x in divisible_by_3_and_4(100)))


# 4. Generator 'squares' that yields square of all numbers from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2


print("\n4. Squares from 2 to 8:")
for value in squares(2, 8):
    print(f"   {value}", end="")
print()


# 5. Generator that returns all numbers from n down to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


print("\n5. Countdown from 10:")
for num in countdown(10):
    print(f"   {num}", end="")
print()
