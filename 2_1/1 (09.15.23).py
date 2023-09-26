from typing import Any, Callable, Union, Optional, NoReturn
import inspect
import os
import platform
import time
import random
try:
    import psutil
except ImportError:
    psutil = None

class Task:
    def __init__(self, function: Callable, input_ranges: dict[str, tuple[int | None, int | None]], id: int, name: str, description: str, comment: str) -> None:
        self.function: Callable = function
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.comment: str = comment
        self.subtasks: list[SubTask] = []
        self.input_ranges: dict[str, tuple[int | None, int | None]] = input_ranges

class SubTask:
    def __init__(self, function: Callable, input_ranges: dict[str, tuple[int | None, int | None]], parent_id: int, id: int, name: str, description: str, comment: str) -> None:
        self.parent_id: int = parent_id
        self.function: Callable = function
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.comment: str = comment
        self.input_ranges: dict[str, tuple[int | None, int | None]] = input_ranges

class TaskManager:
    def __init__(self, ui) -> None:
        self.tasks: list[Task] = []
        self.ui: TerminalUI = ui
        self.last_used_id: int = 0

    def add_task(self, function: Callable, input_ranges: dict[str, tuple[int | None, int | None]], name: str, description: str, comment: str = '') -> None:
        self.last_used_id += 1
        task = Task(function, input_ranges, self.last_used_id, name, description, comment)
        self.tasks.append(task)

    def add_subtask(self, function: Callable, input_ranges: dict[str, tuple[int | None, int | None]], parent_id: int, name: str, description: str, comment: str = '') -> None:
        parent_task: Task = self.tasks[parent_id - 1]
        subtask_id: int = len(parent_task.subtasks) + 2
        subtask = SubTask(function, input_ranges, parent_id, subtask_id, name, description, comment)
        parent_task.subtasks.append(subtask)

class TerminalUI:
    def __init__(self) -> None:
        self.message = 'Ctrl+C/Del для возврата'
        self.current_menu: str = 'tasks'
        self.previous_menu: str | None = None
        self.current_task: Optional[Task] = None
        self.current_subtask: Optional[SubTask] = None

    def back(self) -> None:
        if not self.previous_menu:
            self.clear_console()
            print('Приложение закрыто по запросу пользователя.')
            exit()
        if self.previous_menu and self.previous_menu != self.current_menu:
            self.current_menu = self.previous_menu

    def set_message(self, message: str) -> None:
        self.message: str = message

    def display_message(self, message = None) -> None:
        if message:
            print('\033[40m|' + message + '|\033[0m' + '\n')
            return
        print('\033[40m|' + self.message + '|\033[0m' + '\n')

    def clear_console(self) -> None:
        system: str = platform.system()
        if system == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def input_task_menu(self, tasks: list[Task]) -> Optional[Task]:
        self.previous_menu = None
        self.current_menu = 'tasks'
        self.set_message('Ctrl+C/Del для закрытия приложения')
        while True:
            self.clear_console()
            self.display_message()
            print('Доступные задачи:')
            print('\033[33m—————————————————\033[0m')
            for i, task in enumerate(tasks, start=1):
                print(f"\033[34;4m{i}\033[0m: {task.name}")
            print('\033[33m—————————————————\033[0m')
            try:
                task_number: int = int(input('\n\033[47m\033[30mВведите номер задачи:\033[0m '))
            except ValueError:
                self.set_message('Ошибка: Введённое значение не номер')
                continue
            except KeyboardInterrupt:
                self.back()
                return

            if 0 < task_number <= len(tasks):
                selected_task: Task = tasks[task_number - 1]
                if selected_task.subtasks:
                    self.current_task = selected_task
                    self.current_menu = 'tasks'
                    self.current_menu = 'subtasks'
                    return
                else:
                    return selected_task
            else:
                self.set_message('Ошибка: Введённого номера нет в списке')

    def input_subtask_menu(self, parent_task: Task) -> Optional[Task | SubTask]:
        tasks: list[SubTask] = parent_task.subtasks
        self.previous_menu = 'tasks'
        self.current_menu = 'subtasks'
        self.set_message('Ctrl+C/Del для возвращения в предыдущее меню')
        while True:
            self.clear_console()
            self.display_message()
            print(f"Задача {parent_task.id}:")
            print('\033[33m—————————————————\033[0m')
            print(f"{parent_task.id}.\033[34;4m1\033[0m: {parent_task.name}")
            print('\033[33m—————————————————\033[0m')
            print(f"Подзадачи:")
            print('\033[33m—————————————————\033[0m')
            for i, task in enumerate(tasks, start=2):
                print(f"{parent_task.id}.\033[34;4m{i}\033[0m: {task.name}")
            print('\033[33m—————————————————\033[0m')
            try:
                task_number: int = int(input('\n\033[47m\033[30mВведите номер задачи:\033[0m '))
            except ValueError:
                self.set_message('Ошибка: Введёное значение не номер')
                continue
            except KeyboardInterrupt:
                self.back()
                return

            if 1 < task_number <= len(tasks) + 1:
                selected_task: Task | SubTask = tasks[task_number - 2]
                if len(tasks) > 1:
                    self.current_menu = 'subtasks'
                    self.current_subtask = selected_task
                    return selected_task
                else:
                    self.current_subtask = selected_task
                    return selected_task
            elif task_number == 1:
                selected_task = parent_task
                return selected_task
            else:
                self.set_message('Ошибка: Введённого номера нет в списке')

    def task_menu(self, task: Union[Task, SubTask]) -> None:
        self.previous_menu = self.current_menu
        self.current_menu = 'task'
        self.clear_console()

        argspec = inspect.getfullargspec(task.function)
        input_args: dict = {}
        if argspec.args or argspec.varargs:
            self.message = 'Введите значения для аргументов или вернитесь в предыдущее меню с помощью Ctrl+C/Del'
            self.display_message()
            if isinstance(task, Task):
                if task.subtasks:
                    print(f"Задача {task.id}.1: {task.name}")
                else:
                    print(f"Задача {task.id}: {task.name}")
            elif isinstance(task, SubTask):
                print(f"Задача {task.parent_id}.{task.id}: {task.name}")
        else:
            if isinstance(task, Task):
                if task.subtasks:
                    print(f"Задача {task.id}.1: {task.name}")
                else:
                    print(f"Задача {task.id}: {task.name}")
            elif isinstance(task, SubTask):
                print(f"Задача {task.parent_id}.{task.id}: {task.name}")
        print(f"Описание: {task.description}")
        print(f"Комментарий: {task.comment}", '\n')

        if argspec.varargs:
            arg: str = argspec.varargs
            arg_type: Optional[type] = None
            if arg in argspec.annotations:
                arg_type = argspec.annotations[arg]
            while True:
                try:
                    arg_count = int(input(f"\033[47m\033[30mВведите количество аргументов {argspec.varargs} ({arg_type.__name__ if arg_type and arg_type.__name__ != 'list' and arg_type.__name__ != 'tuple'  and arg_type.__name__ != 'dict' else arg_type if arg_type else 'тип не указан'}) которое вы желаете передать задаче:\033[0m "))
                    if arg_count >= 0:
                        break
                    else:
                        self.display_message('Ошибка: Введите не отрицательное число')
                except ValueError:
                    self.display_message('Ошибка: Введите натуральное число')
                except KeyboardInterrupt:
                    self.back()
                    return

            var_args: tuple = tuple()
            for i in range(arg_count):
                while True:
                    try:
                        arg_value: Any = input(f"\033[47m\033[30mВведите значение аргумента {argspec.varargs} {i + 1} ({arg_type.__name__ if arg_type and arg_type.__name__ != 'list' and arg_type.__name__ != 'tuple'  and arg_type.__name__ != 'dict' else arg_type if arg_type else 'тип не указан'}){f' в диапазоне {task.input_ranges.get(arg, None)}' if task.input_ranges and task.input_ranges[arg] else ''}:\033[0m ")
                        if arg_type:
                            arg_value = arg_type(arg_value)
                        if task.input_ranges and task.input_ranges[arg]:
                            min_limit, max_limit = task.input_ranges[arg]
                            if isinstance(arg_value, str):
                                if min_limit and max_limit and not min_limit <= len(arg_value) <= max_limit:
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                                elif min_limit and not min_limit <= len(arg_value):
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                                elif max_limit and not len(arg_value) <= max_limit:
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                            elif isinstance(arg_value, (int, float)):
                                if min_limit and max_limit and not min_limit <= arg_value <= max_limit:
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                                elif min_limit and not min_limit <= arg_value:
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                                elif max_limit and not arg_value <= max_limit:
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                        var_args += (arg_value,)
                        break
                    except ValueError:
                        self.display_message(f"Ошибка: Не удалось преобразовать введенное значение в тип {arg_type.__name__ if arg_type and arg_type.__name__ != 'list' and arg_type.__name__ != 'tuple'  and arg_type.__name__ != 'dict' else arg_type if arg_type else 'тип не указан'}. Попробуйте ещё раз")
                    except KeyboardInterrupt:
                        self.back()
                        return
                input_args[arg] = var_args

        if argspec.args:
            for arg in argspec.args:
                arg_type = None
                if arg in argspec.annotations:
                    arg_type: Optional[type] = argspec.annotations[arg]
                while True:
                    try:
                        if arg_type and (arg_type.__name__ == 'list' or arg_type.__name__ == 'dict' or arg_type.__name__ == 'tuple'):
                            arg_value = arg_type()
                            while True:
                                try:
                                    arg_count = int(input(f"\033[47m\033[30mВведите количество аргументов {arg} ({arg_type.__name__ if arg_type and arg_type.__name__ != 'list' and arg_type.__name__ != 'tuple'  and arg_type.__name__ != 'dict' else arg_type if arg_type else 'тип не указан'}) которое вы желаете передать задаче:\033[0m "))
                                    if arg_count >= 0:
                                        break
                                    else:
                                        self.display_message('Ошибка: Введите не отрицательное число')
                                except ValueError:
                                    self.display_message('Ошибка: Введите натуральное число')
                                except KeyboardInterrupt:
                                    self.back()
                                    return
                            for i in range(arg_count):
                                while True:
                                    val = None
                                    try:
                                        val: Any = input(f"\033[47m\033[30mВведите значение аргумента {arg} {i + 1} ({arg_type.__args__[0].__name__ if arg_type.__args__ else 'тип не указан'}):\033[0m ") # type: ignore
                                        if arg_type.__args__[0]: # type: ignore
                                            val = arg_type.__args__[0](val) # type: ignore
                                    except ValueError:
                                        self.display_message(f"Ошибка: Не удалось преобразовать введенное значение в тип {arg_type.__args__[0].__name__}") # type: ignore
                                        continue
                                    except KeyboardInterrupt:
                                        self.back()
                                        return
                                    arg_value.append(val)
                                    break
                        else:
                            arg_value = input(f"\033[47m\033[30mВведите значение аргумента '{arg}' {f'в диапазоне {task.input_ranges.get(arg, None)}' if task.input_ranges and task.input_ranges[arg] else ''}({arg_type.__name__ if arg_type and arg_type.__name__ != 'list' and arg_type.__name__ != 'tuple' and arg_type.__name__ != 'dict' else arg_type if arg_type else 'тип не указан'}):\033[0m ")
                            if arg_type:
                                arg_value = arg_type(arg_value)

                        if task.input_ranges and task.input_ranges[arg]:
                            min_limit, max_limit = task.input_ranges[arg]
                            if isinstance(arg_value, (str, list, dict, tuple, set)):
                                if min_limit and max_limit and not min_limit <= len(arg_value) <= max_limit:
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                                elif min_limit and not min_limit <= len(arg_value):
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                                elif max_limit and not len(arg_value) <= max_limit:
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                            elif isinstance(arg_value, (int, float)):
                                if min_limit and max_limit and not min_limit <= arg_value <= max_limit:
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                                elif min_limit and not min_limit <= arg_value:
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue
                                elif max_limit and not arg_value <= max_limit:
                                    self.display_message(f"Ошибка: Значение не входит в заданный диапазон {task.input_ranges.get(arg, None)}. Попробуйте ещё раз")
                                    continue

                        input_args[arg] = arg_value
                        break
                    except ValueError:
                        self.display_message(f"Ошибка: Не удалось преобразовать введенное значение в тип {arg_type.__name__ if arg_type and arg_type.__name__ != 'list' and arg_type.__name__ != 'tuple'  and arg_type.__name__ != 'dict' else arg_type if arg_type else 'тип не указан'}. Попробуйте ещё раз")
                    except KeyboardInterrupt:
                        self.back()
                        return

        result = None
        try:
            if argspec.varargs and argspec.varargs in input_args:
                result = task.function(*input_args[argspec.varargs])
            else:
                result = task.function(**input_args)
        except Exception as e:
            self.display_message(f"Ошибка выполнения задачи {task.id}: {e}")
            try:
                input("[Enter для закрытия задачи]")
            except KeyboardInterrupt:
                self.back()
                return
            return
        try:
            if argspec.annotations['return']:
                if isinstance(result, tuple):
                    print(f"\033[37;42mРезультат ({argspec.annotations['return']}):\033[0m")
                    for item in result:
                        print(item)
                if isinstance(result, list):
                    print(f"\033[37;42mРезультат ({argspec.annotations['return']}):\033[0m")
                    for item in result:
                        print(str(item).replace("[", "").replace("]", "").replace(",", "").replace("'", ""))
                elif isinstance(result, dict):
                    print(f"\033[37;42mРезультат ({argspec.annotations['return']}):\033[0m")
                    for key, item in result.items():
                        print(key, item)
                else:
                    print(f"\033[37;42mРезультат ({argspec.annotations['return'].__name__ if argspec.annotations['return'] else 'тип не указан'}):\033[0m {result}")
            else:
                print(f"\033[37;42mРезультат ('тип не указан'):\033[0m {result}")
            input("\n[Enter для закрытия задачи]")
        except KeyboardInterrupt:
            self.back()
            return

        self.current_subtask = None
        if self.previous_menu == 'tasks':
            self.current_menu = 'tasks'
            self.current_task = None
        elif self.previous_menu == 'subtasks':
            self.current_menu = 'subtasks'

def measure_memory_time(func, *args, **kwargs) -> tuple[Any, Optional[float], Optional[float]]:
    if not psutil:
        result: Any = func(*args, **kwargs)
        return result, None, None
    start_time: float = time.time()
    start_memory: Any = psutil.Process().memory_info().rss

    result = func(*args, **kwargs)

    end_time: float = time.time()
    end_memory: Any = psutil.Process().memory_info().rss

    elapsed_time: float = end_time - start_time
    memory_diff: Any = end_memory - start_memory

    return result, elapsed_time, memory_diff

def format_float(number: float, precision=2) -> str:
    number_parts: list[str] = str(number).split('.')
    if len(number_parts) == 2:
        return number_parts[0] + '.' + number_parts[1][:-(len(number_parts[1].lstrip('0'))-precision) if len(number_parts[1].lstrip('0'))-precision > 0 else 0] if number_parts[1].lstrip('0') else number_parts[0]
    else:
        return number_parts[0]

def main() -> NoReturn:
    ui = TerminalUI()
    manager = TaskManager(ui)

    # Добавление задач в менеджер
    manager.add_task(task_1_1, {}, 'Обмен значениями переменных', 'Составьте программу обмена значениями трех переменных a, b, и c, так чтобы b получила значение c, c получила значение a, а a получила значение b.')
    manager.add_task(task_2_1, {}, 'Проверка ввода двух чисел и их сумма', 'Пользователь вводит два числа. Проверьте, что введенные данные - это числа. Если нет, выведите ошибку. Если да, то выведите их сумму.')
    manager.add_subtask(task_2_2, {}, 2, 'Проверка ввода n чисел и их сумма', 'Доработайте задачу 2.1 так, чтобы пользователь мог вводить n разных чисел, а затем выведите их сумму. Предоставьте возможность пользователю ввести значение n.')
    manager.add_task(task_3_1, {'x': (0, 100)},'Возведение в 5 степень', 'Дано число x в диапазоне от 0 до 100. Вычислите x в 5-ой степени.', 'x вычесляется с помощью функции `x**5`')
    manager.add_subtask(task_3_2, {'x': (0, 100)}, 3, 'Возведение в 5 степень с помощью умножения', 'Измените задачу 3.1 так, чтобы для вычисления степени использовалось только умножение.', 'Невозможно создать более оптимизированный метод возведения в степени сложности O(1) по времени и памяти чем `x**5` как в задаче 3.1, потому что операция слишком проста, но первый способ яляется предпочтительным из-за лучшей семантики.')
    manager.add_task(task_4_1, {'number': (0, 250)},'Проверка числа на соответствие Числу Фибоначчи', 'Пользователь может вводить число от 0 до 250. Проверьте, принадлежит ли введенное число числам Фибоначчи.')
    manager.add_task(task_5_1, {},'Получение времени года по месяцу (1 способ)', 'Реализуйте программу двумя способами на определение времени года в зависимости от введенного месяца года.')
    manager.add_subtask(task_5_2, {}, 5, 'Получение времени года по месяцу (2 способ)', 'Реализуйте программу двумя способами на определение времени года в зависимости от введенного месяца года.')
    manager.add_task(task_6_1, {'N': (2, None)},'Получение уммы, кол-ва чётных и нечётных чисел из диапазона', 'Реализуйте программу двумя способами на определение времени года в зависимости от введенного месяца года.')
    manager.add_task(task_7_1, {'N': (2, 250)},'Получение количества делителей для чисел из диапазона', 'Для каждого из чисел от 1 до N, где N меньше 250 выведите количество делителей. N вводит пользователь. Выведите число и через пробел количество его делителей. Делителем может быть 1.')
    manager.add_task(task_8_1, {}, 'Пифагоровы тройки', 'Найти все различные пифагоровы тройки из интервала от N до М.')
    manager.add_task(task_9_1, {'N': (1, None)}, 'Числа, делящиеся на свои цифры', 'Найти все целые числа из интервала от N до M, которые делятся на каждую из своих цифр.')
    manager.add_task(task_10_1, {}, 'Совершенные числа', 'Натуральное число называется совершенным, если оно равно сумме всех своих делителей, включая единицу. Вывести первые N (N<5) совершенных чисел на экран.')
    manager.add_task(task_11_1, {}, 'Последний элемент массива', 'Задайте одномерный массив в коде и выведите в консоль последний элемент данного массива тремя способами.', 'первый способ - array[-1], второй способ - array[len(array)-1], третий способ - next(reversed(array))')
    manager.add_task(task_12_1, {}, 'Массив в обратном порядке', 'Задайте одномерный массив в коде и выведите в консоль массив в обратном порядке.', 'Зачем в коде если уже реализован интерфейс')
    manager.add_task(task_13_1, {}, 'Сумма элементов массива через рекурсию', 'Реализуйте нахождение суммы элементов массива через рекурсию. Массив можно задать в коде.', 'Зачем в коде если уже реализован интерфейс')
    manager.add_task(task_15_1, {'N': (5, 20), 'M': (5, 20)}, 'Таблица умножения', 'Реализуйте вывод таблицы умножения в консоль размером N на M которые вводит пользователь, но при этом они не могут быть больше 20 и меньше 5.')
    manager.add_task(task_16_1, {}, 'Морской бой', 'Реализуйте вывод в консоль поле для морского боя с выставленными кораблями. Данные о кораблях, можно подгружать из файла или генерировать самостоятельно.')

    # Основной цикл
    while True:
        ui.clear_console()
        if ui.current_menu == 'tasks':
            task: Optional[Union[Task, SubTask]] = ui.input_task_menu(manager.tasks)
        elif ui.current_menu == 'subtasks' and ui.current_task:
            task = ui.input_subtask_menu(ui.current_task)
        else:
            task = ui.current_task or ui.current_subtask

        if task:
            ui.task_menu(task)

# Функции задач
def task_1_1(a: int, b: int, c: int) -> str:
    a, b, c = b, c, a
    return f"a = {a}, b = {b}, c = {c}"

def task_2_1(number1, number2) -> str:
    try:
        summ: int = int(number1) + int(number2)
        return f"Все введёные значения — числа, их сумма: {summ}"
    except ValueError:
        return 'Одно или несколько введённых значений — не числа'

def task_2_2(*numbers) -> str:
    summ: int | float = 0
    for number in numbers:
        try:
            summ += int(number)
        except:
            try:
                summ += float(number)
            except:
                return 'Одно или несколько введённых значений — не числа'
    return f"Все введёные значения — числа, их сумма: {summ}"

def task_3_1(x: int) -> str:
    def power_of_five(x: int) -> int:
        return x**5
    result, time, memory_diff = measure_memory_time(power_of_five, x)
    return f"x^5: {result}, время: {format_float(time, 5) if time != None else time} секунд, память: {format_float(memory_diff, 5) if memory_diff != None else memory_diff} байт"

def task_3_2(x: int) -> str:
    def power_of_five(x: int) -> int:
        return x*x*x*x*x
    result, time, memory_diff = measure_memory_time(power_of_five, x)
    return f"x^5: {result}, время: {format_float(time, 5) if time != None else time} секунд, память: {format_float(memory_diff, 5) if memory_diff != None else memory_diff} байт"

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

def task_5_1(month: int) -> str:
    if month in [12, 1, 2]:
        return 'Зима'
    elif month in [3, 4, 5]:
        return 'Весна'
    elif month in [6, 7, 8]:
        return 'Лето'
    elif month in [9, 10, 11]:
        return 'Осень'
    else:
        return 'В 1 году — 12 месяцев. Время года не определенно'

def task_5_2(month: int) -> str:
    seasons: dict[int, str] = {1: 'Зима', 2: 'Зима', 3: 'Весна', 4: 'Весна', 5: 'Весна',
               6: 'Лето', 7: 'Лето', 8: 'Лето', 9: 'Осень', 10: 'Осень',
               11: 'Осень', 12: 'Зима'}
    return seasons.get(month, 'В 1 году — 12 месяцев. Время года не определенно')

def task_6_1(N: int) -> str:
    even_count: int = N // 2
    odd_count: int = N - even_count
    return f"сумма: {sum(range(1, N + 1))}, кол-во чётных: {even_count}, кол-во нечётных: {odd_count}"

def task_7_1(N: int) -> dict[int, int]:
    result: dict[int, int] = {}
    for number in range(1, N + 1):
        result[number] = len([i for i in range(1, number + 1) if number % i == 0])
    return result

def task_8_1(N: int, M: int) -> list[tuple[int, int, int]]:
    pythagorean_triples: list[tuple[int, int, int]] = []
    for a in range(N, M+1):
        for b in range(a, M+1):
            c = (a**2 + b**2)**0.5
            if c.is_integer() and c <= M:
                pythagorean_triples.append((a, b, int(c)))
    return pythagorean_triples

def task_9_1(N: int, M: int) -> list[int]:
    numbers: list[int] = []
    for number in range(N, M+1):
        digits: list[int] = [int(digit) for digit in str(number) if int(digit) != 0]
        if all(number % digit == 0 for digit in digits):
            numbers.append(number)
    return numbers

def task_10_1(N: int) -> list[int]:
    perfect_numbers: list[int] = []
    i = 1
    while len(perfect_numbers) < N:
        if sum(divisor for divisor in range(1, i//2 + 1) if i % divisor == 0) == i:
            perfect_numbers.append(i)
        i += 1
    return perfect_numbers

def task_11_1(array: list[int]) -> str:
    def last_element_1() -> int:
        return array[-1]
    def last_element_2() -> int:
        return array[len(array)-1]
    def last_element_3() -> int:
        return next(reversed(array))
    result1, time1, memory1 = measure_memory_time(last_element_1)
    result2, time2, memory2 = measure_memory_time(last_element_2)
    result3, time3, memory3 = measure_memory_time(last_element_3)
    return f"последний элемент: {result1 or result2 or result3}, время способа 1: {format_float(time1, 5) if time1 else time1}, время способа 2: {format_float(time2, 5) if time2 else time2}, время способа 3: {format_float(time3, 5) if time3 else time3}"

def task_12_1(array: list[int]) -> list[int]:
    return array[::-1]

def task_13_1(array: list[int]) -> int:
    if len(array) == 0:
        return 0
    else:
        return array[0] + task_13_1(array[1:])

# Задача 14.1 и Задача 14.2 требуют создания графического интерфейса пользователя и не могут быть реализованы в текстовом формате.

def task_15_1(N: int, M: int) -> list[str]:
    result: list[str] = []
    for i in range(1, N+1):
        for j in range(1, M+1):
            result.append(f"{i} * {j} = {i*j}")
    return result

def task_16_1() -> list[list[str]]:
    board: list[list[str]] = []
    for i in range(0, 10):
        board.append(["🟦"] * 10)

    def can_place_ship(board, ship_length, start_row, start_col, orientation) -> bool:
        if orientation == 'horizontal':
            if start_col + ship_length > len(board[0]):
                return False
            for i in range(max(0, start_col - 1), min(len(board[0]), start_col + ship_length + 2)):
                for j in range(max(0, start_row - 1), min(len(board), start_row + 2)):
                    if board[j][i] == '⬜':
                        return False
        else:
            if start_row + ship_length > len(board):
                return False
            for i in range(max(0, start_col - 1), min(len(board[0]), start_col + 2)):
                for j in range(max(0, start_row - 1), min(len(board), start_row + ship_length + 2)):
                    if board[j][i] == '⬜':
                        return False
        return True

    def place_ship(board, ship_length) -> None:
        while True:
            orientation: str = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                start_row: int = random.randint(0, len(board) - 1)
                start_col: int = random.randint(0, len(board[0]) - ship_length)
                if can_place_ship(board, ship_length, start_row, start_col, orientation):
                    for i in range(ship_length):
                        board[start_row][start_col + i] = '⬜'
                    break
            else:
                start_row = random.randint(0, len(board) - ship_length)
                start_col = random.randint(0, len(board[0]) - 1)
                if can_place_ship(board, ship_length, start_row, start_col, orientation):
                    for i in range(ship_length):
                        board[start_row + i][start_col] = '⬜'
                    break

    for ship_length in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
        place_ship(board, ship_length)
    return board

if __name__ == '__main__':
    main()
