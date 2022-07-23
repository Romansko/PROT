"""
PROT - Python Replication & Obfuscation Tools
Python 3.10
file pfh.py: PythonFileHandler. Wrap Python file handling logic.
https://github.com/Romansko/PROT/blob/main/prot/pfh.py
"""
from os import path
import ast  # abstract syntax tree - used to parse source code.


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

    def extractCodeObject(self, code):
        """
        Parse opened python file and return a code object.
        """
        if not code:
            return None
        if not code.strip():
            print(f"[!] File '{self.fileHandle.name}' is empty.")
            return None
        try:
            tree = ast.parse(code, 'exec')
            co = compile(tree, self.fileHandle.name, 'exec')  # code object
            return co  # code object
        except Exception as e:
            print(f"[!] {e}")
            return None

    def exec(self, code):
        """
        Executes a python file.
        """
        co = self.extractCodeObject(code)
        if not co:
            return False
        try:
            namespace = {}
            exec(co, namespace)
            return True
        except Exception as e:
            print(f"[!] {e}")
            return False

    @staticmethod
    def dump(filepath, code):
        """
        Dump python code to a file.
        """
        with open(filepath, 'w') as f:
            f.write(code)
            print(f"[*] Dumped code to '{filepath}'.")
