from typing import Callable, Union, Optional
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

class SubTask:
    def __init__(self, function: Callable, parent_id: int, id: int, name: str, description: str):
        self.parent_id = parent_id
        self.function = function
        self.id = id
        self.name = name
        self.description = description

class TerminalUI:
    def __init__(self):
        self.message = 'Ctrl+C/Del для возврата'
        self.current_menu = 'tasks'
        self.previous_menu = None
        self.current_task = None

    def back(self):
        if self.previous_menu and self.previous_menu != self.current_menu:
            self.current_menu = self.previous_menu


    def set_message(self, message: str):
        self.message = message

    def display_message(self):
        print('|' + self.message + '|' + '\n')

    def clear_console(self):
        system = platform.system()
        if system == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def input_task_menu(self, tasks: list[Task]) -> Optional[Task]:
        while True:
            self.previous_menu = None
            self.current_menu = 'tasks'
            self.clear_console()
            self.display_message()
            print('Доступные задачи:')
            print('—————————————————')
            for i, task in enumerate(tasks, start=1):
                print(f"\033[4m{i}\033[0m: {task.name}")
            print('—————————————————')
            try:
                task_number = int(input('Введите номер задачи: ')) - 1
            except ValueError:
                self.set_message('Ошибка: Введён некорректный номер задачи')
                continue
            except KeyboardInterrupt:
                self.clear_console()
                print('Приложение закрыто по запросу пользователя.')
                exit()

            if 0 <= task_number < len(tasks):
                selected_task = tasks[task_number]
                if len(selected_task.subtasks) > 1:
                    self.current_menu = 'subtasks'
                    self.current_task = selected_task
                    return self.input_subtask_menu(selected_task)
                else:
                    return selected_task
            else:
                self.set_message('Ошибка: Введён некорректный номер задачи')

    def input_subtask_menu(self, parent_task: Task) -> Optional[Task]:
        while True:
            self.previous_menu = 'tasks'
            self.current_menu = 'subtasks'
            self.clear_console()
            self.display_message()
            parent_id = parent_task.id
            print(f"Пункты задачи {parent_id}:")
            print('—————————————————')
            for i, task in enumerate(parent_task.subtasks, start=1):
                print(f"{parent_id}.\033[4m{i}\033[0m: {task.name}")
            print('—————————————————')
            try:
                subtask_number = int(input('Введите номер подзадачи: ')) - 1
            except ValueError:
                self.set_message('Ошибка: Введён некорректный номер подзадачи')
                continue
            except KeyboardInterrupt:
                self.back()
                return

            if 0 <= subtask_number < len(parent_task.subtasks):
                return parent_task.subtasks[subtask_number]
            else:
                self.set_message('Ошибка: Введён некорректный номер подзадачи')

    def task_menu(self, task: Union[Task, SubTask]):
        self.previous_menu = self.current_menu
        self.current_menu = 'task'
        self.clear_console()

        argspec = inspect.getfullargspec(task.function)
        input_args = {}
        if argspec.args:
            print('|Введите значения для аргументов|\n')
            print(f"Задача: {task.name}")
            print(f"Описание: {task.description}", '\n')
            for arg in argspec.args:
                arg_type = None

                if arg in argspec.annotations:
                    arg_type = argspec.annotations[arg]

                while True:
                    try:
                        user_input = input(f"'{arg}' ({arg_type.__name__ if arg_type else 'тип не указан'}): ")
                        if arg_type:
                            input_args[arg] = arg_type(user_input)
                        else:
                            input_args[arg] = user_input
                        break
                    except ValueError:
                        self.set_message(f'|Ошибка: Не удалось преобразовать введенное значение в тип {arg_type.__name__ if arg_type else "тип не указан"}. Попробуйте еще раз|')
                    except KeyboardInterrupt:
                        self.back()
                        return

        try:
            return task.function(**input_args)
        except Exception as e:
            print(f"|Ошибка выполнения задачи {task.name}: {e}|")
            return

class TaskManager:
    def __init__(self, ui):
        self.tasks = []
        self.ui = ui
        self.last_used_id = 0

    def get_task(self, id):
        if 0 <= id < len(self.tasks):
            return self.tasks[id]
        return None

    def add_task(self, function: Callable, name: str, description: str):
        self.last_used_id += 1
        task = Task(function, self.last_used_id, name, description)
        self.tasks.append(task)

    def add_subtask(self, function: Callable, parent_id: int, name: str, description: str):
        parent_task = self.get_task(parent_id - 1)
        if parent_task:
            subtask_id = len(parent_task.subtasks) + 1
            subtask = SubTask(function, parent_id, subtask_id, name, description)
            parent_task.subtasks.append(subtask)
            self.last_used_id += 1
        else:
            print(f"|Ошибка: Родительская задача с ID {parent_id} не найдена|")

def main():
    ui = TerminalUI()
    manager = TaskManager(ui)

    # Добавление задач в менеджер
    manager.add_task(task1, 'Обмен значениями переменных', 'Составьте программу обмена значениями трех переменных a, b, и c, так чтобы b получила значение c, c получила значение a, а a получила значение b.')
    manager.add_task(task2_1, 'Проверка ввода двух чисел и их сумма', 'Пользователь вводит два числа. Проверьте, что введенные данные - это числа. Если нет, выведите ошибку. Если да, то выведите их сумму.')
    manager.add_subtask(task2_2, 2, 'Проверка ввода n чисел и их сумма', 'Доработайте задачу 2.1 так, чтобы пользователь мог вводить n разных чисел, а затем выведите их сумму. Предоставьте возможность пользователю ввести значение n.')

    # Основной цикл
    while True:
        ui.clear_console()
        if ui.current_menu == 'tasks':
            task = ui.input_task_menu(manager.tasks)
        elif ui.current_menu == 'subtasks':
            task = ui.input_subtask_menu(ui.current_task)
        else:
            task = ui.current_task

        result = None
        if task:
            result = ui.task_menu(task)
        try:
            if result is not None:
                input(f"Результат: {result}\n[Enter для закрытия задачи]")
            else:
                input(f"[Enter для закрытия задачи]")
        except KeyboardInterrupt:
            ui.back()


# Функции решающие задачи
def task1(a: int, b: int, c: int):
    a, b, c = b, c, a
    return f"a = {a}, b = {b}, c = {c}"

def task2_1(number1, number2):
    while True:
        try:
            summ = int(number1) + int(number2)
            print('Все введённые значения — числа')
            return summ
        except ValueError:
            print('Одно или несколько введённых значений — не числа')
            break

def task2_2(numbers: list):
    for value in numbers:
        if not isinstance(value, (int, float)):
            print('Одно или несколько введённых значений — не числа')
            return
    print('Все введённые значения — числа')
    return sum(numbers)

if __name__ == '__main__':
    main()
