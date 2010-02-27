#!/usr/bin/env python

from encodings import idna
from types import *

def mightDecode(s):
    if s[:4] == "xn--":
        return idna.ToUnicode(s)
    return s

def applySplit(s, f):
    foo = s.split("@")
    if len(foo) > 1:
        r = foo[0]
        for i in foo[1:]:
            r += "@" + applySplit(i, f)
        if type(r) == StringType:
            return r.decode("iso-8859-15")
        return r
    l = []
    for i in s.split("."):
        l.append(f(i))
    return ".".join(l)

def latin12p(s):
    if s == "":
        return s
    if type(s) == TupleType or type(s) == ListType:
        return map(latin12p, s)
    if type(s) == StringType:
        s = s.decode("iso-8859-15")
    if type(s) == UnicodeType:
        return applySplit(s, idna.ToASCII)
    return s
def utf82p(s):
    if s == "":
        return s
    if type(s) == TupleType or type(s) == ListType:
        return map(utf82p, s)
    if type(s) == StringType:
        s = s.decode("utf-8")
    if type(s) == UnicodeType:
        return applySplit(s, idna.ToASCII)
    return s
def p2latin1(s):
    if s == "":
        return s
    if type(s) == TupleType or type(s) == ListType:
        return map(p2latin1, s)
    if type(s) == StringType:
    	try:
	    value = applySplit(s, mightDecode)
	    return value.encode("iso-8859-15")
            #return applySplit(s, mightDecode).encode("iso-8859-15")
	except UnicodeEncodeError:
	    return applySplit(s, mightDecode)
    return s

def p2utf8(s):
    if s == "":
        return s
    if type(s) == TupleType or type(s) == ListType:
        return map(p2utf8, s)
    if type(s) == StringType:
        return applySplit(s, mightDecode).encode("utf-8")
    return s

