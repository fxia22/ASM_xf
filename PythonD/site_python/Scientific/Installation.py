# Definitions for compilation of C modules that use Scientific.
#
# Written by Konrad Hinsen
# last revision: 1999-7-23
#

_undocumented = 1

import os, string, sys

# Package path
scientific_package_path = os.path.split(__file__)[0]

# Include path
include_path = os.path.join(scientific_package_path, "Include")

# Shared library path
shared_library_path = os.path.join(scientific_package_path, sys.platform)
