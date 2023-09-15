import inspect

class Task():
    last_used_id = 1

    def __init__(self, function, requires_input, name, description):
        self.id = Task.last_used_id
        Task.last_used_id += 1

        self.function = function
        self.requires_input = requires_input
        self.name = name
        self.description = description
class TaskManager:
    def __init__(self):
        """
        Инициализация менеджера задач.
        """
        self.tasks = []

    def add_task(self, task_function, requires_input, task_name, task_description):
        """
        Добавление задачи в менеджер.

        :param task_function: Функция, выполняющая задачу.
        :param requires_input: Указывает, требуются ли аргументы для выполнения задачи.
        :param task_name: Название задачи.
        :param task_description: Описание задачи.
        """
        task = Task(task_function, requires_input, task_name, task_description )
        self.tasks.append(task)

    def run_task(self, task_id):
        """
        Запуск задачи по её идентификатору.

        :param task_id: Уникальный идентификатор задачи.
        """
        task = None
        for t in self.tasks:
            if t.id == task_id:
                task = t
                break

        if task is None:
            print(f"Задача с id {task_id} не найдена.")
            return

        # Получаем информацию о сигнатуре функции
        argspec = inspect.getfullargspec(task.function)
        input_args = {}
        for arg in argspec.args:
            arg_type = None

            # Проверяем, есть ли аннотация аргумента
            if arg in argspec.annotations:
                arg_type = argspec.annotations[arg]

            # Запрашиваем значение аргумента
            user_input = input(f"Введите значение для аргумента '{arg}' ({arg_type.__name__ if arg_type else 'не указан тип'}): ")

            # Преобразуем введенное значение в соответствующий тип
            try:
                if arg_type:
                    input_args[arg] = arg_type(user_input)
                else:
                    input_args[arg] = user_input
            except ValueError:
                print(f"Ошибка: Не удалось преобразовать введенное значение в тип {arg_type.__name__ if arg_type else 'не указан тип'}.")
                return

        try:
            output = task.function(**input_args)
        except Exception as e:
            print(f"Ошибка выполнения задачи: {e}")
            return

        print(f"Задача: {task.name}")
        print(f"Описание: {task.description}")
        print(f"Результат: {output}")

# Создаём функции решающие задачи
def task1(a:int, b:int, c:int):
    a, b, c = b, c, a
    return  f'a = {a}, b = {b}, c = {c}'

# Создаем менеджер и добавляем задачи
manager = TaskManager()
manager.add_task(task1, True, 'Обмен значениями переменных','Составьте программу обмена значениями трех переменных a, b, и c, так чтобы b получила значение c, c получила значение a, а a получила значение b.')

if __name__ == '__main__':
    while True:
        try:
            print("\nДоступные задачи:")
            for task in manager.tasks:
                print(f"{task.id}: {task.name}")
            print('---')
            task_id = int(input("Введите id задачи (или 0 для завершения): "))
            if task_id == 0:
                break
            manager.run_task(task_id)
        except ValueError:
            print("Ошибка: Введите корректный id задачи (целое число).")
        except KeyboardInterrupt:
            print("\nПрограмма завершена по запросу пользователя.")
            break
else:
    print('Это консольное приложение, запустите основной файл Python')