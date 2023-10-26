
import unittest
from pathlib import Path
import sys
path_root = Path(__file__).parents[2] / 'wappl'
sys.path.append(str(path_root))

from wappl import parse_program
import generation.vanilla_py as generation
import os

class TestCodeGenerationOrderManagement(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.program = None


    def test_parse_ordermanagement(self):
        self.program = parse_program(
            Path(__file__).parent / ".wappl" / "order-management.wappl")
        code_generator = generation.PythonDataLayerGenerator(self.program)
        generated_code = code_generator.generate()
        __location__ = Path(__file__).parents[2] / 'wappl'


        with open(Path(__file__).parent / ".results" / "generated" / "order_management.py", "w") as f:
            f.write(generated_code)

        with open(Path(__file__).parent / ".results" / "expected" / "order_management.py", "r") as f:
            self.assertEqual(generated_code, f.read())
            
if __name__ == '__main__':
    unittest.main()
