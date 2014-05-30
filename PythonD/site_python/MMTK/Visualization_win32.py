# This module contains interfaces to external visualization programs
# and a visualization base class
#
# Written by Konrad Hinsen
# last revision: 1999-6-21
#

"""This module provides visualization of chemical objects and animated
visualization of normal modes and sequences of configurations, including
trajectories. Visualization depends on external visualization programs.
On Unix systems, these programs are defined by environment variables.
Under Windows NT, the system definitions for files with extension
"pdb" and "wrl" are used.

A viewer for PDB files can be defined by the environment variable
'PDBVIEWER'. For showing a PDB file, MMTK will execute a command
consisting of the value of this variable followed by a space
and the name of the PDB file.

A viewer for VRML files can be defined by the environment variable
'VRMLVIEWER'. For showing a VRML file, MMTK will execute a command
consisting of the value of this variable followed by a space
and the name of the VRML file.

Since there is no standard for launching viewers for animation,
MMTK supports only two programs: VMD and XMol. MMTK detects
these programs by inspecting the value of the environment
'PDBVIEWER'. This value must be the file name of the executable,
and must give "vmd" or "xmol" after stripping off an optional
directory specification.
"""

import ConfigIO, PDB, Universe, Utility
import Numeric, string, sys, tempfile, os

#
# If you want temporary files in a non-standard directory, make
# its name the value of this variable:
#
tempdir = None

#
# Get visualization program names
#
viewer = {}
prog = None
try:
    viewer['pdb'] = os.environ['PDBVIEWER']
    prog = os.path.split(string.split(viewer['pdb'])[0])[1]
except KeyError: pass
try:
    viewer['vrml'] = os.environ['VRMLVIEWER']
except KeyError: pass

#
# Visualization base class. Defines methods for general visualization
# tasks.
#
class Viewable:

    """Any viewable chemical object

    This class is a Glossary:MixInClass that defines a general
    visualization method for all viewable objects, i.e. chemical
    objects (atoms, molecules, etc.), collections, and universes.
    """

    def graphicsObjects(self, **options):
        """Returns a list of graphics objects that represent
        the object for which the method is called. All options
        are specified as keyword arguments:

        |configuration| -- the configuration in which the objects
                           are drawn (default: the current configuration)

        |model| -- a string specifying one of several graphical
                   representations ("wireframe", "tube", "ball_and_stick").
                   Default is "wireframe".

        |ball_radius| -- the radius of the balls representing the atoms
                         in a ball-and-stick model, default: 0.03
    
        |stick_radius| -- the radius of the sticks representing the bonds
                          in a ball-and-stick or tube model, default: 0.02
                          for the tube model, 0.01 for the ball-and-stick model

        |graphics_module| -- the module in which the elementary graphics
                             objects are defined
                             (default: Scientific.Visualization.VRML)

        |color_values| -- a Class:MMTK.ParticleScalar object that defines
                          a value for each atom which defines that
                          atom's color via the color scale object specified
                          by the option |color_scale|. If no value is
                          given for |color_values|, the atoms' colors are
                          taken from the attribute 'color' of each
                          atom object (default values for each chemical
                          element are provided in the chemical database).

        |color_scale| -- an object that returns a color object (as defined
                         in the module Scientific.Visualization.Color)
                         when called with a number argument. Suitable
                         objects are defined by
                         Scientific.Visualization.Color.ColorScale and
                         Scientific.Visualization.Color.SymmetricColorScale.
                         The object is used only when the option
                         |color_values| is specified as well. The default
                         is a blue-to-red color scale that covers the
                         range of the values given in |color_values|.
                         
        |color| -- a color name predefined in the module
                   Scientific.Visualization.Color. The corresponding
                   color is applied to all graphics objects that are
                   returned.
        """
        conf = options.get('configuration', None)
        model = options.get('model', 'wireframe')
        if model == 'tube':
            model = 'ball_and_stick'
            radius = options.get('stick_radius', 0.02)
            options['stick_radius'] = radius
            options['ball_radius'] = radius
	try:
	    module = options['graphics_module']
	except KeyError:
	    from Scientific.Visualization import VRML
	    module = VRML
        color = options.get('color', None)
        if color is None:
            color_values = options.get('color_values', None)
            if color_values is not None:
                lower = Numeric.minimum.reduce(color_values.array)
                upper = Numeric.maximum.reduce(color_values.array)
                options['color_scale'] = module.ColorScale((lower, upper))
	try:
	    distance_fn = self.universe().distanceVector
	except AttributeError:
	    distance_fn = Universe.InfiniteUniverse().distanceVector
	return self._graphics(conf, distance_fn, model, module, options)

    def _atomColor(self, atom, options):
        color = options.get('color', None)
        if color is not None:
            return color
        color_values = options.get('color_values', None)
        if color_values is None:
            return atom.color
        else:
            scale = options['color_scale']
            return scale(color_values[atom])

#
# View anything viewable.
#
def view(object, *parameters):
    "Equivalent to |object|.view(parameters)."
    apply(object.view, parameters)

#
# Display an object or a collection of objects using an external
# viewing program.
#
def genericViewConfiguration(object, configuration = None, format = 'pdb'):
    format = string.lower(format)
    if format[:6] == 'opengl':
        from Scientific.Visualization import PyOpenGL
        model = format[7:]
        if model == '':
            model = 'wireframe'
        g_objects = object.graphicsObjects(configuration = None,
                                           model = model,
                                           graphics_module = PyOpenGL)
        scene = PyOpenGL.Scene(g_objects)
        scene.view()
        scene.mainloop()
        return None

    if sys.platform != 'win32':
        if len(viewer) == 0:
            Utility.warning('No PDB or VRML viewer defined.')
            return
        format = string.lower(format)
        viewer_format = string.split(format, '.')[0]
        if not viewer.has_key(viewer_format):
            format = viewer.keys()[0]
            viewer_format = string.split(format, '.')[0]
    tempfile.tempdir = tempdir
    filename = tempfile.mktemp()
    tempfile.tempdir = None
    if sys.platform == 'win32':
        if format[:3] == 'pdb':
            filename = filename + '.pdb'
        elif format[:4] == 'vrml':
            filename = filename + '.wrl'
        object.writeToFile(filename, configuration, format)
        import win32api
        win32api.ShellExecute(0, "open", filename, None, "", 1)
    else:
        object.writeToFile(filename, configuration, format)
        if os.fork() == 0:
            pipe = os.popen(viewer[viewer_format] + ' ' + filename + \
                            ' 1> /dev/null 2>&1', 'w')
            pipe.close()
            os.unlink(filename)
            os._exit(0)

viewConfiguration = genericViewConfiguration

#
# Normal mode and trajectory animation: in general not available
#
def viewSequence(object, conf_list, periodic = 0):
    """Launches an external viewer with animation capabilities
    to display |object| in the configurations given in
    |conf_list|, which can be any sequence of configurations,
    including the variable "configuration" from a
    Class:MMTK.Trajectory.Trajectory object. If |periodic|
    is 1, the configurations will be repeated periodically,
    provided that the external viewer supports this operation.
    """
    Utility.warning('No viewer with animation feature defined.')

def viewTrajectory(trajectory, first=0, last=None, step=1, subset = None):
    """Launches an external viewer with animation capabilities
    to display the configurations from |first| to |last| in increments
    of |step| in |trajectory|. The trajectory can be specified by
    a Class:MMTK.Trajectory.Trajectory object or by a string which
    is interpreted as the file name of a trajectory file. An optional
    parameter |subset| can specify an object which is a subset of the
    universe contained in the trajectory, in order to restrict
    visualization to this subset.
    """
    if type(trajectory) == type(''):
	from Trajectory import Trajectory
	trajectory = Trajectory(None, trajectory, 'r')
    if last is None:
	last = len(trajectory)
    elif last < 0:
	last = len(trajectory) + last
    universe = trajectory.universe
    if subset is None:
	subset = universe
    viewSequence(subset, trajectory.configuration[first:last:step])
    
def viewMode(mode, factor=1., subset=None):
    universe = mode.universe
    if subset is None:
	subset = universe
    conf = universe.configuration()
    viewSequence(subset, [conf, conf+factor*mode, conf, conf-factor*mode], 1)

def dosSlash(str):
    return string.replace(str, "\\", "\\\\")

#
# XMol support
#    
if prog == 'xmol':
    #
    # Animation with XMol.
    #
    def viewSequence(object, conf_list, periodic = 0):
        """Launches an external viewer with animation capabilities
        to display |object| in the configurations given in
        |conf_list|, which can be any sequence of configurations,
        including the variable "configuration" from a
        Class:MMTK.Trajectory.Trajectory object. If |periodic|
        is 1, the configurations will be repeated periodically,
        provided that the external viewers supports this operation.
        """
	tempfile.tempdir = tempdir
	file_list = []
	for conf in conf_list:
	    file = tempfile.mktemp()
	    file_list.append(file)
	    object.writeToFile(file, conf, 'pdb')
	bigfile = tempfile.mktemp()
	tempfile.tempdir = None
        if sys.platform == 'win32':
            file_list = map(dosSlash, file_list)
            bigfile = dosSlash(bigfile)
	os.system('cat ' + string.join(file_list, ' ') + ' > ' + bigfile)
	for file in file_list:
	    os.unlink(file)
        if sys.playform == 'win32':
            os.system('xmol -readFormat pdb ' + bigfile)
	    os.unlink(bigfile)
            return
	if os.fork() == 0:                
	    pipe = os.popen('xmol -readFormat pdb ' + bigfile + \
			    ' 1> /dev/null 2>&1', 'w')
	    pipe.close()
	    os.unlink(bigfile)
	    os._exit(0)

#
# VMD support
#
if prog == 'vmd' or prog == 'WINVMD':
    #
    # View configuration
    #
    def viewConfiguration(object, configuration = None, format = 'pdb'):
	format = string.lower(format)
	if format != 'pdb':
	    return genericViewConfiguration(object, configuration, format)
	tempfile.tempdir = tempdir
	filename = tempfile.mktemp()
	script = tempfile.mktemp()
	tempfile.tempdir = None
        object.writeToFile(filename, configuration, format)
        file = open(script, 'w')
        file.write('mol load pdb %s\n' % dosSlash(filename))
        file.write('color Name 1 white\n')
        file.write('color Name 2 white\n')
        file.write('color Name 3 white\n')
        if sys.platform != 'win32':
            file.write('file delete ' + filename + '\n')
            file.write('file delete ' + script + '\n')
        file.close()
        comstr = viewer[format] + ' -nt -e ' + script
        if sys.platform != 'win32':
            comstr = comstr + ' 1> /dev/null 2>&1'
        os.system(comstr)
    #
    # Animate sequence
    #
    def viewSequence(object, conf_list, periodic = 0):
        """Launches an external viewer with animation capabilities
        to display |object| in the configurations given in
        |conf_list|, which can be any sequence of configurations,
        including the variable "configuration" from a
        Class:MMTK.Trajectory.Trajectory object. If |periodic|
        is 1, the configurations will be repeated periodically,
        provided that the external viewers supports this operation.
        """
        tempfile.tempdir = tempdir
        script = tempfile.mktemp()
        np = object.numberOfPoints()
        universe = object.universe()
        if np == universe.numberOfPoints() \
           and len(conf_list) > 2:
            import DCD
            pdbfile = tempfile.mktemp()
            dcdfile = tempfile.mktemp()
            tempfile.tempdir = None
            universe.configuration()
            pdb = PDB.PDBOutputFile(pdbfile)
            pdb.write(object, conf_list[0])
            indices = map(lambda a: a.index, pdb.atom_sequence)
            pdb.close()
            del pdb
            DCD.writeDCD(conf_list[1:], dcdfile, indices)
            file = open(script, 'w')
            file.write('mol load pdb %s\n' % dosSlash(pdbfile))
            file.write('animate read dcd %s\n' % dosSlash(dcdfile))
            if periodic:
                file.write('animate style loop\n')
            else:
                file.write('animate style once\n')
            file.write('animate forward\n')
            if sys.platform != 'win32':
                file.write('file delete ' + pdbfile + '\n')
                file.write('file delete ' + dcdfile + '\n')
                file.write('file delete ' + script + '\n')
            file.close()
        else:
            file_list = []
            for conf in conf_list:
                file = tempfile.mktemp()
                file_list.append(file)
                object.writeToFile(file, conf, 'pdb')
            file_list = map(dosSlash, file_list)
            tempfile.tempdir = None
            file = open(script, 'w')
            file.write('mol load pdb ' + file_list[0] + '\n')
            for conf in file_list[1:]:
                file.write('animate read pdb ' + conf + '\n')
            if periodic:
                file.write('animate style loop\n')
            else:
                file.write('animate style once\n')
            file.write('animate forward\n')
            if sys.platform != 'win32':
                for conf in file_list:
                    file.write('file delete ' + conf + '\n')
                file.write('file delete ' + script + '\n')
            file.close()
        comstr = viewer['pdb'] + ' -nt -e ' + script
        if sys.platform != 'win32':
            comstr = comstr + ' 1> /dev/null 2>&1'
        os.system(comstr)
