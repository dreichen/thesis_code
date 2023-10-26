from textx import get_location, TextXSemanticError

from wappl.language_builtins import Date, Datetime

BUILTINS_TYPE_MAPPING = {
    "Date.now()" : Date,
    "Datetime.now()" : Datetime
}

class PreconditionNames:
    def __init__(self):
        self.names = set()
        self.names_fields = set()

    def add(self, name):
        self.names.add(name)
        if name.find("self.") != -1:
            self.names_fields.add(name)


class Precondition:
    def __init__(self, **kwargs):
        self.expressions = kwargs.pop('expressions')

        # pass down to Primary rule and fill there
        self.referenced_names = PreconditionNames()
        self.build_name_references(self.referenced_names)

    @property
    def python_code(self):
        code = f"({ self.expressions[0].python_code })"
        for exp in self.expressions[1:]:
            code += f" and ({ exp.python_code })"
        return code

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        self.expressions[0].traverse(func_name, **kwargs)
        for exp in self.expressions[1:]:
            exp.traverse(func_name, **kwargs)

    def check_operator_types(self, **kwargs):
        pass
    
    def build_name_references(self, referenced_names):
        self.expressions[0].build_name_references(referenced_names)
        for exp in self.expressions[1:]:
            exp.build_name_references(referenced_names)

    def py_code(self, **kwargs):
        code = f"({ self.expressions[0].py_code(**kwargs) })"
        for exp in self.expressions[1:]:
            code += f" and ({ exp.py_code(**kwargs) })"
        return code

    
    def pddl_code(self, **kwargs):
        code = f"({ self.expressions[0].pddl_code(**kwargs) })"
        for exp in self.expressions[1:]:
            code += f"(and { exp.pddl_code(**kwargs) })\n"
        return code


class Expression:
    def __init__(self, **kwargs):
        self.condition = kwargs.pop('condition')
        self.if_case = kwargs.pop('if')
        self.else_case = kwargs.pop('else')
        self.dis = kwargs.pop('dis')
        self.python_code = ""
        self.pddl_code_ = ""
        
    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        if self.condition and self.if_case and self.else_case:
            self.if_case.traverse(func_name, **kwargs)
            self.condition.traverse(func_name, **kwargs)
            self.else_case.traverse(func_name, **kwargs)
        else:
            return self.dis.traverse(func_name, **kwargs)

    def check_operator_types(self, **kwargs):
        pass

    def build_name_references(self, referenced_names):
        if self.condition and self.if_case and self.else_case:
            self.if_case.build_name_references(referenced_names)
            self.condition.build_name_references(referenced_names)
            self.else_case.build_name_references(referenced_names)
        else:
            return self.dis.build_name_references(referenced_names)

    def py_code(self, **kwargs):
        if self.condition and self.if_case and self.else_case:
            self.python_code = f"{self.if_case.py_code(**kwargs)} if {self.condition.py_code(**kwargs)} else {self.else_case.py_code(**kwargs)}"
        else:
            self.python_code = self.dis.py_code(**kwargs)
        return self.python_code

    
    def pddl_code(self, **kwargs):
        if self.condition and self.if_case and self.else_case:
            self.pddl_code_ = f"{self.if_case.pddl_code(**kwargs)} if {self.condition.pddl_code(**kwargs)} else {self.else_case.pddl_code(**kwargs)}"
        else:
            self.pddl_code_ = self.dis.pddl_code(**kwargs)
        return self.pddl_code_


class Disjunction:
    def __init__(self, **kwargs):
        self.op = kwargs.pop('op')

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        self.op[0].traverse(func_name, **kwargs)
        for op in self.op[1:]:
            op.traverse(func_name, **kwargs)

    def check_operator_types(self, **kwargs):
        pass

    def build_name_references(self, referenced_names):
        self.op[0].build_name_references(referenced_names)
        for op in self.op[1:]:
            op.build_name_references(referenced_names)

    def py_code(self, **kwargs):
        code = f"{self.op[0].py_code(**kwargs)}"
        for op in self.op[1:]:
            code += f" or {op.py_code(**kwargs)}"
        return code

    
    def pddl_code(self, **kwargs):
        code = f"{self.op[0].pddl_code(**kwargs)}"
        for op in self.op[1:]:
            code += f" or {op.pddl_code(**kwargs)}"
        return code


class Conjunction:
    def __init__(self, **kwargs):
        self.op = kwargs.pop('op')

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        self.op[0].traverse(func_name, **kwargs)
        for op in self.op[1:]:
            op.traverse(func_name, **kwargs)

    def check_operator_types(self, **kwargs):
        pass

    def build_name_references(self, referenced_names):
        self.op[0].build_name_references(referenced_names)
        for op in self.op[1:]:
            op.build_name_references(referenced_names)

    def py_code(self, **kwargs):
        code = f"{self.op[0].py_code(**kwargs)}"
        for op in self.op[1:]:
            code += f" and {op.py_code(**kwargs)}"
        return code

    
    def pddl_code(self, **kwargs):
        code = f"{self.op[0].pddl_code(**kwargs)}"
        for op in self.op[1:]:
            code += f" and {op.pddl_code(**kwargs)}"
        return code


class Inversion:
    def __init__(self, **kwargs):
        self.op = kwargs.pop('op')
        self.not_ = kwargs.pop('not')

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        if self.not_:
            self.not_.traverse(func_name, **kwargs)
        else:
            self.op.traverse(func_name, **kwargs)

    def check_operator_types(self, **kwargs):
        pass

    def build_name_references(self, referenced_names):
        if self.not_:
            self.not_.build_name_references(referenced_names)
        else:
            self.op.build_name_references(referenced_names)

    def py_code(self, **kwargs):
        return f"not {self.op.py_code(**kwargs)}" if self.not_ else self.op.py_code(**kwargs)

    
    def pddl_code(self, **kwargs):
        return f"not {self.op.pddl_code(**kwargs)}" if self.not_ else self.op.pddl_code(**kwargs)


def get_real_type(a):
    if hasattr(a, "parent_type"):
        return a.parent_type
    else:
        return a
    
def is_compatible(a, b):
    # to be refactored
    comp_matrix = {
        str : ["Text", "string"],
        "Text": [str, "string"],
        "string": [str, "Text"],
        int : ["Integer", "integer"],
        "Integer": [int, "integer"],
        "integer": [int, "Integer"],
        float: ["Decimal", "decimal"],
        "Decimal": ["decimal", float],
        "decimal": ["Decimal", float],
        "boolean": [bool],
        bool: ["boolean"],
        "Date": ["Date"],
        "Date": [Date],
        Date: ["Date"],
        "DateTime": ["DateTime"],
        "DateTime": [Datetime],
        Datetime: ["DateTime"],
    }

    if type(a) == type(b):
        return a == b
    elif a in comp_matrix.keys() and b in comp_matrix.keys() and b in comp_matrix[a] and a in comp_matrix[b]:
        return True
    return False
    
class Comparison:
    def __init__(self, **kwargs):
        self.op = kwargs.pop('op')
        self.sign = kwargs.pop('sign')

    def check_operator_types(self, **kwargs):
        names = kwargs["step_names"]
        names.update(kwargs["task_names"])

        if len(self.op) > 1:
            typ = None
            for op in self.op:
                resolved_name  = op.py_code(**kwargs)
                if type(resolved_name) == str:
                    resolved_name = resolved_name.replace("self.get('", "self.").replace("', <step_args>)", "")
                    if 'PythonDataLayer' in resolved_name:
                        return True
                if resolved_name in names.keys(): # name reference
                    if "ComputedProperty" not in names[resolved_name]._tx_fqn: # do not check operator types for computed properties for now
                        temp_typ = get_real_type(names[resolved_name].type)
                    else:
                        return True
                elif resolved_name in BUILTINS_TYPE_MAPPING.keys():
                    temp_typ = BUILTINS_TYPE_MAPPING[resolved_name]
                elif resolved_name in ["False", "True", "true", "false"]:
                    temp_typ = bool
                elif type(resolved_name) in [str, bool, int, float]: # builtin type like string, bool or integer
                    temp_typ = type(resolved_name)
                else:
                    raise TypeError()

                if not typ:
                    typ = temp_typ

                elif not is_compatible(typ, temp_typ):
                    raise TextXSemanticError(f"type {typ} is not comparable to type {temp_typ}", **get_location(op))

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        if len(self.op) == 1:
            self.op[0].traverse(func_name, **kwargs)
        else:
            self.op[0].traverse(func_name, **kwargs)
            self.op[1].traverse(func_name, **kwargs)

    def build_name_references(self, referenced_names):
        if len(self.op) == 1:
            self.op[0].build_name_references(referenced_names)
        else:
            self.op[0].build_name_references(referenced_names)
            self.op[1].build_name_references(referenced_names)

    def py_code(self, **kwargs):
        if len(self.op) == 1:
            return self.op[0].py_code(**kwargs)
        return f"{self.op[0].py_code(**kwargs)} {self.sign} {self.op[1].py_code(**kwargs)}"

    
    def pddl_code(self, **kwargs):
        if len(self.op) == 1:
            return self.op[0].pddl_code(**kwargs)
        return f"{self.op[0].pddl_code(**kwargs)} {self.sign} {self.op[1].pddl_code(**kwargs)}"


class Sum:
    def __init__(self, **kwargs):
        self.op = kwargs.pop('op')
        self.sign = kwargs.pop('sign')

    def check_operator_types(self, **kwargs):
        pass

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        if len(self.sign) < 1:
            self.op[0].traverse(func_name, **kwargs)
        else:
            self.op[0].traverse(func_name, **kwargs)

            for i, op in enumerate(self.op[1:]):
                self.sign[i].traverse(func_name, **kwargs)
                op.traverse(func_name, **kwargs)

    def build_name_references(self, referenced_names):
        if len(self.sign) < 1:
            self.op[0].build_name_references(referenced_names)
        else:
            self.op[0].build_name_references(referenced_names)

            for i, op in enumerate(self.op[1:]):
                self.sign[i].build_name_references(referenced_names)
                op.build_name_references(referenced_names)

    def py_code(self, **kwargs):
        if len(self.sign) < 1:
            return self.op[0].py_code(**kwargs)
        code = f"{self.op[0].py_code(**kwargs)}"
        for i, op in enumerate(self.op[1:]):
            code += f" {self.sign[i]} {op.py_code(**kwargs)}"
        return code

    
    def pddl_code(self, **kwargs):
        if len(self.sign) < 1:
            return self.op[0].pddl_code(**kwargs)
        code = f"{self.op[0].pddl_code(**kwargs)}"
        for i, op in enumerate(self.op[1:]):
            code += f" {self.sign[i]} {op.pddl_code(**kwargs)}"
        return code


class Term:
    def __init__(self, **kwargs):
        self.op = kwargs.pop('op')
        self.operation = kwargs.pop('operation')

    def check_operator_types(self, **kwargs):
        pass

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        if len(self.operation) < 1:
            self.op[0].traverse(func_name, **kwargs)
        else:
            self.op[0].traverse(func_name, **kwargs)
            for i, op in enumerate(self.op[1:]):
                op.traverse(func_name, **kwargs)

    def build_name_references(self, referenced_names):
        if len(self.operation) < 1:
            self.op[0].build_name_references(referenced_names)
        else:
            self.op[0].build_name_references(referenced_names)
            for i, op in enumerate(self.op[1:]):
                op.build_name_references(referenced_names)

    def py_code(self, **kwargs):
        if len(self.operation) < 1:
            return self.op[0].py_code(**kwargs)
        code = f"{self.op[0].py_code(**kwargs)}"
        for i, op in enumerate(self.op[1:]):
            code += f" {self.operation[i]} {op.py_code(**kwargs)}"
        return code

    
    def pddl_code(self, **kwargs):
        if len(self.operation) < 1:
            return self.op[0].pddl_code(**kwargs)
        code = f"{self.op[0].pddl_code(**kwargs)}"
        for i, op in enumerate(self.op[1:]):
            code += f" {self.operation[i]} {op.pddl_code(**kwargs)}"
        return code


class Factor:
    def __init__(self, **kwargs):
        self.op = kwargs.pop('op')
        self.expression = kwargs.pop('expression')
        self.operation = kwargs.pop('operation')

    def check_operator_types(self, **kwargs):
        pass

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        if self.expression:
            self.expression.traverse(func_name, **kwargs)

        for i, op in enumerate(self.op):
            op.traverse(func_name, **kwargs)

    def build_name_references(self, referenced_names):
        if self.expression:
            self.expression.build_name_references(referenced_names)

        for i, op in enumerate(self.op):
            op.build_name_references(referenced_names)

    def py_code(self, **kwargs):
        if self.expression:
            return f"({self.expression.py_code(**kwargs)})"

        if len(self.operation) < 1:
            return self.op[0].py_code(**kwargs)
        code = f"{self.op[0].py_code(**kwargs)}"
        for i, op in enumerate(self.op[1:]):
            code += f" {self.operation[i]} {op.py_code(**kwargs)}"
        return code

    
    def pddl_code(self, **kwargs):
        if self.expression:
            return f"({self.expression.pddl_code(**kwargs)})"

        if len(self.operation) < 1:
            return self.op[0].pddl_code(**kwargs)
        code = f"{self.op[0].pddl_code(**kwargs)}"
        for i, op in enumerate(self.op[1:]):
            code += f" {self.operation[i]} {op.pddl_code(**kwargs)}"
        return code


class Power:
    def __init__(self, **kwargs):
        self.op = kwargs.pop('op')
        self.factor = kwargs.pop('factor')

    def check_operator_types(self, **kwargs):
        pass

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        if self.factor:
            self.op.traverse(func_name, **kwargs)
        else:
            self.op.traverse(func_name, **kwargs)

    def build_name_references(self, referenced_names):
        if self.factor:
            self.op.build_name_references(referenced_names)
        else:
            self.op.build_name_references(referenced_names)

    def py_code(self, **kwargs):
        if self.factor:
            return f"{self.op.py_code(**kwargs)} ** {self.factor}"
        return self.op.py_code(**kwargs)

    
    def pddl_code(self, **kwargs):
        if self.factor:
            return f"{self.op.pddl_code(**kwargs)} ** {self.factor}"
        return self.op.pddl_code(**kwargs)


class Primary:
    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        if type(self.id) == list:
            self.id = ".".join(self.id)

        self.number = kwargs.pop('number')
        self.boolean = kwargs.pop('boolean')
        self.string = kwargs.pop('string')
        self.func = kwargs.pop('func')

    def check_operator_types(self, **kwargs):
        pass

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)
        
    def build_name_references(self, referenced_names):
        if self.id:
            referenced_names.add(self.id)

    def py_code(self, **kwargs):
        names = dict(kwargs['task_names'])
        names.update(dict(kwargs['step_names']))
        names.update({"self": self})

        if self.func:
            return self.func.py_code(**kwargs)
        
        if self.id:
            if not self.id in names and self.id not in BUILTINS_TYPE_MAPPING.keys():
                raise TextXSemanticError(
                    f"{self.id} is unknown in this context", **get_location(self))
            if "self." in self.id:
                return f"self.get('{'.'.join(self.id.split('.')[1:])}', <step_args>)"
            
            return self.id

        if self.number:
            return self.number

        if self.string:
            return f'"{self.string}"'

        return str(self.boolean).capitalize()

    
    def pddl_code(self, **kwargs):
        names = dict(kwargs['task_names'])
        names.update(dict(kwargs['step_names']))
        names.update({"self": self})

        if self.func:
            return self.func.pddl_code(**kwargs)
        
        if self.id:
            if not self.id in names and self.id not in BUILTINS_TYPE_MAPPING.keys():
                raise TextXSemanticError(
                    f"{self.id} is unknown in this context", **get_location(self))
            return self.id

        if self.number:
            return self.number

        if self.string:
            return f'"{self.string}"'

        return str(self.boolean).capitalize()

class BuiltinFunctionCall:
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.iterable = kwargs.pop('iterable')
        self.field = kwargs.pop('field')
        self.argumentSyncExpr = kwargs.pop('argumentSyncExpr')
        self.dateFunction = kwargs.pop('dateFunction')

    def check_operator_types(self, **kwargs):
        pass

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)

    def py_code(self, **kwargs):
        if self.iterable:
            field_names = {".".join(name.split(".")[1:]) : value for name, value in kwargs["task_names"].items()}
            field_names.update({".".join(name.split(".")[1:]) : value for name, value in kwargs["step_names"].items()})
            field = f", '{self.field.py_code(task_names={}, step_names=field_names)}'" if self.field else ""
            return f"aggregation('{self.name}', self.{self.iterable.py_code(**kwargs)}{field})"
        elif not self.name and self.argumentSyncExpr:
            return self.argumentSyncExpr.py_code(**kwargs)
        elif not self.name and self.dateFunction:
            return self.dateFunction.py_code(**kwargs)
        else:
            return self.name.capitalize()

    
    def pddl_code(self, **kwargs):
        if self.iterable:
            field_names = {".".join(name.split(".")[1:]) : value for name, value in kwargs["task_names"].items()}
            field_names.update({".".join(name.split(".")[1:]) : value for name, value in kwargs["step_names"].items()})
            field = f", '{self.field.py_code(task_names={}, step_names=field_names)}'" if self.field else ""
            return f"aggregation('{self.name}', self.{self.iterable.py_code(**kwargs)}{field})"
        elif not self.name and self.argumentSyncExpr:
            return self.argumentSyncExpr.py_code(**kwargs)
        elif not self.name and self.dateFunction:
            return self.dateFunction.py_code(**kwargs)
        else:
            return self.name.capitalize()

class DatFunctionCall:
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.arg = kwargs.pop('arg')
        self.functionName = kwargs.pop('functionName')


    def check_operator_types(self, **kwargs):
        pass

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)

    def py_code(self, **kwargs):
        return f"{self.name.capitalize()}.{self.functionName}({self.arg if self.arg else ''})"

    
    def pddl_code(self, **kwargs):
        return "tbd: DateFunctionCall"
    
class ArgumentSync:
    def __init__(self, **kwargs):
        self.task = kwargs.pop('task')
        self.wildcard = kwargs.pop('wildcard')
        self.taskArgs = kwargs.pop('arguments')
        self.stepWildcard = kwargs.pop('stepWildcard')
        self.stepArg = kwargs.pop('stepArg')

    def check_operator_types(self, **kwargs):
        pass

    def traverse(self, func_name, **kwargs):
        getattr(self, func_name)(**kwargs)

    def py_code(self, **kwargs):
        task_args = '"*"' if self.wildcard else ",".join([entity.name for entity in self.taskArgs])
        step_arg = '"*"' if self.stepWildcard else self.stepArg.name
        return f'PythonDataLayer.find_instance({self.task.name}Task, ({task_args},), {step_arg}, "{self.fieldName}", {self.expression.py_code(**kwargs)})'

    
    def pddl_code(self, **kwargs):
        return "task argument sync"