from typing import Callable, Union
import inspect
import os
import platform

class Task:
    def __init__(self, function: Callable, id: int, name: str, description: str):
        self.function = function
        self.id = id
        self.name = name
        self.description = description
        self.subtasks = [self]

class SubTask():
    def __init__(self, function: Callable, parent_id: int, id: int, name: str, description: str):
        self.parent_id = parent_id
        self.function = function
        self.id = id
        self.name = name
        self.description = description

class ConsoleUI:
    def __init__(self):
        self.message = 'Ctrl+C/Del для завершения программы'

    def set_message(self, message):
        self.message = message

    def display_message(self):
        print('|' + self.message + '|' + '\n')

    def clear_console(self):
        system = platform.system()
        if system == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def display_tasks(self, tasks):
        print('Доступные задачи:')
        print('—————————————————')
        for i, task in enumerate(tasks, start=1):
            print(f"{i}: {task.name}")
        print('—————————————————')

    def display_subtasks(self, subtasks):
        parent_id = subtasks[0].parent_id
        print(f"Пункты задачи {parent_id}:")
        print('—————————————————')
        for i, task in enumerate(subtasks, start=1):
            print(f"{parent_id}.{i}: {task.name}")
        print('—————————————————')

class TaskManager:
    last_used_id = 0

    def __init__(self, ui):
        self.tasks = []
        self.ui = ui

    def get_task(self, id):
        if id < 0 or id >= len(self.tasks):
            return None
        return self.tasks[id]

    def add_task(self, function: Callable, name: str, description: str):
        self.last_used_id += 1
        task = Task(function, self.last_used_id, name, description)
        self.tasks.append(task)

    def add_subtask(self, function: Callable, parent_id: int, name: str, description: str):
        parent_task = self.get_task(parent_id - 1)
        if parent_task is not None:
            subtask_id = len(parent_task.subtasks) + 1
            subtask = SubTask(function, parent_id, subtask_id, name, description)
            parent_task.subtasks.append(subtask)
            self.last_used_id += 1
        else:
            print(f"|Ошибка: Родительская задача с ID {parent_id} не найдена|")

    def run_task(self, task: Task):
        self.ui.clear_console()
        print(f"Задача: {task.name}")
        print(f"Описание: {task.description}", '\n')

        argspec = inspect.getfullargspec(task.function)
        input_args = {}
        if argspec.args:
            print('|Введите значения для аргументов|')
            for arg in argspec.args:
                arg_type = None

                if arg in argspec.annotations:
                    arg_type = argspec.annotations[arg]

                while True:
                    try:
                        user_input = input(f"'{arg}' ({arg_type.__name__ if arg_type else 'тип не указан'}): ")
                        try:
                            if arg_type:
                                input_args[arg] = arg_type(user_input)
                            else:
                                input_args[arg] = user_input
                            break
                        except ValueError:
                            print(f"|Ошибка: Не удалось преобразовать введенное значение в тип {arg_type.__name__ if arg_type else 'тип не указан'}. Попробуйте еще раз|")
                    except KeyboardInterrupt:
                        print("\nПрограмма завершена по запросу пользователя (Ctrl+C/Del).")
                        exit()
        try:
            return task.function(**input_args)
        except Exception as e:
            print(f"|Ошибка выполнения задачи {task.name}: {e}|")
            return

    def input_task(self):
        while True:
            try:
                self.ui.clear_console()
                self.ui.display_message()
                self.ui.display_tasks(self.tasks)
                try:
                    task_id = int(input('Введите номер задачи: ')) - 1
                except KeyboardInterrupt:
                    print("\nПрограмма завершена по запросу пользователя (Ctrl+C/Del).")
                    exit()
                if task_id < 0 or task_id >= len(self.tasks):
                    self.ui.set_message('Ошибка: Введён некорректный номер задачи')
                    continue

                selected_task = self.tasks[task_id]
                if len(selected_task.subtasks) > 1:
                    return self.input_subtask(selected_task)
                else:
                    return selected_task
            except ValueError:
                self.ui.set_message('Ошибка: Введён некорректный номер задачи')
                continue
            except KeyboardInterrupt:
                print('\nclosed')
                break

    def input_subtask(self, parent_task: Union[Task, SubTask]):
        while True:
            try:
                self.ui.clear_console()
                self.ui.display_message()
                self.ui.display_subtasks(parent_task.subtasks)
                try:
                    subtask_id = int(input('Введите номер подзадачи: ')) - 1
                except KeyboardInterrupt:
                    print("\nПрограмма завершена по запросу пользователя (Ctrl+C/Del).")
                    exit()
                if subtask_id < 0 or subtask_id >= len(parent_task.subtasks):
                    self.ui.set_message('Ошибка: Введён некорректный номер подзадачи')
                    continue

                selected_subtask = parent_task.subtasks[subtask_id]
                return selected_subtask
            except ValueError:
                self.ui.set_message('Ошибка: Введён некорректный номер подзадачи')
                continue
            except KeyboardInterrupt:
                print('\nclosed')
                break

def main():
    ui = ConsoleUI()
    manager = TaskManager(ui)

    # Добавление задач в менеджер
    manager.add_task(task1, 'Обмен значениями переменных', 'Составьте программу обмена значениями трех переменных a, b, и c, так чтобы b получила значение c, c получила значение a, а a получила значение b.')
    manager.add_task(task2, 'Проверка ввода двух чисел и их сумма', 'Пользователь вводит два числа. Проверьте, что введенные данные - это числа. Если нет, выведите ошибку. Если да, то выведите их сумму.')
    manager.add_subtask(task2_1, 2, 'Проверка ввода n чисел и их сумма', 'Доработайте задачу 2.1 так, чтобы пользователь мог вводить n разных чисел, а затем выведите их сумму. Предоставьте возможность пользователю ввести значение n.')

    # Основной цикл
    while True:
        manager.ui.clear_console()
        task = manager.input_task()
        result = None
        if task:
            result = manager.run_task(task)
        try:
            if result is not None:
                input(f"Результат: {result}\n[Enter для закрытия задачи]")
            else:
                input(f"[Enter для закрытия задачи]")
        except KeyboardInterrupt:
            print("\nПрограмма завершена по запросу пользователя (Ctrl+C/Del).")
            exit()

# Функции решающие задачи
def task1(a: int, b: int, c: int):
    a, b, c = b, c, a
    return f"a = {a}, b = {b}, c = {c}"

def task2(number1, number2):
    while True:
        try:
            summ = int(number1) + int(number2)
            print('Все введённые значения — числа')
            return summ
        except ValueError:
            print('Одно или несколько введённых значений — не числа')
            break

def task2_1(numbers: list):
    for value in numbers:
        if not isinstance(value, (int, float)):
            print('Одно или несколько введённых значений — не числа')
            return
    print('Все введённые значения — числа')
    return sum(numbers)

if __name__ == '__main__':
    main()
