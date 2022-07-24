"""
PROT - Python Replication & Obfuscation Tools
Python 3.10
file replicator.py: code replication logics.
https://github.com/Romansko/PROT/blob/main/prot/replicator.py
"""
import inspect

import utils
from sys import argv, exit
from os import path


class Replicator:
    """ Replication logics """

    def __init__(self):
        self.ci = None  # code info object
        self.ico = None  # injected code object
        self.infectedCode = None  # injected code object

    def deco(self, func):
        """ Decorate given function with the user's code. """

        def ret(*args):
            # If injected code fails, try to continue not letting the user know
            _ = utils.execute(self.ico)
            try:
                func(*args)
            except TypeError:
                pass  # argument types might mismatch. do nothing.

        return ret  # return self function

    def affect(self, obj):
        """ Affect and Evaluate """
        if not obj:
            return
        elif isinstance(obj, dict):
            for key in obj:
                self.affect(obj[key])  # affect dictionary objects.
        elif isinstance(obj, (tuple, list)):
            for o in obj:
                self.affect(o)  # affect tuple / list objects.
        elif inspect.isclass(obj):
            try:
                setattr(obj, "deco", self.deco)
                setattr(obj, "affect", self.affect)
            except:  # probably immutable type error.
                pass  # Do nothing. Silent infection.
            self.affect(dir(obj))  # affect class objects.
        elif callable(obj):
            try:
                infected_method = self.deco(obj)
                setattr(obj.__class__, obj.__name__, infected_method)
            except:
                pass  # Do nothing. Silent infection.

    def replicate(self, targetCode, injectedCode):
        """ Replicate targetCode with injectedCode. """
        if not targetCode or not injectedCode:
            print("[!] Invalid arguments.")
            return False
        ci = utils.CodeInfo(targetCode)
        co = ci.compile()
        if not co:
            print(f"[!] Unable to compile target code!")
        ici = utils.CodeInfo(injectedCode)  # injected code info
        ico = ici.compile()  # injected code object
        if not ico:
            print(f"[!] Unable to compile injected code!")
            return False
        self.ico = ico
        namespace = utils.execute(co)
        if not namespace:
            print(f"[!] Unable to execute target code!")
            return False
        self.affect(namespace)

        return True


class FileReplicator(Replicator):
    def __init__(self):
        super().__init__()

    def replicate(self, filepath, injectedCode):
        """
        Load a target file, replicate user's code within callable object.
        """
        if not filepath or not injectedCode:
            print("[!] Invalid arguments.")
            return False
        fh = utils.PythonFileHandler()
        if not fh.open(filepath):
            return False
        code = fh.read()
        fh.close()
        if not code:
            print(f"[!] Unable to read target code {filepath}!")
            return False
        if path.isfile(injectedCode):
            icfh = utils.PythonFileHandler()
            if not icfh.open(injectedCode):
                return False
            injectedCode = icfh.read()
            icfh.close()
            if not injectedCode:
                return False
        return super().replicate(code, injectedCode)


def replicate(targetFile, injectedCode):
    replicator = FileReplicator()
    return replicator.replicate(targetFile, injectedCode)


if __name__ == '__main__':
    if not argv or len(argv) < 3:
        exit(f"[!] Usage: python {path.basename(__file__)} <target_file.py> (<injected_code.py> | \"Injected Code\")")
    if not replicate(argv[1], argv[2]):
        print("[!] Replication failed!")
