import os


def clear():
    os.system("clear" if os.name == "posix" else "cls")
    for i in range(1, 3):
        print()
