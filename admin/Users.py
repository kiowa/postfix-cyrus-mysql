from SitePage import SitePage
from FormKit import Form, Fields, Validators
from FormKit.FormKitMixIn import FormKitMixIn
from Validators import PasswordVerifier, QuotaValidator, UserDoesNotExist, CompanyAccess, VirtualAccess, ValidEmail, AdminAccess
import Auth,types


class Users(FormKitMixIn, SitePage):
    global ACCESS_TYPES
    ACCESS_TYPES = (("general", "Access to login"), ("comp","Access to companies dialog"), ("mail","Access to mail dialog"), ("dns","Access to dns dialog"), ("global","Access to all companies"), ("admin","Admin privs"))

    def __init__(self):
        SitePage.__init__(self)
        self.userFormInput = None
        self.virtualFormInput = None
        ## Users add form
        self.userForm = userForm = Form.Form(validators=[PasswordVerifier()])
        self.addForm(userForm)
        userForm.addField(Fields.SelectField('company',label='Company'))
        userForm.addField(Fields.TextField("user",label="Username", validators=[UserDoesNotExist(self.db),Validators.MinLength(3)]))
        userForm.addField(Fields.TextField("firstname",label="Firstname", validators=[Validators.NotEmpty()]))
        userForm.addField(Fields.TextField("lastname", label="Lastname", validators=[Validators.NotEmpty()]))
        userForm.addField(Fields.PasswordField("password",label="Password", validators=[Validators.MinLength(5)]))
        userForm.addField(Fields.PasswordField("password_again",label="Password Again", validators=[Validators.MinLength(5)]))
        userForm.addField(Fields.TextField("quota", label="Quota", validators=[QuotaValidator()]))
        userForm.addField(Fields.SelectField('quota_type', label='Quota Type'))
        for type in self.getQuotaTypes():
            userForm.quota_type.addChoice(type,type)
        #userForm.addField(Fields.MultiSelectField("access", label="Access"))
        #for atype,adescr in ACCESS_TYPES:
        #    userForm.access.addChoice(atype, adescr)
        userForm.addField(Fields.CheckboxSet("active",label="Active"))
        userForm.active.addChoice("status","")
        userForm.seed({"active":"status"})
        userForm.addField(Fields.WebKitSubmitButton("add",label="Add"))


        ## Users edit form
        self.editUserForm = editUserForm = Form.Form(validators=[PasswordVerifier()])
        self.addForm(editUserForm)
        #editUserForm.addField(Fields.SelectField('company',label='Company', attributes={"disabled":1}))
        editUserForm.addField(Fields.SelectField('company',label='Company'))
        editUserForm.addField(Fields.HiddenField("cid", label="Comp. id"))
        editUserForm.addField(Fields.TextField("user",label="Username", attributes={"readonly":1}))
        editUserForm.addField(Fields.TextField("firstname",label="Firstname", validators=[Validators.NotEmpty()]))
        editUserForm.addField(Fields.TextField("lastname", label="Lastname", validators=[Validators.NotEmpty()]))
        editUserForm.addField(Fields.PasswordField("password",label="Password"))
        editUserForm.addField(Fields.PasswordField("password_again",label="Password Again"))
        editUserForm.addField(Fields.TextField("quota", label="Quota", validators=[QuotaValidator()]))
        editUserForm.addField(Fields.SelectField('quota_type', label='Quota Type'))
        for type in self.getQuotaTypes():
            editUserForm.quota_type.addChoice(type,type)
        editUserForm.addField(Fields.MultiSelectField("access", label="Access"))
        for atype,adescr in ACCESS_TYPES:
            editUserForm.access.addChoice(atype, adescr)
        editUserForm.addField(Fields.CheckboxSet("active",label="Active"))
        editUserForm.active.addChoice("status","")
        editUserForm.addField(Fields.WebKitSubmitButton("edit",label="Update"))
        editUserForm.addField(Fields.WebKitSubmitButton("delete",label="Delete"))



        # User search form
        self.searchForm = searchForm = Form.Form()
        self.addForm(searchForm)
        searchForm.addField(Fields.TextField("search", attributes={'size':5}))
        searchForm.addField(Fields.WebKitSubmitButton("userget",label="Search"))
        
        # Virtual add form
        self.virtualForm = virtualForm = Form.Form(validators=[ValidEmail()])
        self.addForm(virtualForm)
        virtualForm.addField(Fields.TextField("virtual", label="Virtual", validators=[Validators.NotEmpty()]))
        #virtualForm.addField(Fields.SelectField("domain", label="Domain"))
        virtualForm.addField(Fields.TextField("domain", label="Domain", validators=[Validators.NotEmpty()]))
        virtualForm.addField(Fields.HiddenField("company", label="Company"))
        virtualForm.addField(Fields.HiddenField("user", label="user"))
        virtualForm.addField(Fields.CheckboxSet("active", label="Active"))
        virtualForm.active.addChoice("status", "")
        virtualForm.seed({"active":"status"})
        virtualForm.addField(Fields.WebKitSubmitButton("add_virtual", label="Add"))

        # Virtual edit form
        self.editVirtualForm = editVirtualForm = Form.Form()
        self.addForm(editVirtualForm)
        editVirtualForm.addField(Fields.TextField("virtual", label="Virtual", attributes={"readonly":1}))
        #editVirtualForm.addField(Fields.SelectField("domain", label="Domain", attributes={"disabled":1}))
        editVirtualForm.addField(Fields.TextField("domain", label="Domain", validators=[Validators.NotEmpty()]))
        editVirtualForm.addField(Fields.HiddenField("id",label="id"))
        editVirtualForm.addField(Fields.HiddenField("company", label="Company"))
        editVirtualForm.addField(Fields.HiddenField("user", label="user"))
        editVirtualForm.addField(Fields.CheckboxSet("active", label="Active"))
        editVirtualForm.active.addChoice("status", "")
        editVirtualForm.addField(Fields.WebKitSubmitButton("edit_virtual", label="Update"))
        editVirtualForm.addField(Fields.WebKitSubmitButton("del_virtual", label="Delete"))
        


    def actions(self):
        return ["add","edit","delete","userget","add_virtual","edit_virtual","del_virtual"]
                          
    def add(self):
        if self.userForm.isSuccessful():
            self.addUser(self.userForm.values())
            self.userFormInput = self.getUserInfo(self.userForm.values()["user"])
        else:
            pass
        
    def edit(self):
        if self.editUserForm.isSuccessful():
            self.editUser(self.editUserForm.values())
            self.userFormInput = self.getUserInfo(self.editUserForm.values()["user"])
        else:
            pass

    def delete(self):
        if self.editUserForm.isSuccessful():
            self.delUser(self.editUserForm.values()["user"])
            self.userFormInput = None
            self.resetForms()


    def add_virtual(self):
        if self.virtualForm.isSuccessful():
            val = self.virtualForm.values()
            alias = val["virtual"]+"@"+val["domain"]
            dest = user = val["user"]
            status = 0
            if val["active"] == "status":
                status = 1
            self.addVirtual(alias, dest, user=user, status=status)



    def edit_virtual(self):
        if self.editVirtualForm.isSuccessful():
            val = self.editVirtualForm.values()
            #alias = val["virtual"]+"@"+val["domain"]
            dest = val["user"]
            alias = dest = None
            id = val["id"]
            status = 0
            if val["active"] == "status":
                status = 1
            self.updateVirtual(id, dest, status)

            

    def del_virtual(self):
        if self.editVirtualForm.isSuccessful():
            id = self.editVirtualForm.values()["id"]
            self.delVirtual(id)


    def userget(self):
        """ Search for users """
        self.users = self.userSearch(self.searchForm.values()["search"])
        if len(self.users) == 1:
            for user in self.users.keys():
                self.userFormInput = self.getUserInfo(user)


    def htTitle(self):
        return "Brukere"
    
    def needAccess(self):
        return "mail"
    
    def awake(self,trans):
        SitePage.awake(self,trans)
        self.trans = trans
        comps = self.compGet()
        self.userForm.company.clearChoices()
        self.editUserForm.company.clearChoices()
        if comps:
            for id,comp in comps:
                self.userForm.company.addChoice(id,comp)
                self.editUserForm.company.addChoice(id,comp)
        if trans.request().hasField("userid"):
            self.userForm.user.clearValidators()
            self.userForm.password.clearValidators()
            self.userForm.password_again.clearValidators()
            if not self.userFormInput:
                self.userFormInput = self.getUserInfo(trans.request().field("userid"))

        # Update the validators since they depend upon session data and cannot be used across
        # sessions.
        self.userForm.company.clearValidators()
        self.editUserForm.cid.clearValidators()
        self.editUserForm.access.clearValidators()
        self.virtualForm._validators = []

        #self.userForm.company.addValidator(CompanyAccess(self.getUser(), self.db))
        #self.editUserForm.cid.addValidator(CompanyAccess(self.getUser(), self.db))
        self.virtualForm.addFormValidator(VirtualAccess(self.getUser(), self.db))
        self.virtualForm.addFormValidator(ValidEmail())
        if self.userFormInput:
            self.editUserForm.access.addValidator(AdminAccess(self.getUser(), self.db,self.userFormInput["user"]))
      
        




                
    def writeMenu(self):
        self.write(self.searchForm.startTags())
        self.write(self.searchForm.search.tag())
        self.write(self.searchForm.userget.tag())
        self.write(self.searchForm.endTags())

        if self.searchForm.isSuccessful():
            self.writeln("%s hit(s)<br>" % len(self.users))
            for i in self.users.keys():
                if self.users[i].has_key("active"):
                    status = "enabled"
                else:
                    status = "disabled"
                self.writeln('<a class="%s" href="Users?userid=%s">%s (%s %s)</a><br>' % (status, i,i,self.users[i]["firstname"],self.users[i]["lastname"]))



    def writeCenter(self):
        trans = self.trans
        
        if trans.request().hasField("virtualid") and not self.editVirtualForm.isSuccessful():
            try:
                self.virtualFormInput = self.getVirtualId(trans.request().field("virtualid"))
                self.trans.request().delField("virtualid")
            except KeyError: # Faulty virtualid
                self.virtualFormInput = None
        else:
            self.virtualForm.reset()

        
        if self.userFormInput:
            self.editUserForm.seed(self.userFormInput)
            action = "Edit"
        else:
            action = "Add"

        if action == "Edit":
            self.startBox("Edit user")
            if self.userForm.isSuccessful():
                self.writeln('<span class="error">User has been edited/added</span><br>')
            if self.userForm.error():
                self.writeln('<span class="error">%s</span>' % self.userForm.error())
            self.write(self.editUserForm.dump())
            self.endBox()

        if action == "Add":
            self.startBox("Add user")
            self.write(self.userForm.dump())
            self.endBox()


        # Draw virtual box
        if action == "Edit":
            self.startBox("Virtuals")

            #self.virtualForm.domain.clearChoices()
            #self.editVirtualForm.domain.clearChoices()
            #for domain in self.getDomains(self.userFormInput["company"]):
            #    self.virtualForm.domain.addChoice(domain, domain)
            #    self.editVirtualForm.domain.addChoice(domain, domain)
                
            r = self.getVirtual(self.userFormInput["user"])
            if r:
                self.writeln('<table border="0" cellspacing="2" cellpadding="2">')
                self.writeln('<tr>')
                count = 0
                for i in r:
                    id,alias,dest,username,status = i
                    if status:
                        self.writeln('<td><a href="Users?userid=%s&virtualid=%s">%s</td>' % (username,id,alias))
                    else:
                        self.writeln('<td><a class="error" href="Users?userid=%s&virtualid=%s">%s</td>' % (username,id,alias))
                    if count % 2:
                        self.writeln('</tr><tr>')
                    count +=1
                self.writeln('</table>')

            self.virtualForm.seed({'user': self.userFormInput["user"], 'company': self.userFormInput["company"]})

            if self.virtualFormInput:
                self.editVirtualForm.seed(self.virtualFormInput)
                self.write(self.editVirtualForm.dump())
            else:
                if self.virtualForm.error():
                    self.writeln('<div class="error">%s</div>' % self.virtualForm.error())
                self.writeln(self.virtualForm.dump())

            self.endBox()

        
            
    def sleep(self,trans):
        self.resetForms()
        self.virtualFormInput = None
        self.userFormInput = None
        SitePage.sleep(self,trans)
        
    def setquota(self,user,quota,type):
        self.syslog.write(self.getUser(), "Setting quota for %s: (%s %s)" % (user, quota, type))
        self.cyrus.setquota(user,quota,type)

    def getquota(self,user):
        return self.cyrus.getquota(user)

    def rmquota(self,user):
        self.syslog.write(self.getUser(), "Removing quota for %s" % user)
        self.cyrus.rmquota(user)

    def addUser(self,values):
        password = self.passcrypt(values["password"])
        user = values["user"]
        first = values["firstname"]
        last = values["lastname"]
        company = values["company"]
        status = 0
        if values["active"] == "status":
            status = 1
        quota = values["quota"]
        quota_type = values["quota_type"]

        self.cyrus.addUser(user, quota, quota_type)
        self.db.addUser(user, first, last, password, company, status)
        self.syslog.write(self.getUser(), "Adding user %s" % user)

    def editUser(self, values):
        user = values["user"]
        first = values["firstname"]
        last = values["lastname"]
        company = values["company"]
        status = 0
        if values["active"] == "status":
            status = 1
        quota = values["quota"]
        quota_type = values["quota_type"]
        password = None
        if values["password"]:
            password = self.passcrypt(values["password"])

        self.cyrus.editUser(user, quota, quota_type)
        self.db.editUser(user, first, last, password, status, company)
        if type(values["access"]) is not types.ListType:
            values["access"] = [values["access"]]
        self.db.setAccess(user, values["access"])
        self.syslog.write(self.getUser(), "Edited user %s" % user)


    def delUser(self,user):
        #self.cyrus.delUser(user)
        self.db.delUser(user)
        self.db.setAccess(user, [None])
        self.syslog.write(self.getUser(), "Deleted user %s" % user)


    def getQuotaTypes(self):
        """ Returns a list of valid quota types """
        types = self.conf.get("cyrus", "quota_types")
        types = types.split(",")
        return types

    def compEdit(self,id,values):
        self.db.compEdit(id,values)
        self.syslog.write(self.getUser(), "Edited company %s: %s" % (id, values))

    def compAdd(self,fields):
        self.syslog.write(self.getUser(), "Adding company: %s" % fields)
        return self.db.compAdd(fields)


    def compDel(self,id):
        info = self.compGet(id=id)
        self.db.compDel(id)
        self.syslog.write(self.getUser(), "Deleted company: %s" % id)

    
    def userSearch(self,search):
        data = self.db.userSearch(search)
        for user in data.keys():
            data[user]["quota"] = self.getquota(user)
    
        return data

    def passcrypt(self,password):
        method = self.conf.get("global", "pwdtype")
        return Auth.passcrypt(password, method=method)

    def getDomains(self, company):
        """ Returns a list of domains connected to a company """
        return self.db.getDomains(company)

    def getVirtualId(self,id):
        return self.db.getVirtualId(id)

    def getVirtual(self,user):
        """ Get all virtuals for a user"""
        return self.db.getVirtual(user)

    def delVirtual(self,id):
        info = self.db.getVirtualId(id)
        self.db.delVirtual(id)
        self.syslog.write(self.getUser(), "Deleted virtual: %s" % info)

    def addVirtual(self,alias,dest,user=None,status=1):
        self.db.addVirtual(alias,dest,user=user,status=status)
        self.syslog.write(self.getUser(), "Adding virtual for %s: (%s, %s)" % (user, alias, dest))

    def updateVirtual(self, id ,dest, status):
        self.db.updateVirtual(id, dest, status)
        self.syslog.write(self.getUser(), "Edited virtual id %s: (%s, %s)" % (id, dest, status))

     
    def compGet(self,id=None):
        return self.db.compGet(id=id)

    def numUsers(self):
        return self.db.numUsers()


    def getUserInfo(self,user):
        data = self.db.getUserInfo(user)
        if not len(data):
            return None
        quota = self.cyrus.getquota(user)
        data["quota_used"] = quota[1]
        data["quota"] = quota[2]
        return data
