def task_15_1(N: int, M: int) -> list[str]:
    result: list[str] = []
    for i in range(1, N+1):
        for j in range(1, M+1):
            result.append(f"{i} * {j} = {i*j}")
    return result