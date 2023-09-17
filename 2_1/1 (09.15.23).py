from typing import Union, Callable
import inspect
import os
import platform

class Task:
    def __init__(self, function: Callable, id: int, name: str, description: str):
        self.function = function
        self.id = id
        self.name = name
        self.description = description
        self.subtasks = []

class SubTask(Task):
    def __init__(self, function: Callable, parent_id: int, id: int, name: str, description: str):
        self.parent_id = parent_id
        super().__init__(function, id, name, description)

class TaskManager:
    last_used_id = 0

    def __init__(self, ui):
        self.tasks = []
        self.ui = ui

    def get_task(self, id_chain: Union[list[int], int]) -> Union[Task, None]:
        if isinstance(id_chain, int):
            id_chain = [id_chain]

        current_task = None
        for id in id_chain:
            if current_task is None:
                current_task = next((t for t in self.tasks if t.id == id), None)
            else:
                current_task = next((st for st in current_task.subtasks if st.id == id), None)
            if current_task is None:
                break
        if current_task == None:
            return
        return current_task

    def add_task(self, function: Callable, name: str, description: str):
        self.last_used_id += 1
        task = Task(function, self.last_used_id, name, description)
        self.tasks.append(task)

    def add_subtask(self, function: Callable, parent_id: int, name: str, description: str):
        parent_task = self.get_task(parent_id)
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
                    user_input = input(f"'{arg}' ({arg_type.__name__ if arg_type else 'тип не указан'}): ")
                    try:
                        if arg_type:
                            input_args[arg] = arg_type(user_input)
                        else:
                            input_args[arg] = user_input
                        break
                    except ValueError:
                        print(f"|Ошибка: Не удалось преобразовать введенное значение в тип {arg_type.__name__ if arg_type else 'тип не указан'}. Попробуйте еще раз|")

        try:
            return task.function(**input_args)
        except Exception as e:
            print(f"|Ошибка выполнения задачи {task.name}: {e}|")
            return

    def display_tasks(self):
        print('Доступные задачи:')
        print('—————————————————')
        for task in self.tasks:
            print(f"{task.id}: {task.name}")
        print('—————————————————')

    def display_subtasks(self, parent_task: Task):
        print(f"Пункты задачи {parent_task.id}:")
        print('—————————————————')
        for task in parent_task.subtasks:
            print(f"{task.id}: {task.name}")
        print('—————————————————')

    def input_task(self):
        while True:
            try:
                self.ui.clear_console()
                self.ui.display_message()
                self.display_tasks()
                task_id = int(input('Введите номер задачи: '))
                if task_id < 1:
                    self.ui.set_message('Ошибка: Введён некорректный id задачи')
                    continue

                selected_task = self.get_task(task_id)
                if selected_task:
                    if selected_task.subtasks:
                        while True:
                            self.ui.clear_console()
                            self.display_subtasks(selected_task)
                            subtask_id = int(input('Введите номер подзадачи: '))
                            if subtask_id < 1:
                                self.ui.set_message('Ошибка: Введён некорректный id подзадачи')
                                continue

                            selected_subtask = self.get_task([task_id, subtask_id])
                            if selected_subtask:
                                return selected_subtask
                            else:
                                self.ui.set_message('Ошибка: Подзадача с указанным id не найдена')
                    else:
                        return selected_task
                else:
                    self.ui.set_message('Ошибка: Задача с указанным id не найдена')

            except ValueError:
                self.ui.set_message('Ошибка: Введён некорректный id задачи или подзадачи, id - целое число')
                continue
            except KeyboardInterrupt:
                print('\nclosed')
                break

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

# Основная программа
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
            if result:
                input(f"Результат: {result}\n[Enter для закрытия задачи]")
            else:
                input(f"[Enter для закрытия задачи]")
        except KeyboardInterrupt:
            print('\nclosed')
            break
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

# Исполнение программы
if __name__ == '__main__':
    main()
