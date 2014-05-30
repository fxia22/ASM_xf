"""
sasl.py - support for SASL mechanism
written by Hans Aschauer <Hans.Aschauer@Physik.uni-muenchen.de>

See http://python-ldap.sourceforge.net for details.

\$Id: sasl.py,v 1.7 2003/08/18 11:36:10 stroeder Exp $

Description:
The ldap.sasl module provides SASL authentication classes.
Each class provides support for one SASL mechanism. This is done by
implementing a callback() - method, which will be called by the
LDAPObject's sasl_bind_s() method.

Implementing support for new sasl mechanism is very easy --- see
the examples of digest_md5 and gssapi.

Compability:
- Tested with Python 2.0+ but should work with Python 1.5.x
"""

__version__ = '0.0.2'

class sasl:
    """This class handles SASL interactions for authentication.
    If an instance of this class is passed to ldap's sasl_bind_s()
    method, the library will call its callback() method. For
    specific SASL authentication mechanisms, this method can be
    overridden"""

    # These are the SASL callback id's , as defined in sasl.h
    CB_USER        = 0x4001
    CB_AUTHNAME    = 0x4002
    CB_LANGUAGE    = 0x4003
    CB_PASS        = 0x4004
    CB_ECHOPROMPT  = 0x4005
    CB_NOECHOPROMPT= 0x4006
    CB_GETREALM    = 0x4007
    
    def __init__(self,dict,mech):
        """ The (generic) base class takes a dictionary of
        question-answer pairs. Questions are specified by the respective
        SASL callback id's. The mech argument is a string that specifies
        the SASL mechaninsm to be uesd."""
        self.dict = dict
        self.mech = mech

    def callback(self,id, challenge, prompt, defresult):
        """ The callback method will be called by the sasl_bind_s()
        method several times. Each time it will provide the id, which
        tells us what kind of information is requested (the CB_ ...
        constants above). The challenge might be a short (english) text
        or some binary string, from which the return value is calculated.
        The prompt argument is always a human-readable description string;
        The defresult is a default value provided by the sasl library

        Currently, we do not use the challenge and prompt information, and
        return only information which is stored in the self.dict
        dictionary. Note that the current callback interface is not very
        useful for writing generic sasl GUIs, which would need to know all
        the questions to ask, before the answers are returned to the sasl
        lib (in contrast to one question at a time)."""
        
        # The following print command might be useful for debugging
        # new sasl mechanisms. So it is left here
        #print "id=%d, challenge=%s, prompt=%s, defresult=%s" % \
        #       (id, challenge, prompt, defresult)
        if self.dict.has_key(id):
            return self.dict[id]
        return defresult
    
class digest_md5 (sasl):
    """This class handles SASL DIGEST-MD5 authentication."""

    mechanism = "DIGEST-MD5"

    def __init__(self,username, password, authorization=""):
        auth_dict = {sasl.CB_AUTHNAME:username, sasl.CB_PASS:password,
                     sasl.CB_USER:authorization}
        sasl.__init__(self,auth_dict,self.mechanism)

class gssapi(sasl):
    """This class handles SASL GSSAPI (i.e. Kerberos V)
    authentication."""

    mechanism = "GSSAPI"

    def __init__(self, authorization=""):
        sasl.__init__(self, {sasl.CB_USER:authorization},self.mechanism)


class external(sasl):
    """This class handles SASL EXTERNAL authentication
    (i.e. X.509 client certificate)"""

    mechanism = "EXTERNAL"

    def __init__(self):
        sasl.__init__(self,{},self.mechanism)


saslmech_handler_class = {}

for _name in dir():
  o = eval(_name)
  if hasattr(o,'mechanism'):
    saslmech_handler_class[o.mechanism] = o

