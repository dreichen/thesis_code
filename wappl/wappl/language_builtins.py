from decimal import Decimal, getcontext
import re
import datetime
import statistics

getcontext().prec = 4
getcontext().Emax = 2
getcontext().Emin = 0

class User:
    def __init__(self):
        self.mail = None
        self.name = None
        
    def has_permissions(self, permissions):
        return True


class InvalidMailException(TypeError):
    def __init__(self, mail):
        super().__init__(f"'{mail}' is not a valid email address")


class InvalidBooleanException(TypeError):
    def __init__(self, bool):
        super().__init__(f"'{bool}' is not a valid boolean")

class InvalidIntegerException(TypeError):
    def __init__(self, integer):
        super().__init__(f"'{integer}' is not a valid integer")


class InvalidStringException(TypeError):
    def __init__(self, string):
        super().__init__(f"'{string}' is not a valid string")


class InvalidTextException(TypeError):
    def __init__(self, text):
        super().__init__(f"'{text}' is not a valid text")

class InvalidFileException(TypeError):
    def __init__(self, file):
        super().__init__(f"'{file}' is not a valid file")

class InvalidDateException(TypeError):
    def __init__(self, date_):
        super().__init__(f"'{date_}' is not a valid date")


class InvalidDateTimeException(TypeError):
    def __init__(self, date_):
        super().__init__(f"'{date_}' is not a valid datetime")

class TaskIsLockedException(Exception):
    def __init__(self, steps):
        super().__init__(f"This Task was locked by step {steps[0]} and no other steps can be executed until it is manually unlocked")

class BuiltinType:
    def __eq__(self, value):
        return type(self) == type(value) and value.value == self.value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"


class CustomType:
    def __eq__(self, value):
        return type(self) == type(value) and value.value == self.value or value == self.value

class File(BuiltinType):
    def __init__(self, file):
        if not type(file) == File and not type(file) == str:
            raise InvalidFileException(file)

        self.value = file

    def __eq__(self, value):
        return str(self) == str(value)

    def __str__(self):
        return str(self.value)

    @property
    def name(self):
        return f"File: {self.value}"
    
class Text(BuiltinType):
    def __init__(self, text):
        if not type(text) == str:
            raise InvalidTextException(text)

        self.value = text

    def __eq__(self, value):
        return str(self) == str(value)

    def __str__(self):
        return self.value

    @property
    def name(self):
        return "Text"

class Address(BuiltinType):
    def __init__(self, address):
        if not type(address) == str:
            raise InvalidTextException(address)

        self.value = address


class Date(BuiltinType, datetime.datetime):
    days = (lambda x : datetime.timedelta(days=x))
    minutes = (lambda x : datetime.timedelta(minutes=x))
    hours = (lambda x : datetime.timedelta(hours=x))
    seconds = (lambda x : datetime.timedelta(seconds=x))
    def __new__(cls, *args, **kwargs):
        try:
            d = datetime.datetime.strptime(args[0], '%d.%m.%Y')
        except:
            raise InvalidDateException(args[0])
        return datetime.datetime.__new__(cls, d.year, d.month, d.day, 0, 0, 0, 0, **kwargs)
    
    @staticmethod
    def now():
        return datetime.datetime.now()

class Datetime(BuiltinType, datetime.datetime):
    days = (lambda x : datetime.timedelta(days=x))
    minutes = (lambda x : datetime.timedelta(minutes=x))
    hours = (lambda x : datetime.timedelta(hours=x))
    seconds = (lambda x : datetime.timedelta(seconds=x))
    def __new__(cls, *args, **kwargs):
        try:
            d = datetime.datetime.strptime(args[0], '%d.%m.%Y %H:%M:%S')
        except:
            raise InvalidDateTimeException(args[0])
        return datetime.datetime.__new__(cls, d.year, d.month, d.day, d.hour, d.minute, d.second, 0, **kwargs)
    
    @staticmethod
    def now():
        return datetime.datetime.now()

class Emailaddress(BuiltinType):
    def __init__(self, mail):
        if not type(mail) == str:
            raise InvalidMailException(mail)

        regexp = re.compile(
            r"^\S+@\S+\.\S+$")

        if not re.fullmatch(regexp, mail):
            raise InvalidMailException(mail)

        self.value = mail


class String(BuiltinType):
    def __init__(self, string):
        try:
            self.value = str(string)
        except Exception as e:
            raise InvalidStringException


class Integer(BuiltinType):
    def __init__(self, integer):
        try:
            self.value = int(integer)
        except Exception as e:
            raise InvalidIntegerException

class Boolean(BuiltinType):
    def __init__(self, boolean):
        try:
            self.value = bool(boolean)
        except Exception as e:
            raise InvalidBooleanException
        
    def __eq__(self, o):
        return self.value == o or self.value == o.value
        
def remove_none(iterable):
    return filter(lambda item : item != None, iterable)

def abstract_aggr(func, iterable, field_name):
    if field_name:
        l =  list(remove_none(getattr(instance, field_name) for instance in iterable))
    else:
        l = list(remove_none(instance for instance in iterable))
    
    if len(l) == 0:
        return 0
    
    return func(l)
    
def entityAggregation(fun, iterable, field_name):
    entities = filter(lambda item : item.__dict__[field_name] != None, iterable)
    return fun(entities, key=lambda x : x.__dict__[field_name])

def aggregation(name, iterable, field=None):
    mapping = {
        "sum": lambda iterable, field : abstract_aggr(sum, iterable, field),
        "mean": lambda iterable, field : abstract_aggr(statistics.mean, iterable, field),
        "median": lambda iterable, field : abstract_aggr(statistics.median, iterable, field),
        "min": lambda iterable, field : abstract_aggr(min, iterable, field),
        "max": lambda iterable, field : abstract_aggr(max, iterable, field),
        "count": lambda iterable, field : abstract_aggr(len, iterable, field),
        "minEntity": lambda iterable, field : entityAggregation(min, iterable, field),
        "maxEntity": lambda iterable, field : entityAggregation(max, iterable, field),
    }
    return mapping[name](iterable, field)


def sendMail(to, body, subject='Automatic E-Mail'):
    try:
        import smtplib, ssl, os

        message = """Subject: {subject}
        \n
        {body}"""
        from_address = os.environ['MAIL_FROM']
        password = os.environ['MAIL_PW']

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.strato.de", 465, context=context) as server:
            server.login(from_address, password)
            server.sendmail(
                from_address,
                to,
                message.format(subject=subject, body=body),
            )
    except Exception as e:
        print(f"Mail sending -> {to}: Subject [{subject}] Body: {body}")