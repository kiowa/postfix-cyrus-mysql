from SitePage import SitePage
from MiscUtils.Funcs import uniqueId
import string, types


class Login(SitePage):
    def title(self):
        return "Logg inn"

    def htTitle(self):
        return ""

    def htBodyArgs(self):
        return SitePage.htBodyArgs(self) + ' onload="document.loginform.username.focus();"' % locals()


    def writeMenu(self):
        return

    def writeNavbar(self):
        pass
    
    def needAccess(self):
        return 0


    def writeCenter(self):
        if self.getUser() and not self.request().hasField("extra"):
            self.writeln('<div align="center"><b>Du er allerede innlogget.')
            return
        self.writeln('<p align="center"><table border="0" cellpadding="20" cellspacing="20" width="300">')

        # Create a "unique" login id and put it in the form as well as in the session.
        # Login will only be allowed if they match.
        loginid = uniqueId(self)
        self.session().setValue('loginid', loginid)

        action = self.request().field('action', '')
        if action:
            action = 'action="%s"' % action
        else:
            action = 'action="Index"'


        self.writeln('<tr><td><form method="post" name="loginform" %s>' % action)
        self.write('<table border="0" cellpadding="3" cellspacing="0" class="shade">')
        extra = self.request().field('extra', None)
        if not extra and self.request().isSessionExpired() and not self.request().hasField('logout'):
            extra = 'Du har automatisk blitt logget ut p.g.a. inaktivitet.'
        if extra:
            self.write('<tr><td align="left" class="error" colspan="2">%s</td></tr><tr><td>&nbsp;</td><td>&nbsp;</td></tr>' % self.htmlEncode(extra))
        self.writeln('''
                <tr><td>&nbsp;</td><td>&nbsp;</td></tr>
                <tr>
                <td align="right">Brukernavn</td>
                <td><input type="TEXT" name="username"></td>
                </tr>
                <tr>
                <td align="right">Passord</td>
                <td><input type="PASSWORD" name="password"></td>
                </tr>
                <tr>
                <td>&nbsp;</td>
                <td><input type="submit" name="login" value="Login"></td>
                </tr>
                <tr><td>&nbsp;</td><td>&nbsp;</td></tr>
                <tr><td><input type="hidden" name="loginid" value="%s">&nbsp;</td><td>&nbsp;</td></tr>
             </table>
            </form>
           </td>
           ''' % loginid)
        self.writeln('</td></tr></table>')
