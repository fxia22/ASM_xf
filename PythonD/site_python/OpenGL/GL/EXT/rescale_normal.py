import string
__version__ = string.split('$Revision: 1.10 $')[1]
__date__ = string.join(string.split('$Date: 2001/07/20 23:53:30 $')[1:3], ' ')
__author__ = 'Tarn Weisner Burton <twburton@users.sourceforge.net>'
__doc__ = 'http://oss.sgi.com/projects/ogl-sample/registry/EXT/rescale_normal.txt'
__api_version__ = 0x107

GL_RESCALE_NORMAL_EXT = 0x803A

def glInitRescaleNormalEXT():
	from OpenGL.GL import __has_extension
	return __has_extension("GL_EXT_rescale_normal")


def __info():
	if glInitRescaleNormalEXT():
		return []
