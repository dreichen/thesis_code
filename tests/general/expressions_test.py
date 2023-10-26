from textx import get_location, TextXSemanticError
import unittest
from pathlib import Path
import sys
path_root = Path(__file__).parents[2] / 'wappl'
sys.path.append(str(path_root))

from wappl import parse_program

class TestExpressionGrammar(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)

    def test_incompatible(self):
        with self.assertRaises(TextXSemanticError):
            self.program = parse_program(
                Path(__file__).parent / ".wappl" / "expressions_types_incompatible_1.wappl")
            
        with self.assertRaises(TextXSemanticError):
            self.program = parse_program(
                Path(__file__).parent / ".wappl" / "expressions_types_incompatible_2.wappl")

    def test_compatible(self):
        parse_program(
            Path(__file__).parent / ".wappl" / "expressions_types_compatible.wappl")


if __name__ == '__main__':
    unittest.main()
