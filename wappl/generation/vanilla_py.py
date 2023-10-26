from .base_generator import LayerGenerator
from .pddl_gen import *

class PythonDataLayerGenerator(LayerGenerator):
    def __jinja_context(self, objs):
        return list(map(lambda t: t.jinja_context,  objs))

    def generate(self):
        template = self.get_template('vanilla_py.data_layer.py.template')

        context = {
            "custom_types": self.__jinja_context(self.program.types),
            "entities":     self.__jinja_context(self.program.entities),
            "tasks":        self.__jinja_context(self.program.tasks),
            "roles":        self.program.roles
        }

        return template.render(context) 
    
class PythonInteractionLayerGenerator(LayerGenerator):
    def __jinja_context(self, objs):
        return list(map(lambda t: t.jinja_context,  objs))

    def generate(self):
        template = self.get_template('vanilla_py.interaction_layer.py.template')

        context = {
            "custom_types": self.__jinja_context(self.program.types),
            "entities":     self.__jinja_context(self.program.entities),
            "tasks":        self.__jinja_context(self.program.tasks),
        }
        
        return template.render(context) 
