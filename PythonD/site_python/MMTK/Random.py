# Functions for finding random points and orientations.
#
# Written by: Konrad Hinsen
# Last revision: 2000-8-9
# 

"""This module defines various random quantities that are useful in
molecular simulations. For obtaining random numbers, it tries to use
the RNG module, which is part of the LLNL package distribution, which
also contains Numerical Python. If RNG is not available, it
uses the random number generators in modules RandomArray (part of
Numerical Python) and whrandom (in the Python standard library).
"""

import Numeric
from Scientific.Geometry import Vector
from Numeric import dot
from Scientific.Geometry.Transformation import Rotation
import ParticleProperties, Units

try:
    import RNG
except ImportError:
    RNG = None


if RNG is None:

    random = __import__('random')
    import whrandom
    from RandomArray import uniform, seed
    seed(1, 1)
    whrandom.seed(1, 1, 1)

    def initializeRandomNumbersFromTime():
        whrandom.seed(0, 0, 0)
        seed(0, 0)

    def gaussian(mean, std, shape=None):
        if shape is None:
            x = random.normalvariate(0., 1.)
        else:
            x = Numeric.zeros(shape, Numeric.Float)
            xflat = Numeric.ravel(x)
            for i in range(len(xflat)):
                xflat[i] = random.normalvariate(0., 1.)
        return mean + std*x

else:

    _uniform_generator = \
                    RNG.CreateGenerator(-1, RNG.UniformDistribution(0., 1.))
    _gaussian_generator = \
                    RNG.CreateGenerator(-1, RNG.NormalDistribution(0., 1.))

    def initializeRandomNumbersFromTime():
        global _uniform_generator, _gaussian_generator
        _uniform_generator = \
                       RNG.CreateGenerator(0, RNG.UniformDistribution(0., 1.))
        _gaussian_generator = \
                       RNG.CreateGenerator(0, RNG.NormalDistribution(0., 1.))

    def uniform(x1, x2, shape=None):
        if shape is None:
            x = _uniform_generator.ranf()
        else:
            n = Numeric.multiply.reduce(shape)
            x = _uniform_generator.sample(n)
            x.shape = shape
        return x1+(x2-x1)*x

    def gaussian(mean, std, shape=None):
        if shape is None:
            x = _gaussian_generator.ranf()
        else:
            n = Numeric.multiply.reduce(shape)
            x = _gaussian_generator.sample(n)
            x.shape = shape
        return mean+std*x

#
# Random point in a rectangular box centered around the origin
#
def randomPointInBox(a, b = None, c = None):
    """Returns a vector drawn from a uniform distribution within a
    rectangular box with edge lengths |a|, |b|, |c|. If |b| and/or |c|
    are omitted, they are taken to be equal to |a|."""
    if b is None: b = a
    if c is None: c = a
    x = uniform(-0.5*a, 0.5*a)
    y = uniform(-0.5*b, 0.5*b)
    z = uniform(-0.5*c, 0.5*c)
    return Vector(x, y, z)

#
# Random point in a sphere around the origin.
#
def randomPointInSphere(r):
    """Returns a vector drawn from a uniform distribution within
    a sphere of radius |r|."""
    rsq = r*r
    while 1:
	x = uniform(-r, r, (3,))
	if dot(x, x) < rsq: break
    return Vector(x)

#
# Random direction (unit vector).
#
def randomDirection():
    """Returns a vector drawn from a uniform distribution on
    the surface of a unit sphere."""
    r = randomPointInSphere(1.)
    return r.normal()

def randomDirections(n):
    """Returns a list of |n| vectors drawn from a uniform distribution on
    the surface of a unit sphere. If |n| is negative, return a deterministic
    list of not more than -|n| vectors of unit length (useful for
    testing purposes)."""
    if n < 0:
        list = [Vector(1., 0., 0.), Vector(0., -1., 0.), Vector(0., 0., 1.),
                Vector(-1., 1., 0.).normal(), Vector(-1., 0., 1.).normal(),
                Vector(0., 1., -1.).normal(), Vector(1., -1., 1.).normal()]
        list = list[:-n]
    else:
        list = []
        for i in range(n):
            list.append(randomDirection())
    return list

#
# Random rotation.
#
def randomRotation(max_angle = Numeric.pi):
    """Returns a Rotation object describing a random rotation
    with a uniform axis distribution and angles drawn from
    a uniform distribution between -|max_angle| and |max_angle|."""
    return Rotation(randomDirection(), uniform(-max_angle, max_angle))

#
# Random velocity (gaussian)
#
def randomVelocity(temperature, mass):
    """Returns a random velocity vector for a particle of a given
    |mass|, drawn from a Boltzmann distribution for the given
    |temperature|."""
    sigma = Numeric.sqrt((temperature*Units.k_B)/(mass*Units.amu))
    return Vector(gaussian(0., sigma, (3,)))

#
# Random ParticleVector (gaussian)
#
def randomParticleVector(universe, width):
    """Returns a ParticleVector object in which each vector is
    drawn from a Gaussian distribution with a given |width| centered
    around zero."""
    data = gaussian(0., 0.577350269189*width, (universe.numberOfPoints(), 3))
    return ParticleProperties.ParticleVector(universe, data)


#
# Test code
#
if __name__ == '__main__':

    mean = 1.
    std = 5.
    n = 10000

    values = gaussian(mean, std, (n,))
    m = Numeric.sum(values)/n
    print mean, m
    print std, Numeric.sqrt(Numeric.sum((values-m)**2)/n)
