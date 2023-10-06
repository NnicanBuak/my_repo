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