from SitePage import SitePage


class Logs(SitePage):
    def htTitle(self):
        return "Logs"

    def needAccess(self):
        return "general"

    def writeCenter(self):
        logs = self.syslog.read()
        if not logs:
            self.writeln("No logs available.")
            return
        
        self.writeln('<p><table cellspacing="1" cellpadding="1" border="0">')
        count = 0
        for l in logs:
            if count % 2:
                self.writeln('<tr class="shade">')
            else:
                self.writeln('<tr>')
            self.writeln('<td>%s</td>' % l)
            self.writeln('</tr>')
            count +=1
        self.writeln('</table></p>')
        
    def writeMenu(self):
        pass
        
    
    
