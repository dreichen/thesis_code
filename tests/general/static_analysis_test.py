from textx import get_location, TextXSemanticError
import unittest
from pathlib import Path
import sys
path_root = Path(__file__).parents[2] / 'wappl'
sys.path.append(str(path_root))

from wappl import parse_program
import generation.static_analysis as static_analysis

class TestStaticAnalysis(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_step_unreachable(self):
        with self.assertRaises(TextXSemanticError):
            self.program = parse_program(
                Path(__file__).parent / ".wappl" / "static_analysis_unreachable.wappl")

    def test_step_reachable(self):
        program = parse_program(
            Path(__file__).parent / ".wappl" / "static_analysis_reachable.wappl")

        for task in program.tasks:
            self.assertIsNotNone(task.reachability_plan)
            expected_plan = [
                ['firstA', 'firstB'],
                ['second'],
                ['lastA', 'lastB']
            ]

            self.assertListEqual(
                [sorted(sublist) for sublist in task.reachability_plan], expected_plan)


if __name__ == '__main__':
    unittest.main()
