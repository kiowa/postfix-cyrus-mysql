"""
This library is derived from the work of Christopher Arndt <chris.arndt@web.de>

"""
import string, sys, termios, time, whrandom

try:
    import crypt
except ImportError:
    try:
        import fcrypt
        crypt = fcrypt
    except ImportError:
        raise ImportError, "Could import neither crypt nor fcrypt module."

try:
    from Crypto.Hash import MD5
    md5 = MD5
except ImportError:
    import md5


DES_SALT = list('./0123456789' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 'abcdefghijklmnopqrstuvwxyz') 



def check_passwd(plain, crypted, method="md5"):
    """ Validates a password """
    if not crypted: return 0
    salt = crypted[3:11]
    if passcrypt(plain,salt=salt,method=method) == crypted:
        return 1
    return 0


def login(user, password, db, method="md5"):
    """ Try to login a user
    name : user name to auth
    password : given password you wish to auth with
    db : db.getEncPass(user) should return the encrypted password
    """
    enc_pass = db.getEncPass(user)
    if check_passwd(password, enc_pass):
        return 1
    return 0


def passcrypt(passwd, salt=None, method='md5', magic='$1$'):
    """Encrypt a string according to rules in crypt(3)."""
    
    if method.lower() == 'des':
	if not salt:
	    salt = str(whrandom.choice(DES_SALT)) + \
	      str(whrandom.choice(DES_SALT))

	return crypt.crypt(passwd, salt)
    elif method.lower() == 'md5':
	return passcrypt_md5(passwd, salt, magic)
    elif method.lower() == 'clear':
        return passwd


def _to64(v, n):
    r = ''
    while (n-1 >= 0):
	r = r + DES_SALT[v & 0x3F]
	v = v >> 6
	n = n - 1
    return r

def passcrypt_md5(passwd, salt=None, magic='$1$'):
    """Encrypt passwd with MD5 algorithm."""
    
    if not salt:
	salt = repr(int(time.time()))[-8:]
    elif salt[:len(magic)] == magic:
        # remove magic from salt if present
        salt = salt[len(magic):]

    # salt only goes up to first '$'
    salt = string.split(salt, '$')[0]
    # limit length of salt to 8
    salt = salt[:8]

    ctx = md5.new(passwd)
    ctx.update(magic)
    ctx.update(salt)
    
    ctx1 = md5.new(passwd)
    ctx1.update(salt)
    ctx1.update(passwd)
    
    final = ctx1.digest()
    
    for i in range(len(passwd), 0 , -16):
	if i > 16:
	    ctx.update(final)
	else:
	    ctx.update(final[:i])
    
    i = len(passwd)
    while i:
	if i & 1:
	    ctx.update('\0')
	else:
	    ctx.update(passwd[:1])
	i = i >> 1
    final = ctx.digest()
    
    for i in range(1000):
	ctx1 = md5.new()
	if i & 1:
	    ctx1.update(passwd)
	else:
	    ctx1.update(final)
	if i % 3: ctx1.update(salt)
	if i % 7: ctx1.update(passwd)
	if i & 1:
	    ctx1.update(final)
	else:
	    ctx1.update(passwd)
        final = ctx1.digest()
    
    rv = magic + salt + '$'
    final = map(ord, final)
    l = (final[0] << 16) + (final[6] << 8) + final[12]
    rv = rv + _to64(l, 4)
    l = (final[1] << 16) + (final[7] << 8) + final[13]
    rv = rv + _to64(l, 4)
    l = (final[2] << 16) + (final[8] << 8) + final[14]
    rv = rv + _to64(l, 4)
    l = (final[3] << 16) + (final[9] << 8) + final[15]
    rv = rv + _to64(l, 4)
    l = (final[4] << 16) + (final[10] << 8) + final[5]
    rv = rv + _to64(l, 4)
    l = final[11]
    rv = rv + _to64(l, 2)
    
    return rv


