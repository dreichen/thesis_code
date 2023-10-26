from tokenize import tokenize
from io import BytesIO
import re

DSL = {
    "CONFIG":  """
                entity Configuration = {
                    mailSubjectTemplate : Text
                    mailContentTemplate : Text
                    mailCC : EMailAddress*
                    orderConfirmationDeadlineDefaultDays : integer
                    orderFullfillmentDeadlineDefaultDays : integer 
                    paymentGoalDays : integer
                    defaultProvisionSupplier : decimal
                    defaultProvisionClerk : decimal
                    defaultDiscount : decimal
                    defaultSkonto : decimal
                    defaultSkontoDeadlineDays : integer
                    autoCompleteCategories : Text*
                    mailServerAddress : string
                    mailServerPort : integer
                    mailServerUseSSL : boolean
                    mailServerSendingAddress : EMailAddress
                    mailServerLogin : Text?
                    mailServerPassword : Text?
                }""",
    "COMPANY": """
                entity Company = {
                    name : Text
                    address : Address
                    knownSince : Date
                    description : Text
                    clerks -> AccountingClerk*
                    isSupplier : boolean?
                    isCustomer : boolean?
                }""",
    "CONTACT": """
                entity Contact = {
                    company -> Company
                    title : Text
                    firstName : Text
                    lastName : Text
                    mail : EMailAddress
                    phone : PhoneNumber?
                    phoneMobile : PhoneNumber?
                    fax : PhoneNumber?
                    address : Address?
                    department : Text?
                    birthday : Date?
                    lastVisit : Date?
                }
                """,
    "ORDER": """
            entity Order = {
                clerk -> AccountingClerk
                provisionClerk : decimal?
                customer -> Company
                contact -> Contact?
                brand -> Company
                deadline : Date?
                paymentGoal : Date?
                category : Text*
                block : boolean?
                type : Text
                year : Year
                season : Tex
                poNumber : integer?
                quantity : integer
                amount : Money
                orderOrigin : Text
                orderDate : Date
                deliveryDate : Date
                discount : decimal
                specialConditions : Text?
                provision : decimal
                skonto : decimal
                applySkonto : boolean
                skontoDeadline : Date?
            }
            """,
}

# Order Management python code examples removed due to confidentiality 
GPL = {
    "CONFIG": "",
    "COMPANY": "",
    "CONTACT": "",
    "ORDER": ""
}

def py_tokenize(s):
    tokens = tokenize(BytesIO(s.encode('utf-8')).readline)
    # remove all tokens of type 0 (ENDMARKER), 4 (NEWLINE), 5 (INDENT), 60 (NL) -> also newline, 61 (COMMENT), 62 (ENCODING)
    return sum(map(lambda e : 0 if e.type in [0, 4, 5, 6, 60, 61, 62] else 1, tokens))

def dsl_tokenize(s):
    return len(s.split()) + s.count('*') + s.count('?')


print(dsl_tokenize(DSL["CONFIG"]))
print(dsl_tokenize(DSL["COMPANY"]))
print(dsl_tokenize(DSL["CONTACT"]))
print(dsl_tokenize(DSL["ORDER"]))

# Order Management python code examples removed due to confidentiality 
# print(py_tokenize(GPL["CONFIG"]))
# print(py_tokenize(GPL["COMPANY"]))
# print(py_tokenize(GPL["CONTACT"]))
# print(py_tokenize(GPL["ORDER"]))