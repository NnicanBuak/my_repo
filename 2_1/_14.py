import random
import tkinter as tk
from tkinter import messagebox

def task_14_1():
    def convert_to_usd() -> None:
        rub: str = rub_entry.get()
        try:
            usd: float = float(rub) / exchange_rate
            result_label.config(text=f"{usd:.2f} USD")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")

    window = tk.Tk()
    window.title("Конвертер валют: RUB в USD")

    exchange_rate = 97.0

    rub_label = tk.Label(window, text="RUB:")
    rub_label.pack()

    rub_entry = tk.Entry(window)
    rub_entry.pack()

    convert_button = tk.Button(window, text="Конвертировать", command=convert_to_usd)
    convert_button.pack()

    result_label = tk.Label(window, text="")
    result_label.pack()

    window.mainloop()

def task_14_2() -> None:
    def convert_currency() -> None:
        amount: str = amount_entry.get()
        currency: str = var.get()
        try:
            if currency == "RUB":
                result = float(amount) * exchange_rate
            else:
                result: float = float(amount) / exchange_rate
            result_label.config(text=f"{result:.2f} {currency}")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")

    window = tk.Tk()
    window.title("Конвертер валют: RUB и USD")

    exchange_rate = 97.0

    amount_label = tk.Label(window, text="Сумма:")
    amount_label.pack()

    amount_entry = tk.Entry(window)
    amount_entry.pack()

    var = tk.StringVar(value="RUB")

    rub_to_usd_radio = tk.Radiobutton(window, text="RUB в USD", variable=var, value="USD")
    rub_to_usd_radio.pack()

    usd_to_rub_radio = tk.Radiobutton(window, text="USD в RUB", variable=var, value="RUB")
    usd_to_rub_radio.pack()

    convert_button = tk.Button(window, text="Конвертировать", command=convert_currency)
    convert_button.pack()

    result_label = tk.Label(window, text="")
    result_label.pack()

    window.mainloop()