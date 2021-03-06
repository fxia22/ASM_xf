import string
__version__ = string.split('$Revision: 1.5 $')[1]
__date__ = string.join(string.split('$Date: 2001/07/20 23:53:31 $')[1:3], ' ')
__author__ = 'Tarn Weisner Burton <twburton@users.sourceforge.net>'
__doc__ = 'http://oss.sgi.com/projects/ogl-sample/registry/PGI/vertex_hints.txt'
__api_version__ = 0x101

GL_VERTEX_DATA_HINT_PGI =                107050
GL_VERTEX_CONSISTENT_HINT_PGI =          107051
GL_MATERIAL_SIDE_HINT_PGI =              107052
GL_MAX_VERTEX_HINT_PGI =                 107053

GL_COLOR3_BIT_PGI =                   0x00010000
GL_COLOR4_BIT_PGI =                   0x00020000
GL_EDGEFLAG_BIT_PGI =                 0x00040000
GL_INDEX_BIT_PGI =                    0x00080000
GL_MAT_AMBIENT_BIT_PGI =              0x00100000
GL_MAT_AMBIENT_AND_DIFFUSE_BIT_PGI =  0x00200000
GL_MAT_DIFFUSE_BIT_PGI =              0x00400000
GL_MAT_EMISSION_BIT_PGI =             0x00800000
GL_MAT_COLOR_INDEXES_BIT_PGI =        0x01000000
GL_MAT_SHININESS_BIT_PGI =            0x02000000
GL_MAT_SPECULAR_BIT_PGI =             0x04000000
GL_NORMAL_BIT_PGI =                   0x08000000
GL_TEXCOORD1_BIT_PGI =                0x10000000
GL_TEXCOORD2_BIT_PGI =                0x20000000
GL_TEXCOORD3_BIT_PGI =                0x40000000
GL_TEXCOORD4_BIT_PGI =                0x80000000
GL_VERTEX23_BIT_PGI =                 0x00000004
GL_VERTEX4_BIT_PGI =                  0x00000008


def glInitVertexHintsPGI():
	from OpenGL.GL import __has_extension
	return __has_extension("GL_PGI_vertex_hints")


def __info():
	if glInitVertexHintsPGI():
		return []
