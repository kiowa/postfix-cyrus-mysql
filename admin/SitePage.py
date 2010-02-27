import time,imaplib, Auth, syslog, types
from WebKit.Page import Page
from Cyrus import Cyrus
from ConfigParser import ConfigParser

class SitePage(Page):
    def __init__(self):
        # a list of all available modules
        # ("short_desc", "filename", "required_access_level", "long_desc")
        self.modules = [
                ("Bedrifter","Companies.py","comp","Her kan du editere bedriftsdatabasen"),
                ("Brukere","Users.py","mail","Legge til eller endre brukere"),
                ("MailingLists","Sympa.py","mail","Administrasjon av epost-lister"),
                ("Virtual/Aliaser","Virtual.py","mail","Gj&oslash;re endringer i aliases og virtuals som ikke er knyttet opp mot brukere"),
                ]
    
        Page.__init__(self)
        self.syslog = Syslog()
        conf = ConfigParser()
        self.conf = conf
        conf.readfp(open("site.conf"))
        if conf.get("global","database") == "mysql":
            from Mysql import Database

        self.cyrus = Cyrus(conf)
        self.db = Database(conf)
        self.allow_caching = 0


    def awake(self,trans):
        # Awake our superclass
        self.trans = trans
        app = trans.application()
        session = trans.session()
        request = self.trans.request()
        response = trans.response()
        Page.awake(self,trans)
        if not self.allow_caching:
            response.setHeader("Cache-Control","no-cache, must-revalidate")
            response.setHeader("Pragma","no-cache")
            year, month, day, hh, mm, ss, wd, y, z = time.gmtime(time.time())
            s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
                ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][wd],
                day, [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov',
                      'Dec'][month], year,hh, mm, ss)
            response.setHeader("Expires",s)
            response.setHeader("Last-Modified",s)

        loginid = session.value('loginid',None)
        if loginid:
            session.delValue("loginid")
        # Are they logging out?
        if request.hasField("logout"):
            session.values().clear()
            request.setField('extra', 'You have been logged out.')
            request.setField('action', request.urlPath().split('/')[-1])
            request.delField('logout')
            app.forward(trans, 'Index')
        elif request.hasField("username") and request.hasField("password"):
            # They are logging in. Clear session.
            session.values().clear()
            username = request.field("username")
            password = request.field("password")
            # And check if they can log in.
            if request.field("loginid","nologin") == loginid and self.loginUser(username, password, method=self.conf.get("global", "pwdtype")):
                # Successful login.
                # Clear out the login parameters
                request.delField('username')
                request.delField('password')
                #request.delField('login')
                request.delField('loginid')
            else:
                # Failed login attempt; have them try again.
                request.delField('username')
                request.delField('password')
                request.delField('login')
                request.delField('loginid')
                request.setField('extra', 'Login failed.  Please try again.')

        if self.needAccess():
            if not self.needAccess() in self.session().value("access",[]):
                request.setField('extra','Du har ikke adgang til denne siden (level: %s)' % self.needAccess())


    def htBodyArgs(self):
        return ""

    def writeStyleSheet(self):
        self.writeln('\t<link rel="stylesheet" href="StyleSheet.css" type="text/css">')

    def writeMenu(self):
        pass

    def writeCenter(self):
        pass


    def title(self):
        return "NS Admin"

    def htTitle(self):
        return ""

    def writeNavbar(self):
        # Header
        self.writeln('<div id="banner">%s: %s' % (self.title(),self.htTitle()))
        self.writeln('<br>')
        access = self.session().value("access", [])
        for mod in self.modules:
            short, filename, req_access, long = mod
            if req_access in access:
               self.writeln('<a href="%s">%s</a> | ' % (filename, short))

        self.writeln('<a href="?logout=1">Logout</a>')
        self.writeln('</div>')
        
    def needAccess(self):
        """ Return the needed access-level required to open this page """
        return 0

    def writeBodyParts(self):
        request = self.trans.request()
        if not self.getUser() and not request.urlPath().split("/")[-1] == "Login":
            self.trans.application().forward(self.trans,"Login")

        if self.needAccess():
            if not self.needAccess() in self.session().value("access", []):
                self.writeln('You do not have access to this page')
                return
        

        # Navbar
        self.writeNavbar()
        # Left menu
        self.writeln('<div id="leftcontent">')
        self.writeMenu()
        self.writeln('</div>')

        # Center page
        self.writeln('<div id="centercontent">')
        self.writeCenter()
        self.writeln('</div>')


    def respond(self,trans):
        Page.respond(self,trans)


    def getUser(self):
        """ Gets the name of the logged-in user, or returns None if there is
        no logged-in user."""
        return self.session().value("user_uname", None)


    def startBox(self, title):
        self.writeln('<p><div class="box">')
        self.writeln('<h1>%s</h1>' % title)

    def endBox(self):
        self.writeln('</div></p>')


    def loginUser(self, user, passwd, method="md5"):
        """ Authenticate a user """
        self.loggedInUser = None
        if Auth.login(user, passwd, self.db):
            access = self.getAccess(user)
            if access:
                self.session().setValue("user_uname", user)
                self.session().setValue("access", access)
                self.syslog.write(user, "Successful login")
                return 1
        self.session().setValue("user_uname", None)
        self.syslog.write(user, "Login failed")
        return 0


    def getAccess(self,user):
        """ Return a list of access-rights for a user """
        return self.db.getAccess(user)



class Syslog:
    def __init__(self):
        syslog.openlog("nsadmin", syslog.LOG_USER, syslog.LOG_MAIL)

    def write(self, user, msg):
        syslog.openlog("nsadmin/"+user, syslog.LOG_USER, syslog.LOG_MAIL)
        syslog.syslog(msg)

    def read(self):
        data = []
        f = open("/var/log/mail.log")
        l = f.readline()
        while l:
            if l.split()[4][:7] == "nsadmin":
                data.append(l)
            l = f.readline()
        return data
    
