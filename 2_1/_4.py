def task_4_1(number: int) -> str:
    def get_fibonacci(n: int) -> int:
        if n == 0 or 1:
            return n
        else:
            return get_fibonacci(n-1) + get_fibonacci(n-2)
    for n in range(0, 13):
        if number == get_fibonacci(n):
            return f"{number} — Число Фибоначчи!"
    return f"{number} — не Число Фибоначчи"