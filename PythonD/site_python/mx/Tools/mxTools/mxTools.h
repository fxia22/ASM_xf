#ifndef MXTOOLS_H
#define MXTOOLS_H
/* 
  mxTools -- Misc. tools for Python

  Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
  Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
*/

/* The extension's name */
#define MXTOOLS_MODULE "mxTools"

/* --- No servicable parts below this line ----------------------*/

/* Include generic mx extension header file */
#include "mxh.h"

#ifdef MX_BUILDING_MXTOOLS
# define MXTOOLS_EXTERNALIZE MX_EXPORT
#else
# define MXTOOLS_EXTERNALIZE MX_IMPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

/* Symbols to be exported. */

/* EOF */
#ifdef __cplusplus
}
#endif
#endif
