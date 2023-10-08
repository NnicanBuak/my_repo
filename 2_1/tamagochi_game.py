import os
import platform
import time
import random
import threading
import keyboard

class terminal:
    @staticmethod
    def clear() -> None:
      system: str = platform.system()
      if system == 'Windows':
          os.system('cls')
      else:
          os.system('clear')


MAX_FULLNESS = 200
MAX_FUN = 200
SCALES_DIVISION_PRICE = 3
FULLNESS_OVERSATURATION_LIMIT = 100
FUN_OVERINDULGENCE_LIMIT = 100
FEED_COOLDOWN = 30
PLAY_COOLDOWN = 15

FULLNESS_SCALE_LENGTH = FULLNESS_OVERSATURATION_LIMIT
FUN_SCALE_LENGTH = FUN_OVERINDULGENCE_LIMIT
FULLNESS_SCALE_DIVISIONS = FULLNESS_SCALE_LENGTH // SCALES_DIVISION_PRICE
FUN_SCALE_DIVISIONS = FUN_SCALE_LENGTH // SCALES_DIVISION_PRICE

class Pet:
    def __init__(self, name: str = "Nnican", fullness=100, fun=50) -> None:
        self.name: str = name
        self.is_alive = True
        self.stop_event = threading.Event()
        self.__art: str = "    ≽(._.)≼\n      ( )_"
        self.__fullness: int = fullness
        self.__fun: int = fun
        self.__feed_cooldown: int = 0
        self.__play_cooldown: int = 0

    @property
    def fullness(self) -> int:
        return self.__fullness

    @property
    def fun(self) -> int:
        return self.__fun

    @property
    def feed_cooldown(self) -> int:
        return self.__feed_cooldown

    @property
    def play_cooldown(self) -> int:
        return self.__play_cooldown

    @fullness.setter
    def fullness(self, value) -> None:
        if value < MAX_FULLNESS:
            self.__fullness = value
        else:
            self.__fullness = MAX_FULLNESS
        if self.fullness <= 0:
            self.is_alive = False
        self.check_state()
        self.display()

    @fun.setter
    def fun(self, value) -> None:
        if value < MAX_FUN:
            self.__fun = value
        else:
            self.__fun = MAX_FUN
        if self.fun <= 0:
            self.is_alive = False
        self.check_state()
        self.display()

    @feed_cooldown.setter
    def feed_cooldown(self, value) -> None:
        self.__feed_cooldown = value
        # self.display()

    @play_cooldown.setter
    def play_cooldown(self, value) -> None:
        self.__play_cooldown = value
        # self.display()

    def display(self) -> None:
        fullness_scale_divisions: int = self.fullness // SCALES_DIVISION_PRICE
        fun_scale_divisions: int = self.fun // SCALES_DIVISION_PRICE
        terminal.clear()
        output: str = f"""
\033[01;38;05;15m{self.__art}\033[0m

   \033[01;38;05;15mFullness: {self.fullness}\033[m
\033[01;38;05;252m0\033[01;38;05;15m|\033[01;38;05;179m{'▇' * fullness_scale_divisions if fullness_scale_divisions <= FULLNESS_SCALE_DIVISIONS else '▇' * FULLNESS_SCALE_DIVISIONS}\033[01;38;05;238m{'▇' * ((FULLNESS_SCALE_LENGTH // SCALES_DIVISION_PRICE) - fullness_scale_divisions) if fullness_scale_divisions > 0 else '▇' * FULLNESS_SCALE_DIVISIONS}\033[01;38;05;15m|\033[01;38;05;252m{FULLNESS_SCALE_LENGTH}\033[0m
   \033[01;38;05;15mFun: {self.fun}\033[0m
\033[01;38;05;252m0\033[01;38;05;15m|\033[01;38;05;139m{'▇' * fun_scale_divisions if fun_scale_divisions <= FUN_SCALE_DIVISIONS else '▇' * FUN_SCALE_DIVISIONS}\033[01;38;05;238m{'▇' * ((FUN_SCALE_LENGTH // SCALES_DIVISION_PRICE) - fun_scale_divisions) if fun_scale_divisions > 0 else '▇' * FUN_SCALE_DIVISIONS}\033[01;38;05;15m|\033[01;38;05;252m{FUN_SCALE_LENGTH}\033[0m

feed cooldown: {self.feed_cooldown}; play cooldown: {self.play_cooldown}

[F]eed [P]lay [Q]uit
"""
        print(f"\n{' ' * (6 - (len(self.name) // 2 - 1 if len(self.name) % 2 == 0 else len(self.name) // 2)) if len(self.name) <= 10 else ''}\033[01;37;42m {self.name} \033[0m" if self.is_alive else f"     \033[01;38;05;15;48;05;242m {self.name} \033[0m", output)

    def feed(self) -> None:
        print("f")
        if self.feed_cooldown == 0 and not self.fullness >= 100:
            self.fullness += 20

            self.feed_cooldown = FEED_COOLDOWN

    def play(self) -> None:
        if self.play_cooldown == 0 and not self.fun >= 100 and self.fullness > 10:
            self.fun += 20
            self.fullness -= 10

            self.play_cooldown = PLAY_COOLDOWN

    def check_state(self) -> None:
        if self.fun <= 0 and self.fullness > 0:
            self.__art = "\n≽(‾-‾)≼ )_\n╱     ╲"
        elif self.fullness <= 0:
            self.__art = "\n≽(x_x)≼ )_"

        if self.fullness > 100 and self.fun > 100:
            self.__art = "    ≽(*v*)≼\n      (@)_"
        elif self.fullness > 100 and 75 <= self.fun < 100:
            self.__art = "    ≽(^⏝​^)≼\n      (@)_"
        elif self.fullness > 100 and 25 <= self.fun < 75:
            self.__art = "    ≽(^_^)≼\n      (@)_"
        elif self.fullness > 100 and 0 < self.fun < 25:
            self.__art = "    ≽(._.)≼\n      (@)_"

        if 75 <= self.fullness < 100 and self.fun > 100:
            self.__art = "    ≽(*v*)≼\n      ( )_"
        elif 75 <= self.fullness < 100 and 75 <= self.fun < 100:
            self.__art = "    ≽(^⏝​^)≼\n      ( )_"
        elif 75 <= self.fullness < 100 and 25 <= self.fun < 75:
            self.__art = "    ≽(^_^)≼\n      ( )_"
        elif 75 <= self.fullness < 100 and 0 < self.fun < 25:
            self.__art = "    ≽(._.)≼\n      ( )_"

        if 25 <= self.fullness < 75 and self.fun > 100:
            self.__art = "    ≽(*v*)≼\n      ( )_"
        elif 25 <= self.fullness < 75 and 75 <= self.fun < 100:
            self.__art = "    ≽(^⏝​^)≼\n      ( )_"
        elif 25 <= self.fullness < 75 and 25 <= self.fun < 75:
            self.__art = "    ≽(^_^)≼\n      ( )_"
        elif 25 <= self.fullness < 75 and 0 < self.fun < 25:
            self.__art = "    ≽(._.)≼\n      ( )_"

        if 0 < self.fullness < 25 and self.fun > 100:
            self.__art = "    ≽(*v*)≼\n      (≋)_"
        elif 0 < self.fullness < 25 and 75 <= self.fun < 100:
            self.__art = "    ≽(^⏝​^)≼\n      (≋)_"
        elif 0 < self.fullness < 25 and 25 <= self.fun < 75:
            self.__art = "    ≽(^_^)≼\n      (≋)_"
        elif 0 < self.fullness < 25 and 0 < self.fun < 25:
            self.__art = "    ≽(._.)≼\n      (≋)_"


        elif self.fullness > 120 or self.fun > 120:
            state_thread = threading.Thread(target=self.handle_overindulgence)
            state_thread.start()
            # Пооток состояния
            state_thread.join()

    def handle_overindulgence(self) -> None:
        while self.fullness > FULLNESS_OVERSATURATION_LIMIT or self.fun > FUN_OVERINDULGENCE_LIMIT and not self.stop_event.is_set():
            time.sleep(30)
            if self.fullness > 120:
                self.fullness -= 10
                if self.fullness < 0:
                    self.fullness = 0
            if self.fun > 120:
                self.fun -= 10
                if self.fun < 0:
                    self.fun = 0

    def update(self) -> None:
        start_time: float = time.time()
        self.display()
        time.sleep(10)
        while (self.is_alive or time.time() - start_time <= 600) and not self.stop_event.is_set():
            self.fullness -= random.randint(5, 15)
            self.fun -= random.randint(3, 8)
            for t in range(random.randint(30, 60)):
                if not ((self.is_alive or time.time() - start_time <= 600) and not self.stop_event.is_set()):
                    break
                time.sleep(1)

    def cooldown_timer(self) -> None:
        while self.is_alive and not self.stop_event.is_set():
            time.sleep(1)
            if self.__feed_cooldown > 0:
                self.__feed_cooldown -= 1
            if self.__play_cooldown > 0:
                self.__play_cooldown -= 1

            self.display()


class Game:
    def __init__(self) -> None:
        self.pet = None
        self.update_thread = None
        self.cooldown_update_thread = None

    def quit(self) -> None:
        if self.pet:
            self.pet.stop_event.set()
            self.update_thread.join() # type: ignore
            self.cooldown_update_thread.join() # type: ignore

    def start(self) -> None:
        name: str = input("Set pet name: ")
        if not name:
            name = "Axolotl"
        self.pet = Pet(name)
        if self.pet:
            keyboard.add_hotkey('q', self.quit)
            keyboard.add_hotkey('f', lambda: self.pet.feed()) # type: ignore
            keyboard.add_hotkey('p', lambda: self.pet.play()) # type: ignore

            self.update_thread = threading.Thread(target=self.pet.update)
            self.cooldown_update_thread = threading.Thread(target=self.pet.cooldown_timer)

            self.update_thread.start()
            self.cooldown_update_thread.start()

            self.update_thread.join()
            self.quit()

            self.cooldown_update_thread.join()

            if self.pet.is_alive:
                print(f"You gave {self.pet.name} to good hands.")
            else:
                print(f"{self.pet.name} left you.")
        else:
            raise AttributeError("No pet")

if __name__ == "__main__":
    game = Game()
    game.start()