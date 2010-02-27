import re
from FormKit import BaseValidatorClasses
from FormKit.BaseValidatorClasses import ValidatorConverter, InvalidField

class PasswordVerifier(BaseValidatorClasses.FormValidator):
    """ Check if the two passwords corresponds """
    def validate(self,valueDict):
        if not valueDict["password"] == valueDict["password_again"]:
            raise BaseValidatorClasses.InvalidField, "The passwords doesn't match"

    def validatePartialForm(self):
        return 1
    

class QuotaValidator(ValidatorConverter):
    """ The quota needs to either be an integer or empty """
    def _validate(self,value):
        if value:
            try:
                int(value)
            except ValueError:
                return "Quota needs to be either an integer or empty"


class UserDoesNotExist(ValidatorConverter):
    """ Check if the user already exists"""
    def __init__(self, db):
        self.db = db
        
    def _validate(self,value):
        if self.db.getUserInfo(value):
            return "The user already exists."


class CompanyAccess(ValidatorConverter):
    """ Checks to see if this user has access to add users in this company """
    def __init__(self, user, db):
        self.authName = user
        self.db = db
        
    def _validate(self, value):
        if not self.db.authUser(self.authName, value):
            return "You do not have access to this company"


class VirtualAccess(BaseValidatorClasses.FormValidator):
    """ Checks to see if the logged in user has access to change this user """
    def __init__(self, user, db):
        self.authName = user
        self.db = db
        
    def validate(self, valueDict):
        if not self.db.authUser(self.authName, valueDict["company"]):
            raise BaseValidatorClasses.InvalidField, "You do not have access to this user"


class ValidEmail(BaseValidatorClasses.FormValidator):
    """ Checks to see if the virtual and domain parts form a valid email """
    def validate(self, valueDict):
        value = valueDict["virtual"]+"@"+valueDict["domain"]
        if re.match('[^@]+@[^\.@]+(\.[^\.]+)+',value) is None:
            raise BaseValidatorClasses.InvalidField, "Not a valid virtual entry."


class CompanyDoesNotExist(ValidatorConverter):
    """ Make sure a company doesn't exist before we add it """
    def __init__(self, db):
        self.db = db

    def _validate(self,value):
        if self.db.compExists(value):
            return "This company already exists."
        return None


class AliasExist(ValidatorConverter):
    """ Checks wether the alias entry already exists """
    def __init__(self, db):
        self.db = db

    def _validate(self, value):
        if self.db.aliasExist(value):
            return "This alias already exists."
        return None

class VirtualExist(BaseValidatorClasses.FormValidator):
    """ Checks if this virtual already exists """
    def __init__(self, db):
        self.db = db

    def validate(self, valueDict):
        virtual = valueDict["virtual"]+"@"+valueDict["domain"]
        if self.db.virtualExist(virtual):
            raise BaseValidatorClasses.InvalidField, "This virtual already exists"

        

class UniquePrefix(ValidatorConverter):
    def __init__(self, db):
        self.db = db

    def _validate(self, value):
        if self.db.prefixExist(value):
            return "This prefix already exist"
        return None



class ListExist(BaseValidatorClasses.FormValidator):
    """ Checks if this virtual already exists """
    def __init__(self, db):
        self.db = db

    def validate(self, valueDict):
        virtual = valueDict["listname"]+"@"+valueDict["domain"]
        if self.db.virtualExist(virtual):
            raise BaseValidatorClasses.InvalidField, "This list already exists"

class AdminAccess(ValidatorConverter):
    """ Check if the user has admin privileges """
    def __init__(self, admin, db, user):
        self.admin = admin
        self.db = db
        self.user = user
        
    def _validate(self, value):
        types = self.db.getAccess(self.admin)
        if not "admin" in types and self.hasChanged(value):
            return "You do not have access to edit the rights of this user"
        return None


    def hasChanged(self, value, edit):
        types = self.db.getAccess(self.user)
        if not value and types:
            return True
        if not value and not types:
            return False
        for i in value:
            if not i in types:
                return True
        return False


