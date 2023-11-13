import os
from interpreter import Interpreter
import sys


def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    interp = Interpreter()
    examples_dir = 'pascal'

    while True:
        clear_console()
        print("\nAvailable files:")
        files = list_files(examples_dir)
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")

        print("\nEnter the number of the file to run (0 to exit):")
        choice = input(">> ")

        if choice == '0':
            print("Exiting...")
            break

        try:
            file_index = int(choice) - 1
            selected_file = files[file_index]
            file_path = os.path.join(examples_dir, selected_file)

            with open(file_path, 'r') as f:
                code = f.read()

            try:
                result = interp.eval(code)
                print(result)
            except (SyntaxError, ValueError, TypeError) as e:
                print(f"{type(e).__name__}: {e}", file=sys.stderr)

            input("Press Enter to continue...")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid file number.")


if __name__ == "__main__":
    main()
