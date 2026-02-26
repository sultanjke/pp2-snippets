import math


# 1. Convert degree to radian
degree = float(input("1. Input degree: "))
radian = math.radians(degree)
print(f"   Output radian: {radian:.6f}")


# 2. Calculate the area of a trapezoid
height = float(input("\n2. Height: "))
base_1 = float(input("   Base, first value: "))
base_2 = float(input("   Base, second value: "))
trapezoid_area = 0.5 * (base_1 + base_2) * height
print(f"   Expected Output: {trapezoid_area}")


# 3. Calculate the area of a regular polygon
num_sides = int(input("\n3. Input number of sides: "))
side_length = float(input("   Input the length of a side: "))
polygon_area = (num_sides * side_length ** 2) / (4 * math.tan(math.pi / num_sides))
print(f"   The area of the polygon is: {polygon_area:.0f}")


# 4. Calculate the area of a parallelogram
base = float(input("\n4. Length of base: "))
height_p = float(input("   Height of parallelogram: "))
parallelogram_area = base * height_p
print(f"   Expected Output: {parallelogram_area}")
