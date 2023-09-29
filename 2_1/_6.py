def task_6_1(N: int) -> str:
    even_count: int = N // 2
    odd_count: int = N - even_count
    return f"сумма: {sum(range(1, N + 1))}, кол-во чётных: {even_count}, кол-во нечётных: {odd_count}"
