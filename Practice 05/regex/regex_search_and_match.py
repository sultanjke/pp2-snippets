# =============================================================
# re.search() and re.match() — Finding Matches
# =============================================================

import re


# --- re.search(): finds the FIRST match anywhere in the string ---

text = "Order #12345 was placed on 2026-03-15 for $99.99"

# Returns a Match object or None
match = re.search(r'\d+', text)

print("--- re.search() ---")
print(f"  Text: '{text}'")
print(f"  Pattern: '\\d+'")
print(f"  Match found: {match is not None}")
print(f"  Matched value: {match.group()}")
print(f"  Start position: {match.start()}")
print(f"  End position: {match.end()}")
print(f"  Span: {match.span()}")


# search() finds the first occurrence, not all of them
print(f"\n  First number found: {match.group()} (not all numbers)")


# Using groups to extract parts of a match
date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)

print(f"\n--- Groups ---")
print(f"  Full date: {date_match.group()}")
print(f"  Year:  {date_match.group(1)}")
print(f"  Month: {date_match.group(2)}")
print(f"  Day:   {date_match.group(3)}")
print(f"  All groups: {date_match.groups()}")


# Named groups with (?P<name>...)
named_match = re.search(
    r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', text
)

print(f"\n--- Named Groups ---")
print(f"  Year:  {named_match.group('year')}")
print(f"  Month: {named_match.group('month')}")
print(f"  Day:   {named_match.group('day')}")


# --- re.match(): matches only at the BEGINNING of the string ---

print(f"\n\n--- re.match() ---")

# match() only checks the start of the string
result_1 = re.match(r'Order', text)
result_2 = re.match(r'placed', text)

print(f"  match('Order', text):  {result_1 is not None}")   # True — starts with "Order"
print(f"  match('placed', text): {result_2 is not None}")   # False — not at start

# search() would find "placed" anywhere
result_3 = re.search(r'placed', text)
print(f"  search('placed', text): {result_3 is not None}")  # True


# --- Safe pattern matching with if/else ---

print(f"\n--- Safe matching ---")

user_input = "sultan.m@kbtu.kz"
email_pattern = r'^[\w.+-]+@[\w-]+\.\w{2,}$'

email_match = re.match(email_pattern, user_input)
if email_match:
    print(f"  '{user_input}' is a valid email")
else:
    print(f"  '{user_input}' is NOT a valid email")

bad_input = "not-an-email"
if re.match(email_pattern, bad_input):
    print(f"  '{bad_input}' is a valid email")
else:
    print(f"  '{bad_input}' is NOT a valid email")


# Practical application: parsing log lines
log_lines = [
    "2026-03-15 10:30:45 ERROR Database connection failed",
    "2026-03-15 10:31:02 INFO  Server restarted",
    "2026-03-15 10:31:15 WARN  High memory usage: 92%",
    "2026-03-15 10:32:00 ERROR Timeout on request /api/users",
]

log_pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+)\s+(.*)'

print(f"\n--- Parsing log lines ---")
for line in log_lines:
    log_match = re.search(log_pattern, line)
    if log_match:
        date, time, level, message = log_match.groups()
        if level == "ERROR":
            print(f"  [{date} {time}] {level}: {message}")
