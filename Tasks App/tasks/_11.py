from modules import measure
from modules import superformat

def task_11_1(array: list[int]) -> str:
    def last_element_1() -> int:
        return array[-1]
    def last_element_2() -> int:
        return array[len(array)-1]
    def last_element_3() -> int:
        return next(reversed(array))
    result1, time1, memory1 = measure.measure(last_element_1)
    result2, time2, memory2 = measure.measure(last_element_2)
    result3, time3, memory3 = measure.measure(last_element_3)
    return f"последний элемент: {result1 or result2 or result3}, время способа 1: {superformat.float(time1, 5) if time1 else time1}, время способа 2: {superformat.float(time2, 5) if time2 else time2}, время способа 3: {superformat.float(time3, 5) if time3 else time3}"