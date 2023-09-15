import inspect
import os
import platform

def clear_console():
    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

class Task():
    last_used_id = 1

    def __init__(self, function, name, description):
        self.id = Task.last_used_id
        Task.last_used_id += 1

        self.function = function
        self.name = name
        self.description = description

class TaskManager:
    def __init__(self):
        '''
        Инициализация менеджера задач.
        '''
        self.tasks = []

    def add_task(self, task_function, task_name, task_description):
        '''
        Добавление задачи в менеджер.

        :param task_function: Функция, выполняющая задачу.
        :param task_name: Название задачи.
        :param task_description: Описание задачи.
        '''
        task = Task(task_function, task_name, task_description)
        self.tasks.append(task)

    def run_task(self, task: object):
        '''
        Запуск задачи.

        :param task: Задача.
        '''
        clear_console()
        print(f"Задача: {task.name}")
        print(f"Описание: {task.description}", '\n')

        argspec = inspect.getfullargspec(task.function)
        if argspec.args:
            input_args = {}
            for arg in argspec.args:
                arg_type = None

                if arg in argspec.annotations:
                    arg_type = argspec.annotations[arg]

                while True:
                    user_input = input(f"Введите значение для аргумента '{arg}' ({arg_type.__name__ if arg_type else 'тип не указан'}): ")

                    try:
                        if arg_type:
                            input_args[arg] = arg_type(user_input)
                        else:
                            input_args[arg] = user_input
                        break
                    except ValueError:
                        print("\n", f"[Ошибка: Не удалось преобразовать введенное значение в тип {arg_type.__name__ if arg_type else 'не указан тип'}. Попробуйте еще раз]")

        try:
            return task.function(**input_args)
        except Exception as e:
            print("\n", f"[Ошибка выполнения задачи {task.name}: {e}]")
            return

# Создаём функции, решающие задачи
def task1(a: int, b: int, c: int):
    a, b, c = b, c, a
    return f"a = {a}, b = {b}, c = {c}"

# Создаем менеджер и добавляем задачи
manager = TaskManager()
manager.add_task(task1, 'Обмен значениями переменных', 'Составьте программу обмена значениями трех переменных a, b, и c, так чтобы b получила значение c, c получила значение a, а a получила значение b.')

# Исполнение программы
if __name__ == '__main__':
    message = ''
    while True:
        try:
            clear_console()
            print(message, '\n')
            print('Доступные задачи:')
            print('—————————————————')
            for task in manager.tasks:
                print(f"{task.id}: {task.name}")
            print('—————————————————')

            task_id = int(input('Введите номер задачи: '))

            if task_id < 1:
                message = '\n [Ошибка: Введён некорректный id задачи]'
                pass

            task = next((t for t in manager.tasks if t.id == task_id), None)

            if task =

            result = manager.run_task(task)
            input(f"Результат: {result}")

        except ValueError:
            message = '\n [Ошибка: Введён некорректный id задачи (требуется целое число)]'
        except KeyboardInterrupt:
            print('\n', '[Программа завершена по запросу пользователя]')
            break
else:
    print('[Предупреждение: Это консольное приложение, запустите основной файл Python]')
