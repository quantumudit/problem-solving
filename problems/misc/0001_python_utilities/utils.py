def minutes_to_seconds(minutes: int) -> int:
    if not isinstance(minutes, int) or minutes < 0:
        raise ValueError("Minutes must be a non-negative integer")
    return minutes * 60


def sum_two_numbers(num1: int | float, num2: int | float) -> int | float:
    if not isinstance(num1, int | float) or not isinstance(num2, int | float):
        raise ValueError("Both inputs must be integers or floats")
    return num1 + num2


def fizzbuzz(n: int) -> list[str]:
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Input must be a positive integer")

    output = []
    for num in range(1, n + 1):
        if num % 3 == 0 and num % 5 == 0:
            output.append("FizzBuzz")
        elif num % 3 == 0:
            output.append("Fizz")
        elif num % 5 == 0:
            output.append("Buzz")
        else:
            output.append(str(num))

    return output


def sign_and_parity(num: int) -> tuple[str, str]:
    if not isinstance(num, int):
        raise ValueError("Input must be an integer")
    sign = "Positive" if num > 0 else "Negative" if num < 0 else "Zero"
    parity = "Even" if num % 2 == 0 else "Odd"
    return (sign, parity)
