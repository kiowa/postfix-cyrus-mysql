from SitePage import SitePage
from FormKit import Form, Fields, Validators
from FormKit.FormKitMixIn import FormKitMixIn
from Validators import CompanyDoesNotExist, UniquePrefix, CompanyAccess
from Brreg import Brreg


class Companies(FormKitMixIn, SitePage):
    def __init__(self):

        SitePage.__init__(self)
        self.formInput = None
        self.tempFormInput = None
        ### Company brreg fetch form
        self.brregForm = brregForm = Form.Form()
        self.addForm(brregForm)
        brregForm.addField(Fields.TextField("orgnr",label="ORG-NR",validators=[Validators.ExactLength(9),Validators.ConvertToInt()]))
        brregForm.addField(Fields.WebKitSubmitButton("brreg",label="Fetch"))
        
        

        ### Company add form
        self.compForm = compForm = Form.Form()
        self.addForm(compForm)
        compForm.addField(Fields.TextField("name",label="Name", validators=[Validators.MinLength(2), CompanyDoesNotExist(self.db)]))
        compForm.addField(Fields.TextField("prefix", label="Prefix", validators=[UniquePrefix(self.db), Validators.MinLength(2)], attributes={'size':3}))
        compForm.addField(Fields.TextAreaField("businessaddr", label="Business Address", attributes={"rows":2, "cols":30}))
        compForm.addField(Fields.TextField("county",label="County"))
        compForm.addField(Fields.TextAreaField("postaddr", label="Post Address",attributes={"rows":2, "cols":30}))
        compForm.addField(Fields.TextField("email",label="Email"))
        compForm.addField(Fields.TextField("url",label="Webpage"))
        compForm.addField(Fields.TextField("telephone",label="Telephone"))
        compForm.addField(Fields.TextField("fax",label="Fax"))
        compForm.addField(Fields.TextField("mobile", label="Cellphone"))
        compForm.addField(Fields.TextField("contact",label="Contact Person"))
        compForm.addField(Fields.HiddenField("orgnr"))
        

##        for i in self.compKeys():
##            id,text,type,size,position = i
##            validators = []
##            for j in self.getValidators(id):
##                validators.append(eval("Validators."+j))
##            compForm.addField(eval("Fields." + type + "(text, label=text, validators=validators, attributes={'size':size})"))
        self.compForm.addField(Fields.WebKitSubmitButton("add",
                                                         label="Add"))


        ### Company edit form
        self.editCompForm = editCompForm = Form.Form()
        self.addForm(editCompForm)
        editCompForm.addField(Fields.TextField("name",label="Name"))
        editCompForm.addField(Fields.TextField("prefix", label="Prefix", attributes={"readonly":1, "size":3}))
        editCompForm.addField(Fields.HiddenField("id"))
        editCompForm.addField(Fields.TextAreaField("businessaddr", label="Business Address", attributes={"rows":2, "cols":30}))
        editCompForm.addField(Fields.TextField("county",label="County"))
        editCompForm.addField(Fields.TextAreaField("postaddr", label="Post Address", attributes={"rows":2, "cols":30}))
        editCompForm.addField(Fields.TextField("email",label="Email"))
        editCompForm.addField(Fields.TextField("url",label="Webpage"))
        editCompForm.addField(Fields.TextField("telephone",label="Telephone"))
        editCompForm.addField(Fields.TextField("fax",label="Fax"))
        editCompForm.addField(Fields.TextField("mobile", label="Cellphone"))
        editCompForm.addField(Fields.TextField("contact",label="Contact Person"))
        editCompForm.addField(Fields.TextField("orgnr", label="Org-NR", validators=[Validators.ExactLength(9), Validators.ConvertToInt()]))



##        for i in self.compKeys():
##            id,text,type,size,position = i
##            validators = []
##            for j in self.getValidators(id):
##                validators.append(eval("Validators."+j))
##            editCompForm.addField(eval("Fields." + type + "(text, label=text, validators=validators, attributes={'size':size})"))
        self.editCompForm.addField(Fields.WebKitSubmitButton("edit",
                                                             label="Save"))
        self.editCompForm.addField(Fields.WebKitSubmitButton("delete",
                                                             label="Delete"))
        self.editCompForm.addField(Fields.WebKitSubmitButton("brreg_update",
                                                             label="Update from Brreg"))
                                                             
        
        ### Company search form
        self.searchForm = searchForm = Form.Form()
        self.addForm(searchForm)
        searchForm.addField(Fields.TextField("search", attributes={'size':5}))
        searchForm.addField(Fields.WebKitSubmitButton("compget",label="Search"))


    def actions(self):
        return ["add","edit","compget","delete","brreg", "brreg_update"]

    def brreg(self):
        if self.brregForm.isSuccessful():
            self.tempFormInput = Brreg().load_org(int(self.brregForm.values()["orgnr"]))

    def brreg_update(self):
        if self.editCompForm.isSuccessful():
            self.formInput = Brreg().load_org(int(self.editCompForm.values()["orgnr"]))
            self.formInput["id"] = self.editCompForm.values()["id"]



    def delete(self):
        if self.editCompForm.isSuccessful():
            self.compDel(self.editCompForm.values()["id"])
            self.delCompAccess(self.editCompForm.values()["id"])
            self.formInput = None
        else:
            pass

    def compget(self):
        """ Search for companies"""
        self.companies = self.compSearch(self.searchForm.values()["search"])
        if len(self.companies) == 1:
            for key in self.companies.keys():
                print "KEY: ", key
                self.formInput = self.compGet(key)
                print "FOOBAR",self.formInput
                #self.formInput["id"] = key
            
    def add(self):
        if self.compForm.isSuccessful():
            id = self.compAdd(self.compForm.values())
            self.formInput = self.compForm.values()
            self.formInput["id"] = id
            if not self.authUser(self.getUser(), id):
                self.addCompAccess(self.getUser(), id)
        else:
            pass
        
    def edit(self):
        if self.editCompForm.isSuccessful():
            self.compEdit(self.id,self.editCompForm.values())
            self.formInput = self.editCompForm.values()
        else:
            pass

    def htTitle(self):
        return "Companies"

    def awake(self,trans):
        SitePage.awake(self,trans)

        self.editCompForm.id.clearValidators()
        #self.editCompForm.id.addValidator(CompanyAccess(self.getUser(), self.db))

        if trans.request().hasField('id'):
            self.id = id = trans.request().field('id')
            #if not self.formInput:
                #self.formInput = {}
            self.formInput = self.compGet(id=id)
            #if self.formInput:
            #      self.formInput["id"] = id



    def needAccess(self):
        return "comp"
    

    def writeCenter(self):
        if self.formInput:
            self.editCompForm.seed(self.formInput)
            action = "Edit"
        else:
            action= "Add"
            if self.tempFormInput:
                self.compForm.seed(self.tempFormInput)

        if action == "Add":
            self.startBox("Add company")
            self.write(self.brregForm.dump())
            self.write(self.compForm.dump())
            self.endBox()
            
        if action == "Edit":
            self.startBox("Edit company")
            self.writeln('<a href="Companies">New</a>')
            if self.compForm.isSuccessful():
                self.writeln('<span class="error">Successfully added company</span>')
            if self.editCompForm.isSuccessful() and not self.formInput.has_key("sektorkode"):
                self.writeln('<span class="error">Successfully edited company</span>')
            if self.editCompForm.isSuccessful() and self.formInput.has_key("sektorkode"):
                self.writeln('<span class="error">Retrieved settings from Brreg, remember to save your data</span>')
                
            self.write(self.editCompForm.dump())
            self.endBox()
            id = self.formInput["id"]
            r = None
            if id:
                r = self.getUserByCompany(id)
            if r:
              	self.startBox("Users connected to this company")
                self.writeln('<table border="0" cellspacing="2" cellpadding="2">')
                self.writeln('<tr>')
                count = 0
                for i in r.keys():
                    #user,first,last = i
                    user = r[i]
                    self.writeln('<td><a href="Users?userid=%s">%s (%s %s)</a>' % (i,i,user["first"],user["last"]))
                    for v in user["virtuals"]:
                        self.writeln('%s, ' % v[1])
                    self.writeln('</td>')
                    if count % 2:
                      self.writeln('</tr><tr>')
                    count +=1
                self.writeln('</table>')
                self.endBox()
				
    def register(self,fields):
        self.compAdd(fields)
            

    def writeMenu(self):
        self.write(self.searchForm.startTags())
        self.write(self.searchForm.search.tag())
        self.write(self.searchForm.compget.tag())
        self.write(self.searchForm.endTags())

        if self.searchForm.isSuccessful():
            for i in self.companies.keys():
                self.writeln('<a href="Companies?id=%s">%s</a><br>' % (i,self.companies[i]["name"]))
        
    def sleep(self,trans):
        self.resetForms()
        self.formInput = None
        self.tempFormInput = None
        # Clear id fields.
        if self.trans.request().hasField("id"):
            self.trans.request().delField("id")
        SitePage.sleep(self,trans)


    def addCompAccess(self, uname, company):
        self.db.addCompAccess(uname, company)

    def delCompAccess(self, company):
        self.db.delCompAccess(company)

    def compKeys(self):
        """ Returns all available company options """
        return self.db.compKeys()


    def compSearch(self,search):
        return self.db.compSearch(search)

    def getUserByCompany(self,company,order="username"):
		users = {}
		r = self.db.getUserByCompany(company,order=order)
		for i in r:			
			user,first,last = i
			virtuals = self.db.getVirtual(user)
			users[user] = {"first":first, "last":last, "virtuals":virtuals}
		return users

    def authUser(self, uname, company):
        """ Check if the user has access to edit this company """
        return self.db.authUser(uname, company)


    def compAdd(self, fields):
        return self.db.compAdd(fields)
    
    def compGet(self,id=None):
        return self.db.compGet(id=id)

    def compEdit(self,id,values):
        self.db.compEdit(id,values)
        self.syslog.write(self.getUser(), "Edited company %s: %s" % (id, values))

    def compDel(self,id):
        info = self.compGet(id=id)
        self.db.compDel(id)
        self.syslog.write(self.getUser(), "Deleted company: %s" % id)
