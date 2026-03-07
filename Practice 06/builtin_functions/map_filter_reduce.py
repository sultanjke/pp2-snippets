from functools import reduce


def main() -> None:
    numbers = [1, 2, 3, 4, 5, 6]

    squared = list(map(lambda n: n * n, numbers))
    evens = list(filter(lambda n: n % 2 == 0, numbers))
    total = reduce(lambda acc, n: acc + n, numbers, 0)

    print("numbers:", numbers)
    print("map (squared):", squared)
    print("filter (evens):", evens)
    print("reduce (sum):", total)

    # Common aggregation built-ins.
    print("len:", len(numbers))
    print("sum:", sum(numbers))
    print("min:", min(numbers))
    print("max:", max(numbers))
    print("sorted descending:", sorted(numbers, reverse=True))


if __name__ == "__main__":
    main()
