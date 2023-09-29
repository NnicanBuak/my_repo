from typing import Any, Callable, Union, Optional, NoReturn
import inspect
import os
import platform

from modules import terminal
from tasks import *

class Task:
    def __init__(self, function: Callable, input_ranges: dict[str, tuple[Optional[int], Optional[int]]], id: int, name: str, description: str, comment: str) -> None:
        self.function: Callable = function
        self.input_ranges: dict[str, tuple[Optional[int], Optional[int]]] = input_ranges
        self.subtasks: list[SubTask] = []
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.comment: str = comment

class SubTask:
    def __init__(self, function: Callable, input_ranges: dict[str, tuple[Optional[int], Optional[int]]], parent_id: int, id: int, name: str, description: str, comment: str) -> None:
        self.function: Callable = function
        self.input_ranges: dict[str, tuple[Optional[int], Optional[int]]] = input_ranges
        self.parent_id: int = parent_id
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.comment: str = comment

class TaskManager:
    def __init__(self, category: str) -> None:
        self.__last_used_id: int = 0
        self.tasks: list[Task] = []
        self.category: str = category

    def add_task(self, function: Callable, input_ranges: dict[str, tuple[Optional[int], Optional[int]]], name: str, description: str, comment: str = '') -> None:
        self.__last_used_id += 1
        task = Task(function, input_ranges, self.__last_used_id, name, description, comment)
        self.tasks.append(task)

    def add_subtask(self, function: Callable, input_ranges: dict[str, tuple[Optional[int], Optional[int]]], parent_id: int, name: str, description: str, comment: str = '') -> None:
        parent_task: Task = self.tasks[parent_id - 1]
        subtask_id: int = len(parent_task.subtasks) + 2
        subtask = SubTask(function, input_ranges, parent_id, subtask_id, name, description, comment)
        parent_task.subtasks.append(subtask)

class TerminalUI:
    def __init__(self, managers: list[TaskManager]) -> None:
        self.managers: list[TaskManager] = managers
        self.message = 'Ctrl+C/Del для возврата'
        self.current_menu: str = 'main'
        self.previous_menu: Optional[str] = None
        self.current_task: Optional[Task] = None
        self.current_subtask: Optional[SubTask] = None

    def back(self) -> None:
        if not self.previous_menu:
            terminal.clear()
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

    def main_menu(self) -> Optional[TaskManager]:
        self.previous_menu = None
        self.current_menu = 'main'
        self.set_message('Ctrl+C/Del для закрытия приложения')
        categories: list[str] = [manager.category for manager in self.managers]
        while True:
            terminal.clear()
            self.display_message()
            print(f"Доступные категории задач:")
            print('\033[33m—————————————————\033[0m')
            for i, category in enumerate(categories, start=1):
                print(f"\033[34;4m{i}\033[0m: {category}")
            print('\033[33m—————————————————\033[0m')
            try:
                category_number: int = int(input('\n\033[47m\033[30mВведите номер категории:\033[0m '))
            except ValueError:
                self.set_message('Ошибка: Введённое значение не номер')
                continue
            except KeyboardInterrupt:
                self.back()
                return

            if 0 < category_number <= len(self.managers):
                selected_manager: TaskManager = self.managers[category_number - 1]
                self.current_menu = 'tasks'
                return selected_manager
            else:
                self.set_message('Ошибка: Введённого номера нет в списке')
    def input_task_menu(self, category: TaskManager) -> Optional[Task]:
        self.previous_menu = 'main'
        self.set_message('Ctrl+C/Del для возвращения в предыдущее меню')
        while True:
            terminal.clear()
            self.display_message()
            print('Доступные задачи:')
            print('\033[33m—————————————————\033[0m')
            for i, task in enumerate(category.tasks, start=1):
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

            if 0 < task_number <= len(category.tasks):
                selected_task: Task = category.tasks[task_number - 1]
                if selected_task.subtasks:
                    self.current_task = selected_task
                    self.current_menu = 'subtasks'
                    return
                else:
                    return selected_task
            else:
                self.set_message('Ошибка: Введённого номера нет в списке')

    def input_subtask_menu(self, parent_task: Task) -> Optional[Union[Task, SubTask]]:
        tasks: list[SubTask] = parent_task.subtasks
        self.previous_menu = 'tasks'
        self.set_message('Ctrl+C/Del для возвращения в предыдущее меню')
        while True:
            terminal.clear()
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
                selected_task: Union[Task, SubTask] = tasks[task_number - 2]
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
        terminal.clear()

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
                            arg_value = input(f"\033[47m\033[30mВведите значение аргумента '{arg}' в диапазоне {task.input_ranges[arg] if task.input_ranges and task.input_ranges.get(arg, False) else ''} ({arg_type.__name__ if arg_type and arg_type.__name__ != 'list' and arg_type.__name__ != 'tuple' and arg_type.__name__ != 'dict' else arg_type if arg_type else 'тип не указан'}):\033[0m ") # type: ignore
                            if arg_type:
                                arg_value = arg_type(arg_value)

                        if task.input_ranges and task.input_ranges.get(arg, (None, None)):
                            min_limit, max_limit = task.input_ranges.get(arg, (None, None))
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

def main() -> NoReturn:
    category1 = TaskManager('Задаче на базе 1 курса университета')
    category2 = TaskManager('Задачи по курсу "ООП"')
    category3 = TaskManager('Задачи по курсу "Вычислительные системы и компьютерные сети"')
    ui = TerminalUI([category1, category2, category3])

    # Добавление задач в менеджер
    category1.add_task(task_1_1, {}, 'Обмен значениями переменных', 'Составьте программу обмена значениями трех переменных a, b, и c, так чтобы b получила значение c, c получила значение a, а a получила значение b.')
    category1.add_task(task_2_1, {}, 'Проверка ввода двух чисел и их сумма', 'Пользователь вводит два числа. Проверьте, что введенные данные - это числа. Если нет, выведите ошибку. Если да, то выведите их сумму.')
    category1.add_subtask(task_2_2, {}, 2, 'Проверка ввода n чисел и их сумма', 'Доработайте задачу 2.1 так, чтобы пользователь мог вводить n разных чисел, а затем выведите их сумму. Предоставьте возможность пользователю ввести значение n.')
    category1.add_task(task_3_1, {'x': (0, 100)},'Возведение в 5 степень', 'Дано число x в диапазоне от 0 до 100. Вычислите x в 5-ой степени.', 'x вычесляется с помощью функции `x**5`')
    category1.add_subtask(task_3_2, {'x': (0, 100)}, 3, 'Возведение в 5 степень с помощью умножения', 'Измените задачу 3.1 так, чтобы для вычисления степени использовалось только умножение.', 'Невозможно создать более оптимизированный метод возведения в степени сложности O(1) по времени и памяти чем `x**5` как в задаче 3.1, потому что операция слишком проста, но первый способ яляется предпочтительным из-за лучшей семантики.')
    category1.add_task(task_4_1, {'number': (0, 250)},'Проверка числа на соответствие Числу Фибоначчи', 'Пользователь может вводить число от 0 до 250. Проверьте, принадлежит ли введенное число числам Фибоначчи.')
    category1.add_task(task_5_1, {},'Получение времени года по месяцу (1 способ)', 'Реализуйте программу двумя способами на определение времени года в зависимости от введенного месяца года.')
    category1.add_subtask(task_5_2, {}, 5, 'Получение времени года по месяцу (2 способ)', 'Реализуйте программу двумя способами на определение времени года в зависимости от введенного месяца года.')
    category1.add_task(task_6_1, {'N': (2, None)},'Получение суммы, кол-ва чётных и нечётных чисел из диапазона', 'Реализуйте программу двумя способами на определение времени года в зависимости от введенного месяца года.')
    category1.add_task(task_7_1, {'N': (2, 250)},'Получение количества делителей для чисел из диапазона', 'Для каждого из чисел от 1 до N, где N меньше 250 выведите количество делителей. N вводит пользователь. Выведите число и через пробел количество его делителей. Делителем может быть 1.')
    category1.add_task(task_8_1, {}, 'Пифагоровы тройки', 'Найти все различные пифагоровы тройки из интервала от N до М.')
    category1.add_task(task_9_1, {'N': (1, None)}, 'Числа, делящиеся на свои цифры', 'Найти все целые числа из интервала от N до M, которые делятся на каждую из своих цифр.')
    category1.add_task(task_10_1, {'N': (None, 4)}, 'Совершенные числа', 'Натуральное число называется совершенным, если оно равно сумме всех своих делителей, включая единицу. Вывести первые N (N<5) совершенных чисел на экран.')
    category1.add_task(task_11_1, {}, 'Последний элемент массива', 'Задайте одномерный массив в коде и выведите в консоль последний элемент данного массива тремя способами.', 'первый способ - array[-1], второй способ - array[len(array)-1], третий способ - next(reversed(array))')
    category1.add_task(task_12_1, {}, 'Массив в обратном порядке', 'Задайте одномерный массив в коде и выведите в консоль массив в обратном порядке.', 'Зачем в коде если уже реализован интерфейс')
    category1.add_task(task_13_1, {}, 'Сумма элементов массива через рекурсию', 'Реализуйте нахождение суммы элементов массива через рекурсию. Массив можно задать в коде.', 'Зачем в коде если уже реализован интерфейс')
    category1.add_task(task_14_1, {}, 'Запуск оконного приложения конвертера рублей в доллары', 'Реализуйте оконное приложение-конвертер рублей в доллары. Создайте окно ввода для суммы в рублях.')
    category1.add_subtask(task_14_2, {}, 14, 'Запуск оконного приложения конвертера рублей в доллары и наооборот', 'Реализуйте оконное приложение-конвертер рублей в доллары. Создайте окно ввода для суммы в рублях.')
    category1.add_task(task_15_1, {'N': (5, 20), 'M': (5, 20)}, 'Таблица умножения', 'Реализуйте вывод таблицы умножения в консоль размером N на M которые вводит пользователь, но при этом они не могут быть больше 20 и меньше 5.')
    category1.add_task(task_16_1, {}, 'Морской бой', 'Реализуйте вывод в консоль поле для морского боя с выставленными кораблями. Данные о кораблях, можно подгружать из файла или генерировать самостоятельно.')

    category2.add_task(tamagochi, {}, 'Аксомагочи', 'Зверушка должна иметь две шкалы (сытость и радость) и два метода (накормить и поиграть). С течением времени (длина такт от 1 до 10 секунд на ваш выбор) зверушка становится грустнее и голоднее. При опустошении одной из шкал игра заканчивается. Действие поиграть отнимает очки из шкалы сытости. Красивое оформление позволяет получить до 1.5 баллов дополнительно, но не является обязательным, достаточно текстового интерфейса. Программа должна быть дружелюбной и понятной.', '>~<')

    # Основной цикл
    manager_of_category = None
    task = None
    while True:
        ui.clear_console()
        if ui.current_menu == 'main':
            manager_of_category: Optional[TaskManager] = ui.main_menu()
        if manager_of_category and ui.current_menu == 'tasks':
            task: Optional[Union[Task, SubTask]] = ui.input_task_menu(manager_of_category)
        if ui.current_menu == 'subtasks' and ui.current_task:
            task = ui.input_subtask_menu(ui.current_task)
        elif not task:
            task = ui.current_task or ui.current_subtask

        if task:
            ui.task_menu(task)

if __name__ == '__main__':
    main()