def task_9_1(N: int, M: int) -> list[int]:
    numbers: list[int] = []
    for number in range(N, M+1):
        digits: list[int] = [int(digit) for digit in str(number) if int(digit) != 0]
        if all(number % digit == 0 for digit in digits):
            numbers.append(number)
    return numbers