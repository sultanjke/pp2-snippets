# =============================================================
# RegEx Flags and Practical Patterns
# =============================================================

import re


# --- re.IGNORECASE (re.I) ---

text = "Python is great. PYTHON is powerful. python is fun."

without_flag = re.findall(r'python', text)
with_flag = re.findall(r'python', text, re.IGNORECASE)

print("--- re.IGNORECASE ---")
print(f"  Without flag: {without_flag}")
print(f"  With flag:    {with_flag}")


# --- re.MULTILINE (re.M) ---
# Makes ^ and $ match start/end of each LINE, not just start/end of string

multiline_text = """First line
Second line
Third line"""

without_multi = re.findall(r'^\w+', multiline_text)
with_multi = re.findall(r'^\w+', multiline_text, re.MULTILINE)
line_ends = re.findall(r'\w+$', multiline_text, re.MULTILINE)

print(f"\n--- re.MULTILINE ---")
print(f"  Without flag: {without_multi}")
print(f"  With flag:    {with_multi}")
print(f"  Line endings: {line_ends}")


# --- re.DOTALL (re.S) ---
# Makes . match newline characters too

html_block = "<div>\n  <p>Hello</p>\n</div>"

without_dotall = re.findall(r'<div>.*</div>', html_block)
with_dotall = re.findall(r'<div>.*</div>', html_block, re.DOTALL)

print(f"\n--- re.DOTALL ---")
print(f"  Without flag: {without_dotall}")
print(f"  With flag:    {with_dotall}")


# --- re.VERBOSE (re.X) ---
# Allows comments and whitespace in patterns for readability

phone_pattern = re.compile(r'''
    (\d{3})     # area code
    [-.\s]?     # optional separator
    (\d{3})     # first 3 digits
    [-.\s]?     # optional separator
    (\d{4})     # last 4 digits
''', re.VERBOSE)

print(f"\n--- re.VERBOSE ---")
test_phones = ["701-555-1234", "702.555.5678", "703 555 9012", "7045551234"]
for phone in test_phones:
    match = phone_pattern.search(phone)
    if match:
        print(f"  {phone} -> ({match.group(1)}) {match.group(2)}-{match.group(3)}")


# --- Combining flags with | ---

messy_html = "<DIV>\nSome Content\n</div>"
combined = re.findall(r'<div>(.*?)</div>', messy_html, re.IGNORECASE | re.DOTALL)
print(f"\n--- Combined flags (IGNORECASE | DOTALL) ---")
print(f"  Match: {combined}")


# --- re.compile() for reusable patterns ---

email_pattern = re.compile(r'[\w.+-]+@[\w-]+\.\w{2,}', re.IGNORECASE)

texts = [
    "Contact ADMIN@KBTU.KZ for help",
    "Email sultan.m@gmail.com or info@university.edu",
    "No email here, just text",
]

print(f"\n--- re.compile() ---")
for line in texts:
    found = email_pattern.findall(line)
    print(f"  '{line[:40]}...' -> {found}")


# --- Practical validation patterns ---

print(f"\n--- Practical validators ---")

validators = {
    "Email":    r'^[\w.+-]+@[\w-]+\.\w{2,}$',
    "Phone":    r'^\+?7[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$',
    "Password": r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$',
    "URL":      r'^https?://[\w.-]+\.\w{2,}(/\S*)?$',
}

test_cases = {
    "Email":    ["sultan@kbtu.kz", "invalid-email", "test@test.com"],
    "Phone":    ["+7 701 234 56 78", "+77011234567", "123"],
    "Password": ["Str0ngPass", "weakpass", "NoDigit!"],
    "URL":      ["https://kbtu.kz", "http://example.com/page", "not-a-url"],
}

for name, pattern in validators.items():
    print(f"\n  {name} validator:")
    for value in test_cases[name]:
        is_valid = re.match(pattern, value) is not None
        status = "VALID" if is_valid else "INVALID"
        print(f"    {value:<25} -> {status}")
