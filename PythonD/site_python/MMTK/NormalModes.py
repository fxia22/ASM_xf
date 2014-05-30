# This module implements normal mode calculations.
#
# Written by Konrad Hinsen
# last revision: 2002-3-6
#

"""See also the Example:NormalModes example applications.
"""

import Features, Units, ParticleProperties, Visualization
import Numeric, copy

#
# Class for a single mode
#
class Mode(ParticleProperties.ParticleVector):

    """Single normal mode

    A Glossary:Subclass of Class:MMTK.ParticleVector.

    Mode objects are created by indexing a NormalModes object.
    They contain the atomic displacements corresponding to a
    single mode.

    Mode objects are specializations of Class:MMTK.ParticleVector
    objects and support all their operations. In addition, the
    frequency corresponding to the mode is stored in the attribute
    "frequency".

    Note: the normal mode vectors are *not* mass weighted, and therefore
    not orthogonal to each other.
    """

    def __init__(self, universe, n, frequency, mode):
	self.number = n
	self.frequency = frequency
	ParticleProperties.ParticleVector.__init__(self, universe, mode)

    def __str__(self):
	return 'Mode ' + `self.number` + ' with frequency ' + `self.frequency`

    __repr__ = __str__

    return_class = ParticleProperties.ParticleVector

    def effectiveMassAndForceConstant(self):
	m = self.massWeightedProjection(self)/self.projection(self)
	k = m*(2.*Units.pi*self.frequency)**2
	return m, k

    def view(self, factor=1., subset=None):
        """Start an animation of the mode. The displacements can be
        scaled by a |factor| to make them better visible, and
        a |subset| of the total system can be specified as well.
        This function requires an external viewer, see module
        Module:MMTK.Visualization for details."""
	Visualization.viewMode(self, factor, subset)

#
# Class for a full set of normal modes
#
class NormalModes:

    """Normal modes

    Constructor: NormalModes(|universe|, |temperature|=300)

    Arguments:

    |universe| -- the system for which the normal modes are calculated;
                  it must have a force field which provides the second
                  derivatives of the potential energy

    |temperature| -- the temperature for which the amplitudes of the
                     atomic displacement vectors are calculated. A
                     value of 'None' can be specified to have no scaling
                     at all. In that case the mass-weighted norm
                     of each normal mode is one.

    In order to obtain physically reasonable normal modes, the configuration
    of the universe must correspond to a local minimum of the potential
    energy.

    A NormalModes object behaves like a sequence of modes. Individual
    modes (see class Class:MMTK.NormalModes.Mode) can be extracted by
    indexing with an integer. Looping over the modes is possible as
    well.
    """

    features = []

    def __init__(self, universe=None, temperature = 300):
	if universe == None:
	    return
        Features.checkFeatures(self, universe)
	self.universe = universe
        self.temperature = temperature
	self.sqrt_mass = Numeric.sqrt(self.universe.masses().array)
	self.sqrt_mass = self.sqrt_mass[:, Numeric.NewAxis]

	self._forceConstantMatrix()
	ev = self._diagonalize()

	self.imaginary = Numeric.less(ev, 0.)
	self.frequencies = Numeric.sqrt(Numeric.fabs(ev)) / (2.*Units.pi)
	self.sort_index = Numeric.argsort(self.frequencies)

	self._scale(temperature)
	del self.sqrt_mass

    def __len__(self):
	return self.nmodes

    def __getitem__(self, item):
	index = self.sort_index[item]
	f = self.frequencies[index]
	if self.imaginary[index]:
	    f = f*1.j
	return Mode(self.universe, item, f, self.array[index])

    def __getslice__(self, first, last):
        last = min(last, self.nmodes)
	return map(lambda i, s=self: s[i], range(first, last))

    def reduceToRange(self, first, last):
        """Discards all modes except for those whose numbers are between
        |first| (inclusive) and |last| (exclusive). This is done to
        reduce memory requirements, especially before saving the modes
        to a file."""
	junk1 = list(self.sort_index[:first])
	junk2 = list(self.sort_index[last:])
	junk1.sort()
	junk2.sort()
	if junk1 == range(0, first) and \
	   junk2 == range(last, len(self.sort_index)):
	    self.array = self.array[first:last]
	    self.frequencies = self.frequencies[first:last]
	    self.imaginary = self.imaginary[first:last]
	    self.sort_index = self.sort_index[first:last]-first
	else:
	    keep = self.sort_index[first:last]
	    self.array = Numeric.take(self.array, keep)
	    self.frequencies = Numeric.take(self.frequencies, keep)
	    self.imaginary = Numeric.take(self.imaginary, keep)
	    self.sort_index = Numeric.arange(0, last-first)
	self.nmodes = last-first

    def _forceConstantMatrix(self):
	energy, force_constants = self.universe.energyAndForceConstants()
	self.array = force_constants.array
	self.natoms = self.array.shape[0]
	self.nmodes = 3*self.natoms
	Numeric.divide(self.array,
		       self.sqrt_mass[Numeric.NewAxis, Numeric.NewAxis, :, :],
		       self.array)
	Numeric.divide(self.array,
		       self.sqrt_mass[:, :, Numeric.NewAxis, Numeric.NewAxis],
		       self.array)
	self.array.shape = 2*(self.nmodes,)

    def _diagonalize(self):
	dsyev = None
	try:
	    from lapack_dsy import dsyev
	except ImportError: pass
	if dsyev is None:
	    try:
		from lapack_mmtk import dsyev
	    except ImportError: pass
	if dsyev is None:
	    from LinearAlgebra import eigenvectors
	    _symmetrize(self.array)
	    ev, modes = eigenvectors(self.array)
	    self.array = modes
	    if ev.typecode() == Numeric.Complex:
		ev = ev.real
	    if modes.typecode() == Numeric.Complex:
		modes = modes.real
	else:
	    ev = Numeric.zeros((self.nmodes,), Numeric.Float)
	    lwork = 3*self.nmodes
	    work = Numeric.zeros((lwork,), Numeric.Float)
	    results = dsyev('V', 'L', self.nmodes, self.array, self.nmodes, ev,
			    work, lwork, 0)
	    if results['info'] > 0:
		raise ValueError, 'Eigenvalue calculation did not converge'
	return ev

    def _scale(self, temperature):
	if temperature is not None:
	    factor = Numeric.sqrt(2.*temperature*Units.k_B/Units.amu) / \
		     (2.*Units.pi)
	self.array.shape = (self.nmodes, self.natoms, 3)
	for i in range(self.nmodes):
	    index = self.sort_index[i]
	    if index >= 6 and temperature is not None:
		amplitude = factor/self.frequencies[index]
	    else:
		amplitude = 1.
	    self.array[index] = amplitude*self.array[index] / self.sqrt_mass

    def fluctuations(self):
        """Returns a Class:MMTK.ParticleScalar containing the thermal
        fluctuations for each atom in the universe."""
        f = ParticleProperties.ParticleScalar(self.universe)
        for i in range(6, self.nmodes):
            mode = self[i]
            f = f + mode*mode
        return 0.5*f

#
# Sparse matrix version
#
class SparseMatrixNormalModes(NormalModes):

    """Normal modes using a sparse matrix

    A Glossary:Subclass of Class:MMTK.NormalModes.NormalModes.

    This class differs from the class NormalModes in that it obtains
    the Cartesian force constant matrix in a sparse-matrix format and
    uses a sparse-matrix eigenvalue solver from the ARPACK library.
    This is advantageous if the Cartesian force constant matrix is
    sparse (as it is for force fields without long-range terms), but
    for non-sparse matrices the memory requirements are higher than
    for NormalModes. Note that the calculation time depends not only
    on the size of the system, but also on its frequency spectrum,
    because an iterative algorithm is used.


    Constructor: SparseMatrixNormalModes(|universe|, |nmodes|,
                                         |temperature|=300)

    Arguments:

    |universe| -- the system for which the normal modes are calculated;
                  it must have a force field which provides the second
                  derivatives of the potential energy

    |nmodes| -- the number of modes that is calculated. The calculation
                time can grow significantly with an increasing number
                of modes.

    |temperature| -- the temperature for which the amplitudes of the
                     atomic displacement vectors are calculated. A
                     value of 'None' can be specified to have no scaling
                     at all. In that case the mass-weighted norm
                     of each normal mode is one.

    In order to obtain physically reasonable normal modes, the configuration
    of the universe must correspond to a local minimum of the potential
    energy.

    A SparseMatrixNormalModes object behaves like a sequence of modes.
    Individual modes (see class Class:MMTK.NormalModes.Mode) can be
    extracted by indexing with an integer. Looping over the modes is
    possible as well.
    """

    def __init__(self, universe = None, nmodes = None, temperature = 300):
        self.nmodes = nmodes
        NormalModes.__init__(self, universe, temperature)
        del self.fc

    def _forceConstantMatrix(self):
	from MMTK_forcefield import SparseForceConstants
        self.natoms = self.universe.numberOfCartesianCoordinates()
	fc = SparseForceConstants(self.natoms, 5*self.natoms)
	eval = self.universe.energyEvaluator()
	energy, g, fc = eval(0, fc, 0)
        self.fc = fc
	self.fc.scale(1./self.sqrt_mass[:, 0])

    def _diagonalize(self):
        from MMTK_sparseev import sparseMatrixEV
        eigenvalues, eigenvectors = sparseMatrixEV(self.fc, self.nmodes)
        self.array = eigenvectors[:self.nmodes]
        return eigenvalues

#
# Classes for normal modes with respect to a given basis
#
class SubspaceNormalModes(NormalModes):

    """Normal modes in a subspace

    A Glossary:Subclass of Class:MMTK.NormalModes.NormalModes.

    Constructor: SubspaceNormalModes(|universe|, |basis|, |temperature|=300)

    Arguments:

    |universe| -- the system for which the normal modes are calculated;
                  it must have a force field which provides the second
                  derivatives of the potential energy

    |basis| -- the basis for the subspace in which the normal modes
               are calculated (or, more precisely, a set of vectors
               spanning the subspace; it does not have to be
               orthogonal). This can either be a sequence of
               Class:MMTK.ParticleVector objects or a tuple of two
               such sequences. In the second case, the subspace is
               defined by the space spanned by the first set of
               vectors projected on the complement of the space
               spanned by the second set of vectors. The second set
               thus defines directions that are excluded from the
               subspace.

    |temperature| -- the temperature for which the amplitudes of the
                     atomic displacement vectors are calculated. A
                     value of 'None' can be specified to have no scaling
                     at all. In that case the mass-weighted norm
                     of each normal mode is one.

    In order to obtain physically reasonable normal modes, the configuration
    of the universe must correspond to a local minimum of the potential
    energy.

    A SubspaceNormalModes object behaves like a sequence of modes.
    Individual modes (see class Class:MMTK.NormalModes.Mode) can be
    extracted by indexing with an integer. Looping over the modes is
    possible as well.
    """

    def __init__(self, universe = None, basis = None, temperature = 300):
	if universe is None:
	    return
	self.basis = basis
	NormalModes.__init__(self, universe, temperature)
	del self.basis

    def _setupBasis(self):
	if type(self.basis) is type(()):
	    excluded, basis = self.basis
	else:
	    excluded = []
	    basis = self.basis
        nexcluded = len(excluded)
        nmodes = len(basis)
        ntotal = nexcluded + nmodes
        natoms = len(basis[0])

        try:
            from lapack_dge import dgesvd
        except ImportError:
            from lapack_mmtk import dgesvd

        sv = Numeric.zeros((min(ntotal, 3*natoms),), Numeric.Float)
        work = Numeric.zeros((max(3*min(3*natoms,ntotal)
                                  +max(3*natoms,ntotal),
                                  5*min(3*natoms,ntotal)-4),),
                             Numeric.Float)
        dummy = Numeric.zeros((1,), Numeric.Float)
        if nexcluded > 0:
            self.basis = Numeric.zeros((ntotal, 3*natoms), Numeric.Float)
            for i in range(nexcluded):
                self.basis[i] = Numeric.ravel(excluded[i].array
                                              *self.sqrt_mass)
            result = dgesvd('O', 'N', 3*natoms, nexcluded, self.basis,
                            3*natoms, sv, dummy, 1, dummy, 1,
                            work, work.shape[0], 0)
            if result['info'] != 0:
                raise ValueError, 'Lapack SVD: ' + `result['info']`
            svmax = Numeric.maximum.reduce(sv)
            nexcluded = Numeric.add.reduce(Numeric.greater(sv,
                                                           1.e-10*svmax))
            ntotal = nexcluded + nmodes
            for i in range(nmodes):
                self.basis[i+nexcluded] = \
                        Numeric.ravel(basis[i].array*self.sqrt_mass)
            result = dgesvd('O', 'N', 3*natoms, ntotal, self.basis,
                            3*natoms, sv, dummy, 1, dummy, 1,
                            work, work.shape[0], 0)
            if result['info'] != 0:
                raise ValueError, 'Lapack SVD: ' + `result['info']`
            svmax = Numeric.maximum.reduce(sv)
            ntotal = Numeric.add.reduce(Numeric.greater(sv, 1.e-10*svmax))
            nmodes = ntotal - nexcluded
        else:
            if hasattr(self.basis, 'may_modify') and \
               hasattr(self.basis, 'array'):
                self.basis = self.basis.array
            else:
                self.basis = Numeric.array(map(lambda v: v.array, basis))
            Numeric.multiply(self.basis, self.sqrt_mass, self.basis)
            self.basis.shape = (nmodes, 3*natoms)
            result = dgesvd('O', 'N', 3*natoms, nmodes,
                            self.basis, 3*natoms,
                            sv, dummy, 1, dummy, 1, work, work.shape[0], 0)
            if result['info'] != 0:
                raise ValueError, 'Lapack SVD: ' + `result['info']`
            svmax = Numeric.maximum.reduce(sv)
            nmodes = Numeric.add.reduce(Numeric.greater(sv, 1.e-10*svmax))
            ntotal = nmodes
        self.basis = self.basis[nexcluded:ntotal, :]

    def _forceConstantMatrix(self):
	self._setupBasis()
	NormalModes._forceConstantMatrix(self)
	_symmetrize(self.array)
	self.array = Numeric.dot(Numeric.dot(self.basis, self.array),
				 Numeric.transpose(self.basis))
	self.nmodes = self.array.shape[0]

    def _diagonalize(self):
	ev = NormalModes._diagonalize(self)
	self.array = Numeric.dot(self.array, self.basis)
	return ev


class FiniteDifferenceSubspaceNormalModes(SubspaceNormalModes):

    """Normal modes in a subspace with numerical differentiation

    A Glossary:Subclass of Class:MMTK.NormalModes.SubspaceNormalModes.

    This class differs from SubspaceNormalModes in the way it obtains
    the force constant matrix. Instead of obtaining the full Cartesian
    force constant matrix from the force field and projecting it on
    the subspace, it performs a numerical differentiation of the
    gradients along the basis vectors of the subspace. This is useful
    in two cases:

    - for small subspaces this approach uses less memory, because
      the full Cartesian force constant matrix is not needed

    - it can be used even if the force field does not provide second
      derivatives


    Constructor: FiniteDifferenceSubspaceNormalModes(|universe|,
                        |basis|, |delta|=0.0001, |temperature|=300)

    Arguments:

    |universe| -- the system for which the normal modes are calculated

    |basis| -- the basis for the subspace in which the normal modes
               are calculated (or, more precisely, a set of vectors
               spanning the subspace; it does not have to be orthogonal).
               This can either be a sequence of ParticleVector objects
               or a tuple of two such sequences. In the second case,
               the subspace is defined by the space spanned by the
               first set of vectors projected on the complement of the
               space spanned by the second set of vectors. The second
               set thus defines directions that are excluded from
               the subspace.

    |delta| -- the length of the displacement used for numerical
               differentiation

    |temperature| -- the temperature for which the amplitudes of the
                     atomic displacement vectors are calculated. A
                     value of 'None' can be specified to have no scaling
                     at all. In that case the mass-weighted norm
                     of each normal mode is one.

    In order to obtain physically reasonable normal modes, the configuration
    of the universe must correspond to a local minimum of the potential
    energy.

    A FiniteDifferenceSubspaceNormalModes object behaves like a
    sequence of modes.
    Individual modes (see class Class:MMTK.NormalModes.Mode) can be
    extracted by indexing with an integer. Looping over the modes is
    possible as well.
    """

    def __init__(self, universe = None, basis = None,
		 delta = 0.0001*Units.nm*Numeric.sqrt(Units.amu),
		 temperature = 300.):
	self.delta = delta
	SubspaceNormalModes.__init__(self, universe, basis, temperature)

    def _forceConstantMatrix(self):
	self._setupBasis()
	self.nmodes = len(self.basis)
	self.array = Numeric.zeros((self.nmodes, self.nmodes), Numeric.Float)
	conf = copy.copy(self.universe.configuration())
	conf_array = conf.array
	self.natoms = len(conf_array)
	small_change = 0
	for i in range(self.nmodes):
	    d = self.delta*Numeric.reshape(self.basis[i], (self.natoms, 3)) / \
		self.sqrt_mass
	    conf_array[:] = conf_array+d
	    self.universe.setConfiguration(conf)
	    energy, gradients1 = self.universe.energyAndGradients(None, None,
								  small_change)
	    small_change = 1
	    conf_array[:] = conf_array-2.*d
	    self.universe.setConfiguration(conf)
	    energy, gradients2 = self.universe.energyAndGradients(None, None,
								  small_change)
	    conf_array[:] = conf_array+d
	    v = (gradients1.array-gradients2.array) / \
		(2.*self.delta*self.sqrt_mass)
	    self.array[i] = Numeric.dot(self.basis, Numeric.ravel(v))
	self.universe.setConfiguration(conf)
	self.array = 0.5*(self.array+Numeric.transpose(self.array))


class SparseMatrixSubspaceNormalModes(SubspaceNormalModes):

    """Normal modes in a subspace using a sparse matrix

    A Glossary:Subclass of Class:MMTK.NormalModes.SubspaceNormalModes.

    This class differs from SubspaceNormalModes in that it obtains
    the Cartesian force constant matrix in a sparse-matrix format.
    This is advantageous if the Cartesian force constant matrix
    is sparse (as it is for force fields without long-range terms),
    but for non-sparse matrices the memory requirements are
    higher than for SubspaceNormalModes.


    Constructor: SparseMatrixSubspaceNormalModes(|universe|, |basis|,
                                                 |temperature|=300)

    Arguments:

    |universe| -- the system for which the normal modes are calculated;
                  it must have a force field which provides the second
                  derivatives of the potential energy

    |basis| -- the basis for the subspace in which the normal modes
               are calculated (or, more precisely, a set of vectors
               spanning the subspace; it does not have to be orthogonal).
               This can either be a sequence of ParticleVector objects
               or a tuple of two such sequences. In the second case,
               the subspace is defined by the space spanned by the
               first set of vectors projected on the complement of the
               space spanned by the second set of vectors. The second
               set thus defines directions that are excluded from
               the subspace.

    |temperature| -- the temperature for which the amplitudes of the
                     atomic displacement vectors are calculated. A
                     value of 'None' can be specified to have no scaling
                     at all. In that case the mass-weighted norm
                     of each normal mode is one.

    In order to obtain physically reasonable normal modes, the configuration
    of the universe must correspond to a local minimum of the potential
    energy.

    A SparseMatrixSubspaceNormalModes object behaves like a sequence
    of modes.
    Individual modes (see class Class:MMTK.NormalModes.Mode) can be
    extracted by indexing with an integer. Looping over the modes is
    possible as well.
    """

    def _forceConstantMatrix(self):
	from MMTK_forcefield import SparseForceConstants
	self._setupBasis()
	nmodes, natoms = self.basis.shape
	natoms = natoms/3
	self.nmodes = nmodes
	self.natoms = natoms
	fc = SparseForceConstants(natoms, 5*natoms)
	eval = self.universe.energyEvaluator()
	energy, g, fc = eval(0, fc, 0)
	self.array = Numeric.zeros((nmodes, nmodes), Numeric.Float)
	for i in range(nmodes):
	    v = Numeric.reshape(self.basis[i], (natoms, 3))/self.sqrt_mass
	    v = fc.multiplyVector(v)
	    v = v/self.sqrt_mass
	    v.shape = (3*natoms,)
	    self.array[i, :] = Numeric.dot(self.basis, v)

#
# Helper functions
#

# Fill in the lower triangle of an upper-triangle symmetric matrix

def _symmetrize(a):
    n = a.shape[0]
    for i in range(n):
	for j in range(i+1, n):
	    a[j,i] = a[i,j]
