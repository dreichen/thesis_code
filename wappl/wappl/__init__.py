import os
from textx import language, metamodel_from_file
from textx.scoping.providers import FQN

from .semantic_checks import OBJECT_PROCESSORS, BUILTINS
from ast_nodes import expression
from ast_nodes import wappl

__version__ = "0.1.0.dev"


def __find_classes():
    import sys
    import inspect
    classes = inspect.getmembers(
        sys.modules['ast_nodes.expression']) + inspect.getmembers(sys.modules['ast_nodes.wappl'])
    return list(filter(lambda obj: inspect.isclass(obj[1]) and not "TextXSemanticError" in obj[1].__name__ and not "PreconditionNames" in obj[1].__name__ and not "Date" in obj[1].__name__ and not "Datetime" in obj[1].__name__, classes))


def load_meta_model(debug=False):
    current_dir = os.path.dirname(__file__)
    classes = map(lambda cls: cls[1], __find_classes())
    if debug:
        with open('debug.log', 'w') as f:
            return metamodel_from_file(os.path.join(current_dir, 'wappl.tx'), debug=debug, autokwd=True)
    return metamodel_from_file(os.path.join(current_dir, 'wappl.tx'), autokwd=True, classes=classes, auto_init_attributes=False, builtins=BUILTINS)


def parse_program(file_name, meta_model=None, debug=False):
    if not meta_model:
        meta_model = load_meta_model(debug)

    meta_model.register_obj_processors(OBJECT_PROCESSORS)
    meta_model.register_scope_providers({'*.*': FQN()})

    program =  meta_model.model_from_file(file_name, debug=debug)

    for task in program.tasks:
        for step in task.steps:
            step.check_operator_types()
            step.generate_expressions_code()
            
    return program


@language('wappl', '*.wappl')
def wappl_language():
    "wappl language"
    return load_meta_model()
