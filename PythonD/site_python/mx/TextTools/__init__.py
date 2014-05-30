""" mxTextTools - A tools package for fast text processing.

    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""
from TextTools import *
from TextTools import __version__

### Make the types pickleable:

# Shortcuts for pickle (reduces the pickle's length)
def _BMS(match,translate):
    return BMS(match,translate)
def _FS(match,translate):
    return FS(match,translate)

# Module init
class modinit:

    ### Register the two types
    import copy_reg
    def pickle_BMS(so):
        return _BMS,(so.match,so.translate)
    def pickle_FS(so):
        return _FS,(so.match,so.translate)
    copy_reg.pickle(BMSType,
                    pickle_BMS,
                    _BMS)
    copy_reg.pickle(FSType,
                    pickle_FS,
                    _FS)

del modinit
