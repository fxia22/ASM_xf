#ifndef MXTEXTTOOLS_H
#define MXTEXTTOOLS_H
/* 
  mxTextTools -- Fast text manipulation routines

  Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
  Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
*/

/* The extension's name; must be the same as the init function's suffix */
#define MXTEXTTOOLS_MODULE "mxTextTools"

#include "mxbmse.h"
#ifdef MXFASTSEARCH
# include "private/mxfse.h"
#endif
#include "mxte.h"

/* Include generic mx extension header file */
#include "mxh.h"

#ifdef MX_BUILDING_MXTEXTTOOLS
# define MXTEXTTOOLS_EXTERNALIZE MX_EXPORT
#else
# define MXTEXTTOOLS_EXTERNALIZE MX_IMPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

/* --- Boyer Moore Substring Search Object ----------------------*/

typedef struct {
    PyObject_HEAD
    PyObject *match; 		/* Match string object */
    PyObject *tr; 		/* Translate string object or NULL */
    mxbmse_data *c; 		/* Internal data; see mxbmse.h */
} mxBMSObject;

MXTEXTTOOLS_EXTERNALIZE(PyTypeObject) mxBMS_Type;

#define _mxBMS_Check(v) \
        (((mxBMSObject *)(v))->ob_type == &mxBMS_Type)

#ifdef MXFASTSEARCH

/* --- Fast Search Object --------------------------------------*/

typedef struct {
    PyObject_HEAD
    PyObject *match; 		/* Match string object */
    PyObject *tr; 		/* Translate string object or NULL */
    mxfse_data *c; 		/* Internal data; see mxfse.h */
} mxFSObject;

MXTEXTTOOLS_EXTERNALIZE(PyTypeObject) mxFS_Type;

#define _mxFS_Check(v) \
        (((mxFSObject *)(v))->ob_type == &mxFS_Type)

#endif

/* EOF */
#ifdef __cplusplus
}
#endif
#endif
