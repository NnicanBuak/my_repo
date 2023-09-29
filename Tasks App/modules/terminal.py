import platform
import os


def clear() -> None:
    system: str = platform.system()
    if system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')