class Task():
    last_used_id = 1

    def __init__(self, name, function):
      self.id = Task.last_used_id
      Task.last_used_id += 1
      self.name = name
      self.function = function


class TaskManager:
    def __init__(self):
        """
        Инициализация менеджера задач.
        """
        self.tasks = []

    def list_tasks(self):
        """
        Вывод списка доступных задач в консоль.
        """
        print("Доступные задачи:")
        for task in self.tasks:
            print(f"{task.id}: {task.name}")

    def add_task(self, task_name, task_function):
        """
        Добавление задачи в менеджер.

        :param task_name: Название задачи.
        :param task_function: Функция, выполняющая задачу.
        """
        task = Task(task_name)
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

        result = task.function()
        print(f"Задача: {task.name}")
        print(f"Результат: {result}")

# Создаём функции решающие задачи
def task1(a, b, c):
    a, b, c = b, c, a
    return (a, b, c)

# Создаем менеджер и добавляем задачи
manager = TaskManager()
manager.add_task("Перестановка", task1)

if __name__ == '__main__':
    while True:
        try:
            manager.list_tasks()  # Выводим список задач
            task_id = int(input("Введите id задачи (или 0 для завершения): "))
            if task_id == 0:
                break
            manager.run_task(task_id)
        except ValueError:
            print("Ошибка: Введите корректный id задачи (целое число).")
        except KeyboardInterrupt:
            print("\nПрограмма завершена по запросу пользователя.")
            break
