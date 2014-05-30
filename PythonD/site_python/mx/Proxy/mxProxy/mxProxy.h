#ifndef MXPROXY_H
#define MXPROXY_H

/* 
  mxProxy -- Proxy wrapper type

  Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
  Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
*/

/* The extension's name; must be the same as the init function's suffix */
#define MXPROXY_MODULE "mxProxy"

/* --- No servicable parts below this line ----------------------*/

/* Include generic mx extension header file */
#include "mxh.h"

#ifdef MX_BUILDING_MXPROXY
# define MXPROXY_EXTERNALIZE MX_EXPORT
#else
# define MXPROXY_EXTERNALIZE MX_IMPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

/* --- Proxy Object ------------------------------------------*/

/* Note: The objects internal values are only calculated once and
   are thereafter considered immutable ! */

typedef struct _mxProxyObject {
    PyObject_HEAD
    
    /* Object references that are hidden from the Python programmer */
    PyObject *object;		/* The wrapped object or the index object
				   or NULL */
    PyObject *interface;	/* Dictionary containing names of getattr 
				   accessible attributes or NULL */
    PyObject *passobj;		/* Object that allows unrestricted access
				   to the wrapped object */
    
    /* Cached object methods or NULL */
    PyObject *public_getattr;	
    PyObject *public_setattr;
    PyObject *cleanup;

    /* Pointer to other weak Proxies for this object */
    struct _mxProxyObject *next_weak_proxy;

    /* Flags */
    unsigned isWeak:1;		/* object contains the index object or 
				   NULL */

} mxProxyObject;

/* Flag access macros */
#define mxProxy_isWeak(obj) ((obj)->isWeak)

/* EOF */
#ifdef __cplusplus
}
#endif
#endif
