from functools import reduce
import inspect
import sys
from .base_generator import LayerGenerator
from wappl import language_builtins

class PDDLPlanningLayerGenerator(LayerGenerator):
    def __init__(self, program):
        self.program = program

    def __jinja_context(self, objs):
        return list(map(lambda t: t.jinja_context,  objs))

    def __get_builtin_types(self):
        classes = inspect.getmembers(sys.modules['wappl.language_builtins'])
        return list(filter(lambda obj: inspect.isclass(obj[1]) and "BuiltinType" in repr(inspect.getclasstree([obj[1]])[0][0]), classes))

    def generate(self):
        domain = self.get_template('domain.pddl.template')
        problem = self.get_template('problem.pddl.template')

        context = {
            "domain_name": self.program._tx_filename.split("/")[-1].split(".")[0],
            "builtin_types": self.__get_builtin_types(),
            "requirements": ":strips :fluents :durative-actions :typing :conditional-effects :negative-preconditions :duration-inequalities :equality",
            "types": self.program.types,
            "entities": self.program.entities,
            "tasks": self.__jinja_context(self.program.tasks),
        }

        return {
            "domain": domain.render(context),
            "problem": problem.render(context)
        }