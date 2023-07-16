"""Loader for .bmx.py files. Based on https://stackoverflow.com/a/43573798"""
import sys
import os.path
import os

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location
from libcst_bmx.libcst import parse_module

from transform import BmxTransformer

class MyMetaFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if path is None or path == "":
            path = [os.getcwd()] # top level import -- 
        if "." in fullname:
            *parents, name = fullname.split(".")
        else:
            name = fullname
        for entry in path:
            if os.path.isdir(os.path.join(entry, name)):
                # this module has child modules
                filename = os.path.join(entry, name, "__init__.py")
                submodule_locations = [os.path.join(entry, name)]
            else:
                filename = os.path.join(entry, name + ".bmx.py")
                submodule_locations = None
            if not os.path.exists(filename):
                continue

            return spec_from_file_location(fullname, filename, loader=MyLoader(filename),
                submodule_search_locations=submodule_locations)

        return None # we don't know how to import this

class MyLoader(Loader):
    def __init__(self, filename):
        self.filename = filename
        self.transformer = BmxTransformer()

    def create_module(self, spec):
        return None # use default module creation semantics

    def exec_module(self, module):
        with open(self.filename) as f:
            data = f.read()
            original_tree = parse_module(data)
            modified_tree = original_tree.visit(self.transformer)

        exec(modified_tree.code, vars(module))

def install():
    """Inserts the finder into the import machinery"""
    sys.meta_path.insert(0, MyMetaFinder())

