import MySQLdb
from IDN import latin12p, p2latin1


class Database:
    def __init__(self,config):
	""" Initialize the database module.
	config - an active ConfigParser constructor
	"""
	self.sql = MySQLdb.connect(host=config.get("mysql","host"),
	    user=config.get("mysql","user"),
	    passwd=config.get("mysql","password"),
	    db=config.get("mysql","database"))
	#self.cur = self.sql.cursor()

	self.domainsql = MySQLdb.connect(host=config.get("domain","host"),
	    user=config.get("domain","user"),
	    passwd=config.get("domain","password"),
	    db=config.get("domain","database"))
	self.dcur = self.domainsql.cursor()


    def getCursor(self):
	return self.sql.cursor()

    def getVirtualId(self,id):
	""" Get a virtual entry by id"""
	data = {}
	cur = self.getCursor()
	cur.execute("select alias,dest,status from virtual where id=%s",(id))
	r = cur.fetchone()
	if r:
	    alias,dest,status = r
	    alias = p2latin1(alias)
	    data["virtual"] = alias.split("@")[0]
	    data["domain"] = alias.split("@")[1]
	    data["dest"] = p2latin1(dest)
	    data["id"] = id
	    if status:
		data["active"] = "status"
	return data

    def virtualExist(self, virtual):
	""" Return true if this virtual exists """
	cur = self.getCursor()
	cur.execute("select alias from virtual where alias=%s", latin12p(virtual))
	if cur.fetchone():
	    return True
	return False


    def getVirtual(self,user):
	""" Get all virtuals for a user """
	cur = self.getCursor()
	cur.execute("select id,alias,dest,username,status from virtual where username=%s order by alias",(user))
	return p2latin1(cur.fetchall())


    def delVirtual(self,id):
	""" Deletes a specified virtual entry """
	cur = self.getCursor()
	cur.execute("delete from virtual where id=%s",id)


    def addVirtual(self,alias,dest,user=None,status=1):
	""" Adds an virtual entry """
	cur = self.getCursor()
	try:
	    domain = alias.split("@")[1]
	except IndexError:
	    domain = ""
	if user:
	    cur.execute("insert into virtual (alias,dest,username,domain) values(%s,%s,%s,%s)", (latin12p(alias),latin12p(dest),user,latin12p(domain)))
	else:
	    cur.execute("insert into virtual (alias,dest,domain) values(%s,%s,%s)", (latin12p(alias),latin12p(dest),latin12p(domain)))


    def updateVirtual(self,id ,dest, status):
	""" Updates a virtual alias"""
	cur = self.getCursor()
	cur.execute("update virtual set dest=%s, status=%s where id=%s",(latin12p(dest), status, id))


    def virtualSearch(self, search):
	""" Return all virtuals matching this string """
	search = '%%'+search+'%%'
	cur = self.getCursor()
	cur.execute("select id, alias, status from virtual where username='' and alias like %s order by alias", (search))
	return p2latin1(cur.fetchall())


    def addUser(self,user,firstname,lastname,password,company,status):
	""" Add a new user """
	cur = self.getCursor()
	cur.execute("insert into accountuser (username,firstname,lastname,password,company,status) values(%s,%s,%s,%s,%s,%s)",
	    (user,firstname,lastname,password,company,status))

    def editUser(self,user,firstname,lastname,password,status, company):
	""" Edit a users information """
	cur = self.getCursor()
	if password:
	    cur.execute("update accountuser set password=%s, firstname=%s, lastname=%s,status=%s, company=%s where username=%s",
		(password,firstname,lastname,status,company, user))
	else:
	    cur.execute("update accountuser set firstname=%s, lastname=%s,status=%s, company=%s where username=%s",
		(firstname,lastname,status,company, user))


    def getDomains(self, company):
	""" Returns a list of domains connected to a company """
	domains = []
	if company:
	    self.dcur.execute("select name from domains where company=%s order by name", (company))
	else:
	    self.dcur.execute("select name from domains order by name")
	r = self.dcur.fetchall()
	if r:
	    for d in r:
		domains.append(p2latin1(d[0]))
	return domains


    def delUser(self,user):
	""" Remove an user from the database (remember to also remove the user's mailbox """
	cur = self.getCursor()
	cur.execute("delete from accountuser where username=%s",(user))
	cur.execute("delete from virtual where username=%s",(user))

    def getUserInfo(self,user):
	""" Get information about a user """
	data = {}
	cur = self.getCursor()
	cur.execute("select username,firstname,lastname,company,status from accountuser where username=%s",user)
	r = cur.fetchone()
	if r:
	    username,firstname,lastname,company,status = r
	    data["username"] = username
	    data["user"] = username
	    data["firstname"] = firstname
	    data["lastname"] = lastname
	    data["company"] = company
	    data["cid"] = company
	    data["access"] = self.getAccess(username)
	    if status:
		data["active"] = "status"
	return data



    def userSearch(self,search):
	""" Search for a user, firstname or lastname """
	data = {}
	cur = self.getCursor()
	cur.execute("(select username from accountuser where username like '%%%s%%') union (select username from accountuser where firstname like '%%%s%%') union (select username from accountuser where lastname like '%%%s%%')" % (search,search,search))
	r = cur.fetchall()
	if r:
	    for user in r:
		user = user[0]
		data[user] = self.getUserInfo(user)
	return data



    def saAdd(self,user,pref,value):
	""" Add an spamassassin field """
	cur = self.getCursor()
	cur.execute("insert into spamassassin (username,preference,value) values(%s,%s,%s)",(user,pref,value))


    def saEdit(self,prefid,pref,value):
	""" Edit an spamassassin field """
	cur = self.getCursor()
	cur.execute("update spamassassin set value=%s where prefid=%s",(value,prefid))

    def saDel(self,prefid):
	""" Delete an spamassassin preference """
	cur.execute("delete from spamassassin where prefid=%s",(prefid))

    def saGet(self,user,pref=None):
	""" Gets SA preferences for a user """
	cur = self.getCursor()
	if pref:
	    cur.execute("select prefid,value from spamassassin where username=%s and preference=%s",(user,pref))
	else:
	    cur.execute("select prefid,preference,value from spamassassin where username=%s and preference !='required_hits'",(user))
	return cur.fetchall()


    def getCompanies(self,order="name"):
	""" Returns a tuple of all companies """
	cur = self.getCursor()
	cur.execute("select id,name,prefix from companies order by %s",(order))
	return cur.fetchall()


    def getUserByCompany(self,company,order="username"):
	""" Returns a list of all users connected with company """
	cur = self.getCursor()
	cur.execute("select username,firstname,lastname from accountuser where company = %s order by %s",(company,order))
	return cur.fetchall()


    def prefixExist(self, prefix):
	""" Check if a	prefix already exist """
	cur = self.getCursor()
	cur.execute("select name from companies where prefix=%s", prefix)
	if cur.fetchone():
	    return True
	return False


    def compEdit(self,id,values):
	""" Update a company's information """
	cur = self.getCursor()
	v = values
	cur.execute("update companies set name=%s, busaddr=%s, county=%s, postaddr=%s, email=%s, webpage=%s, telephone=%s, fax=%s, cellphone=%s, contact=%s, orgnr=%s where id=%s",
	    (v["name"],
		v["businessaddr"],
		v["county"],
		v["postaddr"],
		v["email"],
		v["url"],
		v["telephone"],
		v["fax"],
		v["mobile"],
		v["contact"],
		v["orgnr"],
		id,
		))

    def compAdd(self,f):
	""" Add a new company """
	cur = self.getCursor()
	cur.execute("insert into companies (name,prefix,busaddr,county,postaddr,email,webpage,telephone,fax,cellphone,contact,orgnr) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
	    (f["name"], f["prefix"], f["businessaddr"], f["county"], f["postaddr"], f["email"], f["url"], f["telephone"], f["fax"], f["mobile"], f["contact"], f["orgnr"]))
	compid = int(cur.lastrowid)
	return compid

    def compSearch(self,search):
	""" Get a dictionary of companies by a search """
	cur = self.getCursor()
	cur.execute("select id from companies where name like '%%%s%%'" % search)
	r = cur.fetchall()
	data = {}
	if r:
	    for id in r:
		id = id[0]
		data[id] = self.compGet(id=id)
	return data


    def compDel(self,id):
	""" Delete a company by id """
	cur = self.getCursor()
	for i in self.getUserByCompany(id):
	    self.delUser(i[0])
	cur.execute("delete from companies where id=%s",id)


    def compGet(self,id=None):
	""" Get companies, or a company if id is specified as a dictionary"""
	cur = self.getCursor()
	if id:
	    cur.execute("select name,prefix,busaddr,county,postaddr,email,webpage,telephone,fax,cellphone,contact,orgnr from companies where id=%s",(id))
	    r = cur.fetchone()
	    if not r:
		return None
	    data = {"id": id,
		"name": r[0],
		"prefix": r[1],
		"businessaddr": r[2],
		"county": r[3],
		"postaddr": r[4],
		"email": r[5],
		"url": r[6],
		"telephone": r[7],
		"fax": r[8],
		"mobile": r[9],
		"contact": r[10],
		"orgnr": r[11],
		}
	    return data
	else:
	    cur.execute("select id,name from companies order by name")
	    r = cur.fetchall()
	    if not r:
		return None
	    return r

    def aliasAdd(self,alias,dest,status):
	""" Add an alias"""
	cur = self.getCursor()
	cur.execute("insert into alias (alias,dest,status) values(%s,%s,%s)", (latin12p(alias),latin12p(dest),status))

    def aliasEdit(self,id,alias,dest,status):
	""" Edit an alias """
	cur = self.getCursor()
	cur.execute("update alias set alias=%s, dest=%s, status=%s where id=%s", (latin12p(alias),latin12p(dest),status,id))

    def aliasDel(self,id):
	""" Delete an alias """
	cur = self.getCursor()
	cur.execute("delete from alias where id=%s", id)

    def aliasGet(self,id, order="alias"):
	""" Get all info about an alias """
	cur = self.getCursor()
	cur.execute("select id,alias,dest,status from alias where id=%s order by %s",(id, order))
	return p2latin1(cur.fetchone())


    def aliasSearch(self, search):
	cur = self.getCursor()
	search = '%%'+search+'%%'
	cur.execute("select id, alias, status from alias where alias like %s order by alias", search)
	return p2latin1(cur.fetchall())


    def getAccess(self,user):
	""" Returns all access privs for a user"""
	cur = self.getCursor()
	cur.execute("select type from access where uname=%s", user)
	access = []
	for i in cur.fetchall():
	    access.append(i[0])
	return access

    def setAccess(self, user, access):
	""" Updates the access table for a user
	user - the user to be updated
	access - a list of access settings
	"""
	cur = self.getCursor()
	cur.execute("delete from access where uname=%s", user)
	for i in access:
	    if not i:
		return
	    cur.execute("insert into access (uname, type) values(%s, %s)", (user, i))


    def numUsers(self):
	""" Returns the number of users """
	cur = self.getCursor()
	cur.execute("select count(*) from accountuser")
	return cur.fetchone()



    def compExists(self,name):
	""" Return True or False if a company exists """
	cur = self.getCursor()
	cur.execute("select name from companies where name=%s", name)
	r = cur.fetchone()
	if r:
	    return True
	return False


    def getEncPass(self, user):
	""" Get the encrypted password for a user """
	cur = self.getCursor()
	cur.execute("select password from accountuser where username=%s", (user))
	r = cur.fetchone()
	if r:
	    return r[0]
	return None

    def addCompAccess(self, uname, company):
	""" Add access to a user for a company """
	cur = self.getCursor()
	cur.execute("insert into company_access (uname, company) values(%s, %s)", (uname, company))

    def delCompAccess(self, company):
	""" Removes all access attributes for a company """
	cur = self.getCursor()
	cur.execute("delete from company_access where company=%s", company)

    def authUser(self, uname, company):
	""" Check if the user has access to the company in question """
	cur = self.getCursor()
	if company == None:
	    return True
	cur.execute("select uname from access where uname = %s and type = 'global'", (uname))
	if cur.fetchone():
	    return True
	cur.execute("select uname from company_access where uname = %s and company = %s", (uname, company))
	if cur.fetchone():
	    return True
	return False

    def aliasExist(self, alias):
	""" Return True or False wether an aliase already exists """
	cur = self.getCursor()
	cur.execute("select alias from alias where alias=%s", latin12p(alias))
	if cur.fetchone():
	    return True
	return False


    def _sympaAdd(self, virtual, alias, dest, status, domain):
	""" Add an sympa alias"""
	cur = self.getCursor()
	alias = latin12p(alias)
	virtual = latin12p(virtual)
	dest = latin12p(dest)


	cur.execute("insert into sympa (virtual, alias, dest, status, domain) values(%s, %s, %s, %s, %s)",
	    (virtual, alias, dest, status, domain))


    def addSympa(self, company, prefix, domain, listname):
	""" Add aliases and virtuals for a sympa mailing list """
	# Aliases
	cur = self.getCursor()
	alias = prefix+"-"+listname
	domain = latin12p(domain)
	virtual = listname+"@"+domain
	dest = '"| /usr/lib/sympa/bin/queue %s@%s"' % (listname, domain)
	self._sympaAdd(virtual, alias, dest, 1, domain)

	for i in ["request", "subscribe", "unsubscribe"]:
	    virtual = listname+"-"+i+"@"+domain
	    alias = prefix+"-"+listname+"-"+i
	    dest = '"| /usr/lib/sympa/bin/queue %s-%s@%s"' % (listname, i, domain)
	    self._sympaAdd(virtual, alias, dest, 1, domain)

	virtual = "sympa"+"@"+domain
	alias = prefix+"-"+domain.replace(".","-")+"-"+"sympa"
	dest = '"| /usr/lib/sympa/bin/queue sympa@'+domain+'"'
	self._sympaAdd(virtual, alias, dest, 1, domain)

