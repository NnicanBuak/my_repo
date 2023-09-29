import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules import measure
from modules import superformat

def task_3_1(x: int) -> str:
    def power_of_five(x: int) -> int:
        return x**5
    result, time, memory = measure.measure(power_of_five, x)
    return f"x^5: {result}, время: {superformat.float(time, 5) if time != None else time} секунд, память: {superformat.float(memory, 5) if memory != None else memory} байт"

def task_3_2(x: int) -> str:
    def power_of_five(x: int) -> int:
        return x*x*x*x*x
    result, time, memory = measure.measure(power_of_five, x)
    return f"x^5: {result}, время: {superformat.float(time, 5) if time != None else time} секунд, память: {superformat.float(memory, 5) if memory != None else memory} байт"
