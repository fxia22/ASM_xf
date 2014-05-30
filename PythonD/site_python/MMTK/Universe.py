# This module implements the various types of universes
# (infinite, periodic etc.). A universe defines the
# geometry of space, the force field, and external interactions
# (boundary conditions, external fields, etc.)
#
# Written by Konrad Hinsen
# last revision: 2001-5-14
#

import Bonds, ChemicalObjects, Collection, Environment, \
       Random, Utility, ParticleProperties, Visualization
from Scientific.Geometry import Transformation
from Scientific.Geometry import Vector, isVector
import copy, Numeric, operator, string

try:
    import threading
    if not hasattr(threading, 'Thread'):
	threading = None
except ImportError:
    threading = None

#
# The base class for all universes.
#
class Universe(Collection.GroupOfAtoms, Visualization.Viewable):

    """Complete model of chemical system

    A Glossary:Subclass of Class:MMTK.Collection.GroupOfAtoms
    and Class:MMTK.Visualization.Viewable.

    A universe represents a complete model of a chemical system, i.e.
    the molecules, their environment (topology, boundary conditions,
    thermostats, etc.), and optionally a force field.

    The class Universe is an Glossary:abstract-base-class that defines
    properties common to all kinds of universes. To create universe
    objects, use one of its subclasses.

    In addition to the methods listed below, universe objects support
    the following operations ('u' is any universe object, 'o' is any
    chemical object):

    - 'len(u)' yields the number of chemical objects in the universe
    - 'u[i]' returns object number 'i'
    - 'u.name = o' adds 'o' to the universe and also makes it accessible as
      an attribute
    - 'del u.name' removes the object that was assigned to 'u.name' from
       the universe
    """

    def __init__(self, forcefield, properties):
	self._forcefield = forcefield
	self._evaluator = {}
	self.name = ''
	if properties.has_key('name'):
	    self.name = properties['name']
	    del properties['name']
	self._objects = Collection.Collection()
        self._environment = []
	self._configuration = None
	self._atom_properties = {}
        self._atoms = None
        self._bond_database = None
        self._bond_pairs = None
	self._version = 0
	self._np = None

    is_universe = 1
    is_periodic = 0

    def __getstate__(self):
	state = copy.copy(self.__dict__)
	state['_evaluator'] = {}
	state['_configuration'] = None
	del state['_bond_database']
	del state['_bond_pairs']
	del state['_np']
        del state['_spec']
	return state

    def __setstate__(self, state):
	state['_np'] = None
	state['_atoms'] = None
	state['_bond_database'] = None
	state['_bond_pairs'] = None
        self.__dict__['_environment'] = []
        if state.has_key('atom_properties'):
            self.__dict__['_atom_properties'] = state['atom_properties']
            del state['atom_properties']
	for attr, value in state.items():
	    self.__dict__[attr] = value
	self._evaluator = {}
        self._createSpec()

    def __len__(self):
	return len(self._objects)

    def __getitem__(self, item):
	return self._objects[item]

    def __setattr__(self, attr, value):
	self.__dict__[attr] = value
	if attr[0] != '_' and (ChemicalObjects.isChemicalObject(value)
                               or Environment.isEnvironmentObject(value)):
	    self.addObject(value)

    def __delattr__(self, attr):
        try:
            self.removeObject(self.__dict__[attr])
        except ValueError:
            pass
	del self.__dict__[attr]

    def __repr__(self):
	return self.__class__.__name__ + ' ' + self.name + ' containing ' + \
               `len(self._objects)` + ' objects.'
    __str__ = __repr__

    def __copy__(self):
	return copy.deepcopy(self)

    def objectList(self, klass = None):
        """Returns a list of all chemical objects in the universe.
        If |klass| is not None, only objects whose class is equal
        to |klass| are returned."""
	return self._objects.objectList(klass)

    def environmentObjectList(self, klass = None):
        """Returns a list of all environment objects in the universe.
        If |klass| is not None, only objects whose class is equal
        to |klass| are returned."""
        if klass is None:
            return self._environment
        else:
            return filter(lambda o, k=klass: o.__class__ is k,
                          self._environment)

    def atomList(self):
        """Returns a list of all atoms in the universe. This includes
        atoms that make up the compound chemical objects (molecules etc.)."""
        if self._atoms is None:
            self._atoms = self._objects.atomList()
        return self._atoms

    def bondedUnits(self):
        return self._objects.bondedUnits()

    def universe(self):
        "Returns the universe itself."
	return self

    def addObject(self, object):
        """Adds |object| to the universe. If |object| is a Collection,
        all elements of the Collection are added to the universe. An
        object can only be added to a universe if it is not already
        part of another universe."""
        if ChemicalObjects.isChemicalObject(object):
	    if object.parent is not None:
		if isUniverse(object.parent):
		    raise ValueError, `object` + \
			  ' is already in another universe'
		else:
		    raise ValueError, `object` + ' is part of another object'
	    object.parent = self
	    self._objects.addObject(object)
	    self._changed(1)
        elif Environment.isEnvironmentObject(object):
            for o in self._environment:
                o.checkCompatibilityWith(object)
            self._environment.append(object)
            self._changed(0)
	elif Collection.isCollection(object) \
             or Utility.isSequenceObject(object):
	    for o in object:
		self.addObject(o)
        else:
            raise TypeError, repr(object) + ' cannot be added to a universe'

    def removeObject(self, object):
        """Removes |object| from the universe. If |object| is a Collection,
        each of its elements is removed. The object to be removed must
        be in the universe."""
	if Collection.isCollection(object) or Utility.isSequenceObject(object):
	    for o in object:
		self.removeObject(o)
	elif ChemicalObjects.isChemicalObject(object):
	    if object.parent != self:
		raise ValueError, `object` + ' is not in this universe.'
	    object.parent = None
	    self._objects.removeObject(object)
	    self._changed(1)
        elif Environment.isEnvironmentObject(object):
            self._environment.remove(object)
	    self._changed(0)
        else:
            raise ValueError, `object` + ' is not in this universe.'

    def selectShell(self, point, r1, r2=0.):
        """Return a Collection of all objects in the universe whose
        distance from |point| is between |r1| and |r2|."""
	return self._objects.selectShell(point, r1, r2)

    def selectBox(self, p1, p2):
        """Return a Collection of all objects in the universe that lie
        within a box whose corners are given by |p1| and |p2|."""
	return self._objects.selectBox(p1, p2)

    def _changed(self, system_size_changed):
	self._evaluator = {}
        self._bond_database = None
	self._version = self._version + 1
        if system_size_changed:
            self._configuration = None
            self._atom_properties = {}
            self._atoms = None
            self._np = None
            self._bond_pairs = None

    def acquireReadStateLock(self):
        """Acquire the universe read state lock. Any application that
        uses threading must acquire this lock prior to accessing the
        current state of the universe, in particular its configuration
        (particle positions). This guarantees the consistency of the
        data; while any thread holds the read state lock, no other
        thread can obtain the write state lock that permits modifying
        the state. The read state lock should be released as soon as
        possible.

        The read state lock can be acquired only if no thread holds
        the write state lock. If the read state lock cannot be
        acquired immediately, the thread will be blocked until
        it becomes available. Any number of threads can acquire
        the read state lock simultaneously."""
        return self._spec.stateLock(1)

    def acquireWriteStateLock(self):
        """Acquire the universe write state lock. Any application that
        uses threading must acquire this lock prior to modifying the
        current state of the universe, in particular its configuration
        (particle positions). This guarantees the consistency of the
        data; while any thread holds the write state lock, no other
        thread can obtain the read state lock that permits accessing
        the state. The write state lock should be released as soon as
        possible.

        The write state lock can be acquired only if no other thread
        holds either the read state lock or the write state lock. If
        the write state lock cannot be acquired immediately, the
        thread will be blocked until it becomes available."""
        return self._spec.stateLock(-1)

    def releaseReadStateLock(self, write=0):
        "Release the universe read state lock."
        return self._spec.stateLock(2)

    def releaseWriteStateLock(self, write=0):
        "Release the universe write state lock."
        return self._spec.stateLock(-2)

    def acquireConfigurationChangeLock(self, waitflag=1):
        """Acquire the configuration change lock. This lock should be
        acquired before starting an algorithm that changes the
        configuration continuously, e.g. minimization or molecular dynamics
        algorithms. This guarantees the proper order of execution when
        several such operations are started in succession. For example,
        when a minimization should be followed by a dynamics run,
        the use of this flag permits both operations to be started
        as background tasks which will be executed one after the other,
        permitting other threads to run in parallel.

        The configuration change lock should not be confused with
        the universe state lock. The former guarantees the proper
        sequence of long-running algorithms, whereas the latter
        guarantees the consistency of the data. A dynamics algorithm,
        for example, keeps the configuration change lock from the
        beginning to the end, but acquires the universe state lock
        only immediately before modifying configuration and velocities,
        and releases it immediately afterwards.
        
        If |waitflag| is true, the method waits until the lock
        becomes available; this is the most common operation. If
        |waitflag| is false, the method returns immediately even
        if another thread holds the lock. The return value indicates
        if the lock could be acquired (1) or not (0)."""
        if waitflag:
            return self._spec.configurationChangeLock(1)
        else:
            return self._spec.configurationChangeLock(0)

    def releaseConfigurationChangeLock(self):
        "Releases the configuration change lock."
        self._spec.configurationChangeLock(2)

    def setForceField(self, forcefield):
        "Assign a new |forcefield| to the universe."
	self._forcefield = forcefield
	self._evaluator = {}
        self._bond_database = None

    def position(self, object, conf):
	if ChemicalObjects.isChemicalObject(object):
	    return object.position(conf)
	elif isVector(object):
	    return object
	else:
	    return Vector(object)

    def numberOfAtoms(self):
        return self._objects.numberOfAtoms()

    def numberOfPoints(self):
        if self._np is None:
            self._np = Collection.GroupOfAtoms.numberOfPoints(self)
        return self._np

    numberOfCartesianCoordinates = numberOfPoints

    def configuration(self):
        """Return the configuration object describing the current configuration
        of the universe. Note that this is not a copy of the current state;
        the positions in the configuration object will change when coordinate
        changes are applied to the universe in whatever way."""
	if self._configuration is None:
	    np = self.numberOfPoints()
	    coordinates = Numeric.zeros((np, 3), Numeric.Float)
	    indices = range(np)
	    redef = []
	    for a in self.atomList():
		if not a.setArray(coordinates, indices):
		    redef.append(a)
	    for a in redef:
		a.setArray(coordinates, indices[0:1])
		del indices[0]
	    self._configuration = 1
	    self._configuration = \
                         ParticleProperties.Configuration(self, coordinates)
            self._spec.foldCoordinatesIntoBox(coordinates)
	return self._configuration

    def copyConfiguration(self):
        """Returns a copy of the current configuration.

        This operation is thread-safe; it won't return inconsistent
        data even when another thread is modifying the
        configuration."""
        self.acquireReadStateLock()
        try:
            conf = copy.copy(self.configuration())
        finally:
            self.releaseReadStateLock()
        return conf

    def atomNames(self):
	self.configuration()
	names = self.numberOfAtoms()*[None]
	for a in self.atomList():
	    names[a.index] = a.fullName()
	return names

    def setConfiguration(self, configuration, block=1):
        """Copy all positions are from |configuration| (which must be
        a Configuration object) to the current universe configuration.

        This operation is thread-safe; it blocks other threads that
        want to access the configuration while the data is being
        updated. If this is not desired (e.g. when calling from
        a routine that handles locking itself), the optional parameter
        |block| should be set to 0."""
        if not ParticleProperties.isConfiguration(configuration):
            raise TypeError, 'not a universe configuration'
	conf = self.configuration()
        if block:
            self.acquireWriteStateLock()
        try:
            conf.assign(configuration)
            self.setCellParameters(configuration.cell_parameters)
        finally:
            if block:
                self.releaseWriteStateLock()

    def addToConfiguration(self, displacement, block=1):
        """Add |displacement| (a ParticleVector object) to the current
        configuration of the universe.

        This operation is thread-safe; it blocks other threads that
        want to access the configuration while the data is being
        updated. If this is not desired (e.g. when calling from
        a routine that handles locking itself), the optional parameter
        |block| should be set to 0."""
	conf = self.configuration()+displacement
        if block:
            self.acquireWriteStateLock()
        try:
            conf.assign(conf)
        finally:
            if block:
                self.releaseWriteStateLock()

    def getParticleScalar(self, name, datatype = Numeric.Float):
        """Return a ParticleScalar object containing the values of the
        attribute |name| for each atom in the universe."""
	conf = self.configuration()
	array = Numeric.zeros((len(conf),), datatype)
        for a in self.atomList():
	    array[a.index] = getattr(a, name)
	return ParticleProperties.ParticleScalar(self, array)
    getAtomScalarArray = getParticleScalar

    def getParticleBoolean(self, name):
        """Return a ParticleScalar object containing the boolean values
        (0 or 1) of the attribute |name| for each atom in the universe.
        An atom that does not have the attribute |name| is assigned
        a value of zero."""
	conf = self.configuration()
	array = Numeric.zeros((len(conf),), Numeric.Int)
	for a in self.atomList():
	    try:
		array[a.index] = getattr(a, name)
	    except AttributeError: pass
	return ParticleProperties.ParticleScalar(self, array)
    getAtomBooleanArray = getParticleBoolean

    def renumberAtoms(self, indices):
	conf = self.configuration()
	for a in self.atomList():
	    a.index = indices[a.index]
	indices = Numeric.argsort(indices)
	conf.array[:] = Numeric.take(conf.array, indices)
	self._changed(1)

    def masses(self):
        "Return a ParticleScalar object containing the atom masses."
	return self.getParticleScalar('_mass')

    def charges(self):
        """Return a ParticleScalar object containing the atom charges.
        Since charges are parameters defined by a force field, this
        method will raise an exception if no force field is defined or
        if the current force field defines no charges."""
        ff = self._forcefield
        if ff is None:
            raise ValueError, "no force field defined"
        return ff.charges(self)

    def velocities(self):
        """Returns ParticleVector object containing the current velocities of
        all atoms. If no velocities are defined, the return value is 'None'.
        Note that the return value is not a copy of the current state but
        a reference to it; its data will change when any changes are made
        to the current velocities."""
	try:
	    return self._atom_properties['velocity']
	except KeyError:
	    return None

    def setVelocities(self, velocities, block=1):
        """Set the current atom velocities to the values contained in
        the ParticleVector object |velocities|. If |velocities| is
        None, the velocity information is removed from the universe.

        This operation is thread-safe; it blocks other threads that
        want to access the velocities while the data is being
        updated. If this is not desired (e.g. when calling from
        a routine that handles locking itself), the optional parameter
        |block| should be set to 0."""
        if velocities is None:
            try:
                del self._atom_properties['velocity']
            except KeyError:
                pass
        else:
            try:
                v = self._atom_properties['velocity']
            except KeyError:
                v = ParticleProperties.ParticleVector(self)
                self._atom_properties['velocity'] = v
            if block:
                self.acquireWriteStateLock()
            try:
                v.assign(velocities)
            finally:
                if block:
                    self.releaseWriteStateLock()

    def initializeVelocitiesToTemperature(self, temperature):
        """Generate random velocities for all atoms from a Boltzmann
        distribution at the given |temperature|."""
	self.configuration()
	masses = self.masses()
	if self._atom_properties.has_key('velocity'):
	    del self._atom_properties['velocity']
	fixed = self.getParticleBoolean('fixed')
	np = self.numberOfPoints()
	velocities = Numeric.zeros((np, 3), Numeric.Float)
	for i in xrange(np):
	    m = masses[i]
	    if m > 0. and not fixed[i]:
		velocities[i] = Random.randomVelocity(temperature,
                                                           m).array
	self._atom_properties['velocity'] = \
			  ParticleProperties.ParticleVector(self, velocities)
        self.adjustVelocitiesToConstraints()

    def scaleVelocitiesToTemperature(self, temperature, block=1):
        """Scale all velocities by a common factor in order to obtain
        the specified |temperature|.

        This operation is thread-safe; it blocks other threads that
        want to access the velocities while the data is being
        updated.  If this is not desired (e.g. when calling from
        a routine that handles locking itself), the optional parameter
        |block| should be set to 0."""
	velocities = self.velocities()
	factor = Numeric.sqrt(temperature/self.temperature())
        if block:
            self.acquireWriteStateLock()
        try:
            velocities.scaleBy(factor)
        finally:
            if block:
                self.releaseWriteStateLock()

    def degreesOfFreedom(self):
        return GroupOfAtoms.degreesOfFreedom(self) \
               - self.numberOfDistanceConstraints()

    def distanceConstraintList(self):
        "Returns the list of distance constraints."
        return self._objects.distanceConstraintList()

    def numberOfDistanceConstraints(self):
        "Returns the number of distance constraints."
        return self._objects.numberOfDistanceConstraints()

    def setBondConstraints(self):
        "Sets distance constraints for all bonds."
        self.configuration()
        self._objects.setBondConstraints(self)
        self.enforceConstraints()

    def removeDistanceConstraints(self):
        "Removes all distance constraints."
        self._objects.removeDistanceConstraints(self)

    def enforceConstraints(self, configuration=None, velocities=None):
        """Enforces the previously defined distance constraints
        by modifying the configuration and velocities."""
        import Dynamics
        Dynamics.enforceConstraints(self, configuration)
        self.adjustVelocitiesToConstraints(velocities)

    def adjustVelocitiesToConstraints(self, velocities=None, block=1):
        """Modifies the velocities to be compatible with
        the distance constraints, i.e. projects out the velocity
        components along the constrained distances.

        This operation is thread-safe; it blocks other threads that
        want to access the velocities while the data is being
        updated. If this is not desired (e.g. when calling from
        a routine that handles locking itself), the optional parameter
        |block| should be set to 0."""
        import Dynamics
        if velocities is None:
            velocities = self.velocities()
        if velocities is not None:
            if block:
                self.acquireWriteStateLock()
            try:
                Dynamics.projectVelocities(self, velocities)
            finally:
                if block:
                    self.releaseWriteStateLock()

    def bondLengthDatabase(self):
        if self._bond_database is None:
            self._bond_database = None
            if self._bond_database is None:
                ff = self._forcefield
                try:
                    self._bond_database = ff.bondLengthDatabase(self)
                except AttributeError:
                    pass
            if self._bond_database is None:
                self._bond_database = Bonds.DummyBondLengthDatabase(self)
        return self._bond_database

    def forcefield(self):
        "Returns the force field."
	return self._forcefield

    def energyEvaluator(self, subset1 = None, subset2 = None,
                        threads=1, mpi_communicator=None):
	if self._forcefield is None:
	    raise ValueError, "no force field defined"
	try:
	    eval = self._evaluator[(subset1, subset2, threads)]
	except KeyError:
            from ForceFields import ForceField
	    eval = ForceField.EnergyEvaluator(self, self._forcefield,
					      subset1, subset2,
                                              threads, mpi_communicator)
	    self._evaluator[(subset1, subset2, threads)] = eval
	return eval

    def energy(self, subset1 = None, subset2 = None, small_change=0):
        """Returns the energy. Without any parameters, the energy is
        calculated for the whole universe. If |subset1| is given,
        only the energy terms within the atoms in |subset1| are calculated.
        If |subset1| and |subset2| are given, only the energy terms
        between atoms of the two subsets are evaluated. The parameter
        |small_change| can be set to one in order to obtain a faster
        energy evaluation when the current configuration differs from
        the one during the last energy evaluation only by small displacements.
        """
	eval = self.energyEvaluator(subset1, subset2)
	return eval(0, 0, small_change)

    def energyAndGradients(self, subset1 = None, subset2 = None,
			   small_change=0):
        "Returns the energy and the energy gradients (a ParticleVector)."
	eval = self.energyEvaluator(subset1, subset2)
	return eval(1, 0, small_change)

    def energyAndForceConstants(self, subset1 = None, subset2 = None,
				small_change=0):
        """Returns the energy and the force constants
        (a SymmetricParticleTensor)."""
	eval = self.energyEvaluator(subset1, subset2)
	e, g, fc = eval(0, 1, small_change)
	return e, fc

    def energyGradientsAndForceConstants(self, subset1 = None, subset2 = None,
					 small_change=0):
        """Returns the energy, the energy gradients (a ParticleVector),
        and the force constants (a SymmetricParticleTensor)."""
	eval = self.energyEvaluator(subset1, subset2)
	return eval(1, 1, small_change)

    def energyTerms(self, subset1 = None, subset2 = None, small_change=0):
        """Returns a dictionary containing the energy values for each
        energy term separately. The energy terms are defined by the
        force field."""
	eval = self.energyEvaluator(subset1, subset2)
	eval(0, 0, small_change)
	return eval.lastEnergyTerms()

    def distanceVector(self, p1, p2, conf=None):
        """Returns the distance vector between |p1| and |p2| (i.e. the
        vector from |p1| to |p2|) in the
        configuration |conf|. |p1| and |p2| can be vectors
        or subsets of the universe, in which case their center-of-mass
        positions are used. If |conf| is 'None', the current configuration
        of the universe is used. The result takes the universe topology
        (periodic boundary conditions etc.) into account."""
        p1 = self.position(p1, conf)
        p2 = self.position(p2, conf)
        if conf is None:
            return Vector(self._spec.distanceVector(p1.array, p2.array))
        else:
            cell = conf.cell_parameters
            if cell is None:
                return Vector(self._spec.distanceVector(p1.array, p2.array))
            else:
                return Vector(self._spec.distanceVector(p1.array, p2.array,
                                                        cell))
            
    def distance(self, p1, p2, conf = None):
        """Returns the distance between |p1| and |p2|, i.e. the length
        of the distance vector."""
	return self.distanceVector(p1, p2, conf).length()

    def angle(self, p1, p2, p3, conf = None):
        """Returns the angle between the distance vectors |p1|-|p2| and
        |p3|-|p2|."""
	v1 = self.distanceVector(p2, p1, conf)
	v2 = self.distanceVector(p2, p3, conf)
	return v1.angle(v2)

    def dihedral(self, p1, p2, p3, p4, conf = None):
        """Returns the dihedral angle between the plane containing the
        distance vectors |p1|-|p2| and |p3|-|p2| and the plane containing the
        distance vectors |p2|-|p3| and |p4|-|p3|."""
	v1 = self.distanceVector(p2, p1, conf)
	v2 = self.distanceVector(p3, p2, conf)
	v3 = self.distanceVector(p3, p4, conf)
	a = v1.cross(v2).normal()
	b = v3.cross(v2).normal()
	cos = a*b
	sin = b.cross(a)*v2/v2.length()
	return Transformation.angleFromSineAndCosine(sin, cos)

    def _deleteAtom(self, atom):
	pass

    def basisVectors(self):
        """Returns the basis vectors of the elementary cell of a periodic
        universe. For a non-periodic universe the return value is 'None'."""
	return None

    def reciprocalBasisVectors(self):
        """Returns the reciprocal basis vectors of the elementary cell of a
        periodic universe. For a non-periodic universe the return value is
        'None'."""
	return None

    def cellParameters(self):
        return None

    def setCellParameters(self, parameters):
        if parameters is not None:
            raise ValueError, 'incompatible cell parameters'

    def cellVolume(self):
        """Returns the volume of the elementary cell of a periodic
        universe. For a non-periodic universe the return value is 'None'."""
	return None

    def largestDistance(self):
        """Returns the largest possible distance that any two points
        can have in the universe. Returns 'None' if no such upper limit
        exists."""
        return None

    def contiguousObjectOffset(self, objects = None, conf = None,
                               box_coordinates = 0):
        """Returns a ParticleVector with displacements relative to
        the configuration |conf| which when added to the configuration
        create a configuration in which none of the |objects| is split
        across the edge of the elementary cell. For nonperiodic universes
        the return value is 'None'. If no object list is specified, the
        list of elements of the universe is used. The configuration
        defaults to the current configuration of the universe."""
        return None

    def contiguousObjectConfiguration(self, objects = None, conf = None):
        """Returns configuration |conf| (default: current configuration)
        corrected by the contiguous object offsets for that
        configuration."""
        offset = self.contiguousObjectOffset(objects, conf)
        if conf is None:
            conf = self.configuration()
        if offset is not None:
            return conf + offset
        else:
            return copy.copy(conf)

    def realToBoxCoordinates(self, vector):
        """Returns the box coordinate equivalent of |vector|.
        Box coordinates are defined only for periodic universes;
        their components have values between -0.5 and 0.5; these
        extreme values correspond to the walls of the simulation box.
        For a nonperiodic universe, |vector| is returned unchanged."""
        return vector
    
    def boxToRealCoordinates(self, vector):
        """Returns the real-space equivalent of the box coordinate
        |vector|."""
        return vector

    def _realToBoxPointArray(self, array, parameters=None):
        return array

    def _boxToRealPointArray(self, array, parameters=None):
        return array

    def foldCoordinatesIntoBox(self):
        return

    def randomPoint(self):
        """Returns a random point from a uniform distribution within
        the universe. This operation is defined only for finite-volume
        universes, e.g. periodic universes."""
	raise TypeError, "undefined operation"

    def map(self, function):
        """Applies |function| to all objects in the universe and
        returns the list of the results. If the results are chemical
        objects, a Collection is returned instead of a list."""
	return self._objects.map(function)

    def description(self, objects = None, index_map = None):
	if objects is None:
	    objects = self
        attributes = {}
        for attr in dir(self):
            if attr[0] != '_':
                object = getattr(self, attr)
                if ChemicalObjects.isChemicalObject(object) \
                   or Environment.isEnvironmentObject(object):
                    attributes[object] = attr
        items = []
        for o in objects.objectList():
            attr = attributes.get(o, None)
            if attr is not None:
                items.append(repr(attr))
            items.append(o.description(index_map))
        for o in self._environment:
            attr = attributes.get(o, None)
            if attr is not None:
                items.append(repr(attr))
            items.append(o.description())
        s = 'c(%s,[%s])' % \
            (`self.__class__.__name__ + self._descriptionArguments()`,
             string.join(items, ','))
	return s

    def _graphics(self, conf, distance_fn, model, module, options):
	return self._objects._graphics(conf, distance_fn, model,
				       module, options)

    def setFromTrajectory(self, trajectory, step = None):
        """Set the state of the universe to the one stored in
        the given |step| of the given |trajectory|. If no step number
        is given, the most recently written step is used for a restart
        trajectory, and the first step (number zero) for a normal
        trajectory.

        This operation is thread-safe; it blocks other threads that
        want to access the configuration or velocities while the data is
        being updated."""
        if step is None:
            step = trajectory.defaultStep()
        self.acquireWriteStateLock()
        try:
            self.setConfiguration(trajectory.configuration[step], 0)
            vel = self.velocities()
            try:
                vel_tr = trajectory.velocities[step]
            except AttributeError:
                if vel is not None:
                    Utility.warning("velocities were not modified because " +
                                    "the trajectory does not contain " +
                                    "velocity data.")
                return
            if vel is None:
                self._atom_properties['velocity'] = vel_tr
            else:
                vel.assign(vel_tr)
        finally:
            self.releaseWriteStateLock()

    #
    # More efficient reimplementations of methods in Collection.GroupOfAtoms
    #
    def numberOfFixedAtoms(self):
        return self.getParticleBoolean('fixed').sumOverParticles()

    def degreesOfFreedom(self):
        return 3*(self.numberOfAtoms()-self.numberOfFixedAtoms()) \
               - self.numberOfDistanceConstraints()

    def mass(self):
        return self.masses().sumOverParticles()

    def centerOfMass(self, conf = None):
        m = self.masses()
        if conf is None:
            conf = self.configuration()
        return (m*conf).sumOverParticles()/m.sumOverParticles()

    def kineticEnergy(self, velocities = None):
	if velocities is None:
	    velocities = self.velocities()
        return 0.5*velocities.massWeightedDotProduct(velocities)

    def momentum(self, velocities = None):
	if velocities is None:
	    velocities = self.velocities()
        return (self.masses()*velocities).sumOverParticles()

    def translateBy(self, vector):
        conf = self.configuration().array
        Numeric.add(conf, vector.array[Numeric.NewAxis, :], conf)

    def applyTransformation(self, t):
        conf = self.configuration().array
        rot = t.rotation().tensor.array
        conf[:] = Numeric.dot(conf, Numeric.transpose(rot))
        self.translateBy(t.translation().vector)

#
# Infinite universes
#
class InfiniteUniverse(Universe):

    """Infinite (unbounded and nonperiodic) universe.

    A Glossary:Subclass of Class:MMTK.Universe.Universe.

    Constructor: InfiniteUniverse(|forcefield|=None)

    Arguments:

    |forcefield| -- a force field object, or 'None' for no force field
    """

    def __init__(self, forcefield=None, **properties):
	Universe.__init__(self, forcefield, properties)
        self._createSpec()

    def CdistanceFunction(self):
	from MMTK_universe import infinite_universe_distance_function
	return infinite_universe_distance_function, Numeric.array([0.])

    def CcorrectionFunction(self):
	from MMTK_universe import infinite_universe_correction_function
	return infinite_universe_correction_function, Numeric.array([0.])

    def CvolumeFunction(self):
	from MMTK_universe import infinite_universe_volume_function
	return infinite_universe_volume_function, Numeric.array([0.])

    def CboxTransformationFunction(self):
        return None, Numeric.array([0.])

    def _createSpec(self):
        from MMTK_universe import InfiniteUniverseSpec
        self._spec = InfiniteUniverseSpec()

    def _descriptionArguments(self):
        if self._forcefield is None:
            return '()'
        else:
            return '(%s)' % self._forcefield.description()

#
# Orthorhombic universe with periodic boundary conditions
#
class OrthorhombicPeriodicUniverse(Universe):

    """Periodic universe with orthorhombic elementary cell.

    A Glossary:Subclass of Class:MMTK.Universe.Universe.

    Constructor: OrthorhombicPeriodicUniverse(|shape|, |forcefield|=None)

    Arguments:
    
    |shape| -- a sequence of length three specifying the edge
               lengths along the x, y, and z directions

    |forcefield| -- a force field object, or 'None' for no force field
    """

    def __init__(self, size = None, forcefield = None, **properties):
	Universe.__init__(self, forcefield, properties)
	self.data = Numeric.zeros((3,), Numeric.Float)
	if size is not None:
	    self.setSize(size)
        self._createSpec()

    is_periodic = 1

    def __setstate__(self, state):
        Universe.__setstate__(self, state)
        if len(self.data.shape) == 2:
            self.data = self.data[0]

    def setSize(self, size):
        self.data[:] = size

    def scaleSize(self, factor):
        "Multiplies all edge lengths by |factor|."
	self.data[:] = factor*self.data
        self._spec.foldCoordinatesIntoBox(self.configuration().array)

    def setVolume(self, volume):
        """Multiplies all edge lengths by the same factor such that the cell
        volume becomes |volume|."""
        factor = (volume/self.cellVolume())**(1./3.)
        self.scaleSize(factor)

    def foldCoordinatesIntoBox(self):
        self._spec.foldCoordinatesIntoBox(self.configuration().array)

    def setCellParameters(self, parameters):
        if parameters is not None:
            self.data[:] = parameters

    def realToBoxCoordinates(self, vector):
        x, y, z = vector
        return Vector(x/self.data[0],
                      y/self.data[1],
                      z/self.data[2])

    def boxToRealCoordinates(self, vector):
        x, y, z = vector
        return Vector(x*self.data[0],
                      y*self.data[1],
                      z*self.data[2])

    def _realToBoxPointArray(self, array, parameters=None):
        if parameters is None:
            parameters = self.data
        if parameters.shape == (3,):
            parameters = parameters[Numeric.NewAxis, :]
        return array/parameters

    def _boxToRealPointArray(self, array, parameters=None):
        if parameters is None:
            parameters = self.data
        if parameters.shape == (3,):
            parameters = parameters[Numeric.NewAxis, :]
        return array*parameters

    def CdistanceFunction(self):
	from MMTK_universe import orthorhombic_universe_distance_function
	return orthorhombic_universe_distance_function, self.data

    def CcorrectionFunction(self):
	from MMTK_universe import orthorhombic_universe_correction_function
	return orthorhombic_universe_correction_function, self.data

    def CvolumeFunction(self):
	from MMTK_universe import orthorhombic_universe_volume_function
	return orthorhombic_universe_volume_function, self.data

    def CboxTransformationFunction(self):
	from MMTK_universe import orthorhombic_universe_box_transformation
	return orthorhombic_universe_box_transformation, self.data

    def cellParameters(self):
        return self.data

    def basisVectors(self):
	return [self.data[0]*Vector(1., 0., 0.),
                self.data[1]*Vector(0., 1., 0.),
                self.data[2]*Vector(0., 0., 1.)]

    def reciprocalBasisVectors(self):
	return [Vector(1., 0., 0.)/self.data[0],
                Vector(0., 1., 0.)/self.data[1],
                Vector(0., 0., 1.)/self.data[2]]

    def cellVolume(self):
	return Numeric.multiply.reduce(self.data)

    def largestDistance(self):
        return 0.5*Numeric.minimum.reduce(self.data)

    def contiguousObjectOffset(self, objects = None, conf = None,
                               box_coordinates = 0):
        from MMTK_universe import contiguous_object_offset
        if objects is None:
            default = 1
            objects = self._objects.objectList()
            pairs = self._bond_pairs
        else:
            default = 0
            pairs = None
        if conf is None:
            conf = self.configuration()
        cell = conf.cell_parameters
        offset = ParticleProperties.ParticleVector(self)
        if pairs is None:
            pairs = []
            for o in objects:
                new_object = 1
                if ChemicalObjects.isChemicalObject(o):
                    units = o.bondedUnits()
                elif Collection.isCollection(o) or isUniverse(o):
                    included = {}
                    for element in o:
                        top = element.topLevelChemicalObject()
                        for u in top.bondedUnits():
                            included[u] = 1
                    units = included.keys()
                else:
                    raise ValueError, str(o) + " not a chemical object"
                for bu in units:
                    mpairs = bu.traverseBondTree(lambda a: a.index)
                    if len(mpairs) == 0:
                        atoms = bu.atomList()
                        first = atoms[0].index
                        for a in atoms[1:]:
                            mpairs.append((first, a.index))
                    if not new_object and len(pairs) > 0:
                        pairs.append((pairs[-1][1], mpairs[0][0]))
                    new_object = 0
                    pairs = pairs + mpairs
            pairs = Numeric.array(pairs)
            if default:
                self._bond_pairs = pairs
        if cell is None:
            contiguous_object_offset(self._spec, pairs, conf.array,
                                     offset.array, box_coordinates)
        else:
            contiguous_object_offset(self._spec, pairs, conf.array,
                                     offset.array, box_coordinates, cell)
        return offset

    def randomPoint(self):
	return Random.randomPointInBox(self.data[0], self.data[1],
                                       self.data[2])

    def _createSpec(self):
        from MMTK_universe import OrthorhombicPeriodicUniverseSpec
        self._spec = OrthorhombicPeriodicUniverseSpec(self.data)

    def _descriptionArguments(self):
        if self._forcefield is None:
            return '((0.,0.,0.),)'
        else:
            return '((0.,0.,0.),%s)' % self._forcefield.description()

#
# Cubic universe with periodic boundary conditions
#
class CubicPeriodicUniverse(OrthorhombicPeriodicUniverse):

    """Periodic universe with cubic elementary cell.

    A Glossary:Subclass of Class:MMTK.Universe.Universe.

    Arguments:
    
    |shape| -- a number specifying the edge
               length along the x, y, and z directions

    |forcefield| -- a force field object, or 'None' for no force field
    Constructor: CubicPeriodicUniverse(|shape|, |forcefield|=None)
    """

    def setSize(self, size):
	OrthorhombicPeriodicUniverse.setSize(self, 3*(size,))

    def _descriptionArguments(self):
        if self._forcefield is None:
            return '(0.)'
        else:
            return '(0.,%s)' % self._forcefield.description()

#
# Recognition functions
#
def isUniverse(object):
    "Returns 1 if |object| is a Universe."
    return hasattr(object, 'is_universe')
