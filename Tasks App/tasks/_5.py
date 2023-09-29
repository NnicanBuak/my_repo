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
