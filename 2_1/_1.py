def task_1_1(a: int, b: int, c: int) -> str:
    a, b, c = b, c, a
    return f"a = {a}, b = {b}, c = {c}"