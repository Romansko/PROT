"""
PROT - Python Replication & Obfuscation Tools
Python 3.10
file utils.py: Common utilities for PROT
https://github.com/Romansko/PROT/blob/main/prot/utils.py
"""
from os import path
import ast  # abstract syntax tree - used to parse source code.
import keyword
import sys
import builtins
import types


class PythonFileHandler:
    """
    Wrapper for file handling.
    """

    def __init__(self):
        self.fileHandle = None

    def __del__(self):
        self.close()

    def open(self, filepath):
        """
        Opens a python file handler if filepath is a valid python file.
        """
        if not path.isfile(filepath):
            print(f"[!] Invalid filepath provided: '{filepath}'")
            return False
        try:
            fh = open(filepath, 'r')
            if not fh.readable():
                print(f"[!] Unable to read file '{filepath}'.")
                return False
        except Exception as e:
            print(f"[!] {e}")
            return False
        self.close()  # Closes file handler if previously opened.
        self.fileHandle = fh
        return True

    def close(self):
        """
        Closes file handler if opened.
        """
        if self.fileHandle:
            try:
                self.fileHandle.close()
            except Exception as e:
                print(f"[!] {e}")
                pass
            self.fileHandle = None

    def read(self):
        """ read python file's content and return it. """
        if not self.fileHandle:
            print("[!] FileHandle was not opened!")
            return None
        try:
            print(f"[*] Reading {self.fileHandle.name}..")
            self.fileHandle.seek(0)
            return self.fileHandle.read()
        except Exception as e:
            print(f"[!] {e}")
            return None


class CodeInfo:
    """ Code's info object """

    def __init__(self, code):
        self.code = code
        self.consts = []
        self.reserved = []
        self.names = []

    def parseConsts(self, obj):
        """ parse code object and extract const strings from it """
        parsed = []
        if not obj:
            return parsed
        if isinstance(obj, str):
            parsed += [obj]
        elif isinstance(obj, types.CodeType):
            parsed += self.parseConsts(obj.co_consts)
        elif isinstance(obj, (tuple, list)):
            for o in obj:
                parsed += self.parseConsts(o)
        elif isinstance(obj, (dict, set)):
            for k, v in obj.items():
                parsed += self.parseConsts(k)
                parsed += self.parseConsts(v)
        return parsed

    def compile(self):
        """
        Compile python code and return compiled code object.
        """
        if not self.code or not self.code.strip():
            print(f"[!] code is empty!")
            return None
        try:
            tree = ast.parse(self.code, 'exec')
            co = compile(tree, 'target', 'exec')  # code object compiled for exec
            return co
        except Exception as e:
            print(f"[!] {e}")
            return None

    def parse(self):
        """
        Parse python code and return reserved names and const strings.
        """
        self.reserved = dir(object)
        self.reserved += keyword.kwlist
        self.reserved += keyword.softkwlist
        self.reserved += dir(builtins)
        for bi in dir(builtins):
            self.reserved += dir(bi)
        self.reserved += sys.builtin_module_names
        if not self.code or not self.code.strip():
            print(f"[!] code is empty!")
            return False
        co = self.compile()
        if not co:
            return False
        self.names = co.co_names
        consts = self.parseConsts(co.co_consts)
        self.consts = consts
        try:
            namespace = execute(co)
            for k in namespace:
                self.reserved += [k]
                self.reserved += dir(namespace[k])
                if '__module__' in dir(namespace[k]):
                    self.reserved += [str(namespace[k].__module__)]
                    if str(namespace[k].__module__) in sys.modules:
                        self.reserved += dir(sys.modules[str(namespace[k].__module__)])
            self.reserved = list(set(self.reserved))  # remove duplicates
            self.reserved.sort()
            return True
        except Exception as e:
            print(f"[!] {e}")
            return False


def dump(filepath, code):
    """ Dump python code to a file. """
    with open(filepath, 'w') as f:
        f.write(code)
        print(f"[*] Dumped code to '{filepath}'.")


def execute(code):
    """ Executes python code or code object. """
    try:
        namespace = {}
        exec(code, namespace)
        return namespace
    except Exception as e:
        print(f"[!] {e}")
        return None


def extractCodeObject(codeOrFile):
    if not codeOrFile:
        print("[!] extractCodeObject: Invalid argument!")
        return None
    if path.isfile(codeOrFile):
        pfh = PythonFileHandler()
        if not pfh.open(codeOrFile):
            return None
        code = pfh.read()
        pfh.close()
    else:
        code = codeOrFile
    ci = CodeInfo(code)
    co = ci.compile()
    if not co:
        print("[!] extractCodeObject: unable to compile given code!")
        return None
    return co
