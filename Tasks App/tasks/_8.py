def task_8_1(N: int, M: int) -> list[tuple[int, int, int]]:
    pythagorean_triples: list[tuple[int, int, int]] = []
    for a in range(N, M+1):
        for b in range(a, M+1):
            c = (a**2 + b**2)**0.5
            if c.is_integer() and c <= M:
                pythagorean_triples.append((a, b, int(c)))
    return pythagorean_triples