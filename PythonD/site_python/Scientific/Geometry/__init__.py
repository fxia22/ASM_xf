# Subpackage Scientific.Geometry
#
# Written by: Konrad Hinsen <hinsen@cnrs-orleans.fr>
# Last revision: 1999-9-2
#

"""This subpackage contains classes that deal with geometrical
quantities and objects. The geometrical quantities are vectors and
tensors, transformations, and quaternions as descriptions of
rotations.  There are also tensor fields, which were included here
(rather than in the subpackage Scientific.Functions) because they are
most often used in a geometric context. Finally, there are classes for
elementary geometrical objects such as spheres and planes.
"""

# Pretend that Vector and Tensor are defined directly
# in Scientific.Geometry.
from VectorModule import Vector, isVector
from TensorModule import Tensor, isTensor

import sys
if sys.modules.has_key('pythondoc'):
    Vector.__module__ = 'Scientific.Geometry'
    Tensor.__module__ = 'Scientific.Geometry'
    isVector.func_globals['__name__'] = 'Scientific.Geometry'
    isTensor.func_globals['__name__'] = 'Scientific.Geometry'
del sys
