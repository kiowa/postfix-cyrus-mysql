from WebKit.XMLRPCServlet import XMLRPCServlet
from Cyrus import Cyrus
from ConfigParser import ConfigParser

class XMLRPC(XMLRPCServlet):
    def __init__(self):
        XMLRPCServlet.__init__(self)
        conf = ConfigParser()
        conf.readfp(open("/home/webware/mail/conf/Site.conf"))
        self.cyrus = Cyrus(conf.get("cyrus","host"),
                           conf.get("cyrus","user"),
                           conf.get("cyrus","password"),
                           conf.get("mysql","host"),
                           conf.get("mysql","user"),
                           conf.get("mysql","password"),
                           conf.get("mysql","database"),
                           )
        self.allow_caching = 0

    def exposedMethods(self):
        return ["getVirtual", "delVirtual", "addVirtual", "updateVirtual",
                "addUser", "editUser", "delUser",
                "saAdd", "saEdit", "saDel", "saGet",
                "getCompanies", "getUserByCompany", "getUserInfo",
                "compUpdate", "compAdd", "compDel", "compGet",
                "aliasAdd", "aliasEdit", "aliasDel", "aliasGet",
                "test"]

    def test(self, foo, bar = 23):
        return foo + bar

    def getVirtual(self, user):
        return (self.cyrus.getVirtual(user),)

    def delVirtual(self, id):
        self.cyrus.delVirtual(id)
        return True

    def addVirtual(self, alias, dest, user = None, status = 1):
        self.cyrus.addVirtual(alias, dest, user, status)
        return True

    def updateVirtual(self, id, alias, dest, status):
        self.cyrus.updateVirtual(id, alias, dest, status)
        return True

    def addUser(self, user, firstname, lastname, password, company, status, quota):
        self.cyrus.addUser(user, firstname, lastname, password, company, status, quota)
        return True

    def editUser(self, user, firstname, lastname, password, company, status, quota):
        self.cyrus.editUser(user, firstname, lastname, password, company, status, quota)
        return True

    def delUser(self, user):
        self.cyrus.delUser(user)
        return True

    def saAdd(self, user, pref, value):
        self.cyrus.saAdd(user, pref, value)
        return True

    def saEdit(self, prefid, pref, value):
        self.cyrus.saEdit(user, pref, value)
        return True

    def saDel(self, prefid):
        self.cyrus.saDel(prefid)
        return True

    def saGet(self, user, pref = None):
        return (self.cyrus.saGet(user, pref),)

    def getCompanies(self, order = "name"):
        return (self.cyrus.getCompanies(order),)

    def getUserByCompany(self, company, order = "username"):
        return (self.cyrus.getUserByCompany(company, order),)

    def getUserInfo(self, user):
        return (self.cyrus.getUserInfo(user),)

    def compUpdate(self, name, prefix, telephone, fax, email, street, zip, city, id):
        self.cyrus.compUpdate(name, prefix, telephone, fax, email, street, zip, city, id)
        return True

    def compAdd(self, name, prefix, telephone, fax, email, street, zip, city):
        self.cyrus.compAdd(name, prefix, telephone, fax, email, street, zip, city)
        return True

    def compDel(self, id):
        self.cyrus.compDel(id)
        return True

    def aliasAdd(self, alias, dest, status):
        self.cyrus.aliasAdd(alias, dest, status)
        return True

    def aliasEdit(self, id, alias, dest, status):
        self.cyrus.aliasEdit(id, alias, dest, status)
        return True

    def aliasDel(self, id):
        self.cyrus.aliasDel(id)
        return True

    def aliasGet(self, id = None, order = "alias"):
        return (self.cyrus.aliasGet(id, order),)

