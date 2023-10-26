from textx import get_location, TextXSemanticError
from generation.static_analysis import find_stratification

ENTITY_REFERENCE_FLAGS = [
    "zeroOrMore",
    "oneOrMore",
    "nullable"
]


class Entity:
    def __init__(self, **kwargs):
        self.is_entity = True

    @property
    def jinja_context(self):
        flat_entity = {
            "name": self.name,
            "properties": []
        }

        for prop in self.properties:
            flat_prop = {"name": prop.name}
            flag = list(filter(lambda f: hasattr(prop, f) and getattr(prop, f) == True,
                               ENTITY_REFERENCE_FLAGS))
            flag = flag[0] if len(flag) >= 1 else ""

            if hasattr(prop, "entity"):
                flat_prop["type"] = prop.entity.name + "Entity"
            elif hasattr(prop, "type"):
                type_ = prop.type
                if hasattr(prop.type, "name"):
                    type_ = prop.type.name
                flat_prop["type"] = type_.capitalize()

            flat_prop["flag"] = flag
            flat_entity["properties"].append(flat_prop)

        return flat_entity


class Type:
    def __init__(self, **kwargs):
        self.is_type = True

    def __repr__(self):
        return self.name
    
    @property
    def jinja_context(self):
        return {
            "name": self.name.capitalize(),
            "base_type": self.parent_type.capitalize()
        }

def flatten_entity_properties(property, prefix="", names = {}):
    if hasattr(property, "entity") and hasattr(property.entity, "properties") and property._tx_fqn.find("EntityReverseReference") == -1:
        for p in property.entity.properties:
            flatten_entity_properties(p, prefix=f"{prefix}.{property.name}", names=names)
    else:
        names[f"{prefix}.{property.name}"] = property

    names[prefix] = property.parent
    return names
    
class Task:
    def __init__(self, **kwargs):
        self.is_task = True
        self.__create_names_map()
        self.reachability_plan = self.__check_step_reachability()

    def __check_step_reachability(self):
        return find_stratification(set(self.steps), set([""]))

    def __create_names_map(self):
        context = {}
        for argument in self.arguments:
            for property in argument.entity.properties:
                for name, value in flatten_entity_properties(property, prefix=argument.name, names = {}).items():
                    context[name] = value
            context[argument.name] = argument.entity

        for step in self.steps:
            for field in step.fields:
                context[f"self.{field.name}"] = field
                if hasattr(field, "entity"):
                    for name, value in flatten_entity_properties(field, prefix="self", names = {}).items():
                        context[name] = value
                        context[name.replace(f"{field.name}.", "")] = value
            context.update(step.computed_property_names)
        self.names = context
        

    @property
    def jinja_context(self):
        for step in self.steps:
            step = step.jinja_context

        return self


class Step:
    def __init__(self, **kwargs):
        self.is_step = True
        self.__create_names_map()

    @property
    def field_names(self):
        return {f"self.{field.name}": field for field in self.fields}
    
    @property
    def computed_property_names(self):
        return {f"self.{prop.name}": prop for prop in self.computedProperties}
    
    def check_operator_types(self):
        if self.precondition:
            self.precondition.traverse("check_operator_types", step_names=self.names, task_names=self.parent.names)

    def __create_names_map(self):
        context = {}
        for argument in self.arguments:
            if not hasattr(argument.entity, "properties"):
                continue
            for property in argument.entity.properties:
                for name, value in flatten_entity_properties(property, prefix=argument.name, names = {}).items():
                    context[name] = value
            context[argument.name] = argument.entity

        for field in self.fields:
            context[f"self.{field.name}"] = field
            if hasattr(field, "entity"):
                for name, value in flatten_entity_properties(field, prefix="self", names = {}).items():
                    context[name] = value
                    context[name.replace(f"self.{field.name}.", "")] = value

        context.update(self.computed_property_names)

        self.names = context

    def generate_expressions_code(self):
        # generate code for preconditions
        if self.precondition:
            self.precondition.py_code(step_names=self.names, task_names=self.parent.names)
            self.precondition.pddl_code(step_names=self.names, task_names=self.parent.names)

        # generate code for computedProperties and add all referenced names to the 'referenced attribute' 
        for prop in self.computedProperties:
            name_references = set()
            referenced_attributes = []
            prop.expression.build_name_references(name_references)

            code = prop.expression.py_code(step_names=self.names, task_names=self.parent.names)
            if "," in code:
                isSelfAgg = False
                code = code.split(",")
                if code[1].find("self.self.") != -1:
                    isSelfAgg = True
                    code[1] = code[1].replace("self.self.", "self.")
                    code = [code[0], code[1] + "," + code[2]]
                    continue

                iterable = code[1].strip()
                if len(code) == 3:
                    field = code[2][:-1].strip().replace("'", "")
                else:
                    field = None
                iterable = ".".join(iterable.split(".")[1:])
                for level in range(1, len(iterable.split(".")) + 1):
                    referenced_attributes.append(
                        {
                            "field" : field if level == len(iterable.split(".")) else ".".join(iterable.split(".")[level:level + 1]),
                            "iterable": ".".join(iterable.split(".")[0:level]),
                        } 
                    )
            for name_ref in name_references:
                levels = name_ref.split(".")
                for level in range(1, len(levels)):
                    referenced_attributes.append(
                        {
                            "field" : levels[level],
                            "iterable": ".".join(levels[0:level]),
                        } 
                    )
            for e in referenced_attributes:
                e["iterable"] = e["iterable"].replace("<step_args>", ",".join(arg.name for arg in self.parent.arguments))
            prop.referenced_attributes = sorted(referenced_attributes, key=lambda x : x["field"] or "Z")

    @property
    def jinja_context(self):
        for field in self.fields:
            if hasattr(field, "type"):
                field.type_name = field.type.name.capitalize() if hasattr(field.type, "name") else field.type.capitalize()
            if hasattr(field, "entity"):
                field.type_name = f"{ field.entity.name }Entity"
        
        for prop in self.computedProperties:
            # TODO: find better way
            if "," in prop.expression.python_code: # using aggregations
                parts = prop.expression.python_code.split(",")
                iterable, attr_name = parts[1].strip(), parts[2][:-1].strip().replace("'","")
                prop.iterable = iterable
                prop.attr_name = attr_name
            prop.expression.python_code_enriched = prop.expression.python_code.replace("<step_args>", ",".join(arg.name for arg in self.arguments)).replace("self.self.get", "self.get")

        self.pddl_predicates = []
        if self.precondition:
            for name in self.precondition.referenced_names.names:
                base_name = name.split(".")[0]
                if base_name == "self":
                    base_name = ".".join(name.split(".")[0:2])
                base_type = self.names[base_name]
                predicate_name = name.replace(".", "_")
                self.pddl_predicates.append({
                    "name" : predicate_name,
                    "base_name": base_name,
                    "base_type" : base_type.name
                })
            self.precondition.python_code_enriched = self.precondition.python_code.replace("<step_args>", ",".join(arg.name for arg in self.arguments))
        return self

class EntityReference:
    def __init__(self, **kwargs):
        self.reference = self.name

    @property
    def type(self):
        return self.name 
    
class MailEffect:
    def __init__(self, **kwargs):
        pass

    @property
    def jinja_context(self):
        if "self." in self.to.id:
            to = f"self.get('{self.to.id.split('.')[1]}{','.join(arg.name for arg in self.parent.arguments)}').{'.'.join(self.to.id.split('.')[2:])}"
        else:
            to = f"self.{self.to.id}"
        ret = f"sendMail({to}, '{self.body}', '{self.subject}')" if self.subject else f"sendMail({to}, '{self.body}')"
        return ret