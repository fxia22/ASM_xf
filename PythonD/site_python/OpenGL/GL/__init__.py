# This file was created automatically by SWIG.
import __init___
__numeric_present__ = __init___.__numeric_present__
__numeric_support__ = __init___.__numeric_support__


from operator import isSequenceType


# color utility funcs
def glColorub(*args):
	'glColorub(red, green, blue[, alpha]) | glColorub((red, green, blue[, alpha])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glColor3ubv(args)
	elif len(args) == 4:
		glColor4ubv(args)
	else:
		raise TypeError, 'glColorub() takes 1, 3, or 4 arguments (%d given)' % len(args)
def glColorb(*args):
	'glColorb(red, green, blue[, alpha]) | glColorb((red, green, blue[, alpha])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glColor3bv(args)
	elif len(args) == 4:
		glColor4bv(args)
	else:
		raise TypeError, 'glColorb() takes 1, 3, or 4 arguments (%d given)' % len(args)
def glColorus(*args):
	'glColorus(red, green, blue[, alpha]) | glColorus((red, green, blue[, alpha])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glColor3usv(args)
	elif len(args) == 4:
		glColor4usv(args)
	else:
		raise TypeError, 'glColorus() takes 1, 3, or 4 arguments (%d given)' % len(args)
def glColors(*args):
	'glColors(red, green, blue[, alpha]) | glColors((red, green, blue[, alpha])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glColor3sv(args)
	elif len(args) == 4:
		glColor4sv(args)
	else:
		raise TypeError, 'glColors() takes 1, 3, or 4 arguments (%d given)' % len(args)
	
def glColorui(*args):
	'glColorui(red, green, blue[, alpha]) | glColorui((red, green, blue[, alpha])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glColor3uiv(args)
	elif len(args) == 4:
		glColor4uiv(args)
	else:
		raise TypeError, 'glColorui() takes 1, 3, or 4 arguments (%d given)' % len(args)
	
def glColori(*args):
	'glColori(red, green, blue[, alpha]) | glColori((red, green, blue[, alpha])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glColor3iv(args)
	elif len(args) == 4:
		glColor4iv(args)
	else:
		raise TypeError, 'glColori() takes 1, 3, or 4 arguments (%d given)' % len(args)
	
def glColorf(*args):
	'glColorf(red, green, blue[, alpha]) | glColorf((red, green, blue[, alpha])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glColor3fv(args)
	elif len(args) == 4:
		glColor4fv(args)
	else:
		raise TypeError, 'glColorf() takes 1, 3, or 4 arguments (%d given)' % len(args)
	
def glColord(*args):
	'glColord(red, green, blue[, alpha]) | glColord((red, green, blue[, alpha])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glColor3dv(args)
	elif len(args) == 4:
		glColor4dv(args)
	else:
		raise TypeError, 'glColord() takes 1, 3, or 4 arguments (%d given)' % len(args)
glColor = glColord
glColor3 = glColord
glColor4 = glColord


# evalCoord utility funcs
def glEvalCoordf(*args):
	'glEvalCoordf(u[, v]) | glEvalCoordf((u[, v])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 1:
		glEvalCoord1f(args[0])
	elif len(args) == 2:
		glEvalCoord2fv(args)
	else:
		raise TypeError, 'glEvalCoordf() takes 1 or 2 arguments (%d given)' % len(args)
	
def glEvalCoordd(*args):
	'glEvalCoordd(u[, v]) | glEvalCoordd((u[, v])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 1:
		glEvalCoord1d(args[0])
	elif len(args) == 2:
		glEvalCoord2dv(args)
	else:
		raise TypeError, 'glEvalCoordd() takes 1 or 2 arguments (%d given)' % len(args)
		
glEvalCoord = glEvalCoordd
glEvalCoord1 = glEvalCoordd
glEvalCoord2 = glEvalCoordd


# evalPoint utility funcs
def glEvalPoint(*args):
	'glEvalPoint(i[, j]) | glEvalPoint((i[, j])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 1:
		glEvalPoint1(args[0])
	elif len(args) == 2:
		glEvalPoint2f(args[0], args[1])
	else:
		raise TypeError, 'glEvalPoint() takes 1 or 2 arguments (%d given)' % len(args)


glIndex = __init___.glIndexd


glMaterial = __init___.glMaterialfv


# normal utility funcs
def glNormalb(*args):
	'glNormalb(nx, ny, nz) | glNormalb((nx, ny, nz)) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glNormal3bv(args)
	elif len(args) == 4:
		glNormal4bv(args)
	else:
		raise TypeError, 'glNormalb() takes 1 or 3 arguments (%d given)' % len(args)
	
def glNormals(*args):
	'glNormals(nx, ny, nz) | glNormals((nx, ny, nz)) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glNormal3sv(args)
	elif len(args) == 4:
		glNormal4sv(args)
	else:
		raise TypeError, 'glNormals() takes 1 or 3 arguments (%d given)' % len(args)
	
def glNormali(*args):
	'glNormali(nx, ny, nz) | glNormali((nx, ny, nz)) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glNormal3iv(args)
	elif len(args) == 4:
		glNormal4iv(args)
	else:
		raise TypeError, 'glNormali() takes 1 or 3 arguments (%d given)' % len(args)
	
def glNormalf(*args):
	'glNormalf(nx, ny, nz) | glNormalf((nx, ny, nz)) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glNormal3fv(args)
	elif len(args) == 4:
		glNormal4fv(args)
	else:
		raise TypeError, 'glNormalf() takes 1 or 3 arguments (%d given)' % len(args)
	
def glNormald(*args):
	'glNormald(nx, ny, nz) | glNormald((nx, ny, nz)) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 3:
		glNormal3dv(args)
	elif len(args) == 4:
		glNormal4dv(args)
	else:
		raise TypeError, 'glNormald() takes 1 or 3 arguments (%d given)' % len(args)
glNormal = glNormald
glNormal3 = glNormald
glNormal4 = glNormald


# texCoord utility funcs
def glTexCoordb(*args):
	'glTexCoordb(s[, t[, r[, q]]]) | glTexCoordb((s[, t[, r[, q]]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 1:
		glTexCoord1b(args[0])
	elif len(args) == 2:
		glTexCoord2bv(args)
	elif len(args) == 3:
		glTexCoord3bv(args)
	elif len(args) == 4:
		glTexCoord4bv(args)
	else:
		raise TypeError, 'glTexCoordb() takes 1, 2, 3, or 4 arguments (%d given)' % len(args)
	
def glTexCoords(*args):
	'glTexCoords(s[, t[, r[, q]]]) | glTexCoords((s[, t[, r[, q]]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 1:
		glTexCoord1s(args[0])
	elif len(args) == 2:
		glTexCoord2sv(args)
	elif len(args) == 3:
		glTexCoord3sv(args)
	elif len(args) == 4:
		glTexCoord4sv(args)
	else:
		raise TypeError, 'glTexCoords() takes 1, 2, 3, or 4 arguments (%d given)' % len(args)
	
def glTexCoordi(*args):
	'glTexCoordi(s[, t[, r[, q]]]) | glTexCoordi((s[, t[, r[, q]]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 1:
		glTexCoord1i(args[0])
	elif len(args) == 2:
		glTexCoord2iv(args)
	elif len(args) == 3:
		glTexCoord3iv(args)
	elif len(args) == 4:
		glTexCoord4iv(args)
	else:
		raise TypeError, 'glTexCoordi() takes 1, 2, 3, or 4 arguments (%d given)' % len(args)
	
def glTexCoordf(*args):
	'glTexCoordf(s[, t[, r[, q]]]) | glTexCoordf((s[, t[, r[, q]]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 1:
		glTexCoord1f(args[0])
	elif len(args) == 2:
		glTexCoord2fv(args)
	elif len(args) == 3:
		glTexCoord3fv(args)
	elif len(args) == 4:
		glTexCoord4fv(args)
	else:
		raise TypeError, 'glTexCoordf() takes 1, 2, 3, or 4 arguments (%d given)' % len(args)
	
def glTexCoordd(*args):
	'glTexCoordd(s[, t[, r[, q]]]) | glTexCoordd((s[, t[, r[, q]]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 1:
		glTexCoord1d(args[0])
	elif len(args) == 2:
		glTexCoord2dv(args)
	elif len(args) == 3:
		glTexCoord3dv(args)
	elif len(args) == 4:
		glTexCoord4dv(args)
	else:
		raise TypeError, 'glTexCoordd() takes 1, 2, 3, or 4 arguments (%d given)' % len(args)
glTexCoord = glTexCoordd
glTexCoord1 = glTexCoordd
glTexCoord2 = glTexCoordd
glTexCoord3 = glTexCoordd
glTexCoord4 = glTexCoordd


# vertex utility funcs
def glVertexb(*args):
	'glVertexb(x, y[, z[, w]]) | glVertexb((x, y[, z[, w]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 2:
		glVertex2bv(args)
	elif len(args) == 3:
		glVertex3bv(args)
	elif len(args) == 4:
		glVertex4bv(args)
	else:
		raise TypeError, 'glVertexb() takes 2, 3, or 4 arguments (%d given)' % len(args)
	
def glVertexs(*args):
	'glVertexs(x, y[, z[, w]]) | glVertexs((x, y[, z[, w]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 2:
		glVertex2sv(args)
	elif len(args) == 3:
		glVertex3sv(args)
	elif len(args) == 4:
		glVertex4sv(args)
	else:
		raise TypeError, 'glVertexs() takes 2, 3, or 4 arguments (%d given)' % len(args)
	
def glVertexi(*args):
	'glVertexi(x, y[, z[, w]]) | glVertexi((x, y[, z[, w]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 2:
		glVertex2iv(args)
	elif len(args) == 3:
		glVertex3iv(args)
	elif len(args) == 4:
		glVertex4iv(args)
	else:
		raise TypeError, 'glVertexi() takes 2, 3, or 4 arguments (%d given)' % len(args)
	
def glVertexf(*args):
	'glVertexf(x, y[, z[, w]]) | glVertexf((x, y[, z[, w]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 2:
		glVertex2fv(args)
	elif len(args) == 3:
		glVertex3fv(args)
	elif len(args) == 4:
		glVertex4fv(args)
	else:
		raise TypeError, 'glVertexf() takes 2, 3, or 4 arguments (%d given)' % len(args)
	
def glVertexd(*args):
	'glVertexd(x, y[, z[, w]]) | glVertexd((x, y[, z[, w]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 2:
		glVertex2dv(args)
	elif len(args) == 3:
		glVertex3dv(args)
	elif len(args) == 4:
		glVertex4dv(args)
	else:
		raise TypeError, 'glVertexd() takes 2, 3, or 4 arguments (%d given)' % len(args)
glVertex = glVertexd


glFog = __init___.glFogfv


glGetBoolean = __init___.glGetBooleanv


glGetDouble = __init___.glGetDoublev


glGetFloat = __init___.glGetFloatv


glGetInteger = __init___.glGetIntegerv


glLightModel = __init___.glLightModelfv


glLight = __init___.glLightfv


# rasterPos utility funcs
def glRasterPoss(*args):
	'glRasterPoss(x, y[, z[, w]]) | glRasterPoss((x, y[, z[, w]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 2:
		glRasterPos2sv(args)
	elif len(args) == 3:
		glRasterPos3sv(args)
	elif len(args) == 4:
		glRasterPos4sv(args)
	else:
		raise TypeError, 'glRasterPoss() takes 2, 3, or 4 arguments (%d given)' % len(args)
	
def glRasterPosi(*args):
	'glRasterPosi(x, y[, z[, w]]) | glRasterPosi((x, y[, z[, w]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 2:
		glRasterPos2iv(args)
	elif len(args) == 3:
		glRasterPos3iv(args)
	elif len(args) == 4:
		glRasterPos4iv(args)
	else:
		raise TypeError, 'glRasterPosi() takes 2, 3, or 4 arguments (%d given)' % len(args)
	
def glRasterPosf(*args):
	'glRasterPosf(x, y[, z[, w]]) | glRasterPosf((x, y[, z[, w]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 2:
		glRasterPos2fv(args)
	elif len(args) == 3:
		glRasterPos3fv(args)
	elif len(args) == 4:
		glRasterPos4fv(args)
	else:
		raise TypeError, 'glRasterPosf() takes 2, 3, or 4 arguments (%d given)' % len(args)
	
def glRasterPosd(*args):
	'glRasterPosd(x, y[, z[, w]]) | glRasterPosd((x, y[, z[, w]])) -> None'
	if len(args) == 1 and isSequenceType(args[0]):
		args = args[0]
	if len(args) == 2:
		glRasterPos2dv(args)
	elif len(args) == 3:
		glRasterPos3dv(args)
	elif len(args) == 4:
		glRasterPos4dv(args)
	else:
		raise TypeError, 'glRasterPosd() takes 2, 3, or 4 arguments (%d given)' % len(args)
glRasterPos = glRasterPosd
glRasterPos2 = glRasterPosd
glRasterPos3 = glRasterPosd
glRasterPos4 = glRasterPosd


glRotate = __init___.glRotated


glScale = __init___.glScaled


# glSelectWithCallback utility
def glSelectWithCallback(x, y, callback, xsize = 5, ysize = 5, buffer_size = 512):
	'''glSelectWithCallback(int x, int y, Callable callback, int xsize=5, int ysize=5)
  x,y -- x and y window coordinates for the center of the pick box
  rendercallback -- callback (callable Python object) taking 0 arguments
    which performs pick-mode rendering
  xsize,ysize -- x and y dimensions of the pick box (default = 5x5)
The function returns a tuple (possibly empty) of:
  ( (minimumzdepth, maximumzdepth, (name, name, name),...)
    minimumzdepth, maximumzdepth -- depths in integer format
      If you want the more traditional 0.0 to 1.0 numbers, divide
	  by (2**32)-1
      If you want the physical depth, multiply that by the frustrum depth and
        add your near clipping plane.
    name -- the names (integers) used in calls to glPushName( int )'''
	# this import needs to be late binding or Python gets stuck in an infinite import loop	
	from OpenGL.GLU import gluPickMatrix
	viewport = glGetIntegerv(GL_VIEWPORT)
	glSelectBuffer(buffer_size)
	glRenderMode(GL_SELECT)
	glInitNames()
	glMatrixMode(GL_PROJECTION)
	previousviewmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
	glLoadIdentity()
	gluPickMatrix(x, viewport[3] - y, xsize, ysize, viewport)
	glMultMatrixd(previousviewmatrix)
	callback()
	glFlush()
	glMatrixMode(GL_PROJECTION)
	glLoadMatrixd(previousviewmatrix)
	return glRenderMode(GL_RENDER)


glTexGen = __init___.glTexGendv


glTexParameter = __init___.glTexParameterfv


glTranslate = __init___.glTranslated


def __info():
	import string
	return [('GL_VERSION', GL_VERSION, 'sg'),
	        ('GL_VENDOR', GL_VENDOR, 'sg'),
	        ('GL_RENDERER', GL_RENDERER, 'sg'),
	        ('GL_EXTENSIONS', GL_EXTENSIONS, 'eg'),
	        ('GL_MAX_CLIENT_ATTRIB_STACK_DEPTH', GL_MAX_CLIENT_ATTRIB_STACK_DEPTH, 'i'),
	        ('GL_MAX_ATTRIB_STACK_DEPTH', GL_MAX_ATTRIB_STACK_DEPTH, 'i'),
	        ('GL_MAX_CLIP_PLANES', GL_MAX_CLIP_PLANES, 'i'),
	        ('GL_MAX_EVAL_ORDER', GL_MAX_EVAL_ORDER, 'i'),
	        ('GL_MAX_LIGHTS', GL_MAX_LIGHTS, 'i'),
	        ('GL_MAX_LIST_NESTING', GL_MAX_LIST_NESTING, 'i'),
	        ('GL_MAX_MODELVIEW_STACK_DEPTH', GL_MAX_MODELVIEW_STACK_DEPTH, 'i'),
	        ('GL_MAX_NAME_STACK_DEPTH', GL_MAX_NAME_STACK_DEPTH, 'i'),
	        ('GL_MAX_PIXEL_MAP_TABLE', GL_MAX_PIXEL_MAP_TABLE, 'i'),
	        ('GL_MAX_PROJECTION_STACK_DEPTH', GL_MAX_PROJECTION_STACK_DEPTH, 'i'),
	        ('GL_MAX_TEXTURE_SIZE', GL_MAX_TEXTURE_SIZE, 'i'),
	        ('GL_MAX_TEXTURE_STACK_DEPTH', GL_MAX_TEXTURE_STACK_DEPTH, 'i'),
	        ('GL_MAX_VIEWPORT_DIMS', GL_MAX_VIEWPORT_DIMS, 'i')]


GLerror = __init___.GLerror


__numeric_present__ = __init___.__numeric_present__
__numeric_support__ = __init___.__numeric_support__
try:
	import Numeric
except ImportError:
	def contiguous( source ):
		"""Place-holder for contiguous-array function, just returns argument
		This is only visible if Numeric Python is not installed
		"""
		return source
else:
	def contiguous( source, typecode=None ):
		"""Get contiguous array from source
		
		source -- Numeric Python array (or compatible object)
			for use as the data source.  If this is not a contiguous
			array of the given typecode, a copy will be made, 
			otherwise will just be returned unchanged.
		typecode -- optional 1-character typecode specifier for
			the Numeric.array function.
			
		All gl*Pointer calls should use contiguous arrays, as non-
		contiguous arrays will be re-copied on every rendering pass.
		Although this doesn't raise an error, it does tend to slow
		down rendering.
		"""
		if isinstance( source, Numeric.ArrayType):
			if source.iscontiguous() and (typecode is None or typecode==source.typecode()):
				return source
			else:
				return Numeric.array(source,typecode or source.typecode())
		elif typecode:
			return Numeric.array( source, typecode )
		else:
			return Numeric.array( source )


__version__ = __init___.__version__
__date__ = __init___.__date__
__api_version__ = __init___.__api_version__
__author__ = __init___.__author__
__doc__ = __init___.__doc__
glArrayElement = __init___.glArrayElement

glBegin = __init___.glBegin

glCallList = __init___.glCallList

glCallLists = __init___.glCallLists

glColor3b = __init___.glColor3b

glColor3bv = __init___.glColor3bv

glColor3d = __init___.glColor3d

glColor3dv = __init___.glColor3dv

glColor3f = __init___.glColor3f

glColor3fv = __init___.glColor3fv

glColor3i = __init___.glColor3i

glColor3iv = __init___.glColor3iv

glColor3s = __init___.glColor3s

glColor3sv = __init___.glColor3sv

glColor3ub = __init___.glColor3ub

glColor3ubv = __init___.glColor3ubv

glColor3ui = __init___.glColor3ui

glColor3uiv = __init___.glColor3uiv

glColor3us = __init___.glColor3us

glColor3usv = __init___.glColor3usv

glColor4b = __init___.glColor4b

glColor4bv = __init___.glColor4bv

glColor4d = __init___.glColor4d

glColor4dv = __init___.glColor4dv

glColor4f = __init___.glColor4f

glColor4fv = __init___.glColor4fv

glColor4i = __init___.glColor4i

glColor4iv = __init___.glColor4iv

glColor4s = __init___.glColor4s

glColor4sv = __init___.glColor4sv

glColor4ub = __init___.glColor4ub

glColor4ubv = __init___.glColor4ubv

glColor4ui = __init___.glColor4ui

glColor4uiv = __init___.glColor4uiv

glColor4us = __init___.glColor4us

glColor4usv = __init___.glColor4usv

glEdgeFlag = __init___.glEdgeFlag

glEdgeFlagv = __init___.glEdgeFlagv

glEvalCoord1d = __init___.glEvalCoord1d

glEvalCoord1dv = __init___.glEvalCoord1dv

glEvalCoord1f = __init___.glEvalCoord1f

glEvalCoord1fv = __init___.glEvalCoord1fv

glEvalCoord2d = __init___.glEvalCoord2d

glEvalCoord2dv = __init___.glEvalCoord2dv

glEvalCoord2f = __init___.glEvalCoord2f

glEvalCoord2fv = __init___.glEvalCoord2fv

glEvalPoint1 = __init___.glEvalPoint1

glEvalPoint2 = __init___.glEvalPoint2

glIndexd = __init___.glIndexd

glIndexdv = __init___.glIndexdv

glIndexf = __init___.glIndexf

glIndexfv = __init___.glIndexfv

glIndexi = __init___.glIndexi

glIndexiv = __init___.glIndexiv

glIndexs = __init___.glIndexs

glIndexsv = __init___.glIndexsv

glIndexub = __init___.glIndexub

glIndexubv = __init___.glIndexubv

glMaterialf = __init___.glMaterialf

glMaterialfv = __init___.glMaterialfv

glMateriali = __init___.glMateriali

glMaterialiv = __init___.glMaterialiv

glNormal3b = __init___.glNormal3b

glNormal3bv = __init___.glNormal3bv

glNormal3d = __init___.glNormal3d

glNormal3dv = __init___.glNormal3dv

glNormal3f = __init___.glNormal3f

glNormal3fv = __init___.glNormal3fv

glNormal3i = __init___.glNormal3i

glNormal3iv = __init___.glNormal3iv

glNormal3s = __init___.glNormal3s

glNormal3sv = __init___.glNormal3sv

glTexCoord1d = __init___.glTexCoord1d

glTexCoord1dv = __init___.glTexCoord1dv

glTexCoord1f = __init___.glTexCoord1f

glTexCoord1fv = __init___.glTexCoord1fv

glTexCoord1i = __init___.glTexCoord1i

glTexCoord1iv = __init___.glTexCoord1iv

glTexCoord1s = __init___.glTexCoord1s

glTexCoord1sv = __init___.glTexCoord1sv

glTexCoord2d = __init___.glTexCoord2d

glTexCoord2dv = __init___.glTexCoord2dv

glTexCoord2f = __init___.glTexCoord2f

glTexCoord2fv = __init___.glTexCoord2fv

glTexCoord2i = __init___.glTexCoord2i

glTexCoord2iv = __init___.glTexCoord2iv

glTexCoord2s = __init___.glTexCoord2s

glTexCoord2sv = __init___.glTexCoord2sv

glTexCoord3d = __init___.glTexCoord3d

glTexCoord3dv = __init___.glTexCoord3dv

glTexCoord3f = __init___.glTexCoord3f

glTexCoord3fv = __init___.glTexCoord3fv

glTexCoord3i = __init___.glTexCoord3i

glTexCoord3iv = __init___.glTexCoord3iv

glTexCoord3s = __init___.glTexCoord3s

glTexCoord3sv = __init___.glTexCoord3sv

glTexCoord4d = __init___.glTexCoord4d

glTexCoord4dv = __init___.glTexCoord4dv

glTexCoord4f = __init___.glTexCoord4f

glTexCoord4fv = __init___.glTexCoord4fv

glTexCoord4i = __init___.glTexCoord4i

glTexCoord4iv = __init___.glTexCoord4iv

glTexCoord4s = __init___.glTexCoord4s

glTexCoord4sv = __init___.glTexCoord4sv

glVertex2d = __init___.glVertex2d

glVertex2dv = __init___.glVertex2dv

glVertex2f = __init___.glVertex2f

glVertex2fv = __init___.glVertex2fv

glVertex2i = __init___.glVertex2i

glVertex2iv = __init___.glVertex2iv

glVertex2s = __init___.glVertex2s

glVertex2sv = __init___.glVertex2sv

glVertex3d = __init___.glVertex3d

glVertex3dv = __init___.glVertex3dv

glVertex3f = __init___.glVertex3f

glVertex3fv = __init___.glVertex3fv

glVertex3i = __init___.glVertex3i

glVertex3iv = __init___.glVertex3iv

glVertex3s = __init___.glVertex3s

glVertex3sv = __init___.glVertex3sv

glVertex4d = __init___.glVertex4d

glVertex4dv = __init___.glVertex4dv

glVertex4f = __init___.glVertex4f

glVertex4fv = __init___.glVertex4fv

glVertex4i = __init___.glVertex4i

glVertex4iv = __init___.glVertex4iv

glVertex4s = __init___.glVertex4s

glVertex4sv = __init___.glVertex4sv

__has_extension = __init___.__has_extension

glAccum = __init___.glAccum

glAlphaFunc = __init___.glAlphaFunc

glAreTexturesResident = __init___.glAreTexturesResident

glBindTexture = __init___.glBindTexture

glBitmap = __init___.glBitmap

glBlendFunc = __init___.glBlendFunc

glClear = __init___.glClear

glClearAccum = __init___.glClearAccum

glClearColor = __init___.glClearColor

glClearDepth = __init___.glClearDepth

glClearIndex = __init___.glClearIndex

glClearStencil = __init___.glClearStencil

glClipPlane = __init___.glClipPlane

glColorMask = __init___.glColorMask

glColorMaterial = __init___.glColorMaterial

glColorPointer = __init___.glColorPointer

glColorPointerub = __init___.glColorPointerub

glColorPointerb = __init___.glColorPointerb

glColorPointerus = __init___.glColorPointerus

glColorPointers = __init___.glColorPointers

glColorPointerui = __init___.glColorPointerui

glColorPointeri = __init___.glColorPointeri

glColorPointerf = __init___.glColorPointerf

glColorPointerd = __init___.glColorPointerd

glCopyPixels = __init___.glCopyPixels

glCopyTexImage1D = __init___.glCopyTexImage1D

glCopyTexImage2D = __init___.glCopyTexImage2D

glCopyTexSubImage1D = __init___.glCopyTexSubImage1D

glCopyTexSubImage2D = __init___.glCopyTexSubImage2D

glCullFace = __init___.glCullFace

glDeleteLists = __init___.glDeleteLists

glDeleteTextures = __init___.glDeleteTextures

glDepthFunc = __init___.glDepthFunc

glDepthMask = __init___.glDepthMask

glDepthRange = __init___.glDepthRange

glDisable = __init___.glDisable

glDisableClientState = __init___.glDisableClientState

glDrawArrays = __init___.glDrawArrays

glDrawBuffer = __init___.glDrawBuffer

glDrawElements = __init___.glDrawElements

glDrawElementsub = __init___.glDrawElementsub

glDrawElementsus = __init___.glDrawElementsus

glDrawElementsui = __init___.glDrawElementsui

glDrawPixels = __init___.glDrawPixels

glDrawPixelsub = __init___.glDrawPixelsub

glDrawPixelsb = __init___.glDrawPixelsb

glDrawPixelsus = __init___.glDrawPixelsus

glDrawPixelss = __init___.glDrawPixelss

glDrawPixelsui = __init___.glDrawPixelsui

glDrawPixelsi = __init___.glDrawPixelsi

glDrawPixelsf = __init___.glDrawPixelsf

glEdgeFlagPointer = __init___.glEdgeFlagPointer

glEdgeFlagPointerb = __init___.glEdgeFlagPointerb

glEnable = __init___.glEnable

glEnableClientState = __init___.glEnableClientState

glEnd = __init___.glEnd

glEndList = __init___.glEndList

glEvalMesh1 = __init___.glEvalMesh1

glEvalMesh2 = __init___.glEvalMesh2

glFeedbackBuffer = __init___.glFeedbackBuffer

glFinish = __init___.glFinish

glFlush = __init___.glFlush

glFogf = __init___.glFogf

glFogfv = __init___.glFogfv

glFogi = __init___.glFogi

glFogiv = __init___.glFogiv

glFrontFace = __init___.glFrontFace

glFrustum = __init___.glFrustum

glGenLists = __init___.glGenLists

glGenTextures = __init___.glGenTextures

glGetBooleanv = __init___.glGetBooleanv

glGetClipPlane = __init___.glGetClipPlane

glGetDoublev = __init___.glGetDoublev

glGetFloatv = __init___.glGetFloatv

glGetIntegerv = __init___.glGetIntegerv

glGetLightfv = __init___.glGetLightfv

glGetLightiv = __init___.glGetLightiv

glGetMapdv = __init___.glGetMapdv

glGetMapfv = __init___.glGetMapfv

glGetMapiv = __init___.glGetMapiv

glGetMaterialfv = __init___.glGetMaterialfv

glGetMaterialiv = __init___.glGetMaterialiv

glGetPixelMapfv = __init___.glGetPixelMapfv

glGetPixelMapuiv = __init___.glGetPixelMapuiv

glGetPixelMapusv = __init___.glGetPixelMapusv

glGetPolygonStipple = __init___.glGetPolygonStipple

glGetPolygonStippleub = __init___.glGetPolygonStippleub

glGetString = __init___.glGetString

glGetTexEnvfv = __init___.glGetTexEnvfv

glGetTexEnviv = __init___.glGetTexEnviv

glGetTexGendv = __init___.glGetTexGendv

glGetTexGenfv = __init___.glGetTexGenfv

glGetTexGeniv = __init___.glGetTexGeniv

glGetTexImage = __init___.glGetTexImage

glGetTexImageub = __init___.glGetTexImageub

glGetTexImageb = __init___.glGetTexImageb

glGetTexImageus = __init___.glGetTexImageus

glGetTexImages = __init___.glGetTexImages

glGetTexImageui = __init___.glGetTexImageui

glGetTexImagei = __init___.glGetTexImagei

glGetTexImagef = __init___.glGetTexImagef

glGetTexImaged = __init___.glGetTexImaged

glGetTexLevelParameterfv = __init___.glGetTexLevelParameterfv

glGetTexLevelParameteriv = __init___.glGetTexLevelParameteriv

glGetTexParameterfv = __init___.glGetTexParameterfv

glGetTexParameteriv = __init___.glGetTexParameteriv

glHint = __init___.glHint

glIndexMask = __init___.glIndexMask

glIndexPointer = __init___.glIndexPointer

glIndexPointerub = __init___.glIndexPointerub

glIndexPointerb = __init___.glIndexPointerb

glIndexPointers = __init___.glIndexPointers

glIndexPointeri = __init___.glIndexPointeri

glIndexPointerf = __init___.glIndexPointerf

glIndexPointerd = __init___.glIndexPointerd

glInitNames = __init___.glInitNames

glInterleavedArrays = __init___.glInterleavedArrays

glIsEnabled = __init___.glIsEnabled

glIsList = __init___.glIsList

glIsTexture = __init___.glIsTexture

glLightModelf = __init___.glLightModelf

glLightModelfv = __init___.glLightModelfv

glLightModeli = __init___.glLightModeli

glLightModeliv = __init___.glLightModeliv

glLightf = __init___.glLightf

glLightfv = __init___.glLightfv

glLighti = __init___.glLighti

glLightiv = __init___.glLightiv

glLineStipple = __init___.glLineStipple

glLineWidth = __init___.glLineWidth

glListBase = __init___.glListBase

glLoadIdentity = __init___.glLoadIdentity

glLoadMatrixd = __init___.glLoadMatrixd

glLoadMatrixf = __init___.glLoadMatrixf

glLoadName = __init___.glLoadName

glLogicOp = __init___.glLogicOp

glMap1d = __init___.glMap1d

glMap1f = __init___.glMap1f

glMap2d = __init___.glMap2d

glMap2f = __init___.glMap2f

glMapGrid1d = __init___.glMapGrid1d

glMapGrid1f = __init___.glMapGrid1f

glMapGrid2d = __init___.glMapGrid2d

glMapGrid2f = __init___.glMapGrid2f

glMatrixMode = __init___.glMatrixMode

glMultMatrixd = __init___.glMultMatrixd

glMultMatrixf = __init___.glMultMatrixf

glNewList = __init___.glNewList

glNormalPointer = __init___.glNormalPointer

glNormalPointerb = __init___.glNormalPointerb

glNormalPointers = __init___.glNormalPointers

glNormalPointeri = __init___.glNormalPointeri

glNormalPointerf = __init___.glNormalPointerf

glNormalPointerd = __init___.glNormalPointerd

glOrtho = __init___.glOrtho

glPassThrough = __init___.glPassThrough

glPixelMapfv = __init___.glPixelMapfv

glPixelMapuiv = __init___.glPixelMapuiv

glPixelMapusv = __init___.glPixelMapusv

glPixelStoref = __init___.glPixelStoref

glPixelStorei = __init___.glPixelStorei

glPixelTransferf = __init___.glPixelTransferf

glPixelTransferi = __init___.glPixelTransferi

glPixelZoom = __init___.glPixelZoom

glPointSize = __init___.glPointSize

glPolygonMode = __init___.glPolygonMode

glPolygonOffset = __init___.glPolygonOffset

glPolygonStipple = __init___.glPolygonStipple

glPolygonStippleub = __init___.glPolygonStippleub

glPopAttrib = __init___.glPopAttrib

glPopClientAttrib = __init___.glPopClientAttrib

glPopMatrix = __init___.glPopMatrix

glPopName = __init___.glPopName

glPrioritizeTextures = __init___.glPrioritizeTextures

glPushAttrib = __init___.glPushAttrib

glPushClientAttrib = __init___.glPushClientAttrib

glPushMatrix = __init___.glPushMatrix

glPushName = __init___.glPushName

glRasterPos2d = __init___.glRasterPos2d

glRasterPos2dv = __init___.glRasterPos2dv

glRasterPos2f = __init___.glRasterPos2f

glRasterPos2fv = __init___.glRasterPos2fv

glRasterPos2i = __init___.glRasterPos2i

glRasterPos2iv = __init___.glRasterPos2iv

glRasterPos2s = __init___.glRasterPos2s

glRasterPos2sv = __init___.glRasterPos2sv

glRasterPos3d = __init___.glRasterPos3d

glRasterPos3dv = __init___.glRasterPos3dv

glRasterPos3f = __init___.glRasterPos3f

glRasterPos3fv = __init___.glRasterPos3fv

glRasterPos3i = __init___.glRasterPos3i

glRasterPos3iv = __init___.glRasterPos3iv

glRasterPos3s = __init___.glRasterPos3s

glRasterPos3sv = __init___.glRasterPos3sv

glRasterPos4d = __init___.glRasterPos4d

glRasterPos4dv = __init___.glRasterPos4dv

glRasterPos4f = __init___.glRasterPos4f

glRasterPos4fv = __init___.glRasterPos4fv

glRasterPos4i = __init___.glRasterPos4i

glRasterPos4iv = __init___.glRasterPos4iv

glRasterPos4s = __init___.glRasterPos4s

glRasterPos4sv = __init___.glRasterPos4sv

glReadBuffer = __init___.glReadBuffer

glReadPixels = __init___.glReadPixels

glReadPixelsub = __init___.glReadPixelsub

glReadPixelsb = __init___.glReadPixelsb

glReadPixelsus = __init___.glReadPixelsus

glReadPixelss = __init___.glReadPixelss

glReadPixelsui = __init___.glReadPixelsui

glReadPixelsi = __init___.glReadPixelsi

glReadPixelsf = __init___.glReadPixelsf

glReadPixelsd = __init___.glReadPixelsd

glRectd = __init___.glRectd

glRectdv = __init___.glRectdv

glRectf = __init___.glRectf

glRectfv = __init___.glRectfv

glRecti = __init___.glRecti

glRectiv = __init___.glRectiv

glRects = __init___.glRects

glRectsv = __init___.glRectsv

glRenderMode = __init___.glRenderMode

glRotated = __init___.glRotated

glRotatef = __init___.glRotatef

glScaled = __init___.glScaled

glScalef = __init___.glScalef

glScissor = __init___.glScissor

glSelectBuffer = __init___.glSelectBuffer

glShadeModel = __init___.glShadeModel

glStencilFunc = __init___.glStencilFunc

glStencilMask = __init___.glStencilMask

glStencilOp = __init___.glStencilOp

glTexCoordPointer = __init___.glTexCoordPointer

glTexCoordPointerb = __init___.glTexCoordPointerb

glTexCoordPointers = __init___.glTexCoordPointers

glTexCoordPointeri = __init___.glTexCoordPointeri

glTexCoordPointerf = __init___.glTexCoordPointerf

glTexCoordPointerd = __init___.glTexCoordPointerd

glTexEnvf = __init___.glTexEnvf

glTexEnvfv = __init___.glTexEnvfv

glTexEnvi = __init___.glTexEnvi

glTexEnviv = __init___.glTexEnviv

glTexGend = __init___.glTexGend

glTexGendv = __init___.glTexGendv

glTexGenf = __init___.glTexGenf

glTexGenfv = __init___.glTexGenfv

glTexGeni = __init___.glTexGeni

glTexGeniv = __init___.glTexGeniv

glTexImage1D = __init___.glTexImage1D

glTexImage1Dub = __init___.glTexImage1Dub

glTexImage1Db = __init___.glTexImage1Db

glTexImage1Dus = __init___.glTexImage1Dus

glTexImage1Ds = __init___.glTexImage1Ds

glTexImage1Dui = __init___.glTexImage1Dui

glTexImage1Di = __init___.glTexImage1Di

glTexImage1Df = __init___.glTexImage1Df

glTexImage2D = __init___.glTexImage2D

glTexImage2Dub = __init___.glTexImage2Dub

glTexImage2Db = __init___.glTexImage2Db

glTexImage2Dus = __init___.glTexImage2Dus

glTexImage2Ds = __init___.glTexImage2Ds

glTexImage2Dui = __init___.glTexImage2Dui

glTexImage2Di = __init___.glTexImage2Di

glTexImage2Df = __init___.glTexImage2Df

glTexParameterf = __init___.glTexParameterf

glTexParameterfv = __init___.glTexParameterfv

glTexParameteri = __init___.glTexParameteri

glTexParameteriv = __init___.glTexParameteriv

glTexSubImage1D = __init___.glTexSubImage1D

glTexSubImage1Dub = __init___.glTexSubImage1Dub

glTexSubImage1Db = __init___.glTexSubImage1Db

glTexSubImage1Dus = __init___.glTexSubImage1Dus

glTexSubImage1Ds = __init___.glTexSubImage1Ds

glTexSubImage1Dui = __init___.glTexSubImage1Dui

glTexSubImage1Di = __init___.glTexSubImage1Di

glTexSubImage1Df = __init___.glTexSubImage1Df

glTexSubImage2D = __init___.glTexSubImage2D

glTexSubImage2Dub = __init___.glTexSubImage2Dub

glTexSubImage2Db = __init___.glTexSubImage2Db

glTexSubImage2Dus = __init___.glTexSubImage2Dus

glTexSubImage2Ds = __init___.glTexSubImage2Ds

glTexSubImage2Dui = __init___.glTexSubImage2Dui

glTexSubImage2Di = __init___.glTexSubImage2Di

glTexSubImage2Df = __init___.glTexSubImage2Df

glTranslated = __init___.glTranslated

glTranslatef = __init___.glTranslatef

glVertexPointer = __init___.glVertexPointer

glVertexPointerb = __init___.glVertexPointerb

glVertexPointers = __init___.glVertexPointers

glVertexPointeri = __init___.glVertexPointeri

glVertexPointerf = __init___.glVertexPointerf

glVertexPointerd = __init___.glVertexPointerd

glViewport = __init___.glViewport

GL_VERSION_1_1 = __init___.GL_VERSION_1_1
GL_ACCUM = __init___.GL_ACCUM
GL_LOAD = __init___.GL_LOAD
GL_RETURN = __init___.GL_RETURN
GL_MULT = __init___.GL_MULT
GL_ADD = __init___.GL_ADD
GL_NEVER = __init___.GL_NEVER
GL_LESS = __init___.GL_LESS
GL_EQUAL = __init___.GL_EQUAL
GL_LEQUAL = __init___.GL_LEQUAL
GL_GREATER = __init___.GL_GREATER
GL_NOTEQUAL = __init___.GL_NOTEQUAL
GL_GEQUAL = __init___.GL_GEQUAL
GL_ALWAYS = __init___.GL_ALWAYS
GL_CURRENT_BIT = __init___.GL_CURRENT_BIT
GL_POINT_BIT = __init___.GL_POINT_BIT
GL_LINE_BIT = __init___.GL_LINE_BIT
GL_POLYGON_BIT = __init___.GL_POLYGON_BIT
GL_POLYGON_STIPPLE_BIT = __init___.GL_POLYGON_STIPPLE_BIT
GL_PIXEL_MODE_BIT = __init___.GL_PIXEL_MODE_BIT
GL_LIGHTING_BIT = __init___.GL_LIGHTING_BIT
GL_FOG_BIT = __init___.GL_FOG_BIT
GL_DEPTH_BUFFER_BIT = __init___.GL_DEPTH_BUFFER_BIT
GL_ACCUM_BUFFER_BIT = __init___.GL_ACCUM_BUFFER_BIT
GL_STENCIL_BUFFER_BIT = __init___.GL_STENCIL_BUFFER_BIT
GL_VIEWPORT_BIT = __init___.GL_VIEWPORT_BIT
GL_TRANSFORM_BIT = __init___.GL_TRANSFORM_BIT
GL_ENABLE_BIT = __init___.GL_ENABLE_BIT
GL_COLOR_BUFFER_BIT = __init___.GL_COLOR_BUFFER_BIT
GL_HINT_BIT = __init___.GL_HINT_BIT
GL_EVAL_BIT = __init___.GL_EVAL_BIT
GL_LIST_BIT = __init___.GL_LIST_BIT
GL_TEXTURE_BIT = __init___.GL_TEXTURE_BIT
GL_SCISSOR_BIT = __init___.GL_SCISSOR_BIT
GL_ALL_ATTRIB_BITS = __init___.GL_ALL_ATTRIB_BITS
GL_POINTS = __init___.GL_POINTS
GL_LINES = __init___.GL_LINES
GL_LINE_LOOP = __init___.GL_LINE_LOOP
GL_LINE_STRIP = __init___.GL_LINE_STRIP
GL_TRIANGLES = __init___.GL_TRIANGLES
GL_TRIANGLE_STRIP = __init___.GL_TRIANGLE_STRIP
GL_TRIANGLE_FAN = __init___.GL_TRIANGLE_FAN
GL_QUADS = __init___.GL_QUADS
GL_QUAD_STRIP = __init___.GL_QUAD_STRIP
GL_POLYGON = __init___.GL_POLYGON
GL_ZERO = __init___.GL_ZERO
GL_ONE = __init___.GL_ONE
GL_SRC_COLOR = __init___.GL_SRC_COLOR
GL_ONE_MINUS_SRC_COLOR = __init___.GL_ONE_MINUS_SRC_COLOR
GL_SRC_ALPHA = __init___.GL_SRC_ALPHA
GL_ONE_MINUS_SRC_ALPHA = __init___.GL_ONE_MINUS_SRC_ALPHA
GL_DST_ALPHA = __init___.GL_DST_ALPHA
GL_ONE_MINUS_DST_ALPHA = __init___.GL_ONE_MINUS_DST_ALPHA
GL_DST_COLOR = __init___.GL_DST_COLOR
GL_ONE_MINUS_DST_COLOR = __init___.GL_ONE_MINUS_DST_COLOR
GL_SRC_ALPHA_SATURATE = __init___.GL_SRC_ALPHA_SATURATE
GL_TRUE = __init___.GL_TRUE
GL_FALSE = __init___.GL_FALSE
GL_CLIP_PLANE0 = __init___.GL_CLIP_PLANE0
GL_CLIP_PLANE1 = __init___.GL_CLIP_PLANE1
GL_CLIP_PLANE2 = __init___.GL_CLIP_PLANE2
GL_CLIP_PLANE3 = __init___.GL_CLIP_PLANE3
GL_CLIP_PLANE4 = __init___.GL_CLIP_PLANE4
GL_CLIP_PLANE5 = __init___.GL_CLIP_PLANE5
GL_BYTE = __init___.GL_BYTE
GL_UNSIGNED_BYTE = __init___.GL_UNSIGNED_BYTE
GL_SHORT = __init___.GL_SHORT
GL_UNSIGNED_SHORT = __init___.GL_UNSIGNED_SHORT
GL_INT = __init___.GL_INT
GL_UNSIGNED_INT = __init___.GL_UNSIGNED_INT
GL_FLOAT = __init___.GL_FLOAT
GL_2_BYTES = __init___.GL_2_BYTES
GL_3_BYTES = __init___.GL_3_BYTES
GL_4_BYTES = __init___.GL_4_BYTES
GL_DOUBLE = __init___.GL_DOUBLE
GL_NONE = __init___.GL_NONE
GL_FRONT_LEFT = __init___.GL_FRONT_LEFT
GL_FRONT_RIGHT = __init___.GL_FRONT_RIGHT
GL_BACK_LEFT = __init___.GL_BACK_LEFT
GL_BACK_RIGHT = __init___.GL_BACK_RIGHT
GL_FRONT = __init___.GL_FRONT
GL_BACK = __init___.GL_BACK
GL_LEFT = __init___.GL_LEFT
GL_RIGHT = __init___.GL_RIGHT
GL_FRONT_AND_BACK = __init___.GL_FRONT_AND_BACK
GL_AUX0 = __init___.GL_AUX0
GL_AUX1 = __init___.GL_AUX1
GL_AUX2 = __init___.GL_AUX2
GL_AUX3 = __init___.GL_AUX3
GL_NO_ERROR = __init___.GL_NO_ERROR
GL_INVALID_ENUM = __init___.GL_INVALID_ENUM
GL_INVALID_VALUE = __init___.GL_INVALID_VALUE
GL_INVALID_OPERATION = __init___.GL_INVALID_OPERATION
GL_STACK_OVERFLOW = __init___.GL_STACK_OVERFLOW
GL_STACK_UNDERFLOW = __init___.GL_STACK_UNDERFLOW
GL_OUT_OF_MEMORY = __init___.GL_OUT_OF_MEMORY
GL_2D = __init___.GL_2D
GL_3D = __init___.GL_3D
GL_3D_COLOR = __init___.GL_3D_COLOR
GL_3D_COLOR_TEXTURE = __init___.GL_3D_COLOR_TEXTURE
GL_4D_COLOR_TEXTURE = __init___.GL_4D_COLOR_TEXTURE
GL_PASS_THROUGH_TOKEN = __init___.GL_PASS_THROUGH_TOKEN
GL_POINT_TOKEN = __init___.GL_POINT_TOKEN
GL_LINE_TOKEN = __init___.GL_LINE_TOKEN
GL_POLYGON_TOKEN = __init___.GL_POLYGON_TOKEN
GL_BITMAP_TOKEN = __init___.GL_BITMAP_TOKEN
GL_DRAW_PIXEL_TOKEN = __init___.GL_DRAW_PIXEL_TOKEN
GL_COPY_PIXEL_TOKEN = __init___.GL_COPY_PIXEL_TOKEN
GL_LINE_RESET_TOKEN = __init___.GL_LINE_RESET_TOKEN
GL_EXP = __init___.GL_EXP
GL_EXP2 = __init___.GL_EXP2
GL_CW = __init___.GL_CW
GL_CCW = __init___.GL_CCW
GL_COEFF = __init___.GL_COEFF
GL_ORDER = __init___.GL_ORDER
GL_DOMAIN = __init___.GL_DOMAIN
GL_CURRENT_COLOR = __init___.GL_CURRENT_COLOR
GL_CURRENT_INDEX = __init___.GL_CURRENT_INDEX
GL_CURRENT_NORMAL = __init___.GL_CURRENT_NORMAL
GL_CURRENT_TEXTURE_COORDS = __init___.GL_CURRENT_TEXTURE_COORDS
GL_CURRENT_RASTER_COLOR = __init___.GL_CURRENT_RASTER_COLOR
GL_CURRENT_RASTER_INDEX = __init___.GL_CURRENT_RASTER_INDEX
GL_CURRENT_RASTER_TEXTURE_COORDS = __init___.GL_CURRENT_RASTER_TEXTURE_COORDS
GL_CURRENT_RASTER_POSITION = __init___.GL_CURRENT_RASTER_POSITION
GL_CURRENT_RASTER_POSITION_VALID = __init___.GL_CURRENT_RASTER_POSITION_VALID
GL_CURRENT_RASTER_DISTANCE = __init___.GL_CURRENT_RASTER_DISTANCE
GL_POINT_SMOOTH = __init___.GL_POINT_SMOOTH
GL_POINT_SIZE = __init___.GL_POINT_SIZE
GL_POINT_SIZE_RANGE = __init___.GL_POINT_SIZE_RANGE
GL_POINT_SIZE_GRANULARITY = __init___.GL_POINT_SIZE_GRANULARITY
GL_LINE_SMOOTH = __init___.GL_LINE_SMOOTH
GL_LINE_WIDTH = __init___.GL_LINE_WIDTH
GL_LINE_WIDTH_RANGE = __init___.GL_LINE_WIDTH_RANGE
GL_LINE_WIDTH_GRANULARITY = __init___.GL_LINE_WIDTH_GRANULARITY
GL_LINE_STIPPLE = __init___.GL_LINE_STIPPLE
GL_LINE_STIPPLE_PATTERN = __init___.GL_LINE_STIPPLE_PATTERN
GL_LINE_STIPPLE_REPEAT = __init___.GL_LINE_STIPPLE_REPEAT
GL_LIST_MODE = __init___.GL_LIST_MODE
GL_MAX_LIST_NESTING = __init___.GL_MAX_LIST_NESTING
GL_LIST_BASE = __init___.GL_LIST_BASE
GL_LIST_INDEX = __init___.GL_LIST_INDEX
GL_POLYGON_MODE = __init___.GL_POLYGON_MODE
GL_POLYGON_SMOOTH = __init___.GL_POLYGON_SMOOTH
GL_POLYGON_STIPPLE = __init___.GL_POLYGON_STIPPLE
GL_EDGE_FLAG = __init___.GL_EDGE_FLAG
GL_CULL_FACE = __init___.GL_CULL_FACE
GL_CULL_FACE_MODE = __init___.GL_CULL_FACE_MODE
GL_FRONT_FACE = __init___.GL_FRONT_FACE
GL_LIGHTING = __init___.GL_LIGHTING
GL_LIGHT_MODEL_LOCAL_VIEWER = __init___.GL_LIGHT_MODEL_LOCAL_VIEWER
GL_LIGHT_MODEL_TWO_SIDE = __init___.GL_LIGHT_MODEL_TWO_SIDE
GL_LIGHT_MODEL_AMBIENT = __init___.GL_LIGHT_MODEL_AMBIENT
GL_SHADE_MODEL = __init___.GL_SHADE_MODEL
GL_COLOR_MATERIAL_FACE = __init___.GL_COLOR_MATERIAL_FACE
GL_COLOR_MATERIAL_PARAMETER = __init___.GL_COLOR_MATERIAL_PARAMETER
GL_COLOR_MATERIAL = __init___.GL_COLOR_MATERIAL
GL_FOG = __init___.GL_FOG
GL_FOG_INDEX = __init___.GL_FOG_INDEX
GL_FOG_DENSITY = __init___.GL_FOG_DENSITY
GL_FOG_START = __init___.GL_FOG_START
GL_FOG_END = __init___.GL_FOG_END
GL_FOG_MODE = __init___.GL_FOG_MODE
GL_FOG_COLOR = __init___.GL_FOG_COLOR
GL_DEPTH_RANGE = __init___.GL_DEPTH_RANGE
GL_DEPTH_TEST = __init___.GL_DEPTH_TEST
GL_DEPTH_WRITEMASK = __init___.GL_DEPTH_WRITEMASK
GL_DEPTH_CLEAR_VALUE = __init___.GL_DEPTH_CLEAR_VALUE
GL_DEPTH_FUNC = __init___.GL_DEPTH_FUNC
GL_ACCUM_CLEAR_VALUE = __init___.GL_ACCUM_CLEAR_VALUE
GL_STENCIL_TEST = __init___.GL_STENCIL_TEST
GL_STENCIL_CLEAR_VALUE = __init___.GL_STENCIL_CLEAR_VALUE
GL_STENCIL_FUNC = __init___.GL_STENCIL_FUNC
GL_STENCIL_VALUE_MASK = __init___.GL_STENCIL_VALUE_MASK
GL_STENCIL_FAIL = __init___.GL_STENCIL_FAIL
GL_STENCIL_PASS_DEPTH_FAIL = __init___.GL_STENCIL_PASS_DEPTH_FAIL
GL_STENCIL_PASS_DEPTH_PASS = __init___.GL_STENCIL_PASS_DEPTH_PASS
GL_STENCIL_REF = __init___.GL_STENCIL_REF
GL_STENCIL_WRITEMASK = __init___.GL_STENCIL_WRITEMASK
GL_MATRIX_MODE = __init___.GL_MATRIX_MODE
GL_NORMALIZE = __init___.GL_NORMALIZE
GL_VIEWPORT = __init___.GL_VIEWPORT
GL_MODELVIEW_STACK_DEPTH = __init___.GL_MODELVIEW_STACK_DEPTH
GL_PROJECTION_STACK_DEPTH = __init___.GL_PROJECTION_STACK_DEPTH
GL_TEXTURE_STACK_DEPTH = __init___.GL_TEXTURE_STACK_DEPTH
GL_MODELVIEW_MATRIX = __init___.GL_MODELVIEW_MATRIX
GL_PROJECTION_MATRIX = __init___.GL_PROJECTION_MATRIX
GL_TEXTURE_MATRIX = __init___.GL_TEXTURE_MATRIX
GL_ATTRIB_STACK_DEPTH = __init___.GL_ATTRIB_STACK_DEPTH
GL_CLIENT_ATTRIB_STACK_DEPTH = __init___.GL_CLIENT_ATTRIB_STACK_DEPTH
GL_ALPHA_TEST = __init___.GL_ALPHA_TEST
GL_ALPHA_TEST_FUNC = __init___.GL_ALPHA_TEST_FUNC
GL_ALPHA_TEST_REF = __init___.GL_ALPHA_TEST_REF
GL_DITHER = __init___.GL_DITHER
GL_BLEND_DST = __init___.GL_BLEND_DST
GL_BLEND_SRC = __init___.GL_BLEND_SRC
GL_BLEND = __init___.GL_BLEND
GL_LOGIC_OP_MODE = __init___.GL_LOGIC_OP_MODE
GL_INDEX_LOGIC_OP = __init___.GL_INDEX_LOGIC_OP
GL_COLOR_LOGIC_OP = __init___.GL_COLOR_LOGIC_OP
GL_AUX_BUFFERS = __init___.GL_AUX_BUFFERS
GL_DRAW_BUFFER = __init___.GL_DRAW_BUFFER
GL_READ_BUFFER = __init___.GL_READ_BUFFER
GL_SCISSOR_BOX = __init___.GL_SCISSOR_BOX
GL_SCISSOR_TEST = __init___.GL_SCISSOR_TEST
GL_INDEX_CLEAR_VALUE = __init___.GL_INDEX_CLEAR_VALUE
GL_INDEX_WRITEMASK = __init___.GL_INDEX_WRITEMASK
GL_COLOR_CLEAR_VALUE = __init___.GL_COLOR_CLEAR_VALUE
GL_COLOR_WRITEMASK = __init___.GL_COLOR_WRITEMASK
GL_INDEX_MODE = __init___.GL_INDEX_MODE
GL_RGBA_MODE = __init___.GL_RGBA_MODE
GL_DOUBLEBUFFER = __init___.GL_DOUBLEBUFFER
GL_STEREO = __init___.GL_STEREO
GL_RENDER_MODE = __init___.GL_RENDER_MODE
GL_PERSPECTIVE_CORRECTION_HINT = __init___.GL_PERSPECTIVE_CORRECTION_HINT
GL_POINT_SMOOTH_HINT = __init___.GL_POINT_SMOOTH_HINT
GL_LINE_SMOOTH_HINT = __init___.GL_LINE_SMOOTH_HINT
GL_POLYGON_SMOOTH_HINT = __init___.GL_POLYGON_SMOOTH_HINT
GL_FOG_HINT = __init___.GL_FOG_HINT
GL_TEXTURE_GEN_S = __init___.GL_TEXTURE_GEN_S
GL_TEXTURE_GEN_T = __init___.GL_TEXTURE_GEN_T
GL_TEXTURE_GEN_R = __init___.GL_TEXTURE_GEN_R
GL_TEXTURE_GEN_Q = __init___.GL_TEXTURE_GEN_Q
GL_PIXEL_MAP_I_TO_I = __init___.GL_PIXEL_MAP_I_TO_I
GL_PIXEL_MAP_S_TO_S = __init___.GL_PIXEL_MAP_S_TO_S
GL_PIXEL_MAP_I_TO_R = __init___.GL_PIXEL_MAP_I_TO_R
GL_PIXEL_MAP_I_TO_G = __init___.GL_PIXEL_MAP_I_TO_G
GL_PIXEL_MAP_I_TO_B = __init___.GL_PIXEL_MAP_I_TO_B
GL_PIXEL_MAP_I_TO_A = __init___.GL_PIXEL_MAP_I_TO_A
GL_PIXEL_MAP_R_TO_R = __init___.GL_PIXEL_MAP_R_TO_R
GL_PIXEL_MAP_G_TO_G = __init___.GL_PIXEL_MAP_G_TO_G
GL_PIXEL_MAP_B_TO_B = __init___.GL_PIXEL_MAP_B_TO_B
GL_PIXEL_MAP_A_TO_A = __init___.GL_PIXEL_MAP_A_TO_A
GL_PIXEL_MAP_I_TO_I_SIZE = __init___.GL_PIXEL_MAP_I_TO_I_SIZE
GL_PIXEL_MAP_S_TO_S_SIZE = __init___.GL_PIXEL_MAP_S_TO_S_SIZE
GL_PIXEL_MAP_I_TO_R_SIZE = __init___.GL_PIXEL_MAP_I_TO_R_SIZE
GL_PIXEL_MAP_I_TO_G_SIZE = __init___.GL_PIXEL_MAP_I_TO_G_SIZE
GL_PIXEL_MAP_I_TO_B_SIZE = __init___.GL_PIXEL_MAP_I_TO_B_SIZE
GL_PIXEL_MAP_I_TO_A_SIZE = __init___.GL_PIXEL_MAP_I_TO_A_SIZE
GL_PIXEL_MAP_R_TO_R_SIZE = __init___.GL_PIXEL_MAP_R_TO_R_SIZE
GL_PIXEL_MAP_G_TO_G_SIZE = __init___.GL_PIXEL_MAP_G_TO_G_SIZE
GL_PIXEL_MAP_B_TO_B_SIZE = __init___.GL_PIXEL_MAP_B_TO_B_SIZE
GL_PIXEL_MAP_A_TO_A_SIZE = __init___.GL_PIXEL_MAP_A_TO_A_SIZE
GL_UNPACK_SWAP_BYTES = __init___.GL_UNPACK_SWAP_BYTES
GL_UNPACK_LSB_FIRST = __init___.GL_UNPACK_LSB_FIRST
GL_UNPACK_ROW_LENGTH = __init___.GL_UNPACK_ROW_LENGTH
GL_UNPACK_SKIP_ROWS = __init___.GL_UNPACK_SKIP_ROWS
GL_UNPACK_SKIP_PIXELS = __init___.GL_UNPACK_SKIP_PIXELS
GL_UNPACK_ALIGNMENT = __init___.GL_UNPACK_ALIGNMENT
GL_PACK_SWAP_BYTES = __init___.GL_PACK_SWAP_BYTES
GL_PACK_LSB_FIRST = __init___.GL_PACK_LSB_FIRST
GL_PACK_ROW_LENGTH = __init___.GL_PACK_ROW_LENGTH
GL_PACK_SKIP_ROWS = __init___.GL_PACK_SKIP_ROWS
GL_PACK_SKIP_PIXELS = __init___.GL_PACK_SKIP_PIXELS
GL_PACK_ALIGNMENT = __init___.GL_PACK_ALIGNMENT
GL_MAP_COLOR = __init___.GL_MAP_COLOR
GL_MAP_STENCIL = __init___.GL_MAP_STENCIL
GL_INDEX_SHIFT = __init___.GL_INDEX_SHIFT
GL_INDEX_OFFSET = __init___.GL_INDEX_OFFSET
GL_RED_SCALE = __init___.GL_RED_SCALE
GL_RED_BIAS = __init___.GL_RED_BIAS
GL_ZOOM_X = __init___.GL_ZOOM_X
GL_ZOOM_Y = __init___.GL_ZOOM_Y
GL_GREEN_SCALE = __init___.GL_GREEN_SCALE
GL_GREEN_BIAS = __init___.GL_GREEN_BIAS
GL_BLUE_SCALE = __init___.GL_BLUE_SCALE
GL_BLUE_BIAS = __init___.GL_BLUE_BIAS
GL_ALPHA_SCALE = __init___.GL_ALPHA_SCALE
GL_ALPHA_BIAS = __init___.GL_ALPHA_BIAS
GL_DEPTH_SCALE = __init___.GL_DEPTH_SCALE
GL_DEPTH_BIAS = __init___.GL_DEPTH_BIAS
GL_MAX_EVAL_ORDER = __init___.GL_MAX_EVAL_ORDER
GL_MAX_LIGHTS = __init___.GL_MAX_LIGHTS
GL_MAX_CLIP_PLANES = __init___.GL_MAX_CLIP_PLANES
GL_MAX_TEXTURE_SIZE = __init___.GL_MAX_TEXTURE_SIZE
GL_MAX_PIXEL_MAP_TABLE = __init___.GL_MAX_PIXEL_MAP_TABLE
GL_MAX_ATTRIB_STACK_DEPTH = __init___.GL_MAX_ATTRIB_STACK_DEPTH
GL_MAX_MODELVIEW_STACK_DEPTH = __init___.GL_MAX_MODELVIEW_STACK_DEPTH
GL_MAX_NAME_STACK_DEPTH = __init___.GL_MAX_NAME_STACK_DEPTH
GL_MAX_PROJECTION_STACK_DEPTH = __init___.GL_MAX_PROJECTION_STACK_DEPTH
GL_MAX_TEXTURE_STACK_DEPTH = __init___.GL_MAX_TEXTURE_STACK_DEPTH
GL_MAX_VIEWPORT_DIMS = __init___.GL_MAX_VIEWPORT_DIMS
GL_MAX_CLIENT_ATTRIB_STACK_DEPTH = __init___.GL_MAX_CLIENT_ATTRIB_STACK_DEPTH
GL_SUBPIXEL_BITS = __init___.GL_SUBPIXEL_BITS
GL_INDEX_BITS = __init___.GL_INDEX_BITS
GL_RED_BITS = __init___.GL_RED_BITS
GL_GREEN_BITS = __init___.GL_GREEN_BITS
GL_BLUE_BITS = __init___.GL_BLUE_BITS
GL_ALPHA_BITS = __init___.GL_ALPHA_BITS
GL_DEPTH_BITS = __init___.GL_DEPTH_BITS
GL_STENCIL_BITS = __init___.GL_STENCIL_BITS
GL_ACCUM_RED_BITS = __init___.GL_ACCUM_RED_BITS
GL_ACCUM_GREEN_BITS = __init___.GL_ACCUM_GREEN_BITS
GL_ACCUM_BLUE_BITS = __init___.GL_ACCUM_BLUE_BITS
GL_ACCUM_ALPHA_BITS = __init___.GL_ACCUM_ALPHA_BITS
GL_NAME_STACK_DEPTH = __init___.GL_NAME_STACK_DEPTH
GL_AUTO_NORMAL = __init___.GL_AUTO_NORMAL
GL_MAP1_COLOR_4 = __init___.GL_MAP1_COLOR_4
GL_MAP1_INDEX = __init___.GL_MAP1_INDEX
GL_MAP1_NORMAL = __init___.GL_MAP1_NORMAL
GL_MAP1_TEXTURE_COORD_1 = __init___.GL_MAP1_TEXTURE_COORD_1
GL_MAP1_TEXTURE_COORD_2 = __init___.GL_MAP1_TEXTURE_COORD_2
GL_MAP1_TEXTURE_COORD_3 = __init___.GL_MAP1_TEXTURE_COORD_3
GL_MAP1_TEXTURE_COORD_4 = __init___.GL_MAP1_TEXTURE_COORD_4
GL_MAP1_VERTEX_3 = __init___.GL_MAP1_VERTEX_3
GL_MAP1_VERTEX_4 = __init___.GL_MAP1_VERTEX_4
GL_MAP2_COLOR_4 = __init___.GL_MAP2_COLOR_4
GL_MAP2_INDEX = __init___.GL_MAP2_INDEX
GL_MAP2_NORMAL = __init___.GL_MAP2_NORMAL
GL_MAP2_TEXTURE_COORD_1 = __init___.GL_MAP2_TEXTURE_COORD_1
GL_MAP2_TEXTURE_COORD_2 = __init___.GL_MAP2_TEXTURE_COORD_2
GL_MAP2_TEXTURE_COORD_3 = __init___.GL_MAP2_TEXTURE_COORD_3
GL_MAP2_TEXTURE_COORD_4 = __init___.GL_MAP2_TEXTURE_COORD_4
GL_MAP2_VERTEX_3 = __init___.GL_MAP2_VERTEX_3
GL_MAP2_VERTEX_4 = __init___.GL_MAP2_VERTEX_4
GL_MAP1_GRID_DOMAIN = __init___.GL_MAP1_GRID_DOMAIN
GL_MAP1_GRID_SEGMENTS = __init___.GL_MAP1_GRID_SEGMENTS
GL_MAP2_GRID_DOMAIN = __init___.GL_MAP2_GRID_DOMAIN
GL_MAP2_GRID_SEGMENTS = __init___.GL_MAP2_GRID_SEGMENTS
GL_TEXTURE_1D = __init___.GL_TEXTURE_1D
GL_TEXTURE_2D = __init___.GL_TEXTURE_2D
GL_FEEDBACK_BUFFER_POINTER = __init___.GL_FEEDBACK_BUFFER_POINTER
GL_FEEDBACK_BUFFER_SIZE = __init___.GL_FEEDBACK_BUFFER_SIZE
GL_FEEDBACK_BUFFER_TYPE = __init___.GL_FEEDBACK_BUFFER_TYPE
GL_SELECTION_BUFFER_POINTER = __init___.GL_SELECTION_BUFFER_POINTER
GL_SELECTION_BUFFER_SIZE = __init___.GL_SELECTION_BUFFER_SIZE
GL_TEXTURE_WIDTH = __init___.GL_TEXTURE_WIDTH
GL_TEXTURE_HEIGHT = __init___.GL_TEXTURE_HEIGHT
GL_TEXTURE_INTERNAL_FORMAT = __init___.GL_TEXTURE_INTERNAL_FORMAT
GL_TEXTURE_BORDER_COLOR = __init___.GL_TEXTURE_BORDER_COLOR
GL_TEXTURE_BORDER = __init___.GL_TEXTURE_BORDER
GL_DONT_CARE = __init___.GL_DONT_CARE
GL_FASTEST = __init___.GL_FASTEST
GL_NICEST = __init___.GL_NICEST
GL_LIGHT0 = __init___.GL_LIGHT0
GL_LIGHT1 = __init___.GL_LIGHT1
GL_LIGHT2 = __init___.GL_LIGHT2
GL_LIGHT3 = __init___.GL_LIGHT3
GL_LIGHT4 = __init___.GL_LIGHT4
GL_LIGHT5 = __init___.GL_LIGHT5
GL_LIGHT6 = __init___.GL_LIGHT6
GL_LIGHT7 = __init___.GL_LIGHT7
GL_AMBIENT = __init___.GL_AMBIENT
GL_DIFFUSE = __init___.GL_DIFFUSE
GL_SPECULAR = __init___.GL_SPECULAR
GL_POSITION = __init___.GL_POSITION
GL_SPOT_DIRECTION = __init___.GL_SPOT_DIRECTION
GL_SPOT_EXPONENT = __init___.GL_SPOT_EXPONENT
GL_SPOT_CUTOFF = __init___.GL_SPOT_CUTOFF
GL_CONSTANT_ATTENUATION = __init___.GL_CONSTANT_ATTENUATION
GL_LINEAR_ATTENUATION = __init___.GL_LINEAR_ATTENUATION
GL_QUADRATIC_ATTENUATION = __init___.GL_QUADRATIC_ATTENUATION
GL_COMPILE = __init___.GL_COMPILE
GL_COMPILE_AND_EXECUTE = __init___.GL_COMPILE_AND_EXECUTE
GL_CLEAR = __init___.GL_CLEAR
GL_AND = __init___.GL_AND
GL_AND_REVERSE = __init___.GL_AND_REVERSE
GL_COPY = __init___.GL_COPY
GL_AND_INVERTED = __init___.GL_AND_INVERTED
GL_NOOP = __init___.GL_NOOP
GL_XOR = __init___.GL_XOR
GL_OR = __init___.GL_OR
GL_NOR = __init___.GL_NOR
GL_EQUIV = __init___.GL_EQUIV
GL_INVERT = __init___.GL_INVERT
GL_OR_REVERSE = __init___.GL_OR_REVERSE
GL_COPY_INVERTED = __init___.GL_COPY_INVERTED
GL_OR_INVERTED = __init___.GL_OR_INVERTED
GL_NAND = __init___.GL_NAND
GL_SET = __init___.GL_SET
GL_EMISSION = __init___.GL_EMISSION
GL_SHININESS = __init___.GL_SHININESS
GL_AMBIENT_AND_DIFFUSE = __init___.GL_AMBIENT_AND_DIFFUSE
GL_COLOR_INDEXES = __init___.GL_COLOR_INDEXES
GL_MODELVIEW = __init___.GL_MODELVIEW
GL_PROJECTION = __init___.GL_PROJECTION
GL_TEXTURE = __init___.GL_TEXTURE
GL_COLOR = __init___.GL_COLOR
GL_DEPTH = __init___.GL_DEPTH
GL_STENCIL = __init___.GL_STENCIL
GL_COLOR_INDEX = __init___.GL_COLOR_INDEX
GL_STENCIL_INDEX = __init___.GL_STENCIL_INDEX
GL_DEPTH_COMPONENT = __init___.GL_DEPTH_COMPONENT
GL_RED = __init___.GL_RED
GL_GREEN = __init___.GL_GREEN
GL_BLUE = __init___.GL_BLUE
GL_ALPHA = __init___.GL_ALPHA
GL_RGB = __init___.GL_RGB
GL_RGBA = __init___.GL_RGBA
GL_LUMINANCE = __init___.GL_LUMINANCE
GL_LUMINANCE_ALPHA = __init___.GL_LUMINANCE_ALPHA
GL_BITMAP = __init___.GL_BITMAP
GL_POINT = __init___.GL_POINT
GL_LINE = __init___.GL_LINE
GL_FILL = __init___.GL_FILL
GL_RENDER = __init___.GL_RENDER
GL_FEEDBACK = __init___.GL_FEEDBACK
GL_SELECT = __init___.GL_SELECT
GL_FLAT = __init___.GL_FLAT
GL_SMOOTH = __init___.GL_SMOOTH
GL_KEEP = __init___.GL_KEEP
GL_REPLACE = __init___.GL_REPLACE
GL_INCR = __init___.GL_INCR
GL_DECR = __init___.GL_DECR
GL_VENDOR = __init___.GL_VENDOR
GL_RENDERER = __init___.GL_RENDERER
GL_VERSION = __init___.GL_VERSION
GL_EXTENSIONS = __init___.GL_EXTENSIONS
GL_S = __init___.GL_S
GL_T = __init___.GL_T
GL_R = __init___.GL_R
GL_Q = __init___.GL_Q
GL_MODULATE = __init___.GL_MODULATE
GL_DECAL = __init___.GL_DECAL
GL_TEXTURE_ENV_MODE = __init___.GL_TEXTURE_ENV_MODE
GL_TEXTURE_ENV_COLOR = __init___.GL_TEXTURE_ENV_COLOR
GL_TEXTURE_ENV = __init___.GL_TEXTURE_ENV
GL_EYE_LINEAR = __init___.GL_EYE_LINEAR
GL_OBJECT_LINEAR = __init___.GL_OBJECT_LINEAR
GL_SPHERE_MAP = __init___.GL_SPHERE_MAP
GL_TEXTURE_GEN_MODE = __init___.GL_TEXTURE_GEN_MODE
GL_OBJECT_PLANE = __init___.GL_OBJECT_PLANE
GL_EYE_PLANE = __init___.GL_EYE_PLANE
GL_NEAREST = __init___.GL_NEAREST
GL_LINEAR = __init___.GL_LINEAR
GL_NEAREST_MIPMAP_NEAREST = __init___.GL_NEAREST_MIPMAP_NEAREST
GL_LINEAR_MIPMAP_NEAREST = __init___.GL_LINEAR_MIPMAP_NEAREST
GL_NEAREST_MIPMAP_LINEAR = __init___.GL_NEAREST_MIPMAP_LINEAR
GL_LINEAR_MIPMAP_LINEAR = __init___.GL_LINEAR_MIPMAP_LINEAR
GL_TEXTURE_MAG_FILTER = __init___.GL_TEXTURE_MAG_FILTER
GL_TEXTURE_MIN_FILTER = __init___.GL_TEXTURE_MIN_FILTER
GL_TEXTURE_WRAP_S = __init___.GL_TEXTURE_WRAP_S
GL_TEXTURE_WRAP_T = __init___.GL_TEXTURE_WRAP_T
GL_CLAMP = __init___.GL_CLAMP
GL_REPEAT = __init___.GL_REPEAT
GL_CLIENT_PIXEL_STORE_BIT = __init___.GL_CLIENT_PIXEL_STORE_BIT
GL_CLIENT_VERTEX_ARRAY_BIT = __init___.GL_CLIENT_VERTEX_ARRAY_BIT
GL_CLIENT_ALL_ATTRIB_BITS = __init___.GL_CLIENT_ALL_ATTRIB_BITS
GL_POLYGON_OFFSET_FACTOR = __init___.GL_POLYGON_OFFSET_FACTOR
GL_POLYGON_OFFSET_UNITS = __init___.GL_POLYGON_OFFSET_UNITS
GL_POLYGON_OFFSET_POINT = __init___.GL_POLYGON_OFFSET_POINT
GL_POLYGON_OFFSET_LINE = __init___.GL_POLYGON_OFFSET_LINE
GL_POLYGON_OFFSET_FILL = __init___.GL_POLYGON_OFFSET_FILL
GL_ALPHA4 = __init___.GL_ALPHA4
GL_ALPHA8 = __init___.GL_ALPHA8
GL_ALPHA12 = __init___.GL_ALPHA12
GL_ALPHA16 = __init___.GL_ALPHA16
GL_LUMINANCE4 = __init___.GL_LUMINANCE4
GL_LUMINANCE8 = __init___.GL_LUMINANCE8
GL_LUMINANCE12 = __init___.GL_LUMINANCE12
GL_LUMINANCE16 = __init___.GL_LUMINANCE16
GL_LUMINANCE4_ALPHA4 = __init___.GL_LUMINANCE4_ALPHA4
GL_LUMINANCE6_ALPHA2 = __init___.GL_LUMINANCE6_ALPHA2
GL_LUMINANCE8_ALPHA8 = __init___.GL_LUMINANCE8_ALPHA8
GL_LUMINANCE12_ALPHA4 = __init___.GL_LUMINANCE12_ALPHA4
GL_LUMINANCE12_ALPHA12 = __init___.GL_LUMINANCE12_ALPHA12
GL_LUMINANCE16_ALPHA16 = __init___.GL_LUMINANCE16_ALPHA16
GL_INTENSITY = __init___.GL_INTENSITY
GL_INTENSITY4 = __init___.GL_INTENSITY4
GL_INTENSITY8 = __init___.GL_INTENSITY8
GL_INTENSITY12 = __init___.GL_INTENSITY12
GL_INTENSITY16 = __init___.GL_INTENSITY16
GL_R3_G3_B2 = __init___.GL_R3_G3_B2
GL_RGB4 = __init___.GL_RGB4
GL_RGB5 = __init___.GL_RGB5
GL_RGB8 = __init___.GL_RGB8
GL_RGB10 = __init___.GL_RGB10
GL_RGB12 = __init___.GL_RGB12
GL_RGB16 = __init___.GL_RGB16
GL_RGBA2 = __init___.GL_RGBA2
GL_RGBA4 = __init___.GL_RGBA4
GL_RGB5_A1 = __init___.GL_RGB5_A1
GL_RGBA8 = __init___.GL_RGBA8
GL_RGB10_A2 = __init___.GL_RGB10_A2
GL_RGBA12 = __init___.GL_RGBA12
GL_RGBA16 = __init___.GL_RGBA16
GL_TEXTURE_RED_SIZE = __init___.GL_TEXTURE_RED_SIZE
GL_TEXTURE_GREEN_SIZE = __init___.GL_TEXTURE_GREEN_SIZE
GL_TEXTURE_BLUE_SIZE = __init___.GL_TEXTURE_BLUE_SIZE
GL_TEXTURE_ALPHA_SIZE = __init___.GL_TEXTURE_ALPHA_SIZE
GL_TEXTURE_LUMINANCE_SIZE = __init___.GL_TEXTURE_LUMINANCE_SIZE
GL_TEXTURE_INTENSITY_SIZE = __init___.GL_TEXTURE_INTENSITY_SIZE
GL_PROXY_TEXTURE_1D = __init___.GL_PROXY_TEXTURE_1D
GL_PROXY_TEXTURE_2D = __init___.GL_PROXY_TEXTURE_2D
GL_TEXTURE_PRIORITY = __init___.GL_TEXTURE_PRIORITY
GL_TEXTURE_RESIDENT = __init___.GL_TEXTURE_RESIDENT
GL_TEXTURE_BINDING_1D = __init___.GL_TEXTURE_BINDING_1D
GL_TEXTURE_BINDING_2D = __init___.GL_TEXTURE_BINDING_2D
GL_VERTEX_ARRAY = __init___.GL_VERTEX_ARRAY
GL_NORMAL_ARRAY = __init___.GL_NORMAL_ARRAY
GL_COLOR_ARRAY = __init___.GL_COLOR_ARRAY
GL_INDEX_ARRAY = __init___.GL_INDEX_ARRAY
GL_TEXTURE_COORD_ARRAY = __init___.GL_TEXTURE_COORD_ARRAY
GL_EDGE_FLAG_ARRAY = __init___.GL_EDGE_FLAG_ARRAY
GL_VERTEX_ARRAY_SIZE = __init___.GL_VERTEX_ARRAY_SIZE
GL_VERTEX_ARRAY_TYPE = __init___.GL_VERTEX_ARRAY_TYPE
GL_VERTEX_ARRAY_STRIDE = __init___.GL_VERTEX_ARRAY_STRIDE
GL_NORMAL_ARRAY_TYPE = __init___.GL_NORMAL_ARRAY_TYPE
GL_NORMAL_ARRAY_STRIDE = __init___.GL_NORMAL_ARRAY_STRIDE
GL_COLOR_ARRAY_SIZE = __init___.GL_COLOR_ARRAY_SIZE
GL_COLOR_ARRAY_TYPE = __init___.GL_COLOR_ARRAY_TYPE
GL_COLOR_ARRAY_STRIDE = __init___.GL_COLOR_ARRAY_STRIDE
GL_INDEX_ARRAY_TYPE = __init___.GL_INDEX_ARRAY_TYPE
GL_INDEX_ARRAY_STRIDE = __init___.GL_INDEX_ARRAY_STRIDE
GL_TEXTURE_COORD_ARRAY_SIZE = __init___.GL_TEXTURE_COORD_ARRAY_SIZE
GL_TEXTURE_COORD_ARRAY_TYPE = __init___.GL_TEXTURE_COORD_ARRAY_TYPE
GL_TEXTURE_COORD_ARRAY_STRIDE = __init___.GL_TEXTURE_COORD_ARRAY_STRIDE
GL_EDGE_FLAG_ARRAY_STRIDE = __init___.GL_EDGE_FLAG_ARRAY_STRIDE
GL_VERTEX_ARRAY_POINTER = __init___.GL_VERTEX_ARRAY_POINTER
GL_NORMAL_ARRAY_POINTER = __init___.GL_NORMAL_ARRAY_POINTER
GL_COLOR_ARRAY_POINTER = __init___.GL_COLOR_ARRAY_POINTER
GL_INDEX_ARRAY_POINTER = __init___.GL_INDEX_ARRAY_POINTER
GL_TEXTURE_COORD_ARRAY_POINTER = __init___.GL_TEXTURE_COORD_ARRAY_POINTER
GL_EDGE_FLAG_ARRAY_POINTER = __init___.GL_EDGE_FLAG_ARRAY_POINTER
GL_V2F = __init___.GL_V2F
GL_V3F = __init___.GL_V3F
GL_C4UB_V2F = __init___.GL_C4UB_V2F
GL_C4UB_V3F = __init___.GL_C4UB_V3F
GL_C3F_V3F = __init___.GL_C3F_V3F
GL_N3F_V3F = __init___.GL_N3F_V3F
GL_C4F_N3F_V3F = __init___.GL_C4F_N3F_V3F
GL_T2F_V3F = __init___.GL_T2F_V3F
GL_T4F_V4F = __init___.GL_T4F_V4F
GL_T2F_C4UB_V3F = __init___.GL_T2F_C4UB_V3F
GL_T2F_C3F_V3F = __init___.GL_T2F_C3F_V3F
GL_T2F_N3F_V3F = __init___.GL_T2F_N3F_V3F
GL_T2F_C4F_N3F_V3F = __init___.GL_T2F_C4F_N3F_V3F
GL_T4F_C4F_N3F_V4F = __init___.GL_T4F_C4F_N3F_V4F
GL_LOGIC_OP = __init___.GL_LOGIC_OP
GL_TEXTURE_COMPONENTS = __init___.GL_TEXTURE_COMPONENTS

