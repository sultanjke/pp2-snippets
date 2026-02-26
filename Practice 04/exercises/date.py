from datetime import datetime, timedelta


# 1. Subtract five days from current date
today = datetime.now()
five_days_ago = today - timedelta(days=5)

print("1. Subtract five days from current date")
print(f"   Current date: {today.strftime('%Y-%m-%d')}")
print(f"   Five days ago: {five_days_ago.strftime('%Y-%m-%d')}")


# 2. Print yesterday, today, tomorrow
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("\n2. Yesterday, today, tomorrow")
print(f"   Yesterday: {yesterday.strftime('%Y-%m-%d')}")
print(f"   Today:     {today.strftime('%Y-%m-%d')}")
print(f"   Tomorrow:  {tomorrow.strftime('%Y-%m-%d')}")


# 3. Drop microseconds from datetime
now_with_micro = datetime.now()
now_without_micro = now_with_micro.replace(microsecond=0)

print("\n3. Drop microseconds from datetime")
print(f"   With microseconds:    {now_with_micro}")
print(f"   Without microseconds: {now_without_micro}")


# 4. Calculate two date difference in seconds
date_1 = datetime(2026, 1, 1, 0, 0, 0)
date_2 = datetime(2026, 3, 15, 10, 30, 0)
difference = date_2 - date_1

print("\n4. Difference between two dates in seconds")
print(f"   Date 1: {date_1}")
print(f"   Date 2: {date_2}")
print(f"   Difference: {difference.total_seconds():.0f} seconds")
