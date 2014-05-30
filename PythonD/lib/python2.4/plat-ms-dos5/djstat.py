"""DJGPP-DOS specific values and function definitions for PythonD, etc.
website: http://www.caddit.net

Suggested usage: from djgpp import *
"""

# S_IFMT() values for various file types. Needed by stat.py.
S_IFDIR = 12288
S_IFCHR = 8192
S_IFBLK = 4096
S_IFREG = 0
S_IFIFO = 16384
S_IFLNK = 32768
S_IFSOCK = 140000

S_ISUID = 2147483648
S_ISGID = 1073741824
