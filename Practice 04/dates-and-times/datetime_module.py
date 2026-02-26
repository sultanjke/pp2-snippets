# =============================================================
# The datetime Module & Creating Date Objects
# =============================================================

import datetime


# datetime.date — stores year, month, day
today = datetime.date.today()
print(f"Today's date: {today}")
print(f"  Year:  {today.year}")
print(f"  Month: {today.month}")
print(f"  Day:   {today.day}")

# Creating a specific date
independence_day = datetime.date(1991, 12, 16)
print(f"\nKazakhstan Independence Day: {independence_day}")


# datetime.time — stores hour, minute, second, microsecond
class_start = datetime.time(9, 0, 0)
class_end = datetime.time(10, 30, 0)
precise_time = datetime.time(14, 30, 45, 123456)

print(f"\nClass starts: {class_start}")
print(f"Class ends:   {class_end}")
print(f"Precise time: {precise_time}")
print(f"  Hour:        {precise_time.hour}")
print(f"  Minute:      {precise_time.minute}")
print(f"  Second:      {precise_time.second}")
print(f"  Microsecond: {precise_time.microsecond}")


# datetime.datetime — combines date and time
now = datetime.datetime.now()
print(f"\nCurrent date & time: {now}")
print(f"  Date part: {now.date()}")
print(f"  Time part: {now.time()}")

# Creating a specific datetime
exam_datetime = datetime.datetime(2026, 5, 20, 10, 0, 0)
print(f"  Exam scheduled: {exam_datetime}")


# Replacing parts of a datetime
moved_exam = exam_datetime.replace(day=25, hour=14)
print(f"  Exam moved to:  {moved_exam}")


# Weekday info (0=Monday, 6=Sunday)
print(f"\n--- Weekday info ---")
print(f"  Today is weekday #{today.weekday()} ({today.strftime('%A')})")
print(f"  ISO weekday: {today.isoweekday()}")  # 1=Monday, 7=Sunday


# Practical application: event scheduler
events = [
    datetime.datetime(2026, 3, 1, 9, 0),
    datetime.datetime(2026, 3, 5, 14, 30),
    datetime.datetime(2026, 3, 10, 11, 0),
    datetime.datetime(2026, 3, 15, 16, 45),
]

print(f"\n--- Upcoming events ---")
for event in events:
    day_name = event.strftime("%A")
    formatted = event.strftime("%B %d at %H:%M")
    print(f"  {day_name}, {formatted}")
