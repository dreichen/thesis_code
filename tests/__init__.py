import os
import pkgutil
import inspect
import unittest
from pathlib import Path
import sys
path_root = Path(__file__).parents[1] / 'wappl'
sys.path.append(str(path_root))

from wappl import parse_program
import wappl.language_builtins as lb
import generation.vanilla_py as generation
import os


def load_tests(loader, tests, pattern):
    path = [x[0] for x in os.walk(os.path.dirname(__file__))]
    for imp, modname, _ in pkgutil.walk_packages(path):
        if modname.endswith("_test"):
            for name, obj in inspect.getmembers(imp.find_module(modname).load_module(modname)):
                if inspect.isclass(obj):
                    if issubclass(obj, unittest.TestCase):
                        print(f"Found TestCase: {name}")
                        for test in loader.loadTestsFromTestCase(obj):
                            tests.addTest(test)

    print("=" * 70)
    return tests
