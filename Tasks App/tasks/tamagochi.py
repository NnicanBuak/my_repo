import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules import terminal
import threading
import random
import keyboard

class Pet:
    def __init__(self, name: str, hunger=100, fun=50) -> None:
        self.name: str = name
        self.live = True
        self.hunger: int = hunger
        self.fun: int = fun

    def display(self) -> None:
        terminal.clear()
        print(f"{self.name}'s Hunger: {self.hunger}, Fun: {self.fun}\nВведите команду (f - feed, p - play): ")

    def feed(self) -> None:
        self.hunger += 20
        self.fun += 5
        if self.hunger > 120:
            self.hunger = 100

    def play(self) -> None:
        self.hunger -= 5
        self.fun += 10
        if self.fun > 100:
            self.fun = 100

def update_pet(pet) -> None:
    while pet.live:
        pet.hunger -= 10
        pet.fun -= 5
        if pet.hunger <= 0 or pet.fun <= 0:
            pet.live = False
        else:
            pet.display()
        time.sleep(random.randint(2, 60))

def interact_pet(pet) -> None:
    while pet.live:
        command: str = input('\r')
        if command == 'f':
            pet.feed()
            pet.display()
        elif command == 'p':
            pet.play()
            pet.display()

def tamagochi() -> str:
    name: str = input("Введите имя питомца: ")
    axolotl = Pet(name)

    # Создание потоков для обновления питомца и взаимодействия с питомцем
    interact_thread = threading.Thread(target=interact_pet, args=(axolotl,))
    update_thread = threading.Thread(target=update_pet, args=(axolotl,))

    # Запуск потоков
    update_thread.start()
    interact_thread.start()

    # Ожидание завершения потоков
    while update_thread.is_alive():
        try:
            update_thread.join(timeout=1)
        except KeyboardInterrupt:
            print("Вы оставили своего питомца одного...")
            break

    # Остановка потока ввода, если питомец больше не жив
    if not axolotl.live and interact_thread.is_alive():
        interact_thread.join()

    if axolotl.live:
        return f"Вы спасли {axolotl.name}!"
    return f"Вы не сохранили вашего питомца {axolotl.name}..."

print(tamagochi())
