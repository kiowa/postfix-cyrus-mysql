from SitePage import SitePage
from FormKit import Form, Fields, Validators
from FormKit.FormKitMixIn import FormKitMixIn
from Validators import ValidEmail, AliasExist, VirtualExist

class Virtual(FormKitMixIn, SitePage):
    hits = ({}, {})
    
    def htTitle(self):
        return "Virtual/aliases"


    def needAccess(self):
        return "global"


    def __init__(self):
        SitePage.__init__(self)

        # Search form
        self.searchForm = searchForm = Form.Form()
        self.addForm(searchForm)
        searchForm.addField(Fields.TextField("search", attributes={'size':5}))
        searchForm.addField(Fields.WebKitSubmitButton("virtualget",label="Search"))


        # Virtual add form
        self.virtualForm = virtualForm = Form.Form(validators=[VirtualExist(self.db), ValidEmail()])
        self.addForm(virtualForm)
        virtualForm.addField(Fields.TextField("virtual", label="Virtual", validators=[Validators.NotEmpty()]))
        virtualForm.addField(Fields.TextField("domain", label="Domain", validators=[Validators.NotEmpty()]))
        virtualForm.addField(Fields.TextField("dest", label="Destination", validators=[Validators.NotEmpty()]))
        virtualForm.addField(Fields.CheckboxSet("active", label="Active"))
        virtualForm.active.addChoice("status", "")
        virtualForm.seed({"active":"status"})
        virtualForm.addField(Fields.WebKitSubmitButton("add_virtual", label="Add"))

        # Virtual edit form
        self.editVirtualForm = editVirtualForm = Form.Form()
        self.addForm(editVirtualForm)
        editVirtualForm.addField(Fields.TextField("virtual", label="Virtual", attributes={"readonly":1}))
        editVirtualForm.addField(Fields.TextField("domain", label="Domain", attributes={"disabled":1}))
        editVirtualForm.addField(Fields.TextField("dest", label="Destination", validators=[Validators.NotEmpty()]))
        editVirtualForm.addField(Fields.HiddenField("id",label="id"))
        editVirtualForm.addField(Fields.CheckboxSet("active", label="Active"))
        editVirtualForm.active.addChoice("status", "")
        editVirtualForm.addField(Fields.WebKitSubmitButton("edit_virtual", label="Update"))
        editVirtualForm.addField(Fields.WebKitSubmitButton("del_virtual", label="Delete"))


        # Alias add form
        self.aliasForm = aliasForm = Form.Form()
        self.addForm(aliasForm)
        aliasForm.addField(Fields.TextField("alias", label="Alias", validators=[Validators.NotEmpty(), AliasExist(self.db)]))
        aliasForm.addField(Fields.TextField("dest", label="Destination", validators=[Validators.NotEmpty()]))
        aliasForm.addField(Fields.CheckboxSet("active", label="Active"))
        aliasForm.active.addChoice("status", "")
        aliasForm.seed({"active":"status"})
        aliasForm.addField(Fields.WebKitSubmitButton("add_alias", label="Add"))
  

        # Alias edit form
        self.editAliasForm = editAliasForm = Form.Form()
        self.addForm(editAliasForm)
        editAliasForm.addField(Fields.TextField("alias", label="Alias", attributes={"readonly":1}))
        editAliasForm.addField(Fields.TextField("dest", label="Destination", validators=[Validators.NotEmpty()]))
        editAliasForm.addField(Fields.HiddenField("id",label="id"))
        editAliasForm.addField(Fields.CheckboxSet("active", label="Active"))
        editAliasForm.active.addChoice("status", "")
        editAliasForm.addField(Fields.WebKitSubmitButton("edit_alias", label="Update"))
        editAliasForm.addField(Fields.WebKitSubmitButton("del_alias", label="Delete"))


    def actions(self):
        return ["virtualget", "add_virtual", "edit_virtual", "del_virtual", "add_alias", "edit_alias", "del_alias"]


    def add_virtual(self):
        if self.virtualForm.isSuccessful():
            values = self.virtualForm.values()
            alias = values["virtual"]+"@"+values["domain"]
            status = 0
            dest = values["dest"]
            if values["active"] == "status":
                status = 1
            self.addVirtual(alias, dest, status=status)

    def edit_virtual(self):
        if self.editVirtualForm.isSuccessful():
            values = self.editVirtualForm.values()
            id = values["id"]
            status = 0
            dest = values["dest"]
            if values["active"] == "status":
                status = 1
            self.updateVirtual(id, dest, status)

    def del_virtual(self):
        if self.editVirtualForm.isSuccessful():
            self.delVirtual(self.editVirtualForm.values()["id"])
            


    def add_alias(self):
        if self.aliasForm.isSuccessful():
            values = self.aliasForm.values()
            status = 0
            alias, dest = values["alias"], values["dest"]
            if values["active"] == "status":
                status = 1
            self.aliasAdd(alias, dest, status)


    def del_alias(self):
        if self.editAliasForm.isSuccessful():
            self.aliasDel(self.editAliasForm.values()["id"])


    def edit_alias(self):
        if self.editAliasForm.isSuccessful():
            values = self.editAliasForm.values()
            status = 0
            id, alias, dest = values["id"], values["alias"], values["dest"]
            if values["active"] == "status":
                status = 1
            self.aliasEdit(id, alias, dest, status)


    


    def virtualget(self):
        self.hits = self.aliasSearch(self.searchForm.values()["search"])


    def awake(self, trans):
        SitePage.awake(self, trans)
        self.trans = trans
        request = trans.request()

        #self.virtualForm.domain.clearChoices()
        #self.editVirtualForm.domain.clearChoices()
        #for domain in self.getDomains(None):
        #    self.virtualForm.domain.addChoice(domain, domain)
        #    self.editVirtualForm.domain.addChoice(domain, domain)

        self.mode = None
        self.dataInput = {}
        if trans.request().hasField("aid"):
            self.mode = "AID"
            try:
                self.dataInput = self.aliasGet(request.field("aid"))
            except:
                self.mode = None
        elif trans.request().hasField("vid"):
            self.mode = "VID"
            try:
                self.dataInput = self.getVirtualId(request.field("vid"))
            except:
                self.mode = None
        elif trans.request().hasField("new"):
            if trans.request().field("new") == "alias":
                self.mode = "ALIAS"
            if trans.request().field("new") == "virtual":
                self.mode = "VIRTUAL"
        else:
            self.mode = None

    def writeMenu(self):
        self.write(self.searchForm.startTags())
        self.write(self.searchForm.search.tag())
        self.write(self.searchForm.virtualget.tag())
        self.write(self.searchForm.endTags())
        if self.searchForm.isSuccessful():
            aliases, virtuals = self.hits
            self.writeln('<p>Aliases<br>')
            self.writeln("%s hit(s)<br>" % len(aliases))
            for i in aliases.keys():
                if aliases[i]["status"]:
                    status = "enabled"
                else:
                    status = "disabled"
                self.writeln('<a class="%s" href="Virtual?aid=%s">%s</a><br>' % (status, i,aliases[i]["alias"]))
            self.writeln('</p>')
            self.writeln('<p>Virtuals<br>')
            self.writeln('%s hit(s)<br>' % len(virtuals))
            for i in virtuals.keys():
                if virtuals[i]["status"]:
                    status = "enabled"
                else:
                    status = "disabled"
                self.writeln('<a class="%s" href="Virtual?vid=%s">%s</a><br>' % (status, i,virtuals[i]["alias"]))
            self.writeln('</p>')


    def writeCenter(self):
        #request = self.trans.request()

        self.writeln('<p class="box"><a href="Virtual?new=alias">New Alias</a> | <a href="Virtual?new=virtual">New Virtual</a></p>')

        if self.aliasForm.isSuccessful() or self.virtualForm.isSuccessful():
            self.writeln("Successfully added.")
            return

        if self.editAliasForm.isSuccessful() or self.editVirtualForm.isSuccessful():
            self.writeln("Successfully edited")
            return

        
        if self.mode == "ALIAS":
            self.startBox("New alias")
            self.writeln(self.aliasForm.dump())
            self.endBox()
        if self.mode == "VIRTUAL":
            self.startBox("New virtual")
            if self.virtualForm.error():
                self.writeln('<span class="error">%s</span>' % self.virtualForm.error())
            self.writeln(self.virtualForm.dump())
            self.endBox()

        if self.mode == "AID":
            self.startBox("Edit alias")
            self.editAliasForm.seed(self.dataInput)
            self.writeln(self.editAliasForm.dump())
            self.endBox()

        if self.mode == "VID":
            self.startBox("Edit virtual")
            self.editVirtualForm.seed(self.dataInput)
            self.writeln(self.editVirtualForm.dump())
            self.endBox()

        

    def sleep(self,trans):
        self.resetForms()
        SitePage.sleep(self,trans)



    def aliasAdd(self,alias,dest,status):
        self.db.aliasAdd(alias,dest,status)
        self.syslog.write(self.getUser(), "Adding alias: (%s, %s, %s)" % (alias, dest, status))


    def aliasEdit(self,id,alias,dest,status):
        self.db.aliasEdit(id,alias,dest,status)
        self.syslog.write(self.getUser(), "Edited alias %s: (%s, %s, %s)" % (id, alias, dest, status))


    def aliasDel(self, id):
        info = self.aliasGet(id)
        self.db.aliasDel(id)
        self.syslog.write(self.getUser(), "Deleted alias: %s" % info)


    def aliasSearch(self, search):
        """ Searches for aliases/virtuals """
        aliases = {}
        virtuals = {}

        for i in self.db.aliasSearch(search):
            aliases[i[0]] = { "alias": i[1], "status": i[2] }

        for i in self.db.virtualSearch(search):
            virtuals[i[0]] = { "alias": i[1], "status": i[2] }

        return (aliases,virtuals)

    def aliasGet(self, id):
        data = self.db.aliasGet(id)
        alias = { "id": data[0], "alias": data[1], "dest": data[2] }
        if data[3]:
            alias["active"] = "status"
        return alias

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
