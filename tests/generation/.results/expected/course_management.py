from wappl.language_builtins import *
from collections import defaultdict


class Url(CustomType, String):
    def __init__(self, value):
        String.__init__(self, value)

class Grade(CustomType, Decimal):
    def __init__(self, value):
        Decimal.__init__(self)
        self.value = value

class Studentnumber(CustomType, String):
    def __init__(self, value):
        String.__init__(self, value)


class Entity:
    def __repr__(self):
        return self.__class__.__name__

# Block of forward declarations for all entities

class ModuleEntity():
    pass

class ModuleElementEntity():
    pass

class ExamEntity():
    pass

class HomeworkEntity():
    pass

class AssignmentEntity():
    pass

class BNFExecutionEntity():
    pass

class GroupEntity():
    pass

class GroupInvitationEntity():
    pass



class StudentEntity(User):
    def __init__(self, values={}):
        self.values = values
        self.is_role_entity = True

class TeachingAssistantEntity(User):
    def __init__(self, values={}):
        self.values = values
        self.is_role_entity = True


# Block of forward declarations for all Tasks

class HomeworkSubmissionTaskTask():
    pass

class ModuleElementCompletingTask():
    pass

class HomeworkGradingTask():
    pass


class PythonDataLayer:
    entity_mapping = {
            "Module": ModuleEntity,
            "ModuleElement": ModuleElementEntity,
            "Exam": ExamEntity,
            "Homework": HomeworkEntity,
            "Assignment": AssignmentEntity,
            "BNFExecution": BNFExecutionEntity,
            "Group": GroupEntity,
            "GroupInvitation": GroupInvitationEntity,
    }

    task_mapping = {
            "HomeworkSubmissionTask": HomeworkSubmissionTaskTask,
            "ModuleElementCompleting": ModuleElementCompletingTask,
            "HomeworkGrading": HomeworkGradingTask,
    }
    task_instances = {
            repr(HomeworkSubmissionTaskTask): {},
            repr(ModuleElementCompletingTask): {},
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
            repr(ModuleEntity): [],
            repr(ModuleElementEntity): [],
            repr(ExamEntity): [],
            repr(HomeworkEntity): [],
            repr(AssignmentEntity): [],
            repr(BNFExecutionEntity): [],
            repr(GroupEntity): [],
            repr(GroupInvitationEntity): [],
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
    

class ModuleEntity(Entity):
    meta_model = {
                "num": (Integer, ""),
                "title": (Text, ""),
                "elements": (ModuleElementEntity, "zeroOrMore"),
                "date": (Date, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in ModuleEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(ModuleEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in ModuleEntity.meta_model.keys():
            try:
                value = ModuleEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in ModuleEntity.observers.keys():
                    for func in ModuleEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Module"

class ModuleElementEntity(Entity):
    meta_model = {
                "title": (Text, ""),
                "additionalInfoUrls": (Url, "zeroOrMore"),
                "description": (Text, "nullable"),
                "homework": (HomeworkEntity, "nullable"),
                "exam": (ExamEntity, "nullable"),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in ModuleElementEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(ModuleElementEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in ModuleElementEntity.meta_model.keys():
            try:
                value = ModuleElementEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in ModuleElementEntity.observers.keys():
                    for func in ModuleElementEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"ModuleElement"

class ExamEntity(Entity):
    meta_model = {
                "num": (Integer, ""),
                "assignments": (AssignmentEntity, "zeroOrMore"),
                "start": (Datetime, ""),
                "deadline": (Datetime, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in ExamEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(ExamEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in ExamEntity.meta_model.keys():
            try:
                value = ExamEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in ExamEntity.observers.keys():
                    for func in ExamEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Exam"

class HomeworkEntity(Entity):
    meta_model = {
                "num": (Integer, ""),
                "title": (Text, ""),
                "assignments": (AssignmentEntity, "zeroOrMore"),
                "start": (Datetime, ""),
                "deadline": (Datetime, ""),
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
                "needsBnf": (Boolean, ""),
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

class BNFExecutionEntity(Entity):
    meta_model = {
                "code": (Text, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in BNFExecutionEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(BNFExecutionEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in BNFExecutionEntity.meta_model.keys():
            try:
                value = BNFExecutionEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in BNFExecutionEntity.observers.keys():
                    for func in BNFExecutionEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"BNFExecution"

class GroupEntity(Entity):
    meta_model = {
                "name": (Text, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in GroupEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(GroupEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in GroupEntity.meta_model.keys():
            try:
                value = GroupEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in GroupEntity.observers.keys():
                    for func in GroupEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Group"

class GroupInvitationEntity(Entity):
    meta_model = {
                "group": (GroupEntity, ""),
                "recipients": (StudentEntity, "zeroOrMore"),
                "mail": (Emailaddress, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in GroupInvitationEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(GroupInvitationEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in GroupInvitationEntity.meta_model.keys():
            try:
                value = GroupInvitationEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in GroupInvitationEntity.observers.keys():
                    for func in GroupInvitationEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"GroupInvitation"



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
                    "group": GroupEntity,
            },
            "steps": {
                    "submitTextAnswer": {
                            "assignment": AssignmentEntity,
                    },
                    "attachCodeFile": {
                            "assignment": AssignmentEntity,
                    },
                    "deadlineReached": {
                            "assignment": AssignmentEntity,
                    },

            }
        },
        "additional_fields": {
                "submitTextAnswer": {
                        "answer": Text,
                },
                "attachCodeFile": {
                        "attachedFile": File,
                },
                "deadlineReached": {
                },
        },
    }

    def __init__(self, hw, group, user=None):
        if not type(hw) == HomeworkSubmissionTaskTask.meta_model["inputs"]["task"]["hw"]:
            raise TypeError(hw)
        
        self.hw = hw
        if not type(group) == HomeworkSubmissionTaskTask.meta_model["inputs"]["task"]["group"]:
            raise TypeError(group)
        
        self.group = group

        self.fields = defaultdict(lambda: defaultdict(bool))
        self.computed = defaultdict(lambda: defaultdict(bool))

        self.user = User()
        self.final_steps = []
        self.final = False
        permissions = [
                    "",
        ]

        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

        self.steps = [
                self.step_submitTextAnswer,
                self.step_attachCodeFile,
                self.step_deadlineReached,
        ]
        arguments_tuple = (hw,group,)
        if arguments_tuple in PythonDataLayer.task_instances[repr(HomeworkSubmissionTaskTask)].keys():
            raise Exception(f"There already is a Task of type HomeworkSubmissionTaskTask for arguments {arguments_tuple}")
        else: 
            PythonDataLayer.task_instances[repr(HomeworkSubmissionTaskTask)][arguments_tuple] = self

    def get(self, key, *args):
        a = tuple(arg for arg in args)
        if a in self.fields.keys() and key in self.fields[a].keys():
            return self.fields[a][key]
        return self.computed[a][key]
        
    
    def step_submitTextAnswer(self, assignment, fields):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        hw = self.hw
        group = self.group
        
        
        if not ((hw.deadline >= Datetime.now()) and (hw.start <= Datetime.now())):
            raise PreconditionNotMetException('(hw.deadline >= Datetime.now()) and (hw.start <= Datetime.now())')
        
        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in HomeworkSubmissionTaskTask.meta_model["additional_fields"]["submitTextAnswer"].items():
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

        
    
    
    def step_attachCodeFile(self, assignment, fields):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        hw = self.hw
        group = self.group
        
        
        if not ((assignment.needsBnf == True) and (hw.deadline >= Datetime.now()) and (hw.start <= Datetime.now())):
            raise PreconditionNotMetException('(assignment.needsBnf == True) and (hw.deadline >= Datetime.now()) and (hw.start <= Datetime.now())')
        
        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in HomeworkSubmissionTaskTask.meta_model["additional_fields"]["attachCodeFile"].items():
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

        
    
    
    def step_deadlineReached(self, assignment, fields):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        hw = self.hw
        group = self.group
        
        
        if not ((hw.deadline < Datetime.now())):
            raise PreconditionNotMetException('(hw.deadline < Datetime.now())')
        
        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in HomeworkSubmissionTaskTask.meta_model["additional_fields"]["deadlineReached"].items():
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
        self.final_steps.append("deadlineReached")
    
    

class ModuleElementCompletingTask():
    meta_model = {
        "inputs": {
            "task": {
                    "element": ModuleElementEntity,
            },
            "steps": {
                    "checkModuleElement": {
                    },
                    "uncheckModuleElement": {
                    },
                    "classOver": {
                    },

            }
        },
        "additional_fields": {
                "checkModuleElement": {
                },
                "uncheckModuleElement": {
                },
                "classOver": {
                },
        },
    }

    def __init__(self, element, user=None):
        if not type(element) == ModuleElementCompletingTask.meta_model["inputs"]["task"]["element"]:
            raise TypeError(element)
        
        self.element = element

        self.fields = defaultdict(lambda: defaultdict(bool))
        self.computed = defaultdict(lambda: defaultdict(bool))

        self.user = User()
        self.final_steps = []
        self.final = False
        permissions = [
        ]

        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

        self.steps = [
                self.step_checkModuleElement,
                self.step_uncheckModuleElement,
                self.step_classOver,
        ]
        arguments_tuple = (element,)
        if arguments_tuple in PythonDataLayer.task_instances[repr(ModuleElementCompletingTask)].keys():
            raise Exception(f"There already is a Task of type ModuleElementCompletingTask for arguments {arguments_tuple}")
        else: 
            PythonDataLayer.task_instances[repr(ModuleElementCompletingTask)][arguments_tuple] = self

    def get(self, key, *args):
        a = tuple(arg for arg in args)
        if a in self.fields.keys() and key in self.fields[a].keys():
            return self.fields[a][key]
        return self.computed[a][key]
        
    
    def step_checkModuleElement(self,  fields):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        element = self.element
        
        
        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in ModuleElementCompletingTask.meta_model["additional_fields"]["checkModuleElement"].items():
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

        
        self.compute_done__checkModuleElement()
        
    
    def compute_done__checkModuleElement(self):
        element = self.element
        self.computed[()]["done"] = True
    
    
    def step_uncheckModuleElement(self,  fields):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        element = self.element
        
        
        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in ModuleElementCompletingTask.meta_model["additional_fields"]["uncheckModuleElement"].items():
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

        
        self.compute_done__uncheckModuleElement()
        
    
    def compute_done__uncheckModuleElement(self):
        element = self.element
        self.computed[()]["done"] = False
    
    
    def step_classOver(self,  fields):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        element = self.element
        
        
        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in ModuleElementCompletingTask.meta_model["additional_fields"]["classOver"].items():
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

        
        self.compute_done__classOver()
        
        self.final = True
        self.final_steps.append("classOver")
    
    def compute_done__classOver(self):
        element = self.element
        self.computed[()]["done"] = True
    
    

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

    def __init__(self, hw, user=None):
        if not type(hw) == HomeworkGradingTask.meta_model["inputs"]["task"]["hw"]:
            raise TypeError(hw)
        
        self.hw = hw

        self.fields = defaultdict(lambda: defaultdict(bool))
        self.computed = defaultdict(lambda: defaultdict(bool))

        self.user = User()
        self.final_steps = []
        self.final = False
        permissions = [
                    "",
        ]

        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

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
        
    
    def step_gradeAssignment(self, assignment, fields):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        hw = self.hw
        
        
        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

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

        
    
    
    def step_gradeHomework(self,  fields):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        hw = self.hw
        
        
        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

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
        self.computed[()]["totalGrade"] = 5
    
    
