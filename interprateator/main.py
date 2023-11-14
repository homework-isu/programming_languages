import os
from interpreter import Interpreter
import sys


def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    interp = Interpreter()
    filepath = "pascal/1.pas"

    with open(filepath, "r") as file:
        code = file.read()

    result = interp.eval(code)
    print("Pascal code:")
    print(code)
    print("Result:")
    print(result)


if __name__ == "__main__":
    main()
