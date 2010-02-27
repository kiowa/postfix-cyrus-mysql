from SitePage import SitePage

class Print(SitePage):

    def writeCenter(self):
        request = self.request()
        self.writeln("foobar")

    
