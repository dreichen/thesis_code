
import unittest
from pathlib import Path
import sys
path_root = Path(__file__).parents[2] / 'wappl'
sys.path.append(str(path_root))

from wappl import parse_program
import generation.vanilla_py as pddl_gen

class TestCodeGenerationPddl(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.program = parse_program(
            Path(__file__).parent / ".wappl" / "example.wappl") 

    def test_code_generation(self):
        code_generator = pddl_gen.PDDLPlanningLayerGenerator(self.program)
        generated_code = code_generator.generate()

        with open(Path(__file__).parents[2] / 'wappl' / "generated_domain.pddl", "w") as f:
            f.write(generated_code["domain"])

        with open(Path(__file__).parents[2] / 'wappl' / "generated_problem.pddl", "w") as f:
            f.write(generated_code["problem"])

    def test_code_generation_order_management(self):
        program = parse_program(
            Path(__file__).parent / ".wappl" / "order-management.wappl") 
        code_generator = pddl_gen.PDDLPlanningLayerGenerator(program)
        generated_code = code_generator.generate()

        with open(Path(__file__).parents[2] / 'wappl' / "order_management_domain.pddl", "w") as f:
            f.write(generated_code["domain"])

        with open(Path(__file__).parents[2] / 'wappl' / "order_management_problem.pddl", "w") as f:
            f.write(generated_code["problem"])

if __name__ == '__main__':
    unittest.main()
