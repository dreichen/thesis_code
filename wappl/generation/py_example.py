from decimal import Decimal
import re
import datetime


class User:
    def has_permissions(self, permissions):
        return True


class InvalidMailException(TypeError):
    def __init__(self, mail):
        super().__init__(f"'{mail}' is not a valid email address")


class InvalidIntegerException(TypeError):
    def __init__(self, integer):
        super().__init__(f"'{integer}' is not a valid integer")


class InvalidTextException(TypeError):
    def __init__(self, text):
        super().__init__(f"'{text}' is not a valid text")


class InvalidDateException(TypeError):
    def __init__(self, date_):
        super().__init__(f"'{date_}' is not a valid date")


class BuiltinType:
    def __eq__(self, value):
        return type(self) == type(value) and value.value == self.value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"


class CustomType:
    def __eq__(self, value):
        return type(self) == type(value) and value.value == self.value


class Text(BuiltinType):
    def __init__(self, text):
        if not type(text) == str:
            raise InvalidTextException(text)

        self.value = text


class DateType(BuiltinType):
    def __init__(self, date_string):
        try:
            date_ = datetime.datetime.strptime(
                date_string, '%d.%m.%Y %H:%M:%S')
        except Exception as e:
            raise InvalidDateException(date_string)

        self.value = date_


class EMail(BuiltinType):
    def __init__(self, mail):
        if not type(mail) == str:
            raise InvalidMailException(mail)

        regexp = re.compile(
            r"^\S+@\S+\.\S+$")

        if not re.fullmatch(regexp, mail):
            raise InvalidMailException(mail)

        self.value = mail


class Integer(BuiltinType):
    def __init__(self, integer):
        try:
            self.value = int(integer)
        except Exception as e:
            raise InvalidIntegerException


class Grade(CustomType, Decimal):
    def __init__(self, grade):
        Decimal.__init__(grade)


class Entity:
    def __repr__(self):
        return self.__class__.__name__


class HomeworkEntity(Entity):
    meta_model = {
        "title": Text,
        "grade": Grade,
        "test": Integer,
    }

    instances = []

    def __init__(self, values):
        for name, type_ in HomeworkEntity.meta_model.items():
            value = type_(values[name])
            setattr(self, name, value)

        HomeworkEntity.instances.append(self)

    def __str__(self):
        return f"Homework: {self.title}"


class AssignmentEntity(Entity):
    meta_model = {
        "title": Text,
        "homework": HomeworkEntity
    }

    instances = []

    def __init__(self, values):
        for name, type_ in AssignmentEntity.meta_model.items():
            if repr(type_).find("Entity") != -1:  # way to do that more reliably?
                value = values[name]
                if value not in type_.instances:
                    raise Exception
                else:
                    setattr(self, name, value)
            else:
                value = type_(values[name])
                setattr(self, name, value)

        AssignmentEntity.instances.append(self)


class PreconditionNotMetException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class MissingInputException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class InsufficientPermissionsException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class HomeworkSubmissionTask:
    meta_model = {
        "inputs": {
            "task": {
                "hw": HomeworkEntity
            },
            "steps": {
                "submitAnswer": {
                    "assignment": AssignmentEntity,
                },
                "submitAttachedFile": {
                    "assignment": AssignmentEntity,
                }
            }
        },
        "additional_fields": {
            "submitAnswer": {
                "answer": Text,
            },
            "submitAttachedFile": {
                "attachedFile": Text,
            }
        }
    }

    instances = []

    def __init__(self, hw=None, user=None):
        if not hw:
            raise MissingInputException(hw)
        if not type(hw) == HomeworkSubmissionTask.meta_model["inputs"]["task"]["hw"]:
            raise TypeError(hw)

        self.hw = hw
        self.user = User()

        permissions = [
            "SolveQuiz",
            "ReadCoursePlan",
            "CompleteModule",
        ]

        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)

        self.steps = [self.step_submitAnswer, self.step_submitAttachedFile]

        HomeworkSubmissionTask.instances.append(self)

    def __check_pre_condition(self, preconditions):
        # TODO: implement after grammar can parse pre-conditions
        return True

    def __can_execute_step(self, permissions, preconditions):
        if not self.user.has_permissions(permissions):
            raise InsufficientPermissionsException(self.user, permissions)
        elif not self.__check_pre_condition(preconditions):
            raise PreconditionNotMetException(preconditions)

    def step_submitAnswer(self, assignment, fields):
        permissions = [
        ]

        preconditions = [
        ]

        self.__can_execute_step(permissions, preconditions)

        for field_name, field_value in fields.items():
            setattr(assignment, field_name, field_value)

    def step_submitAttachedFile(self, assignment, fields):
        permissions = [
        ]

        preconditions = [
        ]

        self.__can_execute_step(permissions, preconditions)

        for field_name, field_value in fields.items():
            setattr(assignment, field_name, field_value)


class PythonDataLayer:
    entity_mapping = {
        "Assignment": AssignmentEntity,
        "Homework": HomeworkEntity
    }

    task_mapping = {
        "HomeworkSubmissionTask": HomeworkSubmissionTask,
    }

    def get_state(self):
        state = {
            "entities": {
                key: value.instances for key, value in PythonDataLayer.entity_mapping.items()
            },
            "tasks": {
                key: value.instances for key, value in PythonDataLayer.task_mapping.items()
            }
        }
        return state

    def create_entity(self, entity, values):
        return entity(values)

    def create_task(self, task, values):
        return task(values)


if __name__ == '__main__':

    valid = EMail("david@reichenbachs.de")
    valid2 = EMail("justa@test.xyz")
    valid3 = EMail("justa@test.xyz")
    print(valid2 == valid3)

    today = DateType("05.06.2023 15:43:21")

    try:
        invalid_type = EMail(5)
    except Exception as e:
        print(e)

    try:
        invalid_regex = EMail("test@moin")
    except Exception as e:
        print(e)

    hw = HomeworkEntity(
        {"title": "The absolutely most useless homework ever created", "grade": 1})

    try:
        hw2 = HomeworkEntity({})
    except Exception as e:
        print("Error for hw2", e)

    assignment = AssignmentEntity({"title": "t", "homework": hw})
    print(hw)
