from wappl.language_builtins import *
from collections import defaultdict


class Grade(CustomType, Decimal):
    def __init__(self, value):
        Decimal.__init__(self)
        self.value = value

class Test(CustomType, Integer):
    def __init__(self, value):
        Integer.__init__(self, value)


class Entity:
    def __repr__(self):
        return self.__class__.__name__

# Block of forward declarations for all entities

class AssignmentEntity():
    pass

class HomeworkEntity():
    pass

class FooEntity():
    pass



class StudentEntity(User):
    def __init__(self, values={}):
        self.values = values
        for key, value in values.items():
            setattr(self, key, value)
        self.is_role_entity = True


# Block of forward declarations for all Tasks

class HomeworkSubmissionTaskTask():
    pass

class HomeworkGradingTask():
    pass


class PythonDataLayer:
    entity_mapping = {
            "Assignment": AssignmentEntity,
            "Homework": HomeworkEntity,
            "Foo": FooEntity,
    }

    task_mapping = {
            "HomeworkSubmissionTask": HomeworkSubmissionTaskTask,
            "HomeworkGrading": HomeworkGradingTask,
    }
    task_instances = {
            repr(HomeworkSubmissionTaskTask): {},
            repr(HomeworkGradingTask): {},
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
            repr(AssignmentEntity): [],
            repr(HomeworkEntity): [],
            repr(FooEntity): [],
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
    

class AssignmentEntity(Entity):
    meta_model = {
                "title": (Address, ""),
                "grade": (Grade, "nullable"),
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

class HomeworkEntity(Entity):
    meta_model = {
                "text": (Text, ""),
                "grade": (Grade, ""),
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

class FooEntity(Entity):
    meta_model = {
                "number": (Integer, ""),
                "text": (Text, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in FooEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(FooEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in FooEntity.meta_model.keys():
            try:
                value = FooEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in FooEntity.observers.keys():
                    for func in FooEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Foo"



class PreconditionNotMetException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

class MissingInputException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class InsufficientPermissionsException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)



class HomeworkSubmissionTaskTask():
    meta_model = {
        "inputs": {
            "task": {
                    "hw": HomeworkEntity,
            },
            "steps": {
                    "submitAnswer": {
                            "assignment": AssignmentEntity,
                    },
                    "submitAttachedFile": {
                            "assignment": AssignmentEntity,
                    },

            }
        },
        "additional_fields": {
                "submitAnswer": {
                        "answer": Text,
                },
                "submitAttachedFile": {
                        "attachedFile": Text,
                },
        },
    }

    def __init__(self, hw, user=User()):
        if not type(hw) == HomeworkSubmissionTaskTask.meta_model["inputs"]["task"]["hw"]:
            raise TypeError(hw)
        
        self.hw = hw

        self.fields = defaultdict(lambda: defaultdict(bool))
        self.computed = defaultdict(lambda: defaultdict(bool))

        self.final_steps = []
        self.final = False
        permissions = [
                    "",
        ]

        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        self.steps = [
                self.step_submitAnswer,
                self.step_submitAttachedFile,
        ]
        arguments_tuple = (hw,)
        if arguments_tuple in PythonDataLayer.task_instances[repr(HomeworkSubmissionTaskTask)].keys():
            raise Exception(f"There already is a Task of type HomeworkSubmissionTaskTask for arguments {arguments_tuple}")
        else: 
            PythonDataLayer.task_instances[repr(HomeworkSubmissionTaskTask)][arguments_tuple] = self

    def get(self, key, *args):
        a = tuple(arg for arg in args)
        if a in self.fields.keys() and key in self.fields[a].keys():
            return self.fields[a][key]
        return self.computed[a][key]
        
    
    def step_submitAnswer(self, assignment, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        hw = self.hw
        
        
        if not ((hw.text == "random_Text") and (4 + (1 <= 6) and 4 != 6)):
            raise PreconditionNotMetException('precondition \"(hw.text == "random_Text") and (4 + (1 <= 6) and 4 != 6)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in HomeworkSubmissionTaskTask.meta_model["additional_fields"]["submitAnswer"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(assignment,)][field_name].append(*field_values)
                else:
                    self.fields[(assignment,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(assignment,)][field_name] = field_value

        
        self.final = True
        self.final_steps.append("submitAnswer")
    
    
    def step_submitAttachedFile(self, assignment, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        hw = self.hw
        
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in HomeworkSubmissionTaskTask.meta_model["additional_fields"]["submitAttachedFile"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(assignment,)][field_name].append(*field_values)
                else:
                    self.fields[(assignment,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(assignment,)][field_name] = field_value

        
        self.final = True
        self.final_steps.append("submitAttachedFile")
    
    

class HomeworkGradingTask():
    meta_model = {
        "inputs": {
            "task": {
                    "hw": HomeworkEntity,
            },
            "steps": {
                    "gradeAssignment": {
                            "assignment": AssignmentEntity,
                    },
                    "gradeHomework": {
                    },

            }
        },
        "additional_fields": {
                "gradeAssignment": {
                        "grade": Grade,
                },
                "gradeHomework": {
                },
        },
    }

    def __init__(self, hw, user=User()):
        if not type(hw) == HomeworkGradingTask.meta_model["inputs"]["task"]["hw"]:
            raise TypeError(hw)
        
        self.hw = hw

        self.fields = defaultdict(lambda: defaultdict(bool))
        self.computed = defaultdict(lambda: defaultdict(bool))

        self.final_steps = []
        self.final = False
        if type(hw) == list:
            type(hw[0]).observers["assignments"].append(self.compute_totalGrade__gradeHomework)
        else:
            type(hw).observers["assignments"].append(self.compute_totalGrade__gradeHomework)
        if type(hw.assignments) == list:
            type(hw.assignments[0]).observers["grade"].append(self.compute_totalGrade__gradeHomework)
        else:
            type(hw.assignments).observers["grade"].append(self.compute_totalGrade__gradeHomework)
        permissions = [
                    "",
        ]

        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        self.steps = [
                self.step_gradeAssignment,
                self.step_gradeHomework,
        ]
        arguments_tuple = (hw,)
        if arguments_tuple in PythonDataLayer.task_instances[repr(HomeworkGradingTask)].keys():
            raise Exception(f"There already is a Task of type HomeworkGradingTask for arguments {arguments_tuple}")
        else: 
            PythonDataLayer.task_instances[repr(HomeworkGradingTask)][arguments_tuple] = self

    def get(self, key, *args):
        a = tuple(arg for arg in args)
        if a in self.fields.keys() and key in self.fields[a].keys():
            return self.fields[a][key]
        return self.computed[a][key]
        
    
    def step_gradeAssignment(self, assignment, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        hw = self.hw
        
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in HomeworkGradingTask.meta_model["additional_fields"]["gradeAssignment"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(assignment,)][field_name].append(*field_values)
                else:
                    self.fields[(assignment,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(assignment,)][field_name] = field_value

        
    
    
    def step_gradeHomework(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        hw = self.hw
        
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in HomeworkGradingTask.meta_model["additional_fields"]["gradeHomework"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[()][field_name].append(*field_values)
                else:
                    self.fields[()][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[()][field_name] = field_value

        
        self.compute_totalGrade__gradeHomework()
        
        self.final = True
        self.final_steps.append("gradeHomework")
    
    def compute_totalGrade__gradeHomework(self):
        hw = self.hw
        self.computed[()]["totalGrade"] = aggregation('sum', self.hw.assignments, 'grade')
    
    
