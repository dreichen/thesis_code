from wappl.language_builtins import *
from collections import defaultdict


class Grade(CustomType, Decimal):
    def __init__(self, value):
        Decimal.__init__(self)
        self.value = value


class Entity:
    def __repr__(self):
        return self.__class__.__name__

# Block of forward declarations for all entities

class ThesisEntity():
    pass



class StudentEntity(User):
    def __init__(self, values={}):
        self.values = values
        for key, value in values.items():
            setattr(self, key, value)
        self.is_role_entity = True

class SupervisorEntity(User):
    def __init__(self, values={}):
        self.values = values
        for key, value in values.items():
            setattr(self, key, value)
        self.is_role_entity = True


# Block of forward declarations for all Tasks

class ThesisSubmissionTask():
    pass


class PythonDataLayer:
    entity_mapping = {
            "Thesis": ThesisEntity,
    }

    task_mapping = {
            "ThesisSubmission": ThesisSubmissionTask,
    }
    task_instances = {
            repr(ThesisSubmissionTask): {},
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
            repr(ThesisEntity): [],
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
    

class ThesisEntity(Entity):
    meta_model = {
                "title": (Text, ""),
                "thesisType": (Text, ""),
                "student": (StudentEntity, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in ThesisEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(ThesisEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in ThesisEntity.meta_model.keys():
            try:
                value = ThesisEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in ThesisEntity.observers.keys():
                    for func in ThesisEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Thesis"



class PreconditionNotMetException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

class MissingInputException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class InsufficientPermissionsException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)



class ThesisSubmissionTask():
    meta_model = {
        "inputs": {
            "task": {
                    "thesis": ThesisEntity,
            },
            "steps": {
                    "registration": {
                    },
                    "admitRegistration": {
                    },
                    "givePresentation": {
                    },
                    "submitThesis": {
                    },
                    "gradeThesis": {
                    },

            }
        },
        "additional_fields": {
                "registration": {
                },
                "admitRegistration": {
                },
                "givePresentation": {
                        "slideShow": File,
                },
                "submitThesis": {
                        "document": File,
                },
                "gradeThesis": {
                        "grade": Grade,
                },
        },
    }

    def __init__(self, thesis, user=User()):
        if not type(thesis) == ThesisSubmissionTask.meta_model["inputs"]["task"]["thesis"]:
            raise TypeError(thesis)
        
        self.thesis = thesis

        self.fields = defaultdict(lambda: defaultdict(bool))
        self.computed = defaultdict(lambda: defaultdict(bool))

        self.final_steps = []
        self.final = False
        permissions = [
        ]

        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        self.steps = [
                self.step_registration,
                self.step_admitRegistration,
                self.step_givePresentation,
                self.step_submitThesis,
                self.step_gradeThesis,
        ]
        arguments_tuple = (thesis,)
        if arguments_tuple in PythonDataLayer.task_instances[repr(ThesisSubmissionTask)].keys():
            raise Exception(f"There already is a Task of type ThesisSubmissionTask for arguments {arguments_tuple}")
        else: 
            PythonDataLayer.task_instances[repr(ThesisSubmissionTask)][arguments_tuple] = self

    def get(self, key, *args):
        a = tuple(arg for arg in args)
        if a in self.fields.keys() and key in self.fields[a].keys():
            return self.fields[a][key]
        return self.computed[a][key]
        
    
    def step_registration(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        thesis = self.thesis
        
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in ThesisSubmissionTask.meta_model["additional_fields"]["registration"].items():
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

        
        self.compute_submissionDate__registration()
        
        self.compute_registeredAt__registration()
        
    
    def compute_submissionDate__registration(self):
        thesis = self.thesis
        self.computed[()]["submissionDate"] = Datetime.now() + Datetime.days(182)
    
    def compute_registeredAt__registration(self):
        thesis = self.thesis
        self.computed[()]["registeredAt"] = Datetime.now()
    
    
    def step_admitRegistration(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
                    "AdmitRegistration",
        ]
        thesis = self.thesis
        
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in ThesisSubmissionTask.meta_model["additional_fields"]["admitRegistration"].items():
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

        
        self.compute_admitted__admitRegistration()
        
    
    def compute_admitted__admitRegistration(self):
        thesis = self.thesis
        self.computed[()]["admitted"] = True
    
    
    def step_givePresentation(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        thesis = self.thesis
        
        
        if not ((self.get('admitted', ))):
            raise PreconditionNotMetException('precondition \"(self.admitted)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in ThesisSubmissionTask.meta_model["additional_fields"]["givePresentation"].items():
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

        
        self.compute_presentationGiven__givePresentation()
        
    
    def compute_presentationGiven__givePresentation(self):
        thesis = self.thesis
        self.computed[()]["presentationGiven"] = True
    
    
    def step_submitThesis(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        thesis = self.thesis
        
        
        if not ((Datetime.now() < self.get('submissionDate', )) and (self.get('admitted', ))):
            raise PreconditionNotMetException('precondition \"(Datetime.now() < self.submissionDate) and (self.admitted)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in ThesisSubmissionTask.meta_model["additional_fields"]["submitThesis"].items():
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

        
        self.compute_submittedAt__submitThesis()
        
        self.compute_submitted__submitThesis()
        
    
    def compute_submittedAt__submitThesis(self):
        thesis = self.thesis
        self.computed[()]["submittedAt"] = Datetime.now()
    
    def compute_submitted__submitThesis(self):
        thesis = self.thesis
        self.computed[()]["submitted"] = True
    
    
    def step_gradeThesis(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
                    "GradeThesis",
        ]
        thesis = self.thesis
        
        
        if not ((self.get('submitted', )) and (self.get('presentationGiven', ))):
            raise PreconditionNotMetException('precondition \"(self.submitted) and (self.presentationGiven)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in ThesisSubmissionTask.meta_model["additional_fields"]["gradeThesis"].items():
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

        
        sendMail(self.thesis.student.mail, 'Hi, your thesis was graded and published to TUCaN!', 'Your thesis was graded!')
        self.final = True
        self.final_steps.append("gradeThesis")
    
    
