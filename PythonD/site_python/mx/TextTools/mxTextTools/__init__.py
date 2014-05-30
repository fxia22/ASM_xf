""" mxTextTools - A tools package for fast text processing.

    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""
from mxTextTools import *
from mxTextTools import __version__

#
# Make BMS take the role of FS in case the Fast Search object was not built
#
try:
    FS
except NameError:
    FS = BMS
    FSType = BMSType
