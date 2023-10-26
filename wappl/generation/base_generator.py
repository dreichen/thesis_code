from pathlib import Path
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(
    Path(__file__).parent / 'templates'))

class LayerGenerator:
    def __init__(self, program):
        self.program = program

    def __jinja_context(self, objs):
        return list(map(lambda t: t.jinja_context,  objs))
    
    def get_template(self, name):
        return env.get_template(name)
    
    def generate(self):
        raise NotImplementedError