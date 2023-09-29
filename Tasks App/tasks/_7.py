def task_7_1(N: int) -> dict[int, int]:
    result: dict[int, int] = {}
    for number in range(1, N + 1):
        result[number] = len([i for i in range(1, number + 1) if number % i == 0])
    return result