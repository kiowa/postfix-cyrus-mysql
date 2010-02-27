import imaplib,re
#import md5pwd,base64,MySQLdb,re


Commands = {
    'SETACL': ('AUTH', 'SELECTED'),
    'GETACL': ('AUTH', 'SELECTED'),
    'GETQUOTA': ('AUTH', 'SELECTED'),
    'SETQUOTA': ('AUTH', 'SELECTED'),
    'NAMESPACE': ('AUTH',)
    }

DEFAULT_SEP='.'
QUOTE = '"'
imaplib.Commands.update(Commands)

#re_sep = re.compile(r"\(\(\"INBOX.\" \"(.)\"\)\)", re.IGNORECASE)
re_sep = re.compile(r".*user(.).*", re.IGNORECASE)

class IMAP4(imaplib.IMAP4):

    def getsep(self):
        """Gets mailbox separator"""

        name = 'NAMESPACE'
        typ, dat = self._simple_command(name)
        if not self.untagged_responses.has_key(name):
            raise self.error('no NAMESPACE response from server')
        namespace = self.untagged_responses[name][0]
        res = re_sep.match(namespace)
        if res:
            return res.group(1)
        return DEFAULT_SEP
        
    def getacl(self, mailbox):
        """Gets acl on mailbox"""
        name = 'GETACL'
        rsname = 'ACL'
        typ, dat = self._simple_command(name, mailbox)
        return self._untagged_response(typ, dat, rsname)

    def setacl(self, mailbox, id, acl):
        """Sets acl for a mailbox"""
        return self._simple_command('SETACL', mailbox, id, acl)
    
    def getquota(self, mailbox):
        """Gets quota on a mailbox"""
        name = 'GETQUOTA'
        rsname = 'QUOTA'
        typ, dat = self._simple_command(name, mailbox)
        return self._untagged_response(typ, dat, rsname)

    def setquota(self, mailbox, type, limit):
        """Sets quota on a mailbox
        type : STORAGE|MESSAGE (Message is currently not supported with Cyrus)
        limit : number
        """
        if not limit:
            return self._command('SETQUOTA',mailbox,'()')
        quota = "(%s %s)" % (type, limit)
        return self._simple_command('SETQUOTA', mailbox, quota)


class Cyrus:
    def __init__(self,config):
        self.cyr_host = config.get("cyrus","host")
        self.cyr_user = config.get("cyrus","user")
        self.cyr_pass = config.get("cyrus","password")
        self.imap = IMAP4(self.cyr_host)
        self.imap.login(self.cyr_user,self.cyr_pass)


    def setquota(self,user,quota,type):
        mbox = "user."+user
        self.getImap().setquota(mbox,type,quota)


    def getquota(self,mbox):
        """ Returns used_quota,quota """
        mbox = "user."+mbox
        status,data = self.getImap().getquota(mbox)
        if status == "OK":
            m = re.search('\((\S+) ([0-9]+) ([0-9]+)\)',data[0])
            if m:
                return m.group(1),m.group(2),m.group(3)
            else:
                return None,None,""
        else:
            return None,None,""

    def rmquota(self,mbox):
        """ Removes quota for a specified mbox """
        mbox = "user."+mbox
        self.getImap().setquota(mbox,None,None)
        

    def getImap(self):
        """ Convenience function to always return a logged in imap connection """
        try:
            self.imap.noop()
            imap = self.imap
        except:
            self.imap.logout()
            self.imap = IMAP4(self.cyr_host)
            self.imap.login(self.cyr_user,self.cyr_pass)
        return self.imap
    

        
    
    def addUser(self,user,quota,quota_type):
        self.getImap().setacl("user.%s" % user,"cyrus","c")
        self.getImap().create("user.%s" % user)
	self.getImap().create("user.%s.spam" % user)
	self.getImap().create("user.%s.ham" % user)
        if quota:
            self.setquota(user,quota,quota_type)
        

    def editUser(self, user, quota, quota_type):
        if not quota:
            self.rmquota(user)
        else:
            self.setquota(user,quota,quota_type)

    def delUser(self,user):
        self.getImap().setacl("user.%s" % user,"cyrus","c")
        self.getImap().delete("user.%s" % user)
        

    def loginUser(self,user,passwd):
        imap = imaplib.IMAP4(self.cyr_host)
        try:
            imap.login(user,passwd)
            imap.logout()
            return 1
        except:
            self.session().setValue("user_uname",None)
            return 0
        
