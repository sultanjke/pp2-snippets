# =============================================================
# Working with Timezones
# =============================================================

from datetime import datetime, timezone, timedelta


# A "naive" datetime has no timezone info
naive_now = datetime.now()
print(f"Naive (no tz):  {naive_now}")
print(f"  tzinfo:       {naive_now.tzinfo}\n")


# An "aware" datetime knows its timezone
# timezone.utc is the built-in UTC timezone
utc_now = datetime.now(timezone.utc)
print(f"Aware (UTC):    {utc_now}")
print(f"  tzinfo:       {utc_now.tzinfo}")


# Creating fixed-offset timezones with timedelta
almaty_tz = timezone(timedelta(hours=6))        # UTC+6
moscow_tz = timezone(timedelta(hours=3))        # UTC+3
new_york_tz = timezone(timedelta(hours=-5))     # UTC-5
tokyo_tz = timezone(timedelta(hours=9))         # UTC+9

almaty_now = datetime.now(almaty_tz)
moscow_now = datetime.now(moscow_tz)
new_york_now = datetime.now(new_york_tz)
tokyo_now = datetime.now(tokyo_tz)

print(f"\n--- Current time around the world ---")
print(f"  Almaty (UTC+6):    {almaty_now.strftime('%H:%M:%S  %Y-%m-%d')}")
print(f"  Moscow (UTC+3):    {moscow_now.strftime('%H:%M:%S  %Y-%m-%d')}")
print(f"  New York (UTC-5):  {new_york_now.strftime('%H:%M:%S  %Y-%m-%d')}")
print(f"  Tokyo (UTC+9):     {tokyo_now.strftime('%H:%M:%S  %Y-%m-%d')}")


# Converting between timezones with .astimezone()
meeting_almaty = datetime(2026, 3, 15, 10, 0, 0, tzinfo=almaty_tz)

meeting_moscow = meeting_almaty.astimezone(moscow_tz)
meeting_new_york = meeting_almaty.astimezone(new_york_tz)
meeting_utc = meeting_almaty.astimezone(timezone.utc)

print(f"\n--- Meeting at 10:00 Almaty time ---")
print(f"  Almaty:   {meeting_almaty.strftime('%H:%M %Z')}")
print(f"  Moscow:   {meeting_moscow.strftime('%H:%M %Z')}")
print(f"  New York: {meeting_new_york.strftime('%H:%M %Z')}")
print(f"  UTC:      {meeting_utc.strftime('%H:%M %Z')}")


# Making a naive datetime aware
naive_dt = datetime(2026, 6, 15, 12, 0, 0)
aware_dt = naive_dt.replace(tzinfo=almaty_tz)
print(f"\n--- Naive to aware ---")
print(f"  Naive: {naive_dt} (tzinfo={naive_dt.tzinfo})")
print(f"  Aware: {aware_dt} (tzinfo={aware_dt.tzinfo})")


# ISO format — standard way to represent aware datetimes
print(f"\n--- ISO format ---")
print(f"  {aware_dt.isoformat()}")
print(f"  {meeting_utc.isoformat()}")

# Parsing ISO format back
iso_string = "2026-03-15T10:00:00+06:00"
parsed = datetime.fromisoformat(iso_string)
print(f"  Parsed: {parsed} (tz={parsed.tzinfo})")


# Practical application: world clock for a remote team
print(f"\n--- Team availability check ---")
team_members = [
    {"name": "Sultan",  "tz": timezone(timedelta(hours=6)),  "city": "Almaty"},
    {"name": "Anna",    "tz": timezone(timedelta(hours=3)),  "city": "Moscow"},
    {"name": "Jake",    "tz": timezone(timedelta(hours=-5)), "city": "New York"},
    {"name": "Yuki",    "tz": timezone(timedelta(hours=9)),  "city": "Tokyo"},
]

# Find a meeting time that falls within 9:00-18:00 for everyone
proposed_utc = datetime(2026, 3, 15, 8, 0, 0, tzinfo=timezone.utc)

print(f"  Proposed meeting: {proposed_utc.strftime('%H:%M UTC')}\n")
all_available = True

for member in team_members:
    local_time = proposed_utc.astimezone(member["tz"])
    hour = local_time.hour
    is_working = 9 <= hour < 18
    status = "available" if is_working else "OUTSIDE HOURS"
    all_available = all_available and is_working
    print(f"  {member['name']:<8} ({member['city']:<10}) -> {local_time.strftime('%H:%M')} — {status}")

print(f"\n  Everyone available? {'Yes' if all_available else 'No'}")
