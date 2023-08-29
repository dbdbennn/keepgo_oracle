import os


def clear():
    os.system("clear" if os.name == "posix" else "cls")
    print()
