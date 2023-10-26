from textx import get_location, TextXSemanticError

def task_processor(task):
    final_step = None
    for step in task.steps:
        if step.final:
            final_step = step

    if not final_step:
        raise TextXSemanticError(f"Task '{task.name}' does not have a final step which is required", **get_location(task))

    
OBJECT_PROCESSORS = {
    "Task": task_processor,
}

class Test(object):
    def __init__(self, parent, name, attributes):
        self.parent = parent
        self.name = name
        self.attributes = attributes

BUILTINS = {
    "integer": Test(None, 'integer', []),
}