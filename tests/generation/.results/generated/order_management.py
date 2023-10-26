from wappl.language_builtins import *
from collections import defaultdict


class Phonenumber(CustomType, String):
    def __init__(self, value):
        String.__init__(self, value)

class Year(CustomType, Integer):
    def __init__(self, value):
        Integer.__init__(self, value)

class Money(CustomType, Decimal):
    def __init__(self, value):
        Decimal.__init__(self)
        self.value = value


class Entity:
    def __repr__(self):
        return self.__class__.__name__

# Block of forward declarations for all entities

class ConfigurationEntity():
    pass

class CompanyEntity():
    pass

class ContactEntity():
    pass

class OrderEntity():
    pass



class AccountingClerkEntity(User):
    def __init__(self, values={}):
        self.values = values
        for key, value in values.items():
            setattr(self, key, value)
        self.is_role_entity = True

class ConfiguratorEntity(User):
    def __init__(self, values={}):
        self.values = values
        for key, value in values.items():
            setattr(self, key, value)
        self.is_role_entity = True


# Block of forward declarations for all Tasks

class OrderManagementTask():
    pass


class PythonDataLayer:
    entity_mapping = {
            "Configuration": ConfigurationEntity,
            "Company": CompanyEntity,
            "Contact": ContactEntity,
            "Order": OrderEntity,
    }

    task_mapping = {
            "OrderManagement": OrderManagementTask,
    }
    task_instances = {
            repr(OrderManagementTask): {},
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
            repr(ConfigurationEntity): [],
            repr(CompanyEntity): [],
            repr(ContactEntity): [],
            repr(OrderEntity): [],
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
    

class ConfigurationEntity(Entity):
    meta_model = {
                "mailSubjectTemplate": (Text, ""),
                "mailContentTemplate": (Text, ""),
                "mailCC": (Emailaddress, "zeroOrMore"),
                "orderConfirmationDeadlineDefaultDays": (Integer, ""),
                "orderFullfillmentDeadlineDefaultDays": (Integer, ""),
                "paymentGoalDays": (Integer, ""),
                "defaultProvisionSupplier": (Decimal, ""),
                "defaultProvisionClerk": (Decimal, ""),
                "defaultDiscount": (Decimal, ""),
                "defaultSkonto": (Decimal, ""),
                "defaultSkontoDeadlineDays": (Integer, ""),
                "autoCompleteCategories": (Text, "zeroOrMore"),
                "mailServerAddress": (String, ""),
                "mailServerPort": (Integer, ""),
                "mailServerUseSSL": (Boolean, ""),
                "mailServerSendingAddress": (Emailaddress, ""),
                "mailServerLogin": (Text, "nullable"),
                "mailServerPassword": (Text, "nullable"),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in ConfigurationEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(ConfigurationEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in ConfigurationEntity.meta_model.keys():
            try:
                value = ConfigurationEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in ConfigurationEntity.observers.keys():
                    for func in ConfigurationEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Configuration"

class CompanyEntity(Entity):
    meta_model = {
                "name": (Text, ""),
                "address": (Address, ""),
                "knownSince": (Date, ""),
                "description": (Text, ""),
                "clerks": (AccountingClerkEntity, "zeroOrMore"),
                "isSupplier": (Boolean, "nullable"),
                "isCustomer": (Boolean, "nullable"),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in CompanyEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(CompanyEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in CompanyEntity.meta_model.keys():
            try:
                value = CompanyEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in CompanyEntity.observers.keys():
                    for func in CompanyEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Company"

class ContactEntity(Entity):
    meta_model = {
                "company": (CompanyEntity, ""),
                "title": (Text, ""),
                "firstName": (Text, ""),
                "lastName": (Text, ""),
                "mail": (Emailaddress, ""),
                "phone": (Phonenumber, "nullable"),
                "phoneMobile": (Phonenumber, "nullable"),
                "fax": (Phonenumber, "nullable"),
                "address": (Address, "nullable"),
                "department": (Text, "nullable"),
                "birthday": (Date, "nullable"),
                "lastVisit": (Date, "nullable"),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in ContactEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(ContactEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in ContactEntity.meta_model.keys():
            try:
                value = ContactEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in ContactEntity.observers.keys():
                    for func in ContactEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Contact"

class OrderEntity(Entity):
    meta_model = {
                "clerk": (AccountingClerkEntity, ""),
                "provisionClerk": (Decimal, "nullable"),
                "customer": (CompanyEntity, ""),
                "contact": (ContactEntity, "nullable"),
                "brand": (CompanyEntity, ""),
                "deadline": (Date, "nullable"),
                "paymentGoal": (Date, "nullable"),
                "category": (Text, "zeroOrMore"),
                "block": (Boolean, "nullable"),
                "type": (Text, ""),
                "year": (Year, ""),
                "season": (Text, ""),
                "poNumber": (Integer, "nullable"),
                "quantity": (Integer, ""),
                "amount": (Money, ""),
                "orderOrigin": (Text, ""),
                "orderDate": (Date, ""),
                "deliveryDate": (Date, ""),
                "discount": (Decimal, ""),
                "specialConditions": (Text, "nullable"),
                "provision": (Decimal, ""),
                "skonto": (Decimal, ""),
                "applySkonto": (Boolean, ""),
                "skontoDeadline": (Date, "nullable"),
    }

    observers = defaultdict(list)

    def __init__(self, values):
        self.is_entity = True
        # TODO: add exception if field of meta_model is not filled and its not zero or more
        for name, type_flags_tuple in OrderEntity.meta_model.items():
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

        PythonDataLayer.instances[repr(OrderEntity)].append(self)

    def update_attribute(self, attr_name, attr_value):
        if attr_name in OrderEntity.meta_model.keys():
            try:
                value = OrderEntity.meta_model[attr_name][0](attr_value)
                setattr(self, attr_name, value)
                if attr_name in OrderEntity.observers.keys():
                    for func in OrderEntity.observers[attr_name]:
                        func()

            except:
                raise Exception

    def __str__(self):
        return f"Order"



class PreconditionNotMetException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

class MissingInputException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class InsufficientPermissionsException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)



class OrderManagementTask():
    meta_model = {
        "inputs": {
            "task": {
                    "order": OrderEntity,
            },
            "steps": {
                    "addOrderDocument": {
                    },
                    "fillOrder": {
                    },
                    "forwardOrder": {
                    },
                    "uploadOrderConfirmation": {
                    },
                    "acceptOrderConfirmation": {
                    },
                    "uploadInvoice": {
                    },
                    "confirmInvoices": {
                    },
                    "payProvision": {
                    },
                    "completeOrder": {
                    },
                    "cancelOrder": {
                    },

            }
        },
        "additional_fields": {
                "addOrderDocument": {
                        "orderDocument": File,
                        "supplierPoNumber": Integer,
                },
                "fillOrder": {
                },
                "forwardOrder": {
                },
                "uploadOrderConfirmation": {
                        "orderConfirmation": File,
                        "poNumber": Integer,
                        "quantity": Integer,
                        "amount": Money,
                },
                "acceptOrderConfirmation": {
                },
                "uploadInvoice": {
                        "invoice": File,
                        "invoiceNo": Integer,
                        "invoiceQuantity": Integer,
                        "invoiceAmount": Money,
                },
                "confirmInvoices": {
                },
                "payProvision": {
                        "provisionDocument": File,
                        "provisionComment": Text,
                        "provisionAmount": Money,
                },
                "completeOrder": {
                },
                "cancelOrder": {
                        "canceled": Boolean,
                },
        },
    }

    def __init__(self, order, user=User()):
        if not type(order) == OrderManagementTask.meta_model["inputs"]["task"]["order"]:
            raise TypeError(order)
        
        self.order = order

        self.fields = defaultdict(lambda: defaultdict(bool))
        self.computed = defaultdict(lambda: defaultdict(bool))

        self.final_steps = []
        self.final = False
        if type(order) == list:
            type(order[0]).observers["amount"].append(self.compute_expectedPayment__addOrderDocument)
        else:
            type(order).observers["amount"].append(self.compute_expectedPayment__addOrderDocument)
        if type(order) == list:
            type(order[0]).observers["amount"].append(self.compute_expectedProvision__addOrderDocument)
        else:
            type(order).observers["amount"].append(self.compute_expectedProvision__addOrderDocument)
        if type(order) == list:
            type(order[0]).observers["provision"].append(self.compute_expectedProvision__addOrderDocument)
        else:
            type(order).observers["provision"].append(self.compute_expectedProvision__addOrderDocument)
        if type(order) == list:
            type(order[0]).observers["amount"].append(self.compute_clerkProvisionAmount__payProvision)
        else:
            type(order).observers["amount"].append(self.compute_clerkProvisionAmount__payProvision)
        if type(order) == list:
            type(order[0]).observers["provisionClerk"].append(self.compute_clerkProvisionAmount__payProvision)
        else:
            type(order).observers["provisionClerk"].append(self.compute_clerkProvisionAmount__payProvision)
        permissions = [
                    "",
        ]

        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        self.steps = [
                self.step_addOrderDocument,
                self.step_fillOrder,
                self.step_forwardOrder,
                self.step_uploadOrderConfirmation,
                self.step_acceptOrderConfirmation,
                self.step_uploadInvoice,
                self.step_confirmInvoices,
                self.step_payProvision,
                self.step_completeOrder,
                self.step_cancelOrder,
        ]
        arguments_tuple = (order,)
        if arguments_tuple in PythonDataLayer.task_instances[repr(OrderManagementTask)].keys():
            raise Exception(f"There already is a Task of type OrderManagementTask for arguments {arguments_tuple}")
        else: 
            PythonDataLayer.task_instances[repr(OrderManagementTask)][arguments_tuple] = self

    def get(self, key, *args):
        a = tuple(arg for arg in args)
        if a in self.fields.keys() and key in self.fields[a].keys():
            return self.fields[a][key]
        return self.computed[a][key]
        
    
    def step_addOrderDocument(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        order = self.order
        
        
        if not ((self.get('canceled', ) == False)):
            raise PreconditionNotMetException('precondition \"(self.canceled == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in OrderManagementTask.meta_model["additional_fields"]["addOrderDocument"].items():
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

        
        self.compute_expectedPayment__addOrderDocument()
        
        self.compute_expectedProvision__addOrderDocument()
        
    
    def compute_expectedPayment__addOrderDocument(self):
        order = self.order
        self.computed[()]["expectedPayment"] = order.amount
    
    def compute_expectedProvision__addOrderDocument(self):
        order = self.order
        self.computed[()]["expectedProvision"] = order.provision * order.amount
    
    
    def step_fillOrder(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        order = self.order
        
        
        if not ((self.get('orderDocument', ) and self.get('supplierPoNumber', )) and (self.get('canceled', ) == False)):
            raise PreconditionNotMetException('precondition \"(self.orderDocument and self.supplierPoNumber) and (self.canceled == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in OrderManagementTask.meta_model["additional_fields"]["fillOrder"].items():
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

        
        self.compute_filled__fillOrder()
        
    
    def compute_filled__fillOrder(self):
        order = self.order
        self.computed[()]["filled"] = True
    
    
    def step_forwardOrder(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        order = self.order
        
        
        if not ((self.get('filled', )) and (self.get('canceled', ) == False)):
            raise PreconditionNotMetException('precondition \"(self.filled) and (self.canceled == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in OrderManagementTask.meta_model["additional_fields"]["forwardOrder"].items():
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

        
        self.compute_orderForwarded__forwardOrder()
        
        sendMail(self.order.contact.mail, 'Sehr geehrte Damen und Herren, hiermit leite ich ihnen die Bestellung weiter.')
    
    def compute_orderForwarded__forwardOrder(self):
        order = self.order
        self.computed[()]["orderForwarded"] = True
    
    
    def step_uploadOrderConfirmation(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        order = self.order
        
        
        if not ((self.get('filled', )) and (self.get('canceled', ) == False)):
            raise PreconditionNotMetException('precondition \"(self.filled) and (self.canceled == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in OrderManagementTask.meta_model["additional_fields"]["uploadOrderConfirmation"].items():
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

        
    
    
    def step_acceptOrderConfirmation(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        order = self.order
        
        
        if not ((self.get('poNumber', ) == order.poNumber) and (self.get('quantity', ) == order.quantity) and (self.get('amount', ) == order.amount) and (self.get('canceled', ) == False)):
            raise PreconditionNotMetException('precondition \"(self.poNumber == order.poNumber) and (self.quantity == order.quantity) and (self.amount == order.amount) and (self.canceled == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in OrderManagementTask.meta_model["additional_fields"]["acceptOrderConfirmation"].items():
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

        
        self.compute_acceptedOrderConfirmation__acceptOrderConfirmation()
        
    
    def compute_acceptedOrderConfirmation__acceptOrderConfirmation(self):
        order = self.order
        self.computed[()]["acceptedOrderConfirmation"] = True
    
    
    def step_uploadInvoice(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        order = self.order
        
        
        if not ((self.get('acceptedOrderConfirmation', )) and (self.get('canceled', ) == False)):
            raise PreconditionNotMetException('precondition \"(self.acceptedOrderConfirmation) and (self.canceled == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in OrderManagementTask.meta_model["additional_fields"]["uploadInvoice"].items():
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

        
    
    
    def step_confirmInvoices(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        order = self.order
        
        
        if not ((self.get('invoiceQuantity', ) == order.quantity) and (self.get('invoiceAmount', ) == order.amount) and (self.get('invoice', )) and (self.get('canceled', ) == False)):
            raise PreconditionNotMetException('precondition \"(self.invoiceQuantity == order.quantity) and (self.invoiceAmount == order.amount) and (self.invoice) and (self.canceled == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in OrderManagementTask.meta_model["additional_fields"]["confirmInvoices"].items():
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

        
        self.compute_invoicesAccepted__confirmInvoices()
        
    
    def compute_invoicesAccepted__confirmInvoices(self):
        order = self.order
        self.computed[()]["invoicesAccepted"] = True
    
    
    def step_payProvision(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        order = self.order
        
        
        if not ((self.get('invoicesAccepted', )) and (self.get('canceled', ) == False)):
            raise PreconditionNotMetException('precondition \"(self.invoicesAccepted) and (self.canceled == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in OrderManagementTask.meta_model["additional_fields"]["payProvision"].items():
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

        
        self.compute_clerkProvisionAmount__payProvision()
        
    
    def compute_clerkProvisionAmount__payProvision(self):
        order = self.order
        self.computed[()]["clerkProvisionAmount"] = order.amount * order.provisionClerk
    
    
    def step_completeOrder(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        order = self.order
        
        
        if not ((self.get('provisionAmount', ) == self.get('clerkProvisionAmount', )) and (self.get('canceled', ) == False)):
            raise PreconditionNotMetException('precondition \"(self.provisionAmount == self.clerkProvisionAmount) and (self.canceled == False)\" not met')
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in OrderManagementTask.meta_model["additional_fields"]["completeOrder"].items():
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

        
        self.final = True
        self.final_steps.append("completeOrder")
    
    
    def step_cancelOrder(self,  fields, user=User()):
        if self.final:
            raise TaskIsLockedException(self.final_steps)
        permissions = [
        ]
        order = self.order
        
        
        if not user.has_permissions(permissions):
            raise InsufficientPermissionsException(user, permissions)

        # TODO: check if field types match and all required fields were added

        for field_name, field_type in OrderManagementTask.meta_model["additional_fields"]["cancelOrder"].items():
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

        
        self.final = True
        self.final_steps.append("cancelOrder")
    
    
