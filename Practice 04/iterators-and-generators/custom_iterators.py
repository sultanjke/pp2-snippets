# =============================================================
# Custom Iterators: __iter__() and __next__()
# =============================================================

# To make your own iterator, define a class with two methods:
#   __iter__() — returns the iterator object (usually self)
#   __next__() — returns the next value, raises StopIteration when done


class Countdown:
    """Counts down from a starting number to 1."""

    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


print("--- Countdown iterator ---")
for number in Countdown(5):
    print(f"  {number}")


class EvenNumbers:
    """Produces even numbers up to a given limit."""

    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 2
        if self.current > self.limit:
            raise StopIteration
        return self.current


print("\n--- Even numbers up to 12 ---")
for even in EvenNumbers(12):
    print(f"  {even}", end="")
print()


class FibonacciSequence:
    """Produces Fibonacci numbers up to max_count terms."""

    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.previous = 0
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        self.count += 1
        value = self.previous
        self.previous, self.current = self.current, self.previous + self.current
        return value


print("\n--- First 10 Fibonacci numbers ---")
for fib_number in FibonacciSequence(10):
    print(f"  {fib_number}", end="")
print()


# Practical application: paginated data reader
class PaginatedResults:
    """Simulates reading data page by page from a database."""

    def __init__(self, total_items, page_size):
        self.all_items = [f"record_{i+1}" for i in range(total_items)]
        self.page_size = page_size
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.all_items):
            raise StopIteration

        start = self.current_index
        end = min(start + self.page_size, len(self.all_items))
        page = self.all_items[start:end]
        self.current_index = end
        return page


print("\n--- Paginated data (15 records, 4 per page) ---")
page_number = 1
for page in PaginatedResults(total_items=15, page_size=4):
    print(f"  Page {page_number}: {page}")
    page_number += 1
