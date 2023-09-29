def task_10_1(N: int) -> list[int]:
    perfect_numbers: list[int] = []
    i = 1
    while len(perfect_numbers) < N:
        if sum(divisor for divisor in range(1, i//2 + 1) if i % divisor == 0) == i:
            perfect_numbers.append(i)
        i += 1
    return perfect_numbers