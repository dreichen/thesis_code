from wappl.language_builtins import *
from collections import defaultdict


class Age(CustomType, Integer):
    def __init__(self, value):
        Integer.__init__(self, value)


class Entity:
    def __repr__(self):
        return self.__class__.__name__

# Block of forward declarations for all entities

class PersonEntity():
    pass

class MarriageEntity():
    pass

class HouseEntity():
    pass



class CoreUserEntity(User):
    def __init__(self, values={}):
        self.values = values
        for key, value in values.items():
            setattr(self, key, value)
        self.is_role_entity = True


# Block of forward declarations for all Tasks

class MarryingTask():
    pass


class PythonDataLayer:
    entity_mapping = {
            "Person": PersonEntity,
            "Marriage": MarriageEntity,
            "House": HouseEntity,
    }

    task_mapping = {
            "Marrying": MarryingTask,
    }
    task_instances = {
            repr(MarryingTask): {},
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
            repr(PersonEntity): [],
            repr(MarriageEntity): [],
            repr(HouseEntity): [],
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
    

class PersonEntity(Entity):
    meta_model = {
                "name": (Text, ""),
                "age": (Age, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in PersonEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(PersonEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in PersonEntity.meta_model.keys():
            try:
                value = PersonEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in PersonEntity.observers.keys():
                    for func in PersonEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Person"

class MarriageEntity(Entity):
    meta_model = {
                "partnerA": (PersonEntity, ""),
                "partnerB": (PersonEntity, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in MarriageEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(MarriageEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in MarriageEntity.meta_model.keys():
            try:
                value = MarriageEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in MarriageEntity.observers.keys():
                    for func in MarriageEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Marriage"

class HouseEntity(Entity):
    meta_model = {
                "address": (Address, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in HouseEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(HouseEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in HouseEntity.meta_model.keys():
            try:
                value = HouseEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in HouseEntity.observers.keys():
                    for func in HouseEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"House"



class PreconditionNotMetException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

class MissingInputException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class InsufficientPermissionsException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)



class MarryingTask():
    meta_model = {
        "inputs": {
            "task": {
                    "a": PersonEntity,
            },
            "steps": {
                    "proposeTo": {
                            "b": PersonEntity,
                    },
                    "marry": {
                            "b": PersonEntity,
                    },
                    "buildHouse": {
                            "m": MarriageEntity,
                    },
                    "otherStep": {
                            "m": MarriageEntity,
                    },
                    "becomeParents": {
                            "m": MarriageEntity,
                    },

            }
        },
        "additional_fields": {
                "proposeTo": {
                        "proposed": Integer,
                },
                "marry": {
                        "marriage": MarriageEntity,
                },
                "buildHouse": {
                        "house": HouseEntity,
                },
                "otherStep": {
                        "other": PersonEntity,
                },
                "becomeParents": {
                        "child": PersonEntity,
                },
        },
    }

    def __init__(self, a, user=User()):
        if not type(a) == MarryingTask.meta_model["inputs"]["task"]["a"]:
            raise TypeError(a)
        
        self.a = a

        self.fields = defaultdict(lambda: defaultdict(bool))
        self.computed = defaultdict(lambda: defaultdict(bool))

        self.final_steps = []
        self.final = False
        permissions = [
        ]

        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        self.steps = [
                self.step_proposeTo,
                self.step_marry,
                self.step_buildHouse,
                self.step_otherStep,
                self.step_becomeParents,
        ]
        arguments_tuple = (a,)
        if arguments_tuple in PythonDataLayer.task_instances[repr(MarryingTask)].keys():
            raise Exception(f"There already is a Task of type MarryingTask for arguments {arguments_tuple}")
        else: 
            PythonDataLayer.task_instances[repr(MarryingTask)][arguments_tuple] = self

    def get(self, key, *args):
        a = tuple(arg for arg in args)
        if a in self.fields.keys() and key in self.fields[a].keys():
            return self.fields[a][key]
        return self.computed[a][key]
        
    
    def step_proposeTo(self, b, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
                    "A",
        ]
        a = self.a
        
        
        if not ((a.age >= 18) and (b.age >= 18)):
            raise PreconditionNotMetException('precondition \"(a.age >= 18) and (b.age >= 18)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in MarryingTask.meta_model["additional_fields"]["proposeTo"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(b,)][field_name].append(*field_values)
                else:
                    self.fields[(b,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(b,)][field_name] = field_value

        
    
    
    def step_marry(self, b, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        a = self.a
        
        
        if not ((self.get('proposed', b) == 2)):
            raise PreconditionNotMetException('precondition \"(self.proposed == 2)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in MarryingTask.meta_model["additional_fields"]["marry"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(b,)][field_name].append(*field_values)
                else:
                    self.fields[(b,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(b,)][field_name] = field_value

        
    
    
    def step_buildHouse(self, m, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        a = self.a
        
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in MarryingTask.meta_model["additional_fields"]["buildHouse"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(m,)][field_name].append(*field_values)
                else:
                    self.fields[(m,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(m,)][field_name] = field_value

        
    
    
    def step_otherStep(self, m, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        a = self.a
        
        
        if not ((self.get('house', m))):
            raise PreconditionNotMetException('precondition \"(self.house)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in MarryingTask.meta_model["additional_fields"]["otherStep"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(m,)][field_name].append(*field_values)
                else:
                    self.fields[(m,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(m,)][field_name] = field_value

        
    
    
    def step_becomeParents(self, m, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        a = self.a
        
        
        if not ((self.get('house', m))):
            raise PreconditionNotMetException('precondition \"(self.house)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in MarryingTask.meta_model["additional_fields"]["becomeParents"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(m,)][field_name].append(*field_values)
                else:
                    self.fields[(m,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(m,)][field_name] = field_value

        
        self.final = True
        self.final_steps.append("becomeParents")
    
    
