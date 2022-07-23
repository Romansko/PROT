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
            except Exception:
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


def parseConsts(obj):
    """ parse code object and extract const strings from it """
    parsed = []
    if not obj:
        return parsed
    if isinstance(obj, str):
        parsed += [obj]
    elif isinstance(obj, types.CodeType):
        parsed += parseConsts(obj.co_consts)
    elif isinstance(obj, (tuple, list)):
        for o in obj:
            parsed += parseConsts(o)
    elif isinstance(obj, (dict, set)):
        for k, v in obj.items():
            parsed += parseConsts(k)
            parsed += parseConsts(v)
    return parsed


def extractNames(code):
    """
    Parse python code and return reserved names and const strings.
    """
    reserved = keyword.kwlist
    reserved += keyword.softkwlist
    reserved += dir(builtins)
    reserved += sys.builtin_module_names
    if not code:
        return reserved, []
    if not code.strip():
        print(f"[!] code is empty!")
        return reserved, []
    try:
        tree = ast.parse(code, 'exec')
        co = compile(tree, 'target', 'exec')  # code object
        consts = parseConsts(co.co_consts)
    except Exception as e:
        print(f"[!] {e}")
        return reserved, []
    try:
        namespace = {}
        exec(code, namespace)  # execute target file for inner info
        for k in namespace:
            reserved += [k]
            reserved += dir(namespace[k])
        reserved = list(set(reserved))  # remove duplicates
        reserved.sort()
        return reserved, consts
    except Exception as e:
        print(f"[!] {e}")
        return reserved, consts


def dump(filepath, code):
    """
    Dump python code to a file.
    """
    with open(filepath, 'w') as f:
        f.write(code)
        print(f"[*] Dumped code to '{filepath}'.")
