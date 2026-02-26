# =============================================================
# Calculating Time Differences with timedelta
# =============================================================

import datetime


now = datetime.datetime.now()

# timedelta represents a duration between two points in time
one_week = datetime.timedelta(weeks=1)
three_days = datetime.timedelta(days=3)
two_hours = datetime.timedelta(hours=2, minutes=30)

print("--- Adding and subtracting time ---")
print(f"  Now:            {now.strftime('%Y-%m-%d %H:%M')}")
print(f"  + 1 week:       {(now + one_week).strftime('%Y-%m-%d %H:%M')}")
print(f"  - 3 days:       {(now - three_days).strftime('%Y-%m-%d %H:%M')}")
print(f"  + 2h 30m:       {(now + two_hours).strftime('%Y-%m-%d %H:%M')}")


# Subtracting two dates gives a timedelta
semester_start = datetime.date(2026, 1, 12)
semester_end = datetime.date(2026, 5, 22)
semester_length = semester_end - semester_start

print(f"\n--- Semester duration ---")
print(f"  Start:    {semester_start}")
print(f"  End:      {semester_end}")
print(f"  Duration: {semester_length.days} days")
print(f"  Weeks:    {semester_length.days // 7} weeks and {semester_length.days % 7} days")


# Countdown to a future event
today = datetime.date.today()
new_year = datetime.date(today.year + 1, 1, 1)
days_until_new_year = (new_year - today).days

print(f"\n--- Countdown ---")
print(f"  Today: {today}")
print(f"  Days until New Year {new_year.year}: {days_until_new_year}")


# Comparing dates
deadline = datetime.datetime(2026, 4, 15, 23, 59, 59)
is_past_deadline = now > deadline

print(f"\n--- Deadline check ---")
print(f"  Deadline:     {deadline.strftime('%B %d, %Y %H:%M')}")
print(f"  Past due?     {is_past_deadline}")


# timedelta arithmetic
shift_duration = datetime.timedelta(hours=8)
break_time = datetime.timedelta(minutes=45)
actual_work = shift_duration - break_time

print(f"\n--- Work shift ---")
print(f"  Shift:       {shift_duration}")
print(f"  Break:       {break_time}")
print(f"  Actual work: {actual_work}")


# Practical application: project milestone tracker
project_start = datetime.date(2026, 2, 1)

milestones = [
    ("Requirements", datetime.timedelta(weeks=2)),
    ("Design",       datetime.timedelta(weeks=3)),
    ("Development",  datetime.timedelta(weeks=8)),
    ("Testing",      datetime.timedelta(weeks=3)),
    ("Deployment",   datetime.timedelta(weeks=1)),
]

print(f"\n--- Project timeline (start: {project_start}) ---")
current_date = project_start

for milestone_name, duration in milestones:
    end_date = current_date + duration
    print(f"  {milestone_name:<15} {current_date} -> {end_date} ({duration.days} days)")
    current_date = end_date

print(f"  {'Total':<15} {project_start} -> {current_date} ({(current_date - project_start).days} days)")
