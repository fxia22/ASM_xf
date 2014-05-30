"""
ldap.schema -  LDAPv3 schema handling
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id: __init__.py,v 1.4 2003/04/11 12:51:02 stroeder Exp $
"""

__version__ = '0.2.1'

from ldap.schema.subentry import SubSchema,SCHEMA_ATTRS,SCHEMA_CLASS_MAPPING,SCHEMA_ATTR_MAPPING,urlfetch
from ldap.schema.models import *
