# This module defines classes that represent coordinate translations,
# rotations, and combinations of translation and rotation.
#
# Written by: Konrad Hinsen <hinsen@cnrs-orleans.fr>
# Last revision: 2001-1-10
# 

import TensorModule, VectorModule
import Numeric

#
# Abstract base class
#
class Transformation:

    """Linear coordinate transformation.

    Transformation objects represent linear coordinate transformations
    in a 3D space. They can be applied to vectors, returning another vector.
    If 't' is a transformation and 'v' is a vector, 't(v)' returns
    the transformed vector.

    Transformations support composition: if 't1' and 't2' are transformation
    objects, 't1*t2' is another transformation object which corresponds
    to applying t1 *after* t2.

    This class is an abstract base class. Instances can only be created
    of concrete subclasses, i.e. translations or rotations.
    """

    def rotation(self):
        "Returns the rotational component."
        pass

    def translation(self):
        """Returns the translational component. In the case of a mixed
        rotation/translation, this translation is executed
        *after* the rotation."""
        pass

    def inverse(self):
        "Returns the inverse transformation."
        pass

    def screwMotion(self):
        """Returns the four parameters '(reference, direction, angle,
        distance)' of a screw-like motion that is equivalent to the
        transformation. The screw motion consists of a displacement
        of 'distance' (a float) along 'direction' (a normalized vector)
        plus a rotation of 'angle' radians around an axis pointing along
        'direction' and passing through the point 'reference' (a vector).
        """
        pass
#
# Pure translation
#
class Translation(Transformation):

    """Translational transformation.

    This is a subclass of Transformation.

    Constructor: Translation(|vector|), where |vector| is the displacement
    vector.
    """

    def __init__(self, vector):
	self.vector = vector

    is_translation = 1

    def __mul__(self, other):
	if hasattr(other, 'is_translation'):
	    return Translation(self.vector + other.vector)
	elif hasattr(other, 'is_rotation'):
	    return RotationTranslation(other.tensor, self.vector)
	elif hasattr(other, 'is_rotation_translation'):
	    return RotationTranslation(other.tensor, other.vector+self.vector)
	else:
	    raise ValueError, 'incompatible object'

    def __call__(self, vector):
	return self.vector + vector

    def displacement(self):
        "Returns the displacement vector."
	return self.vector

    def rotation(self):
	return Rotation(VectorModule.ez, 0.)

    def translation(self):
	return self

    def inverse(self):
	return Translation(-self.vector)

    def screwMotion(self):
	l = self.vector.length()
	if l == 0.:
	    return VectorModule.Vector(0.,0.,0.), \
                   VectorModule.Vector(0.,0.,1.), 0., 0.
	else:
	    return VectorModule.Vector(0.,0.,0.), self.vector/l, 0., l

#
# Pure rotation
#
class Rotation(Transformation):

    """Rotational transformation.

    This is a subclass of Transformation.

    Constructor:

    - Rotation(|tensor|), where |tensor| is a tensor object containing
      the rotation matrix.

    - Rotation(|axis|, |angle|), where |axis| is a vector and |angle|
      a number (the angle in radians).
    """

    def __init__(self, *args):
	if len(args) == 1:
	    self.tensor = args[0]
	    if not TensorModule.isTensor(self.tensor):
		self.tensor = TensorModule.Tensor(self.tensor)
	elif len(args) == 2:
	    axis, angle = args
	    axis = axis.normal()
	    projector = axis.dyadicProduct(axis)
	    self.tensor = projector - \
			  Numeric.sin(angle)*TensorModule.epsilon*axis + \
			  Numeric.cos(angle)*(TensorModule.delta-projector)
	else:
	    raise TypeError, 'one or two arguments required'

    is_rotation = 1

    def __mul__(self, other):
	if hasattr(other, 'is_rotation'):
	    return Rotation(self.tensor.dot(other.tensor))
	elif hasattr(other, 'is_translation'):
	    return RotationTranslation(self.tensor, self.tensor*other.vector)
	elif hasattr(other, 'is_rotation_translation'):
	    return RotationTranslation(self.tensor.dot(other.tensor),
				       self.tensor*other.vector)
	else:
	    raise ValueError, 'incompatible object'

    def __call__(self,other):
        if hasattr(other,'is_vector'):
           return self.tensor*other
        elif hasattr(other, 'is_tensor') and other.rank == 2:
           _rinv=self.tensor.inverse()
           return _rinv.dot(other.dot(self.tensor))
        elif hasattr(other, 'is_tensor') and other.rank == 1:
           return self.tensor.dot(other)
        else:
            raise ValueError, 'incompatible object'

    def axisAndAngle(self):
        """Returns the axis (a normalized vector) and angle (a float,
        in radians)."""
	as = -self.tensor.asymmetricalPart()
	axis = VectorModule.Vector(as[1,2], as[2,0], as[0,1])
	sine = axis.length()
	if abs(sine) > 1.e-10:
	    axis = axis/sine
	    projector = axis.dyadicProduct(axis)
	    cosine = (self.tensor-projector).trace()/(3.-axis*axis)
	    angle = angleFromSineAndCosine(sine, cosine)
	else:
	    t = 0.5*(self.tensor+TensorModule.delta)
	    i = Numeric.argmax(t.diagonal().array)
	    axis = (t[i]/Numeric.sqrt(t[i,i])).asVector()
	    angle = 0.
	    if t.trace() < 2.:
		angle = Numeric.pi
	return axis, angle

    def rotation(self):
	return self

    def translation(self):
	return Translation(VectorModule.Vector(0.,0.,0.))

    def inverse(self):
	return Rotation(self.tensor.transpose())

    def screwMotion(self):
	axis, angle = self.axisAndAngle()
	return VectorModule.Vector(0., 0., 0.), axis, angle, 0.

#
# Combined translation and rotation
#
class RotationTranslation(Transformation):

    """Combined translational and rotational transformation.

    This is a subclass of Transformation.

    Objects of this class are not created directly, but can be the
    result of a composition of rotations and translations.
    """

    def __init__(self, tensor, vector):
	self.tensor = tensor
	self.vector = vector

    is_rotation_translation = 1

    def __mul__(self, other):
	if hasattr(other, 'is_rotation'):
	    return RotationTranslation(self.tensor.dot(other.tensor),
				       self.vector)
	elif hasattr(other, 'is_translation'):
	    return RotationTranslation(self.tensor,
				       self.tensor*other.vector+self.vector)
	elif hasattr(other, 'is_rotation_translation'):
	    return RotationTranslation(self.tensor.dot(other.tensor),
				       self.tensor*other.vector+self.vector)
	else:
	    raise ValueError, 'incompatible object'

    def __call__(self, vector):
	return self.tensor*vector + self.vector

    def rotation(self):
	return Rotation(self.tensor)

    def translation(self):
	return Translation(self.vector)

    def inverse(self):
	return Rotation(self.tensor.transpose())*Translation(-self.vector)

    def screwMotion(self):
	import LinearAlgebra
	axis, angle = self.rotation().axisAndAngle()
	d = self.vector*axis
	x = d*axis-self.vector
	r0 = Numeric.dot(LinearAlgebra.generalized_inverse(
	                    self.tensor.array-Numeric.identity(3)), x.array)
	return VectorModule.Vector(r0), axis, angle, d

# Utility function

def angleFromSineAndCosine(sine, cosine):
    sine = min(1., max(-1., sine))
    angle = Numeric.arcsin(abs(sine))
    if sine*cosine < 0.:
	angle = -angle
    if cosine < 0.:
	angle = Numeric.pi + angle
    if angle < 0.:
	angle = 2.*Numeric.pi + angle
    return angle

# Test code

if __name__ == '__main__':

    t = Translation(VectorModule.Vector(1,0,0))
    r = Rotation(VectorModule.ex+VectorModule.ey, Numeric.pi)
