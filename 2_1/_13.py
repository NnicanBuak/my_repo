def task_13_1(array: list[int]) -> int:
    if len(array) == 0:
        return 0
    else:
        return array[0] + task_13_1(array[1:])