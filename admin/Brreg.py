import re,urllib2,string
from HTMLParser import HTMLParser


class Brreg:
    def __init__(self):
	self.parser = BrregParser()

    def urlopen(self,url):
	return urllib2.urlopen(urllib2.Request(url))

    def load_org(self,orgnr):
	fh = self.urlopen("http://w2.brreg.no/enhet/sok/detalj.jsp?orgnr=%d" % orgnr)
	self.parser.feed(fh.read())
	return self.parser.map

class BrregParser(HTMLParser):
    keymap = { "Organisasjonsnummer:":"orgnr",
	"Navn/foretaksnavn:":"name",
	"Organisasjonsform:":"orgform",
	"Forretningsadresse:":"businessaddr",
	"Kommune:":"county",
	"Postadresse:":"postaddr",
	"E-postadresse:":"email",
	"Internettadresse:":"url",
	"Telefon:":"telephone",
	"Mobil:":"mobile",
	"Telefaks:":"fax",
	"Registrert i Enhetsregisteret:":"regdato",
	"Stiftelsesdato:":"stiftdato",
	"Innehaver":"contact",
	"Kontaktperson":"contact",
	"Næringskode(r):":"nkode",
	"Sektorkode:":"sektorkode",
	"Også registrert i:":"extrareg",
	"nospam":"nospam",
	}


    map = {}
    key = ""
    inDoc = False
    inKey = False
    inTable = False
    inTR = False
    inValue = False

    def _addKey(self, key, value):
	if not map.has_key(key):
	    map[key] = value

    def handle_comment(self, data):
	if data.strip() == "Her kommer dokumentet":
	    self.inDoc = True

	if data == "Slutt pŒ dokumentet":
	    self.inDoc = False
	    self.inTable = True

    def handle_starttag(self, tag, attrs):
	if not self.inDoc:
	    return

	if tag == "table":
	    if len(attrs) == 3:
		if attrs[2][1] == "1":
		    self.inTable = True

	if self.inTable and tag == "tr":
	    self.inTR = True

	if self.inTR and tag == "b":
	    self.inKey = True

	if self.inTR and tag == "td" and len(attrs) == 2:
	    self.inValue = True

    def handle_endtag(self, tag):
	if not self.inDoc:
	    return

	if self.inTable and tag == "tr":
	    self.inTR = False

	if self.inTR and tag == "b":
	    self.inKey = False

	if self.inTR and tag == "td":
	    self.inValue = False


    def handle_data(self, data):
	data = data.strip()
	if self.inKey:
	    if self.keymap.has_key(data):
		key = self.keymap[data]
		#print "got key: ",key
		self.key = key
	    else:
		self.key = None

	if self.inValue:
	    if self.key:
		self.map[self.key] = data
		#print "got value:",data



