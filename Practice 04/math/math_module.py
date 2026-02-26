# =============================================================
# The math Module: sqrt, ceil, floor, sin, cos, pi, e
# =============================================================

import math


# Constants
print("--- Math constants ---")
print(f"  pi = {math.pi}")
print(f"  e  = {math.e}")
print(f"  tau (2*pi) = {math.tau}")
print(f"  inf = {math.inf}")


# sqrt() — square root
print(f"\n--- sqrt() ---")
print(f"  sqrt(16)  = {math.sqrt(16)}")
print(f"  sqrt(2)   = {math.sqrt(2)}")
print(f"  sqrt(144) = {math.sqrt(144)}")


# ceil() and floor() — rounding up and down
print(f"\n--- ceil() and floor() ---")
values = [2.1, 2.9, -2.1, -2.9]
for val in values:
    print(f"  ceil({val:>5}) = {math.ceil(val):>3}   floor({val:>5}) = {math.floor(val):>3}")


# Trigonometric functions (angles in radians)
print(f"\n--- Trigonometry ---")
angle_degrees = 45
angle_radians = math.radians(angle_degrees)

print(f"  {angle_degrees}° = {angle_radians:.4f} radians")
print(f"  sin(45°) = {math.sin(angle_radians):.4f}")
print(f"  cos(45°) = {math.cos(angle_radians):.4f}")
print(f"  tan(45°) = {math.tan(angle_radians):.4f}")

# Common angles
print(f"\n  Angle |   sin   |   cos")
print(f"  ------|---------|--------")
for deg in [0, 30, 45, 60, 90]:
    rad = math.radians(deg)
    print(f"  {deg:>3}°  | {math.sin(rad):>6.3f}  | {math.cos(rad):>6.3f}")


# Other useful functions
print(f"\n--- Other functions ---")
print(f"  log(100, 10) = {math.log(100, 10)}")     # log base 10
print(f"  log2(1024)   = {math.log2(1024)}")        # log base 2
print(f"  factorial(6) = {math.factorial(6)}")       # 6! = 720
print(f"  gcd(48, 18)  = {math.gcd(48, 18)}")       # greatest common divisor
print(f"  fabs(-7.5)   = {math.fabs(-7.5)}")        # float absolute value
print(f"  pow(2, 10)   = {math.pow(2, 10)}")         # always returns float


# Practical application: distance between two 2D points
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


points = [(0, 0), (3, 4), (6, 8), (1, 7)]

print(f"\n--- Distances between points ---")
for i in range(len(points) - 1):
    x1, y1 = points[i]
    x2, y2 = points[i + 1]
    dist = euclidean_distance(x1, y1, x2, y2)
    print(f"  ({x1},{y1}) -> ({x2},{y2}) = {dist:.2f}")


# Practical application: circle calculations
radius = 7.5
circumference = 2 * math.pi * radius
area = math.pi * radius ** 2

print(f"\n--- Circle (radius={radius}) ---")
print(f"  Circumference: {circumference:.2f}")
print(f"  Area:          {area:.2f}")
