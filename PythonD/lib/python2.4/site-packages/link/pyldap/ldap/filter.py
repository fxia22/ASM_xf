"""
filters.py - misc stuff for handling LDAP filter strings (see RFC2254)
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id: filter.py,v 1.3 2003/05/26 08:34:03 stroeder Exp $

Compability:
- Tested with Python 2.0+
"""

__version__ = '0.0.2'


def escape_filter_chars(assertion_value):
  """
  Replace all special characters found in assertion_value
  by quoted notation  
  """
  s = assertion_value.replace('\\', r'\5c')
  s = s.replace(r'*', r'\2a')
  s = s.replace(r'(', r'\28')
  s = s.replace(r')', r'\29')
  s = s.replace('\x00', r'\00')
  return s 


def filter_format(filter_template,assertion_values):
  """
  filter_template
        String containing %s as placeholder for assertion values.
  assertion_values
        List or tuple of assertion values. Length must match
        count of %s in filter_template.
  """
  return filter_template % (tuple(map(escape_filter_chars,assertion_values)))
