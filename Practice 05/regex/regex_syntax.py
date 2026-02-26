# =============================================================
# RegEx Syntax: Metacharacters, Special Sequences, Sets,
# and Quantifiers
# =============================================================

import re


# --- Metacharacters: . * + ? ^ $ [] | () \ ---

text = "The cat sat on the mat at 3:30pm"

# .  — matches any single character (except newline)
print("--- . (dot) ---")
print(f"  '.at' matches: {re.findall(r'.at', text)}")

# *  — zero or more of the preceding character
print("\n--- * (zero or more) ---")
print(f"  'ca*t' in 'ct cat caat': {re.findall(r'ca*t', 'ct cat caat')}")

# +  — one or more of the preceding character
print("\n--- + (one or more) ---")
print(f"  'ca+t' in 'ct cat caat': {re.findall(r'ca+t', 'ct cat caat')}")

# ?  — zero or one of the preceding character
print("\n--- ? (zero or one) ---")
print(f"  'colou?r' matches: {re.findall(r'colou?r', 'color colour')}")

# ^  — matches start of string
print("\n--- ^ (start of string) ---")
print(f"  '^The' in text: {re.search(r'^The', text) is not None}")
print(f"  '^cat' in text: {re.search(r'^cat', text) is not None}")

# $  — matches end of string
print("\n--- $ (end of string) ---")
print(f"  'pm$' in text: {re.search(r'pm$', text) is not None}")
print(f"  'cat$' in text: {re.search(r'cat$', text) is not None}")

# []  — character set (match any one character inside)
print("\n--- [] (character set) ---")
print(f"  '[cmb]at' matches: {re.findall(r'[cmb]at', text)}")

# |  — OR operator
print("\n--- | (OR) ---")
print(f"  'cat|mat' matches: {re.findall(r'cat|mat', text)}")

# ()  — grouping
print("\n--- () (groups) ---")
match = re.search(r'(\d+):(\d+)', text)
if match:
    print(f"  Full match: {match.group()}")
    print(f"  Group 1 (hour): {match.group(1)}")
    print(f"  Group 2 (min):  {match.group(2)}")

# \  — escape special characters
print("\n--- \\ (escape) ---")
price = "Total: $25.99"
matches = re.findall(r'\$\d+\.\d+', price)
print(f"  '$\\d+\\.\\d+' matches: {matches}")


# --- Special Sequences ---

sample = "Hello World 123 test_var"

print("\n\n--- Special Sequences ---")

# \d — any digit [0-9]
digits = re.findall(r'\d+', sample)
print(f"  \\d+ (digits):       {digits}")

# \D — any NON-digit
non_digits = re.findall(r'\D+', sample)
print(f"  \\D+ (non-digits):   {non_digits}")

# \w — word character [a-zA-Z0-9_]
words = re.findall(r'\w+', sample)
print(f"  \\w+ (words):        {words}")

# \W — non-word character
non_words = re.findall(r'\W+', sample)
print(f"  \\W+ (non-words):    {non_words}")

# \s — whitespace
spaces = re.findall(r'\s', sample)
print(f"  \\s (spaces):        {spaces}")

# \S — non-whitespace
non_spaces = re.findall(r'\S+', sample)
print(f"  \\S+ (non-spaces):   {non_spaces}")

# \A — start of string (like ^ but not affected by MULTILINE)
has_hello = re.search(r'\AHello', sample) is not None
print(f"  \\AHello:            {has_hello}")

# \Z — end of string (like $ but not affected by MULTILINE)
ends_var = re.search(r'var\Z', sample) is not None
print(f"  var\\Z:              {ends_var}")

# \b — word boundary
world_match = re.findall(r'\bWorld\b', sample)
print(f"  \\bWorld\\b:          {world_match}")


# --- Sets and Character Classes ---

print("\n\n--- Sets and Character Classes ---")

data = "abc ABC 123 !@# aB3"

# [a-z] — lowercase letters
print(f"  [a-z]+:      {re.findall(r'[a-z]+', data)}")

# [A-Z] — uppercase letters
print(f"  [A-Z]+:      {re.findall(r'[A-Z]+', data)}")

# [0-9] — digits (same as \d)
print(f"  [0-9]+:      {re.findall(r'[0-9]+', data)}")

# [a-zA-Z] — all letters
print(f"  [a-zA-Z]+:   {re.findall(r'[a-zA-Z]+', data)}")

# [^a-z] — NOT lowercase (^ inside [] means negation)
print(f"  [^a-z ]+:    {re.findall(r'[^a-z ]+', data)}")

# [aeiou] — only vowels
print(f"  [aeiou]:     {re.findall(r'[aeiou]', 'Hello World')}")


# --- Quantifiers: {n}, {n,}, {n,m} ---

print("\n\n--- Quantifiers ---")

codes = "A1 AB12 ABC123 ABCD1234 AB1"

# {n} — exactly n times
exact_2 = re.findall(r'[A-Z]{2}', codes)
print(f"  [A-Z]{{2}}:          {exact_2}")

# {n,} — n or more times
three_plus = re.findall(r'[A-Z]{3,}', codes)
print(f"  [A-Z]{{3,}}:         {three_plus}")

# {n,m} — between n and m times
two_to_three = re.findall(r'\d{2,3}', codes)
print(f"  \\d{{2,3}}:           {two_to_three}")

# Practical: phone number pattern — exactly 3 digits, dash, 3 digits, dash, 4 digits
phones = "Call 701-555-1234 or 702-555-5678 today"
pattern = r'\d{3}-\d{3}-\d{4}'
found_phones = re.findall(pattern, phones)
print(f"\n  Phone numbers: {found_phones}")
