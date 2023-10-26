from wappl.language_builtins import *
from collections import defaultdict


class Dollar(CustomType, String):
    def __init__(self, value):
        String.__init__(self, value)

class Grade(CustomType, Decimal):
    def __init__(self, value):
        Decimal.__init__(self)
        self.value = value


class Entity:
    def __repr__(self):
        return self.__class__.__name__

# Block of forward declarations for all entities

class HomeworkEntity():
    pass

class AssignmentEntity():
    pass




# Block of forward declarations for all Tasks


class PythonDataLayer:
    entity_mapping = {
            "Homework": HomeworkEntity,
            "Assignment": AssignmentEntity,
    }

    task_mapping = {
    }
    task_instances = {
    }

    @staticmethod
    def find_instance(task, taskArgs, stepArgs, key, value):
        for _, instance in PythonDataLayer.task_instances[repr(task)].items():
            if not "*" in taskArgs and not _ == taskArgs and not _ in taskArgs:
                continue
            for k, field in instance.fields.items():
                if (stepArgs == k or stepArgs in k) and key in field.keys():
                    if field[key] == value:
                        return True
                    else:
                        return False
            for k, field in instance.computed.items():
                if stepArgs == '*' and key in field.keys():
                    if field[key] == value:
                        return True
                    else:
                        return False
                elif (stepArgs == k or stepArgs in k) and key in field.keys():
                    if field[key] == value:
                        return True
                    else:
                        return False
        return False

    instances = {
            repr(HomeworkEntity): [],
            repr(AssignmentEntity): [],
    }

    def get_state(self):
        state = {
            "entities": {
                key: PythonDataLayer.instances[value] for key, value in PythonDataLayer.entity_mapping.items()
            },
            "tasks": {
                key:  PythonDataLayer.instances[value] for key, value in PythonDataLayer.task_mapping.items()
            }
        }
        return state

    def create_entity(self, entity, values):
        return entity(values)
    
    def create_task(self, task, values):
        return task(values)
    

class HomeworkEntity(Entity):
    meta_model = {
                "title": (Text, ""),
                "totalGrade": (Grade, "nullable"),
                "assignments": (AssignmentEntity, "zeroOrMore"),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in HomeworkEntity.meta_model.items():
            type_, flags = type_flags_tuple
            if "zeroOrMore" in flags:
                try:
                    value = values[name]
                except Exception as e:
                    value = [] # default -> empty list
                if hasattr(value, "is_entity"): # is entity
                    for v in value:
                        if v not in PythonDataLayer.instances[repr(type_)]:
                            raise Exception
                setattr(self, name, value)

            elif "nullable" in flags:
                try:
                    if name in values: # value provided
                        value = values[name]
                        if hasattr(value, "is_entity"): # is entity
                            if value not in PythonDataLayer.instances[repr(type_)]: # value provided -> check that exists
                                raise Exception
                            setattr(self, name, value)
                        else:
                            value = type_(values[name])
                            setattr(self, name, value)
                    else: # no value provided
                        setattr(self, name, None)
                except KeyError as ke:
                    setattr(self, name, None)

            elif hasattr(values[name], "is_entity"):
                value = values[name]
                if value not in PythonDataLayer.instances[repr(type_)]:
                    raise Exception
                else:
                    setattr(self, name, value)
                    
            elif hasattr(values[name], "is_role_entity"):
                setattr(self, name, values[name])

            else:
                value = type_(values[name])
                setattr(self, name, value)

        PythonDataLayer.instances[repr(HomeworkEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in HomeworkEntity.meta_model.keys():
            try:
                value = HomeworkEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in HomeworkEntity.observers.keys():
                    for func in HomeworkEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Homework"

class AssignmentEntity(Entity):
    meta_model = {
                "num": (Integer, ""),
                "title": (Text, ""),
                "question": (Text, ""),
                "homework": (HomeworkEntity, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in AssignmentEntity.meta_model.items():
            type_, flags = type_flags_tuple
            if "zeroOrMore" in flags:
                try:
                    value = values[name]
                except Exception as e:
                    value = [] # default -> empty list
                if hasattr(value, "is_entity"): # is entity
                    for v in value:
                        if v not in PythonDataLayer.instances[repr(type_)]:
                            raise Exception
                setattr(self, name, value)

            elif "nullable" in flags:
                try:
                    if name in values: # value provided
                        value = values[name]
                        if hasattr(value, "is_entity"): # is entity
                            if value not in PythonDataLayer.instances[repr(type_)]: # value provided -> check that exists
                                raise Exception
                            setattr(self, name, value)
                        else:
                            value = type_(values[name])
                            setattr(self, name, value)
                    else: # no value provided
                        setattr(self, name, None)
                except KeyError as ke:
                    setattr(self, name, None)

            elif hasattr(values[name], "is_entity"):
                value = values[name]
                if value not in PythonDataLayer.instances[repr(type_)]:
                    raise Exception
                else:
                    setattr(self, name, value)
                    
            elif hasattr(values[name], "is_role_entity"):
                setattr(self, name, values[name])

            else:
                value = type_(values[name])
                setattr(self, name, value)

        PythonDataLayer.instances[repr(AssignmentEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in AssignmentEntity.meta_model.keys():
            try:
                value = AssignmentEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in AssignmentEntity.observers.keys():
                    for func in AssignmentEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Assignment"



class PreconditionNotMetException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

class MissingInputException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class InsufficientPermissionsException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


