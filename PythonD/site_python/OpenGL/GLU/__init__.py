# This file was created automatically by SWIG.
import __init___
#-------------- SHADOW WRAPPERS ------------------


def gluPickMatrix(x, y, width, height, viewport = None):
    'gluPickMatrix(x, y, width, height, viewport = None) -> None'
    return __gluPickMatrix(x, y, width, height, viewport)


def gluProject(objx, objy, objz, modelMatrix = None, projMatrix = None, viewport = None):
    'gluProject(objx, objy, objz, modelMatrix = None, projMatrix = None, viewport = None) -> (winx, winy, winz)'
    return __gluProject(objx, objy, objz, modelMatrix, projMatrix, viewport)


def gluUnProject(winx, winy, winz, modelMatrix = None, projMatrix = None, viewport = None):
    'gluUnProject(winx, winy, winz, modelMatrix = None, projMatrix = None, viewport = None) -> (objx, objy, objz)'
    return __gluUnProject(winx, winy, winz, modelMatrix, projMatrix, viewport)


def gluUnProject4(winx, winy, winz, clipW, modelMatrix = None, projMatrix = None, viewport = None, near = 0.0, far = 1.0):
    'gluUnProject4(winx, winy, winz, clipW, modelMatrix = None, projMatrix = None, viewport = None, near = 0.0, far = 1.0) -> (objx, objy, objz, objw)'
    return __gluUnProject4(winx, winy, winz, clipW, modelMatrix, projMatrix, viewport, near, far)


def __info():
    import string
    return [('GLU_VERSION', GLU_VERSION, 'su'),
    ('GLU_EXTENSIONS', GLU_EXTENSIONS, 'eu')]


GLUerror = __init___.GLUerror


__version__ = __init___.__version__
__date__ = __init___.__date__
__api_version__ = __init___.__api_version__
__author__ = __init___.__author__
__doc__ = __init___.__doc__
gluErrorString = __init___.gluErrorString

gluGetString = __init___.gluGetString

gluCheckExtension = __init___.gluCheckExtension

gluOrtho2D = __init___.gluOrtho2D

gluPerspective = __init___.gluPerspective

__gluPickMatrix = __init___.__gluPickMatrix

gluLookAt = __init___.gluLookAt

__gluProject = __init___.__gluProject

__gluUnProject = __init___.__gluUnProject

__gluUnProject4 = __init___.__gluUnProject4

gluScaleImage = __init___.gluScaleImage

gluScaleImageb = __init___.gluScaleImageb

gluScaleImageub = __init___.gluScaleImageub

gluScaleImages = __init___.gluScaleImages

gluScaleImageus = __init___.gluScaleImageus

gluScaleImagei = __init___.gluScaleImagei

gluScaleImageui = __init___.gluScaleImageui

gluScaleImagef = __init___.gluScaleImagef

gluBuild1DMipmaps = __init___.gluBuild1DMipmaps

gluBuild1DMipmapsb = __init___.gluBuild1DMipmapsb

gluBuild1DMipmapsub = __init___.gluBuild1DMipmapsub

gluBuild1DMipmapss = __init___.gluBuild1DMipmapss

gluBuild1DMipmapsus = __init___.gluBuild1DMipmapsus

gluBuild1DMipmapsi = __init___.gluBuild1DMipmapsi

gluBuild1DMipmapsui = __init___.gluBuild1DMipmapsui

gluBuild1DMipmapsf = __init___.gluBuild1DMipmapsf

gluBuild2DMipmaps = __init___.gluBuild2DMipmaps

gluBuild2DMipmapsb = __init___.gluBuild2DMipmapsb

gluBuild2DMipmapsub = __init___.gluBuild2DMipmapsub

gluBuild2DMipmapss = __init___.gluBuild2DMipmapss

gluBuild2DMipmapsus = __init___.gluBuild2DMipmapsus

gluBuild2DMipmapsi = __init___.gluBuild2DMipmapsi

gluBuild2DMipmapsui = __init___.gluBuild2DMipmapsui

gluBuild2DMipmapsf = __init___.gluBuild2DMipmapsf

gluBuild3DMipmaps = __init___.gluBuild3DMipmaps

gluBuild3DMipmapsb = __init___.gluBuild3DMipmapsb

gluBuild3DMipmapsub = __init___.gluBuild3DMipmapsub

gluBuild3DMipmapss = __init___.gluBuild3DMipmapss

gluBuild3DMipmapsus = __init___.gluBuild3DMipmapsus

gluBuild3DMipmapsi = __init___.gluBuild3DMipmapsi

gluBuild3DMipmapsui = __init___.gluBuild3DMipmapsui

gluBuild3DMipmapsf = __init___.gluBuild3DMipmapsf

gluBuild1DMipmapLevels = __init___.gluBuild1DMipmapLevels

gluBuild1DMipmapLevelsb = __init___.gluBuild1DMipmapLevelsb

gluBuild1DMipmapLevelsub = __init___.gluBuild1DMipmapLevelsub

gluBuild1DMipmapLevelss = __init___.gluBuild1DMipmapLevelss

gluBuild1DMipmapLevelsus = __init___.gluBuild1DMipmapLevelsus

gluBuild1DMipmapLevelsi = __init___.gluBuild1DMipmapLevelsi

gluBuild1DMipmapLevelsui = __init___.gluBuild1DMipmapLevelsui

gluBuild1DMipmapLevelsf = __init___.gluBuild1DMipmapLevelsf

gluBuild2DMipmapLevels = __init___.gluBuild2DMipmapLevels

gluBuild2DMipmapLevelsb = __init___.gluBuild2DMipmapLevelsb

gluBuild2DMipmapLevelsub = __init___.gluBuild2DMipmapLevelsub

gluBuild2DMipmapLevelss = __init___.gluBuild2DMipmapLevelss

gluBuild2DMipmapLevelsus = __init___.gluBuild2DMipmapLevelsus

gluBuild2DMipmapLevelsi = __init___.gluBuild2DMipmapLevelsi

gluBuild2DMipmapLevelsui = __init___.gluBuild2DMipmapLevelsui

gluBuild2DMipmapLevelsf = __init___.gluBuild2DMipmapLevelsf

gluBuild3DMipmapLevels = __init___.gluBuild3DMipmapLevels

gluBuild3DMipmapLevelsb = __init___.gluBuild3DMipmapLevelsb

gluBuild3DMipmapLevelsub = __init___.gluBuild3DMipmapLevelsub

gluBuild3DMipmapLevelss = __init___.gluBuild3DMipmapLevelss

gluBuild3DMipmapLevelsus = __init___.gluBuild3DMipmapLevelsus

gluBuild3DMipmapLevelsi = __init___.gluBuild3DMipmapLevelsi

gluBuild3DMipmapLevelsui = __init___.gluBuild3DMipmapLevelsui

gluBuild3DMipmapLevelsf = __init___.gluBuild3DMipmapLevelsf

gluNewQuadric = __init___.gluNewQuadric

gluDeleteQuadric = __init___.gluDeleteQuadric

gluQuadricNormals = __init___.gluQuadricNormals

gluQuadricTexture = __init___.gluQuadricTexture

gluQuadricOrientation = __init___.gluQuadricOrientation

gluQuadricDrawStyle = __init___.gluQuadricDrawStyle

gluCylinder = __init___.gluCylinder

gluDisk = __init___.gluDisk

gluPartialDisk = __init___.gluPartialDisk

gluSphere = __init___.gluSphere

gluQuadricCallback = __init___.gluQuadricCallback

gluNewTess = __init___.gluNewTess

gluDeleteTess = __init___.gluDeleteTess

gluTessBeginPolygon = __init___.gluTessBeginPolygon

gluBeginPolygon = __init___.gluBeginPolygon

gluTessBeginContour = __init___.gluTessBeginContour

gluTessVertex = __init___.gluTessVertex

gluTessEndContour = __init___.gluTessEndContour

gluNextContour = __init___.gluNextContour

gluTessEndPolygon = __init___.gluTessEndPolygon

gluEndPolygon = __init___.gluEndPolygon

gluTessProperty = __init___.gluTessProperty

gluTessNormal = __init___.gluTessNormal

gluTessCallback = __init___.gluTessCallback

gluGetTessProperty = __init___.gluGetTessProperty

gluNewNurbsRenderer = __init___.gluNewNurbsRenderer

gluDeleteNurbsRenderer = __init___.gluDeleteNurbsRenderer

gluBeginSurface = __init___.gluBeginSurface

gluBeginCurve = __init___.gluBeginCurve

gluEndCurve = __init___.gluEndCurve

gluEndSurface = __init___.gluEndSurface

gluBeginTrim = __init___.gluBeginTrim

gluEndTrim = __init___.gluEndTrim

gluPwlCurve = __init___.gluPwlCurve

gluNurbsCurve = __init___.gluNurbsCurve

gluNurbsSurface = __init___.gluNurbsSurface

gluLoadSamplingMatrices = __init___.gluLoadSamplingMatrices

gluNurbsProperty = __init___.gluNurbsProperty

gluGetNurbsProperty = __init___.gluGetNurbsProperty

gluNurbsCallback = __init___.gluNurbsCallback

gluNurbsCallbackData = __init___.gluNurbsCallbackData

__gluNurbsCallbackDataEXT = __init___.__gluNurbsCallbackDataEXT

__gluInitNurbsTessellatorEXT = __init___.__gluInitNurbsTessellatorEXT

GLU_VERSION_1_1 = __init___.GLU_VERSION_1_1
GLU_VERSION_1_2 = __init___.GLU_VERSION_1_2
GLU_VERSION_1_3 = __init___.GLU_VERSION_1_3
GLU_INVALID_ENUM = __init___.GLU_INVALID_ENUM
GLU_INVALID_VALUE = __init___.GLU_INVALID_VALUE
GLU_OUT_OF_MEMORY = __init___.GLU_OUT_OF_MEMORY
GLU_INCOMPATIBLE_GL_VERSION = __init___.GLU_INCOMPATIBLE_GL_VERSION
GLU_VERSION = __init___.GLU_VERSION
GLU_EXTENSIONS = __init___.GLU_EXTENSIONS
GLU_SMOOTH = __init___.GLU_SMOOTH
GLU_FLAT = __init___.GLU_FLAT
GLU_NONE = __init___.GLU_NONE
GLU_POINT = __init___.GLU_POINT
GLU_LINE = __init___.GLU_LINE
GLU_FILL = __init___.GLU_FILL
GLU_SILHOUETTE = __init___.GLU_SILHOUETTE
GLU_OUTSIDE = __init___.GLU_OUTSIDE
GLU_INSIDE = __init___.GLU_INSIDE
GLU_TESS_MAX_COORD = __init___.GLU_TESS_MAX_COORD
GLU_TESS_WINDING_RULE = __init___.GLU_TESS_WINDING_RULE
GLU_TESS_BOUNDARY_ONLY = __init___.GLU_TESS_BOUNDARY_ONLY
GLU_TESS_TOLERANCE = __init___.GLU_TESS_TOLERANCE
GLU_TESS_WINDING_ODD = __init___.GLU_TESS_WINDING_ODD
GLU_TESS_WINDING_NONZERO = __init___.GLU_TESS_WINDING_NONZERO
GLU_TESS_WINDING_POSITIVE = __init___.GLU_TESS_WINDING_POSITIVE
GLU_TESS_WINDING_NEGATIVE = __init___.GLU_TESS_WINDING_NEGATIVE
GLU_TESS_WINDING_ABS_GEQ_TWO = __init___.GLU_TESS_WINDING_ABS_GEQ_TWO
GLU_TESS_BEGIN = __init___.GLU_TESS_BEGIN
GLU_TESS_VERTEX = __init___.GLU_TESS_VERTEX
GLU_TESS_END = __init___.GLU_TESS_END
GLU_TESS_ERROR = __init___.GLU_TESS_ERROR
GLU_TESS_EDGE_FLAG = __init___.GLU_TESS_EDGE_FLAG
GLU_TESS_COMBINE = __init___.GLU_TESS_COMBINE
GLU_TESS_BEGIN_DATA = __init___.GLU_TESS_BEGIN_DATA
GLU_TESS_VERTEX_DATA = __init___.GLU_TESS_VERTEX_DATA
GLU_TESS_END_DATA = __init___.GLU_TESS_END_DATA
GLU_TESS_ERROR_DATA = __init___.GLU_TESS_ERROR_DATA
GLU_TESS_EDGE_FLAG_DATA = __init___.GLU_TESS_EDGE_FLAG_DATA
GLU_TESS_COMBINE_DATA = __init___.GLU_TESS_COMBINE_DATA
GLU_TESS_ERROR1 = __init___.GLU_TESS_ERROR1
GLU_TESS_ERROR2 = __init___.GLU_TESS_ERROR2
GLU_TESS_ERROR3 = __init___.GLU_TESS_ERROR3
GLU_TESS_ERROR4 = __init___.GLU_TESS_ERROR4
GLU_TESS_ERROR5 = __init___.GLU_TESS_ERROR5
GLU_TESS_ERROR6 = __init___.GLU_TESS_ERROR6
GLU_TESS_ERROR7 = __init___.GLU_TESS_ERROR7
GLU_TESS_ERROR8 = __init___.GLU_TESS_ERROR8
GLU_TESS_MISSING_BEGIN_POLYGON = __init___.GLU_TESS_MISSING_BEGIN_POLYGON
GLU_TESS_MISSING_BEGIN_CONTOUR = __init___.GLU_TESS_MISSING_BEGIN_CONTOUR
GLU_TESS_MISSING_END_POLYGON = __init___.GLU_TESS_MISSING_END_POLYGON
GLU_TESS_MISSING_END_CONTOUR = __init___.GLU_TESS_MISSING_END_CONTOUR
GLU_TESS_COORD_TOO_LARGE = __init___.GLU_TESS_COORD_TOO_LARGE
GLU_TESS_NEED_COMBINE_CALLBACK = __init___.GLU_TESS_NEED_COMBINE_CALLBACK
GLU_AUTO_LOAD_MATRIX = __init___.GLU_AUTO_LOAD_MATRIX
GLU_CULLING = __init___.GLU_CULLING
GLU_SAMPLING_TOLERANCE = __init___.GLU_SAMPLING_TOLERANCE
GLU_DISPLAY_MODE = __init___.GLU_DISPLAY_MODE
GLU_PARAMETRIC_TOLERANCE = __init___.GLU_PARAMETRIC_TOLERANCE
GLU_SAMPLING_METHOD = __init___.GLU_SAMPLING_METHOD
GLU_U_STEP = __init___.GLU_U_STEP
GLU_V_STEP = __init___.GLU_V_STEP
GLU_PATH_LENGTH = __init___.GLU_PATH_LENGTH
GLU_PARAMETRIC_ERROR = __init___.GLU_PARAMETRIC_ERROR
GLU_DOMAIN_DISTANCE = __init___.GLU_DOMAIN_DISTANCE
GLU_MAP1_TRIM_2 = __init___.GLU_MAP1_TRIM_2
GLU_MAP1_TRIM_3 = __init___.GLU_MAP1_TRIM_3
GLU_OUTLINE_POLYGON = __init___.GLU_OUTLINE_POLYGON
GLU_OUTLINE_PATCH = __init___.GLU_OUTLINE_PATCH
GLU_NURBS_ERROR1 = __init___.GLU_NURBS_ERROR1
GLU_NURBS_ERROR2 = __init___.GLU_NURBS_ERROR2
GLU_NURBS_ERROR3 = __init___.GLU_NURBS_ERROR3
GLU_NURBS_ERROR4 = __init___.GLU_NURBS_ERROR4
GLU_NURBS_ERROR5 = __init___.GLU_NURBS_ERROR5
GLU_NURBS_ERROR6 = __init___.GLU_NURBS_ERROR6
GLU_NURBS_ERROR7 = __init___.GLU_NURBS_ERROR7
GLU_NURBS_ERROR8 = __init___.GLU_NURBS_ERROR8
GLU_NURBS_ERROR9 = __init___.GLU_NURBS_ERROR9
GLU_NURBS_ERROR10 = __init___.GLU_NURBS_ERROR10
GLU_NURBS_ERROR11 = __init___.GLU_NURBS_ERROR11
GLU_NURBS_ERROR12 = __init___.GLU_NURBS_ERROR12
GLU_NURBS_ERROR13 = __init___.GLU_NURBS_ERROR13
GLU_NURBS_ERROR14 = __init___.GLU_NURBS_ERROR14
GLU_NURBS_ERROR15 = __init___.GLU_NURBS_ERROR15
GLU_NURBS_ERROR16 = __init___.GLU_NURBS_ERROR16
GLU_NURBS_ERROR17 = __init___.GLU_NURBS_ERROR17
GLU_NURBS_ERROR18 = __init___.GLU_NURBS_ERROR18
GLU_NURBS_ERROR19 = __init___.GLU_NURBS_ERROR19
GLU_NURBS_ERROR20 = __init___.GLU_NURBS_ERROR20
GLU_NURBS_ERROR21 = __init___.GLU_NURBS_ERROR21
GLU_NURBS_ERROR22 = __init___.GLU_NURBS_ERROR22
GLU_NURBS_ERROR23 = __init___.GLU_NURBS_ERROR23
GLU_NURBS_ERROR24 = __init___.GLU_NURBS_ERROR24
GLU_NURBS_ERROR25 = __init___.GLU_NURBS_ERROR25
GLU_NURBS_ERROR26 = __init___.GLU_NURBS_ERROR26
GLU_NURBS_ERROR27 = __init___.GLU_NURBS_ERROR27
GLU_NURBS_ERROR28 = __init___.GLU_NURBS_ERROR28
GLU_NURBS_ERROR29 = __init___.GLU_NURBS_ERROR29
GLU_NURBS_ERROR30 = __init___.GLU_NURBS_ERROR30
GLU_NURBS_ERROR31 = __init___.GLU_NURBS_ERROR31
GLU_NURBS_ERROR32 = __init___.GLU_NURBS_ERROR32
GLU_NURBS_ERROR33 = __init___.GLU_NURBS_ERROR33
GLU_NURBS_ERROR34 = __init___.GLU_NURBS_ERROR34
GLU_NURBS_ERROR35 = __init___.GLU_NURBS_ERROR35
GLU_NURBS_ERROR36 = __init___.GLU_NURBS_ERROR36
GLU_NURBS_ERROR37 = __init___.GLU_NURBS_ERROR37
GLU_CW = __init___.GLU_CW
GLU_CCW = __init___.GLU_CCW
GLU_INTERIOR = __init___.GLU_INTERIOR
GLU_EXTERIOR = __init___.GLU_EXTERIOR
GLU_UNKNOWN = __init___.GLU_UNKNOWN
GLU_BEGIN = __init___.GLU_BEGIN
GLU_VERTEX = __init___.GLU_VERTEX
GLU_END = __init___.GLU_END
GLU_ERROR = __init___.GLU_ERROR
GLU_EDGE_FLAG = __init___.GLU_EDGE_FLAG
GLU_NURBS_MODE = __init___.GLU_NURBS_MODE
GLU_NURBS_TESSELLATOR = __init___.GLU_NURBS_TESSELLATOR
GLU_NURBS_RENDERER = __init___.GLU_NURBS_RENDERER
GLU_NURBS_BEGIN = __init___.GLU_NURBS_BEGIN
GLU_NURBS_VERTEX = __init___.GLU_NURBS_VERTEX
GLU_NURBS_NORMAL = __init___.GLU_NURBS_NORMAL
GLU_NURBS_COLOR = __init___.GLU_NURBS_COLOR
GLU_NURBS_TEXTURE_COORD = __init___.GLU_NURBS_TEXTURE_COORD
GLU_NURBS_END = __init___.GLU_NURBS_END
GLU_NURBS_BEGIN_DATA = __init___.GLU_NURBS_BEGIN_DATA
GLU_NURBS_VERTEX_DATA = __init___.GLU_NURBS_VERTEX_DATA
GLU_NURBS_NORMAL_DATA = __init___.GLU_NURBS_NORMAL_DATA
GLU_NURBS_COLOR_DATA = __init___.GLU_NURBS_COLOR_DATA
GLU_NURBS_TEXTURE_COORD_DATA = __init___.GLU_NURBS_TEXTURE_COORD_DATA
GLU_NURBS_END_DATA = __init___.GLU_NURBS_END_DATA
GLU_OBJECT_PARAMETRIC_ERROR = __init___.GLU_OBJECT_PARAMETRIC_ERROR
GLU_OBJECT_PATH_LENGTH = __init___.GLU_OBJECT_PATH_LENGTH

