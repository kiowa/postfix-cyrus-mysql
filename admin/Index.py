from SitePage import SitePage

class Index(SitePage):
    def title(self):
        return "NS Admin"

    def htTitle(self):
        return "Main"


    def needAccess(self):
        return 0

    def writeCenter(self):
        self.writeln('<p><div class="box">')
        self.writeln('<table border="0">')
        access = self.session().value("access",[])
        # Iterate over the available modules (listed in SitePage).
        for mod in self.modules:
            short, filename, req_access, long = mod
            if req_access in access:
                self.writeln('<tr><td><a href="%s">%s</a></td><td>%s</td></tr>' % (filename, short, long))
        self.writeln('</table></div></p>')

