"""
PROT - Python Replication & Obfuscation Tools
Python 3.9.13
file obfuscator.py: Obfuscation logics.
https://github.com/Romansko/PROT/blob/main/prot/obfuscator.py
"""
import re
import utils
import random
import string
from sys import argv, exit
from os import path
from base64 import b64encode


class Obfuscator:
    """ Python Code Obfuscator """

    def __init__(self, minVarNameLen=5, maxVarNameLen=10, minDummyVal=1, maxDummyVal=100000, maxDummies=5):
        self.ci = None  # code info object
        self.minVarNameLen = minVarNameLen
        self.maxVarNameLen = maxVarNameLen
        self.minDummyVal = minDummyVal
        self.maxDummyVal = maxDummyVal
        self.maxDummies = maxDummies

    def obfuscate(self, code):
        """ apply obfuscation logics on code."""
        if not code:
            print("[!] CodeObfuscator::obfuscate: No code to obfuscate!")
            return None
        code = self.removeComments(code)
        ci = utils.CodeInfo(code)
        if not ci.parse():
            print("[!] CodeObfuscator::obfuscate: error parsing code!")
            return None
        self.ci = ci
        code = self.obfuscateStrings(code)
        code = self.obfuscateVariables(code)
        code = self.insertDummies(code)
        return code

    def getRandVarName(self, exclude=None):
        """ Generate a random variable name between min and max length. """
        var = random.choice(string.ascii_letters)  # start with a letter
        for i in range(random.randint(self.minVarNameLen, self.maxVarNameLen)):
            var += random.choice(string.digits + string.ascii_letters)
        if (var in self.ci.reserved) or (exclude and var in exclude):
            print(f"[*] Random variable name {var} is excluded, generating new one..")
            return self.getRandVarName(exclude)
        return var

    def getRandDummy(self):
        """ Generate a random operation with numbers between min and max. """
        ops = random.randint(1, self.maxDummies)
        dummy = self.getRandVarName() + " = "
        for i in range(ops - 1):
            dummy += str(random.randint(self.minDummyVal, self.maxDummyVal)) + " " + \
                     random.choice([' + ', ' - ', ' * ', ' % ', ' // '])
        dummy += str(random.randint(self.minDummyVal, self.maxDummyVal))
        return dummy

    def obfuscateVariables(self, code):
        """ refactor code's variables to random names. """
        if not code:
            print("[!] CodeObfuscator::refactorVariables: No code to obfuscate!")
            return None
        exclude = []
        for var in self.ci.names:
            if var not in self.ci.reserved:
                newvar = self.getRandVarName(exclude)
                code = re.sub(r"\b%s\b" % var, newvar, code)  # replace whole words only
                exclude += [newvar]
        return code

    def obfuscateStrings(self, code):
        """ Encode (base64) const string within code and wrap with base64 decode logic."""
        if not code:
            print("[!] CodeObfuscator::encodeStrings: No code to obfuscate!")
            return None
        code = "from base64 import b64decode\n" + code
        for s in self.ci.consts:
            encoded = b64encode(s.encode()).decode()  # base64 string.
            # Regex to match any string based on https://stackoverflow.com/a/49906750
            # look behind pattern based on https://stackoverflow.com/a/50857637
            code = re.sub(r"(?<=[^bruf])(\"\"\"|\'\'\'|\"|\')(%s)\1" % re.escape(s), f"b64decode('{encoded}').decode()", code)
        return code

    def insertDummies(self, code):
        """ Insert dummy operations into code. """
        if not code:
            print("[!] CodeObfuscator::insertDummies: No code to obfuscate!")
            return None
        lines = code.splitlines()
        i = len(lines) - 1
        while i > 0:
            if lines[i].strip() and lines[i-1].strip():
                spaces = len(lines[i]) - len(lines[i].lstrip())
                if spaces == len(lines[i-1]) - len(lines[i-1].lstrip()):  # some protection
                    if lines[i-1][-1] != ",":
                        newline = ' ' * spaces + self.getRandDummy()
                        lines.insert(i, newline)
            i -= 1
        return "\n".join(lines)

    def removeComments(self, code):
        """ Remove comments from code. """
        if not code:
            print("[!] CodeObfuscator::removeComments: No code to obfuscate!")
            return None
        code = re.sub(r"#.*", "", code)    # remove single line comments
        # Regex to match any string based on https://stackoverflow.com/a/49906750
        code = re.sub(r"(\"\"\"|\'\'\')(?:(?!\1)(?:\\.|[^\\]))*\1", "", code, flags=re.DOTALL)   # remove multi-line comments
        return code


class FileObfuscator(Obfuscator):
    """ Python Files Obfuscator """

    def obfuscate(self, filepath):
        """ Obfuscate a python file. Returns obfuscated code by string. """
        fh = utils.PythonFileHandler()
        if not fh.open(filepath):
            return None
        code = fh.read()
        if not code:
            return None
        fh.close()
        print(f"[*] Obfuscating {filepath}..")
        obfuscated = super().obfuscate(code)
        return obfuscated


def obfuscate(args):
    """ entry function """
    filepath = args[0]
    obs = FileObfuscator()
    obfuscated = obs.obfuscate(filepath)
    if obfuscated:
        nfp = filepath.replace(".py", ".obf.py")
        utils.dump(nfp, obfuscated)
        print(f"[*] Obfuscated file {filepath} saved as {nfp}")
    else:
        print(f"[!] Unable to obfuscate {filepath}.")


if __name__ == '__main__':
    if not argv or len(argv) < 2:
        exit(f"[!] Usage: python {path.basename(__file__)} <target_file.py>")
    obfuscate(argv[1:])
