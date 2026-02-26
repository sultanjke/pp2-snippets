# =============================================================
# re.findall(), re.split(), re.sub() — Bulk Operations
# =============================================================

import re


# --- re.findall(): returns ALL matches as a list ---

text = "My phone is 701-555-1234 and office is 702-555-5678"

print("--- re.findall() ---")

# Find all numbers
all_numbers = re.findall(r'\d+', text)
print(f"  All numbers: {all_numbers}")

# Find all phone numbers
phones = re.findall(r'\d{3}-\d{3}-\d{4}', text)
print(f"  Phone numbers: {phones}")

# Find all words starting with uppercase
sentence = "Alice and Bob went to Central Park in New York"
capitalized = re.findall(r'\b[A-Z][a-z]*\b', sentence)
print(f"  Capitalized words: {capitalized}")

# With groups, findall returns the group contents
html = '<a href="page1.html">Link 1</a> and <a href="page2.html">Link 2</a>'
links = re.findall(r'href="(.*?)"', html)
print(f"  Extracted links: {links}")

# Multiple groups return list of tuples
pairs = re.findall(r'(\w+)=(\d+)', 'x=10 y=20 z=30')
print(f"  Key-value pairs: {pairs}")


# --- re.split(): split string by a pattern ---

print(f"\n--- re.split() ---")

# Split by one or more spaces
messy = "Hello   World    Python   RegEx"
clean = re.split(r'\s+', messy)
print(f"  Split by spaces: {clean}")

# Split by multiple delimiters at once
data = "apple;banana,cherry orange:grape"
fruits = re.split(r'[;,\s:]+', data)
print(f"  Split by ;,: and space: {fruits}")

# maxsplit parameter limits the number of splits
limited = re.split(r'\s+', messy, maxsplit=2)
print(f"  maxsplit=2: {limited}")

# Split and keep the delimiters using groups
parts = re.split(r'(\d+)', "item1cost20qty3")
print(f"  Keep delimiters: {parts}")


# --- re.sub(): replace matches with a new string ---

print(f"\n--- re.sub() ---")

# Basic replacement
censored = re.sub(r'\d', '*', "My card: 4532-1234-5678-9012")
print(f"  Censor digits: {censored}")

# Replace multiple spaces with a single space
cleaned = re.sub(r'\s+', ' ', "Too   many     spaces   here")
print(f"  Clean spaces: '{cleaned}'")

# Remove all non-alphanumeric characters
stripped = re.sub(r'[^a-zA-Z0-9\s]', '', "Hello! How's it going? #great")
print(f"  Remove symbols: '{stripped}'")

# count parameter limits replacements
partial = re.sub(r'\d', 'X', "a1b2c3d4e5", count=3)
print(f"  Replace first 3 digits: {partial}")

# Using a function as replacement
def to_upper(match):
    return match.group().upper()

result = re.sub(r'\b[a-z]', to_upper, "hello world python regex")
print(f"  Capitalize first letters: '{result}'")


# Practical application: cleaning and standardizing data
raw_records = [
    "  John   Doe,  +7-701-111-1111 , john@email.com  ",
    "Jane    Smith,+7-702-222-2222,jane@email.com",
    "  Bob  Johnson , +7-703-333-3333,  bob@email.com ",
]

print(f"\n--- Cleaning raw data ---")
for record in raw_records:
    # Normalize spaces and strip
    clean_record = re.sub(r'\s+', ' ', record.strip())
    # Normalize comma spacing
    clean_record = re.sub(r'\s*,\s*', ', ', clean_record)
    print(f"  {clean_record}")


# Practical application: extracting all emails from a text block
email_text = """
Contact us at support@kbtu.kz or admin@kbtu.kz.
For admissions: admissions@university.edu
Personal: sultan.m@gmail.com
"""

emails = re.findall(r'[\w.+-]+@[\w-]+\.\w{2,}', email_text)
print(f"\n--- Extracted emails ---")
for email in emails:
    print(f"  {email}")
