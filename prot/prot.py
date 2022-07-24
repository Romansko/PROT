"""
PROT - Python Replication & Obfuscation Tools
Python 3.9.13
file prot.py: PROT entry point & main menu.
https://github.com/Romansko/PROT/blob/main/prot/prot.py
"""
from os import system, name, path
from sys import argv
import obfuscator
import replicator


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


def rcHandle(args):
    """
    replicate user's code to current interpreter.
    :param args: user's code = args[0]
    """
    if not args or len(args) < 1:
        print("[!] rcHandle: missing arguments.\n")
        return
    replicator.replicate(args[0])


def rfHandle(args):
    """
    Load target file and replicate user's code into the current interpreter.
    :param args: user's code = args[0]. target file = args[1].
    """
    if not args or len(args) < 2:
        print("[!] rfHandle: missing arguments.\n")
        return
    replicator.replicate(args[0], args[1])


class Menu:
    def __init__(self):
        _tfpy = "<target_file.py>"
        _icpy = "<injected_code.py>"
        self.prog = path.basename(__file__)
        self.options = {
            "-h": Option("-h", "Display help information. (This).", self.printHelp, []),
            "-o": Option("-o", "Obfuscate a target file.", obfuscator.obfuscate, [_tfpy]),
            "-rc": Option("-rc", "Replicate user's code into current interpreter.", rcHandle, [_icpy]),
            "-rf": Option("-rf", "Load target file & inject code into current interpreter.", rfHandle, [_icpy, _tfpy]),
        }
        self.clearCmd = 'cls' if (name == 'nt') else 'clear'  # Windows vs Linux.

    def clear(self):
        system(self.clearCmd)

    def printHelp(self, _=None):
        """
        Prints prot.py usage.
        """
        print(f"[*] Usage:")
        for opt in self.options:
            print(f"\tpython {self.prog} {self.options[opt]}")

    def invoke(self, args):
        if not args or len(args) <= 1:
            self.printHelp()
            return False

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
    _ = menu.invoke(argv)   # interactive menu removed, return value not used atm.
