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

    def run_task(self, task_id: int):
        '''
        Запуск задачи по её идентификатору.

        :param task_id: Уникальный идентификатор задачи.
        '''
        task = None
        for t in self.tasks:
            if t.id == task_id:
                task = t
                break

        if task is None:
            print(f"[Задача с id - {task_id} не найдена]")
            return

        clear_console()
        print(f"Задача: {task.name}")
        print(f"Описание: {task.description}", '\n')

        try:
            return task.function()
        except Exception as e:
            print('\n', f"[Ошибка выполнения задачи {task}: {e}]")
            return

# Создаём функции, решающие задачи
def task1():
    a, b, c = 1, 2, 3  # Замените значения на то, что вам нужно
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
            task_id_input = int(input('Введите id задачи: '))
            if task_id_input == 0:
                break
            result = manager.run_task(task_id_input)
            input(f"Результат: {result}")
        except ValueError:
            message = '\n [Ошибка: Введён некорректный id задачи (требуется целое число)]'
        except KeyboardInterrupt:
            print('\n', '[Программа завершена по запросу пользователя]')
            break
else:
    print('[Предупреждение: Это консольное приложение, запустите основной файл Python]')
