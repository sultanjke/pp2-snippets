# =============================================================
# Generators: The yield Keyword
# =============================================================

# A generator function uses 'yield' instead of 'return'.
# Each call to next() runs until the next yield, pauses,
# and resumes from where it left off.


def countdown(start):
    """Yield numbers from start down to 1."""
    current = start
    while current > 0:
        yield current
        current -= 1


print("--- Generator countdown ---")
for number in countdown(5):
    print(f"  {number}")


# Generators are memory efficient — they produce values
# one at a time instead of building an entire list.

def even_numbers(limit):
    """Yield even numbers from 2 up to limit."""
    number = 2
    while number <= limit:
        yield number
        number += 2


print("\n--- Even numbers up to 14 ---")
for even in even_numbers(14):
    print(f"  {even}", end="")
print()


# A generator with multiple yields acts like a state machine
def traffic_light():
    """Cycle through traffic light states."""
    while True:
        yield "GREEN"
        yield "YELLOW"
        yield "RED"


print("\n--- Traffic light (6 cycles) ---")
light = traffic_light()
for _ in range(6):
    print(f"  {next(light)}")


# yield can also produce transformed data on the fly
def word_lengths(sentences):
    """Yield (word, length) pairs for every word in each sentence."""
    for sentence in sentences:
        for word in sentence.split():
            yield word, len(word)


sample_sentences = [
    "Python is powerful",
    "Generators save memory",
]

print("\n--- Word lengths ---")
for word, length in word_lengths(sample_sentences):
    print(f"  '{word}' -> {length}")


# Practical application: processing a large dataset row by row
def read_sensor_data(readings):
    """
    Yield only abnormal readings (temperature > 40 or < -10)
    from a stream of sensor data.
    """
    for reading in readings:
        if reading["temperature"] > 40 or reading["temperature"] < -10:
            yield reading


sensor_stream = [
    {"sensor_id": "A1", "temperature": 22.5},
    {"sensor_id": "A2", "temperature": 45.3},
    {"sensor_id": "B1", "temperature": -12.0},
    {"sensor_id": "B2", "temperature": 35.1},
    {"sensor_id": "C1", "temperature": 50.7},
    {"sensor_id": "C2", "temperature": 18.9},
]

print("\n--- Abnormal sensor readings ---")
for alert in read_sensor_data(sensor_stream):
    print(f"  ALERT: Sensor {alert['sensor_id']} -> {alert['temperature']}°C")


# Generators can be chained together into pipelines
def parse_lines(raw_lines):
    """Strip whitespace and skip empty lines."""
    for line in raw_lines:
        cleaned = line.strip()
        if cleaned:
            yield cleaned


def to_uppercase(lines):
    """Convert each line to uppercase."""
    for line in lines:
        yield line.upper()


def add_line_numbers(lines):
    """Prefix each line with its number."""
    for index, line in enumerate(lines, start=1):
        yield f"  {index}. {line}"


raw_data = ["  hello  ", "", " world ", "  python  ", "", " generators "]

print("\n--- Generator pipeline ---")
pipeline = add_line_numbers(to_uppercase(parse_lines(raw_data)))
for result in pipeline:
    print(result)
