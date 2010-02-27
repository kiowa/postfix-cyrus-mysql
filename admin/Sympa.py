from SitePage import SitePage
from FormKit import Form, Fields, Validators
from FormKit.FormKitMixIn import FormKitMixIn
from Validators import CompanyAccess, ListExist

class Sympa(FormKitMixIn, SitePage):

    def __init__(self):
        SitePage.__init__(self)
        self.page1 = page1 = Form.Form()
        self.addForm(page1)
        page1.addField(Fields.SelectField('company', label='Company'))
        page1.addField(Fields.WebKitSubmitButton("cont", label="Continue->"))
                       
        self.page2 = page2 = Form.Form(validators=[ListExist(self.db)])
        self.addForm(page2)
        page2.addField(Fields.TextField('listname', label='Listname', validators=[Validators.NotEmpty()]))
        page2.addField(Fields.TextField('domain', label='Domain'))
        page2.addField(Fields.HiddenField('company', label='Company'))
        page2.addField(Fields.WebKitSubmitButton('abort', label='Abort'))
        page2.addField(Fields.WebKitSubmitButton('finish', label='Finish'))


    def htTitle(self):
        return "Sympa mailing list manager"

    def needAccess(self):
        return "mail"
    

    def awake(self, trans):
        SitePage.awake(self, trans)
        self.trans = trans
        comps = self.compGet()
        self.page1.company.clearChoices()
        for id,comp in comps:
            self.page1.company.addChoice(id, comp)
        self.page = 1
        #self.page1.company.addValidator(CompanyAccess(self.getUser(), self.db))

    
    def actions(self):
        return ["abort", "finish", "cont"]


    def cont(self):
        if self.page1.isSuccessful():
            #self.page2.domain.clearChoices()
            #for domain in self.getDomains(self.page1.values()["company"]):
            #    self.page2.domain.addChoice(domain, domain)
            self.page2.seed({"company":self.page1.values()["company"]})
            self.page = 2

    def abort(self):
        self.page = 1

    def finish(self):
        if self.page2.isSuccessful():
            company = self.page2.values()["company"]
            prefix = self.compGet(id=company)["prefix"]
            domain = self.page2.values()["domain"]
            listname = self.page2.values()["listname"]
            self.addSympa(company, prefix, domain, listname)
            self.page = 1
        else:
            self.page = 2


    def writeCenter(self):
	#self.writeln("Mailing list administration has been deactivated (too many bugs)<br>")
	#self.writeln("Alexander Brill <alex@nettstudio.no<br>")
	#return
        if self.page == 1:
            self.startBox("Add mailing list aliases (page 1/2)")
            self.write(self.page1.dump())
            self.endBox()
        else:
            self.startBox("Add mailing list aliases (page 2/2)")
            if self.page2.error():
                self.write('<span class="error">'+self.page2.error()+'</span>')
            self.write(self.page2.dump())
            self.endBox()

    def sleep(self, trans):
        self.resetForms()
        SitePage.sleep(self, trans)

    
    def addSympa(self, company, prefix, domain, listname):
        self.syslog.write(self.getUser(), "Added sympa list for company %s: %s@%s" % (company,listname,domain))
        self.db.addSympa(company, prefix, domain, listname)

    def getDomains(self, company):
        """ Returns a list of domains connected to a company """
        return self.db.getDomains(company)

     
    def compGet(self,id=None):
        return self.db.compGet(id=id)
