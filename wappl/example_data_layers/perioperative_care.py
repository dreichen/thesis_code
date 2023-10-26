from wappl.language_builtins import *
from collections import defaultdict



class Entity:
    def __repr__(self):
        return self.__class__.__name__

# Block of forward declarations for all entities

class CTScanningDeviceEntity():
    pass

class NurseEntity():
    pass

class ChargeNurseEntity():
    pass

class PatientEntity():
    pass

class SurgeonEntity():
    pass




# Block of forward declarations for all Tasks

class PerioperativeProcessTask():
    pass


class PythonDataLayer:
    entity_mapping = {
            "CTScanningDevice": CTScanningDeviceEntity,
            "Nurse": NurseEntity,
            "ChargeNurse": ChargeNurseEntity,
            "Patient": PatientEntity,
            "Surgeon": SurgeonEntity,
    }

    task_mapping = {
            "PerioperativeProcess": PerioperativeProcessTask,
    }
    task_instances = {
            repr(PerioperativeProcessTask): {},
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
            repr(CTScanningDeviceEntity): [],
            repr(NurseEntity): [],
            repr(ChargeNurseEntity): [],
            repr(PatientEntity): [],
            repr(SurgeonEntity): [],
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
    

class CTScanningDeviceEntity(Entity):
    meta_model = {
                "identifier": (String, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in CTScanningDeviceEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(CTScanningDeviceEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in CTScanningDeviceEntity.meta_model.keys():
            try:
                value = CTScanningDeviceEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in CTScanningDeviceEntity.observers.keys():
                    for func in CTScanningDeviceEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"CTScanningDevice"

class NurseEntity(Entity):
    meta_model = {
                "name": (Text, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in NurseEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(NurseEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in NurseEntity.meta_model.keys():
            try:
                value = NurseEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in NurseEntity.observers.keys():
                    for func in NurseEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Nurse"

class ChargeNurseEntity(Entity):
    meta_model = {
                "name": (Text, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in ChargeNurseEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(ChargeNurseEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in ChargeNurseEntity.meta_model.keys():
            try:
                value = ChargeNurseEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in ChargeNurseEntity.observers.keys():
                    for func in ChargeNurseEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"ChargeNurse"

class PatientEntity(Entity):
    meta_model = {
                "name": (Text, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in PatientEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(PatientEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in PatientEntity.meta_model.keys():
            try:
                value = PatientEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in PatientEntity.observers.keys():
                    for func in PatientEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Patient"

class SurgeonEntity(Entity):
    meta_model = {
                "name": (Text, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in SurgeonEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(SurgeonEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in SurgeonEntity.meta_model.keys():
            try:
                value = SurgeonEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in SurgeonEntity.observers.keys():
                    for func in SurgeonEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Surgeon"



class PreconditionNotMetException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

class MissingInputException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class InsufficientPermissionsException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)



class PerioperativeProcessTask():
    meta_model = {
        "inputs": {
            "task": {
                    "p": PatientEntity,
            },
            "steps": {
                    "admitAtWardStart": {
                            "n": NurseEntity,
                    },
                    "admitAtWardEnd": {
                            "n": NurseEntity,
                    },
                    "doDiagnosticTestsStart": {
                            "n": NurseEntity,
                            "ct": CTScanningDeviceEntity,
                    },
                    "doDiagnosticTestsEnd": {
                            "n": NurseEntity,
                            "ct": CTScanningDeviceEntity,
                    },
                    "registerProcedure": {
                            "cn": ChargeNurseEntity,
                    },
                    "startSurgery": {
                            "s": SurgeonEntity,
                            "n": NurseEntity,
                            "nn": NurseEntity,
                    },
                    "endSurgery": {
                            "s": SurgeonEntity,
                            "n": NurseEntity,
                            "nn": NurseEntity,
                    },

            }
        },
        "additional_fields": {
                "admitAtWardStart": {
                },
                "admitAtWardEnd": {
                },
                "doDiagnosticTestsStart": {
                },
                "doDiagnosticTestsEnd": {
                },
                "registerProcedure": {
                },
                "startSurgery": {
                },
                "endSurgery": {
                },
        },
    }

    def __init__(self, p, user=User()):
        if not type(p) == PerioperativeProcessTask.meta_model["inputs"]["task"]["p"]:
            raise TypeError(p)
        
        self.p = p

        self.fields = defaultdict(lambda: defaultdict(bool))
        self.computed = defaultdict(lambda: defaultdict(bool))

        self.final_steps = []
        self.final = False
        permissions = [
        ]

        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        self.steps = [
                self.step_admitAtWardStart,
                self.step_admitAtWardEnd,
                self.step_doDiagnosticTestsStart,
                self.step_doDiagnosticTestsEnd,
                self.step_registerProcedure,
                self.step_startSurgery,
                self.step_endSurgery,
        ]
        arguments_tuple = (p,)
        if arguments_tuple in PythonDataLayer.task_instances[repr(PerioperativeProcessTask)].keys():
            raise Exception(f"There already is a Task of type PerioperativeProcessTask for arguments {arguments_tuple}")
        else: 
            PythonDataLayer.task_instances[repr(PerioperativeProcessTask)][arguments_tuple] = self

    def get(self, key, *args):
        a = tuple(arg for arg in args)
        if a in self.fields.keys() and key in self.fields[a].keys():
            return self.fields[a][key]
        return self.computed[a][key]
        
    
    def step_admitAtWardStart(self, n, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        p = self.p
        
        
        if not ((PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), n, "available", False) == False)):
            raise PreconditionNotMetException('precondition \"(PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), n, "available", False) == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in PerioperativeProcessTask.meta_model["additional_fields"]["admitAtWardStart"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(n,)][field_name].append(*field_values)
                else:
                    self.fields[(n,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(n,)][field_name] = field_value

        
        self.compute_available__admitAtWardStart(n,)
        
        self.compute_admitWardEndTime__admitAtWardStart(n,)
        
    
    def compute_available__admitAtWardStart(self, n):
        p = self.p
        self.computed[(n,)]["available"] = False
    
    def compute_admitWardEndTime__admitAtWardStart(self, n):
        p = self.p
        self.computed[(n,)]["admitWardEndTime"] = Datetime.now() + Datetime.seconds(1)
    
    
    def step_admitAtWardEnd(self, n, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        p = self.p
        
        
        if not ((self.get('available', n) == False) and (self.get('admitWardEndTime', n) <= Datetime.now())):
            raise PreconditionNotMetException('precondition \"(self.available == False) and (self.admitWardEndTime <= Datetime.now())\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in PerioperativeProcessTask.meta_model["additional_fields"]["admitAtWardEnd"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(n,)][field_name].append(*field_values)
                else:
                    self.fields[(n,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(n,)][field_name] = field_value

        
        self.compute_available__admitAtWardEnd(n,)
        
        self.compute_admittedAtWard__admitAtWardEnd(n,)
        
    
    def compute_available__admitAtWardEnd(self, n):
        p = self.p
        self.computed[(n,)]["available"] = True
    
    def compute_admittedAtWard__admitAtWardEnd(self, n):
        p = self.p
        self.computed[(n,)]["admittedAtWard"] = True
    
    
    def step_doDiagnosticTestsStart(self, n,ct, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        p = self.p
        
        
        if not ((PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), n, "available", False) == False) and (PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), ct, "available", False) == False)):
            raise PreconditionNotMetException('precondition \"(PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), n, "available", False) == False) and (PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), ct, "available", False) == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in PerioperativeProcessTask.meta_model["additional_fields"]["doDiagnosticTestsStart"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(n,ct,)][field_name].append(*field_values)
                else:
                    self.fields[(n,ct,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(n,ct,)][field_name] = field_value

        
        self.compute_available__doDiagnosticTestsStart(n,ct,)
        
        self.compute_doDiagnosticTestsEnd__doDiagnosticTestsStart(n,ct,)
        
    
    def compute_available__doDiagnosticTestsStart(self, n, ct):
        p = self.p
        self.computed[(n,ct,)]["available"] = False
    
    def compute_doDiagnosticTestsEnd__doDiagnosticTestsStart(self, n, ct):
        p = self.p
        self.computed[(n,ct,)]["doDiagnosticTestsEnd"] = Datetime.now() + Datetime.seconds(1)
    
    
    def step_doDiagnosticTestsEnd(self, n,ct, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        p = self.p
        
        
        if not ((PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), n, "admittedAtWard", True) == True) and (self.get('available', n,ct) == False)):
            raise PreconditionNotMetException('precondition \"(PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), n, "admittedAtWard", True) == True) and (self.available == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in PerioperativeProcessTask.meta_model["additional_fields"]["doDiagnosticTestsEnd"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(n,ct,)][field_name].append(*field_values)
                else:
                    self.fields[(n,ct,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(n,ct,)][field_name] = field_value

        
        self.compute_available__doDiagnosticTestsEnd(n,ct,)
        
        self.compute_diagnosticsDone__doDiagnosticTestsEnd(n,ct,)
        
    
    def compute_available__doDiagnosticTestsEnd(self, n, ct):
        p = self.p
        self.computed[(n,ct,)]["available"] = True
    
    def compute_diagnosticsDone__doDiagnosticTestsEnd(self, n, ct):
        p = self.p
        self.computed[(n,ct,)]["diagnosticsDone"] = True
    
    
    def step_registerProcedure(self, cn, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        p = self.p
        
        
        if not ((PythonDataLayer.find_instance(PerioperativeProcessTask, (p,), "*", "diagnosticsDone", True) == True) and (PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), cn, "available", False) == False)):
            raise PreconditionNotMetException('precondition \"(PythonDataLayer.find_instance(PerioperativeProcessTask, (p,), "*", "diagnosticsDone", True) == True) and (PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), cn, "available", False) == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in PerioperativeProcessTask.meta_model["additional_fields"]["registerProcedure"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(cn,)][field_name].append(*field_values)
                else:
                    self.fields[(cn,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(cn,)][field_name] = field_value

        
        self.compute_procedureRegistered__registerProcedure(cn,)
        
    
    def compute_procedureRegistered__registerProcedure(self, cn):
        p = self.p
        self.computed[(cn,)]["procedureRegistered"] = True
    
    
    def step_startSurgery(self, s,n,nn, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        p = self.p
        
        
        if not ((PythonDataLayer.find_instance(PerioperativeProcessTask, (p,), "*", "procedureRegistered", True) == True) and (PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), s, "available", False) == False) and (PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), n, "available", False) == False) and (PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), nn, "available", False) == False)):
            raise PreconditionNotMetException('precondition \"(PythonDataLayer.find_instance(PerioperativeProcessTask, (p,), "*", "procedureRegistered", True) == True) and (PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), s, "available", False) == False) and (PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), n, "available", False) == False) and (PythonDataLayer.find_instance(PerioperativeProcessTask, ("*",), nn, "available", False) == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in PerioperativeProcessTask.meta_model["additional_fields"]["startSurgery"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(s,n,nn,)][field_name].append(*field_values)
                else:
                    self.fields[(s,n,nn,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(s,n,nn,)][field_name] = field_value

        
        self.compute_surgeryActive__startSurgery(s,n,nn,)
        
        self.compute_available__startSurgery(s,n,nn,)
        
        self.compute_surgeryEnd__startSurgery(s,n,nn,)
        
    
    def compute_surgeryActive__startSurgery(self, s, n, nn):
        p = self.p
        self.computed[(s,n,nn,)]["surgeryActive"] = True
    
    def compute_available__startSurgery(self, s, n, nn):
        p = self.p
        self.computed[(s,n,nn,)]["available"] = False
    
    def compute_surgeryEnd__startSurgery(self, s, n, nn):
        p = self.p
        self.computed[(s,n,nn,)]["surgeryEnd"] = Datetime.now() + Datetime.seconds(2)
    
    
    def step_endSurgery(self, s,n,nn, fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        p = self.p
        
        
        if not ((self.get('surgeryActive', s,n,nn)) and (self.get('surgeryEnd', s,n,nn) <= Datetime.now())):
            raise PreconditionNotMetException('precondition \"(self.surgeryActive) and (self.surgeryEnd <= Datetime.now())\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in PerioperativeProcessTask.meta_model["additional_fields"]["endSurgery"].items():
            if type(fields[field_name]) == list:
                try:
                    field_values = list(map(lambda x : x, fields[field_name]))
                except KeyError as e:
                    raise Exception(f"You have to specify {field_name} of type list({field_type})")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type list({field_type})")
                if field_name in self.fields[()].keys():
                    self.fields[(s,n,nn,)][field_name].append(*field_values)
                else:
                    self.fields[(s,n,nn,)][field_name] = field_values
            else:
                try:
                    field_value = field_type(fields[field_name])
                except KeyError as e:
                    raise Exception(f"You have to specify field {field_name} of type {field_type}")
                except Exception as e:
                    raise Exception(f"field type {type(fields[field_name])} does not match the required type {field_type}")
                self.fields[(s,n,nn,)][field_name] = field_value

        
        self.compute_surgeryActive__endSurgery(s,n,nn,)
        
        self.compute_available__endSurgery(s,n,nn,)
        
        self.final = True
        self.final_steps.append("endSurgery")
    
    def compute_surgeryActive__endSurgery(self, s, n, nn):
        p = self.p
        self.computed[(s,n,nn,)]["surgeryActive"] = False
    
    def compute_available__endSurgery(self, s, n, nn):
        p = self.p
        self.computed[(s,n,nn,)]["available"] = True
    
    
