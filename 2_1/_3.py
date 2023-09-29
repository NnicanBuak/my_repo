from format_float import format_float
from measure_memory_and_time import measure_memory_time
def task_3_1(x: int) -> str:
    def power_of_five(x: int) -> int:
        return x**5
    result, time, memory = measure_memory_time(power_of_five, x)
    return f"x^5: {result}, время: {format_float(time, 5) if time != None else time} секунд, память: {format_float(memory, 5) if memory != None else memory} байт"

def task_3_2(x: int) -> str:
    def power_of_five(x: int) -> int:
        return x*x*x*x*x
    result, time, memory = measure_memory_time(power_of_five, x)
    return f"x^5: {result}, время: {format_float(time, 5) if time != None else time} секунд, память: {format_float(memory, 5) if memory != None else memory} байт"
