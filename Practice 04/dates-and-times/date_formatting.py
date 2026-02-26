# =============================================================
# Date Formatting: strftime() and strptime()
# =============================================================

import datetime


now = datetime.datetime.now()

# strftime() — datetime object -> formatted string
print("--- strftime(): object -> string ---")
print(f"  Default:      {now}")
print(f"  Full date:    {now.strftime('%Y-%m-%d')}")
print(f"  US style:     {now.strftime('%m/%d/%Y')}")
print(f"  European:     {now.strftime('%d.%m.%Y')}")
print(f"  With time:    {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  12-hour:      {now.strftime('%I:%M %p')}")
print(f"  Day name:     {now.strftime('%A, %B %d, %Y')}")
print(f"  Short form:   {now.strftime('%a, %b %d')}")


# Common format codes reference
print(f"""
--- Format codes ---
  %Y  Full year       -> {now.strftime('%Y')}
  %y  Short year      -> {now.strftime('%y')}
  %m  Month (01-12)   -> {now.strftime('%m')}
  %B  Month name      -> {now.strftime('%B')}
  %b  Month short     -> {now.strftime('%b')}
  %d  Day (01-31)     -> {now.strftime('%d')}
  %A  Weekday name    -> {now.strftime('%A')}
  %a  Weekday short   -> {now.strftime('%a')}
  %H  Hour 24h        -> {now.strftime('%H')}
  %I  Hour 12h        -> {now.strftime('%I')}
  %M  Minute          -> {now.strftime('%M')}
  %S  Second          -> {now.strftime('%S')}
  %p  AM/PM           -> {now.strftime('%p')}
""")


# strptime() — string -> datetime object (parsing)
print("--- strptime(): string -> object ---")

date_string_1 = "2026-03-15"
parsed_1 = datetime.datetime.strptime(date_string_1, "%Y-%m-%d")
print(f"  '{date_string_1}' -> {parsed_1}")

date_string_2 = "March 20, 2026 at 14:30"
parsed_2 = datetime.datetime.strptime(date_string_2, "%B %d, %Y at %H:%M")
print(f"  '{date_string_2}' -> {parsed_2}")

date_string_3 = "15/06/2026"
parsed_3 = datetime.datetime.strptime(date_string_3, "%d/%m/%Y")
print(f"  '{date_string_3}' -> {parsed_3}")


# Converting between formats
original = "2026-05-20 10:30:00"
parsed = datetime.datetime.strptime(original, "%Y-%m-%d %H:%M:%S")
reformatted = parsed.strftime("%A, %B %d, %Y at %I:%M %p")
print(f"\n  Original:    '{original}'")
print(f"  Reformatted: '{reformatted}'")


# Practical application: parsing and sorting event dates
raw_event_dates = [
    "15 Jan 2026 09:00",
    "03 Mar 2026 14:30",
    "28 Feb 2026 11:00",
    "10 Jan 2026 16:45",
    "22 Apr 2026 08:15",
]

parsed_events = []
for raw_date in raw_event_dates:
    event_dt = datetime.datetime.strptime(raw_date, "%d %b %Y %H:%M")
    parsed_events.append(event_dt)

parsed_events.sort()

print("--- Events sorted chronologically ---")
for event in parsed_events:
    print(f"  {event.strftime('%A, %B %d %Y — %H:%M')}")
