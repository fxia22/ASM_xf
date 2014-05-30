# Harmonic restraint terms that can be added to a force field.
#
# Written by Konrad Hinsen
# last revision: 2000-2-10
#

"""This module contains harmonic restraint terms that can be added
to any force field.

Example:

from MMTK import *
from MMTK.ForceFields import Amber94ForceField
from MMTK.ForceFields.Restraints import HarmonicDistanceRestraint

universe = InfiniteUniverse()
universe.protein = Protein('bala1')
force_field = Amber94ForceField() + \
              HarmonicDistanceRestraint(universe.protein[0][1].peptide.N,
                                        universe.protein[0][1].peptide.O,
                                        0.5, 10.)
universe.setForceField(force_field)
"""

from ForceField import ForceField
from MMTK_forcefield import HarmonicDistanceTerm, HarmonicAngleTerm, \
                            CosineDihedralTerm
import Numeric

class HarmonicDistanceRestraint(ForceField):

    """Harmonic distance restraint between two atoms

    Constructor: HarmonicDistanceRestraint(|atom1|, |atom2|,
                                           |distance|, |force_constant|)

    Arguments:

    |atom1|, |atom2| -- the two atoms whose distance is restrained

    |distance| -- the distance at which the restraint is zero

    |force_constant| -- the force constant of the restraint term

    The functional form of the restraint is
    |force_constant|*((r1-r2).length()-|distance|)**2, where
    r1 and r2 are the positions of the two atoms.
    """

    def __init__(self, atom1, atom2, distance, force_constant):
        self.atom1 = atom1
        self.atom2 = atom2
        self.distance = distance
        self.force_constant = force_constant
        ForceField.__init__(self, 'harmonic distance restraint')

    def evaluatorTerms(self, universe, subset1, subset2, global_data):
        if self.atom1.universe() is not universe:
            raise ValueError, "Atom " + `self.atom1` + \
                  'is not in universe ' + `universe`
        if self.atom2.universe() is not universe:
            raise ValueError, "Atom " + `self.atom2` + \
                  'is not in universe ' + `universe`
        if subset1 is not None:
            s1 = subset1.atomList()
            s2 = subset2.atomList()
            if not ((self.atom1 in s1 and self.atom2 in s2) or \
                    (self.atom1 in s2 and self.atom2 in s1)):
                raise ValueError, "restraint outside subset"
        indices = Numeric.array([[self.atom1.index, self.atom2.index]])
        parameters = Numeric.array([[self.distance, self.force_constant]])
        return [HarmonicDistanceTerm(universe._spec, indices, parameters,
                                     self.name)]


class HarmonicAngleRestraint(ForceField):

    """Harmonic angle restraint between three atoms

    Constructor: HarmonicAngleRestraint(|atom1|, |atom2|, |atom3|,
                                        |angle|, |force_constant|)

    Arguments:

    |atom1|, |atom2|, |atom3| -- the three atoms whose angle is restrained;
    |atom2| is the central atom

    |angle| -- the angle at which the restraint is zero

    |force_constant| -- the force constant of the restraint term

    The functional form of the restraint is
    |force_constant|*(phi-|angle|)**2, where
    phi is the angle |atom1|-|atom2|-|atom3|.
    """

    def __init__(self, atom1, atom2, atom3, angle, force_constant):
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom3 = atom3
        self.angle = angle
        self.force_constant = force_constant
        ForceField.__init__(self, 'harmonic angle restraint')

    def evaluatorTerms(self, universe, subset1, subset2, global_data):
        if self.atom1.universe() is not universe:
            raise ValueError, "Atom " + `self.atom1` + \
                  'is not in universe ' + `universe`
        if self.atom2.universe() is not universe:
            raise ValueError, "Atom " + `self.atom2` + \
                  'is not in universe ' + `universe`
        if self.atom3.universe() is not universe:
            raise ValueError, "Atom " + `self.atom3` + \
                  'is not in universe ' + `universe`
        indices = Numeric.array([[self.atom1.index, self.atom2.index,
                                  self.atom3.index]])
        parameters = Numeric.array([[self.angle, self.force_constant]])
        return [HarmonicAngleTerm(universe._spec, indices, parameters,
                                  self.name)]

class HarmonicDihedralRestraint(ForceField):

    """Harmonic dihedral angle restraint between three atoms

    Constructor: HarmonicDihedralRestraint(|atom1|, |atom2|, |atom3|, |atom4|,
                                           |angle|, |force_constant|)

    Arguments:

    |atom1|, |atom2|, |atom3|, |atom4| -- the four atoms whose dihedral angle
    is restrained; |atom2| and |atom3| are on the common axis

    |angle| -- the dihedral angle at which the restraint is zero

    |force_constant| -- the force constant of the restraint term

    The functional form of the restraint is
    |force_constant|*(phi-|distance|)**2, where
    phi is the dihedral angle |atom1|-|atom2|-|atom3|-|atom4|.
    """

    def __init__(self, atom1, atom2, atom3, atom4, dihedral, force_constant):
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom3 = atom3
        self.atom4 = atom4
        self.dihedral = dihedral
        self.force_constant = force_constant
        ForceField.__init__(self, 'harmonic dihedral restraint')

    def evaluatorTerms(self, universe, subset1, subset2, global_data):
        if self.atom1.universe() is not universe:
            raise ValueError, "Atom " + `self.atom1` + \
                  'is not in universe ' + `universe`
        if self.atom2.universe() is not universe:
            raise ValueError, "Atom " + `self.atom2` + \
                  'is not in universe ' + `universe`
        if self.atom3.universe() is not universe:
            raise ValueError, "Atom " + `self.atom3` + \
                  'is not in universe ' + `universe`
        if self.atom4.universe() is not universe:
            raise ValueError, "Atom " + `self.atom4` + \
                  'is not in universe ' + `universe`
        indices = Numeric.array([[self.atom1.index, self.atom2.index,
                                  self.atom3.index, self.atom4.index]])
        parameters = Numeric.array([[0., self.dihedral,
                                     0., self.force_constant]])
        return [CosineDihedralTerm(universe._spec, indices, parameters,
                                   self.name)]
