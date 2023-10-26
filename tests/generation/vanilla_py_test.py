
import unittest
from pathlib import Path
import sys
path_root = Path(__file__).parents[2] / 'wappl'
sys.path.append(str(path_root))

from wappl import parse_program
import generation.vanilla_py as generation
import os

class TestCodeGenerationVanillaPy(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.example_program = parse_program(
            Path(__file__).parent / ".wappl" / "example.wappl")
        self.step_tree_rogram = parse_program(
            Path(__file__).parent / ".wappl" / "step_tree_test.wappl")

        self.entity_program = parse_program(
            Path(__file__).parent / ".wappl" / "entities.wappl")

    def test_example(self):
        code_generator = generation.PythonDataLayerGenerator(
            self.example_program)
        generated_code = code_generator.generate()
        __location__ = Path(__file__).parents[2] / 'wappl'
        # with open(os.path.join(__location__, "vanilla_py_generated.py"), "w") as f:
        #     f.write(generated_code)

        with open(Path(__file__).parent / ".results" / "generated" / "example_generated.py", "w") as f:
            f.write(generated_code)

        with open(Path(__file__).parent / ".results" / "expected" / "example_generated.py", "r") as f:
            self.assertEqual(generated_code, f.read())

    def test_step_execution_tree(self):
        code_generator = generation.PythonDataLayerGenerator(
            self.step_tree_rogram)
        generated_code = code_generator.generate()
        __location__ = Path(__file__).parents[2] / 'wappl'
        with open(os.path.join(__location__, "step_tree_generated.py"), "w") as f:
            f.write(generated_code)

        with open(Path(__file__).parent / ".results" / "generated" / "step_tree_generated.py", "w") as f:
            f.write(generated_code)

        with open(Path(__file__).parent / ".results" / "expected" / "step_tree_generated.py", "r") as f:
            self.assertEqual(generated_code, f.read())

    def test_entity_generation(self):
        code_generator = generation.PythonDataLayerGenerator(
            self.entity_program)
        generated_code = code_generator.generate()
        __location__ = Path(__file__).parents[2] / 'wappl'
        with open(os.path.join(__location__, "entity_generation.py"), "w") as f:
            f.write(generated_code)

        with open(Path(__file__).parent / ".results" / "generated" / "entity_generation.py", "w") as f:
            f.write(generated_code)

        with open(Path(__file__).parent / ".results" / "expected" / "entity_generation.py", "r") as f:
            self.assertEqual(generated_code, f.read())


    def inject_path_resolving(self, code):
        code_to_inject = [
            "from pathlib import Path",
            "import sys",
            "path_root = Path(__file__).parents[4] / 'wappl'",
            "sys.path.append(str(path_root))",
        ]
        for line in code_to_inject[::-1]:
            code = f"{line}\n{code}"
        return code
    
    def test_generated_example(self):
        with open(Path(__file__).parent / ".results" / "generated" / "example_generated.py", "r") as f:
            code = self.inject_path_resolving(f.read())
            exec(code, globals(), globals())

            # Actual testing code:
            assignment = AssignmentEntity({"title" : "any"})
            assignment2 = AssignmentEntity({"title" : "any"})
            assignment3 = AssignmentEntity({"title" : "any"})
            hw = HomeworkEntity({"text": "homework text", "test": 5, "grade": 5.0, "assignments": [ assignment, assignment2, assignment3 ]})
            task = HomeworkGradingTask(hw)
            task.step_gradeAssignment(assignment, {"grade": Grade(5)})
            task.step_gradeHomework({})
            self.assertEqual(task.get("totalGrade"), 0)
            assignment.update_attribute("grade", Grade(5.0))
            self.assertEqual(task.get("totalGrade"), 5.0)

if __name__ == '__main__':
    unittest.main()
