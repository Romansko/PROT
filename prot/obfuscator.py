"""
PROT - Python Replication & Obfuscation Tools
Python 3.10
file Obfuscator.py: Obfuscation logics.
https://github.com/Romansko/PROT/blob/main/prot/obfuscator.py
"""
import pfh
import random
import string
import keyword
from sys import argv, exit
from os import path
from base64 import b64encode
import builtins


class Obfuscator:

    def __init__(self):
        self.rand = 0
        self.reserved = keyword.kwlist
        self.reserved += keyword.softkwlist
        self.reserved += dir(builtins)

    def obfuscate(self, data, metadata):
        pass

    def setRand(self, rand):
        self.rand = rand

    def getRand(self):
        return self.rand


class CodeObfuscator(Obfuscator):
    """ Python Code Obfuscator """

    def obfuscate(self, code, co):
        code = self.refactorVariables(code, co)
        code = self.encodeStrings(code, co)
        return code

    def getRandVarName(self, exclude=None, minLen=5, maxLen=10):
        """ Generate a random variable name between min and max length """
        var = random.choice(string.ascii_letters)  # start with a letter
        for i in range(random.randint(minLen, maxLen)):
            var += random.choice(string.digits + string.ascii_letters)
        if (var in self.reserved) or (exclude and var in exclude):
            print(f"[*] Random variable name {var} is excluded, generating new one..")
            return self.getRandVarName(exclude, minLen, maxLen)
        return var

    def refactorVariables(self, code, co):
        if not code or not co:
            print("[!] CodeObfuscator::refactorVariables: No code to obfuscate!")
            return None
        exclude = []
        for var in co.co_names:
            if var not in self.reserved:
                newvar = self.getRandVarName(exclude)
                code = code.replace(var, newvar)
                exclude += [newvar]
        return code

    def encodeStrings(self, code, co):
        code = "from base64 import b64decode\n" + code
        if not code or not co:
            print("[!] CodeObfuscator::encodeStrings: No code to obfuscate!")
            return None
        for s in co.co_consts:
            if isinstance(s, str):
                encoded = b64encode(s.encode()).decode()  # base64 string.
                # Try both "" and ''
                code = code.replace(f"\"{s}\"", f"b64decode('{encoded}').decode()")
                code = code.replace(f"\'{s}\'", f"b64decode('{encoded}').decode()")
        return code


class FileObfuscator(CodeObfuscator):
    """ Python Files Obfuscator """

    def obfuscate(self, filepath, _=None):
        """ Obfuscate a python file. Returns obfuscated code by string. """
        fh = pfh.PythonFileHandler()
        if not fh.open(filepath):
            return None
        code = fh.read()
        co = fh.extractCodeObject(code)
        fh.close()
        if not code or not co:
            return None
        print(f"[*] Obfuscating {filepath}..")
        obfuscated = super().obfuscate(code, co)
        return obfuscated


def obfuscate(args):
    filepath = args[0]
    obs = FileObfuscator()
    obfuscated = obs.obfuscate(filepath)
    if obfuscated:
        nfp = filepath.replace(".py", ".obf.py")
        pfh.PythonFileHandler.dump(nfp, obfuscated)
        print(f"[*] Obfuscated file {filepath} saved as {nfp}")
    else:
        print(f"[!] Unable to obfuscate {filepath}.")


if __name__ == '__main__':
    if not argv or len(argv) < 2:
        exit(f"[!] Usage: python {path.basename(__file__)} <target_file.py>")
    obfuscate(argv[1:])
