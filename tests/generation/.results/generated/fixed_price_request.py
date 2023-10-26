from wappl.language_builtins import *
from collections import defaultdict


class Money(CustomType, Decimal):
    def __init__(self, value):
        Decimal.__init__(self)
        self.value = value


class Entity:
    def __repr__(self):
        return self.__class__.__name__

# Block of forward declarations for all entities

class SupplierResponseEntity():
    pass

class FixedPriceRequestEntity():
    pass



class RequesterEntity(User):
    def __init__(self, values={}):
        self.values = values
        for key, value in values.items():
            setattr(self, key, value)
        self.is_role_entity = True

class BuyerEntity(User):
    def __init__(self, values={}):
        self.values = values
        for key, value in values.items():
            setattr(self, key, value)
        self.is_role_entity = True

class SupplierEntity(User):
    def __init__(self, values={}):
        self.values = values
        for key, value in values.items():
            setattr(self, key, value)
        self.is_role_entity = True

class ReviewerEntity(User):
    def __init__(self, values={}):
        self.values = values
        for key, value in values.items():
            setattr(self, key, value)
        self.is_role_entity = True


# Block of forward declarations for all Tasks

class FixedPriceRequestTaskTask():
    pass


class PythonDataLayer:
    entity_mapping = {
            "SupplierResponse": SupplierResponseEntity,
            "FixedPriceRequest": FixedPriceRequestEntity,
    }

    task_mapping = {
            "FixedPriceRequestTask": FixedPriceRequestTaskTask,
    }
    task_instances = {
            repr(FixedPriceRequestTaskTask): {},
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
            repr(SupplierResponseEntity): [],
            repr(FixedPriceRequestEntity): [],
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
    

class SupplierResponseEntity(Entity):
    meta_model = {
                "supplier": (SupplierEntity, ""),
                "bidAmount": (Money, "nullable"),
                "declined": (Boolean, "nullable"),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in SupplierResponseEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(SupplierResponseEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in SupplierResponseEntity.meta_model.keys():
            try:
                value = SupplierResponseEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in SupplierResponseEntity.observers.keys():
                    for func in SupplierResponseEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"SupplierResponse"

class FixedPriceRequestEntity(Entity):
    meta_model = {
                "information": (Text, ""),
                "deadline": (Datetime, ""),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in FixedPriceRequestEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(FixedPriceRequestEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in FixedPriceRequestEntity.meta_model.keys():
            try:
                value = FixedPriceRequestEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in FixedPriceRequestEntity.observers.keys():
                    for func in FixedPriceRequestEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"FixedPriceRequest"



class PreconditionNotMetException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

class MissingInputException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class InsufficientPermissionsException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)



class FixedPriceRequestTaskTask():
    meta_model = {
        "inputs": {
            "task": {
                    "request": FixedPriceRequestEntity,
            },
            "steps": {
                    "init": {
                    },
                    "edit": {
                    },
                    "submitToBuyer": {
                    },
                    "modifyByBuyer": {
                    },
                    "approve": {
                    },
                    "submitResponse": {
                    },
                    "evaluateWinner": {
                    },

            }
        },
        "additional_fields": {
                "init": {
                },
                "edit": {
                },
                "submitToBuyer": {
                },
                "modifyByBuyer": {
                        "legalDocument": File,
                        "financialApproval": Boolean,
                },
                "approve": {
                },
                "submitResponse": {
                        "supplierResponses": SupplierResponseEntity,
                },
                "evaluateWinner": {
                },
        },
    }

    def __init__(self, request, user=User()):
        if not type(request) == FixedPriceRequestTaskTask.meta_model["inputs"]["task"]["request"]:
            raise TypeError(request)
        
        self.request = request

        self.fields = defaultdict(lambda: defaultdict(bool))
        self.computed = defaultdict(lambda: defaultdict(bool))

        self.final_steps = []
        self.final = False
        permissions = [
        ]

        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        self.steps = [
                self.step_init,
                self.step_edit,
                self.step_submitToBuyer,
                self.step_modifyByBuyer,
                self.step_approve,
                self.step_submitResponse,
                self.step_evaluateWinner,
        ]
        arguments_tuple = (request,)
        if arguments_tuple in PythonDataLayer.task_instances[repr(FixedPriceRequestTaskTask)].keys():
            raise Exception(f"There already is a Task of type FixedPriceRequestTaskTask for arguments {arguments_tuple}")
        else: 
            PythonDataLayer.task_instances[repr(FixedPriceRequestTaskTask)][arguments_tuple] = self

    def get(self, key, *args):
        a = tuple(arg for arg in args)
        if a in self.fields.keys() and key in self.fields[a].keys():
            return self.fields[a][key]
        return self.computed[a][key]
        
    
    def step_init(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
                    "SubmitRequest",
        ]
        request = self.request
        
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in FixedPriceRequestTaskTask.meta_model["additional_fields"]["init"].items():
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

        
        self.compute_initialized__init()
        
    
    def compute_initialized__init(self):
        request = self.request
        self.computed[()]["initialized"] = True
    
    
    def step_edit(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
                    "EditRequest",
        ]
        request = self.request
        
        
        if not ((self.get('initialized', ) == True)):
            raise PreconditionNotMetException('precondition \"(self.initialized == True)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in FixedPriceRequestTaskTask.meta_model["additional_fields"]["edit"].items():
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

        
        self.compute_edited__edit()
        
    
    def compute_edited__edit(self):
        request = self.request
        self.computed[()]["edited"] = True
    
    
    def step_submitToBuyer(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
                    "SubmitRequest",
        ]
        request = self.request
        
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in FixedPriceRequestTaskTask.meta_model["additional_fields"]["submitToBuyer"].items():
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

        
        self.compute_submitted__submitToBuyer()
        
    
    def compute_submitted__submitToBuyer(self):
        request = self.request
        self.computed[()]["submitted"] = True
    
    
    def step_modifyByBuyer(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
                    "Buy",
        ]
        request = self.request
        
        
        if not ((self.get('submitted', ) == True)):
            raise PreconditionNotMetException('precondition \"(self.submitted == True)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in FixedPriceRequestTaskTask.meta_model["additional_fields"]["modifyByBuyer"].items():
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

        
    
    
    def step_approve(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
                    "Buy",
        ]
        request = self.request
        
        
        if not ((self.get('financialApproval', ) == True)):
            raise PreconditionNotMetException('precondition \"(self.financialApproval == True)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in FixedPriceRequestTaskTask.meta_model["additional_fields"]["approve"].items():
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

        
        self.compute_approved__approve()
        
    
    def compute_approved__approve(self):
        request = self.request
        self.computed[()]["approved"] = True
    
    
    def step_submitResponse(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
                    "Bid",
        ]
        request = self.request
        
        
        if not ((self.get('approved', ) == True)):
            raise PreconditionNotMetException('precondition \"(self.approved == True)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in FixedPriceRequestTaskTask.meta_model["additional_fields"]["submitResponse"].items():
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

        
    
    
    def step_evaluateWinner(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        request = self.request
        
        
        if not ((request.deadline < Datetime.now())):
            raise PreconditionNotMetException('precondition \"(request.deadline < Datetime.now())\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in FixedPriceRequestTaskTask.meta_model["additional_fields"]["evaluateWinner"].items():
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

        
        self.compute_winner__evaluateWinner()
        
        sendMail(self.get('winner').supplier.mail, 'You have won!')
        self.final = True
        self.final_steps.append("evaluateWinner")
    
    def compute_winner__evaluateWinner(self):
        request = self.request
        self.computed[()]["winner"] = aggregation('minEntity', self.get('supplierResponses', ), 'bidAmount')
    
    
