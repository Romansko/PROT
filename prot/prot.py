"""
PROT - Python Replication & Obfuscation Tools
Python 3.10
file prot.py: PROT entry point & main menu.
https://github.com/Romansko/PROT/blob/main/prot/prot.py
"""
from os import system, name, path
from sys import argv, exit
import re
import obfuscator


def getUserInput(description, pattern=None):
    """
    Wrapper to input function. Include validations and program exit point.
    :param description: description to display.
    :param pattern: validate user input with pattern.
    :return: user's validated input.
    """
    try:
        inputText = input(f"[*] {description}: ")
        if pattern:
            while not pattern.match(inputText):
                print("[!] Invalid input. Please try again..")
                inputText = input(f"[*] {description}: ")
        return inputText
    except (EOFError, KeyboardInterrupt):  # (ctrl+z, ctrl+c)
        exit("\n[*] User quitted program.")


class Option:
    def __init__(self, flag, description, callback, args):
        """
        Initialize a program option.
        :param flag: invocation flag.
        :param description: option description.
        :param callback: callback handle.
        :param args: extra arguments
        """
        self.flag = flag
        self.desc = description
        self.cb = callback
        self.args = args

    def __str__(self):
        string = f"{self.flag} "
        for arg in self.args:
            string += arg + " "
        string += f"\n\t\t{self.desc}"
        return string


def rcHandle():
    print("unimplemented")
    return True


def rcfHandle(args):
    if not args or len(args) < 1:
        return False

    # len(args) >= 1. Handle only first argument.
    print("unimplemented")
    return True


def rfHandle(args):
    if not args or len(args) < 1:
        return False

    # len(args) >= 1. Handle only first argument.
    print("unimplemented")
    return True


def rffHandle(args):
    if not args or len(args) < 2:
        return False

    # len(args) >= 2. Handle only first two arguments.
    print("unimplemented")
    return True


class Menu:
    def __init__(self):
        _tfpy = "<target_file.py>"
        _icpy = "<injected_code.py>"
        _repint = "Replicate input code into current python interpreter."
        _repfile = "Load a target file and replicate input code into its callable objects."
        self.prog = path.basename(__file__)
        self.options = {
            "-h": Option("-h", "Display help information", self.printHelp, []),
            "-o": Option("-o", "Obfuscate a target file.", obfuscator.obfuscate, [_tfpy]),
            "-rc": Option("-rc", f"{_repint} (From command line).", rcHandle, []),
            "-rcf": Option("-rcf", f"{_repint} (From python file).", rcfHandle, [_icpy]),
            "-rf": Option("-rf", f"{_repfile} (From command line).", rfHandle, [_tfpy]),
            "-rff": Option("-rff", f"{_repfile} (From python file).", rffHandle, [_tfpy, _icpy])
        }
        self.clearCmd = 'cls' if (name == 'nt') else 'clear'  # Windows vs Linux.

    def clear(self):
        system(self.clearCmd)

    def printHelp(self):
        """
        Prints prot.py usage.
        """
        print(f"[*] Usage:")
        for opt in self.options:
            print(f"\tpython {self.prog} {self.options[opt]}")

    def printMenu(self):
        _title = "=  Welcome to PROT - Python Replication & Obfuscation Tools  ="
        _sep = '=' * len(_title)
        self.clear()
        print("", _sep, _title, _sep, sep='\n')
        print("[0] Display help information.")
        print("[1] Python prot: obfuscate a python file.")
        print("[2] Python replicator: replicate a python code within current python session.")
        print("[3] Python replicator: replicate a python code within a given python file.")
        print()

    def invoke(self, args):
        if not args or len(args) < 1:
            print(f"[!] Please invoke {self.prog} in a standard way.")
            self.printHelp()
            return False

        if len(args) == 1:
            while True:
                self.clear()
                self.printMenu()
                c = getUserInput("Choose option by number. to quit press ctrl + z or ctrl + c", re.compile("^\d$"))
                if c == "0":
                    self.printHelp()
                elif c == "1":
                    fp = getUserInput("Enter target file to obfuscate.")
                    obfuscator.obfuscate([fp])
                system("pause")
            # Never reaches here if invoked with no arguments.

        opt = args[1].lower()
        args = args[2:]
        if opt not in self.options.keys():
            print(f"[!] Invalid argument {opt}!")
            self.printHelp()
            return False

        if len(args) < len(self.options[opt].args):
            print(f"[!] Missing arguments for {opt}!")
            print(f"[*] Usage: \tpython {self.prog} {self.options[opt]}")
            return False

        self.options[opt].cb(args)
        return True


if __name__ == '__main__':
    menu = Menu()
    if not menu.invoke(argv):
        exit()
