#ifndef MXBEEBASE_H
#define MXBEEBASE_H
#ifdef __cplusplus
extern "C" {
#endif

/* 
   mxBeeBase -- B++-Tree implementation build on top of the free source
                code published in:

   SORTING AND SEARCHING ALGORITHMS: A COOKBOOK

   by THOMAS NIEMANN Portland, Oregon 
   email: thomasn@jps.net 
   home: http://members.xoom.com/thomasn/s_man.htm

   From the cookbook:

   Permission to reproduce this document, in whole or in part, is
   given provided the original web site listed below is referenced,
   and no additional restrictions apply. Source code, when part of a
   software project, may be used freely without reference to the
   author.

   The Python interface and the modifications to the above mentioned
   source code base are:

   Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
   Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
*/

/* The extension's name; must be the same as the init function's suffix */
#define MXBEEBASE_MODULE "mxBeeBase"

/* B++-Tree Header file */
#include "btr.h"

/* --- No servicable parts below this line ----------------------*/

/* Include generic mx extension header file */
#include "mxh.h"

#ifdef MX_BUILDING_MXBEEBASE
# define MXBEEBASE_EXTERNALIZE MX_EXPORT
#else
# define MXBEEBASE_EXTERNALIZE MX_IMPORT
#endif

/* --- BeeBase Object ------------------------------------------*/

typedef struct mxBeeIndexObject {
    PyObject_HEAD
    
    /* BTree data */
    bDescription info;		/* Information structure */
    bHandle *handle;		/* Handle for the BTree Index */
    
    long updates;		/* Update count used to identify invalid
				   cursors */

    int length;			/* Cache for current length; don't use
				   directly */
    long length_state;		/* Update count of last length
				   calculation */

    /* Data conversion routines for key management */
    PyObject *(*ObjectFromKey)(struct mxBeeIndexObject *index, void *key);
    void *(*KeyFromObject)(struct mxBeeIndexObject *index, PyObject *obj);

} mxBeeIndexObject;

typedef PyObject *(*mxObjectFromKeyFunc)(struct mxBeeIndexObject *index, void *key);
typedef void *(*mxKeyFromObjectFunc)(struct mxBeeIndexObject *index, PyObject *obj);

/* --- BeeBase Cursor Object -----------------------------------*/

typedef struct {
    PyObject_HEAD
    
    mxBeeIndexObject *index;	/* BeeIndex object */
    bCursor c;			/* Cursor */
    bIdxAddr adr;		/* Cursor's buffer address - needed to
				   check whether the buffer pointed to
				   by cursor is still containing the
				   data we expect */
    long updates;		/* Copy of index's updates value - needed
				   to check whether the index changed after
				   the cursor was created. If it is, then
				   the cursor is invalid. */
    
} mxBeeCursorObject;

/* EOF */
#ifdef __cplusplus
}
#endif
#endif
