/* Generated automatically from ./Modules/config.c.in by makesetup. */
/* -*- C -*- ***********************************************
Copyright (c) 2000, BeOpen.com.
Copyright (c) 1995-2000, Corporation for National Research Initiatives.
Copyright (c) 1990-1995, Stichting Mathematisch Centrum.
All rights reserved.

See the file "Misc/COPYRIGHT" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.
******************************************************************/

/* Module configuration */

/* !!! !!! !!! This file is edited by the makesetup script !!! !!! !!! */

/* This file contains the table of built-in modules.
   See init_builtin() in import.c. */

#include "Python.h"


extern void initsignal(void);
extern void initposix(void);
extern void initerrno(void);
extern void init_sre(void);
extern void init_codecs(void);
extern void initzipimport(void);
extern void init_symtable(void);
extern void initreadline(void);
extern void initarray(void);
extern void initcmath(void);
extern void initmath(void);
extern void initstruct(void);
extern void inittime(void);
extern void initoperator(void);
extern void init_weakref(void);
extern void init_testcapi(void);
extern void init_random(void);
extern void initcollections(void);
extern void inititertools(void);
extern void initstrop(void);
extern void initunicodedata(void);
extern void initfcntl(void);
extern void initpwd(void);
extern void initgrp(void);
extern void initselect(void);
extern void init_csv(void);
extern void init_socket(void);
extern void initxxsubtype(void);

/* -- ADDMODULE MARKER 1 -- */

extern void PyMarshal_Init(void);
extern void initimp(void);
extern void initgc(void);

struct _inittab _PyImport_Inittab[] = {

	{"signal", initsignal},
	{"posix", initposix},
	{"errno", initerrno},
	{"_sre", init_sre},
	{"_codecs", init_codecs},
	{"zipimport", initzipimport},
	{"_symtable", init_symtable},
	{"readline", initreadline},
	{"array", initarray},
	{"cmath", initcmath},
	{"math", initmath},
	{"struct", initstruct},
	{"time", inittime},
	{"operator", initoperator},
	{"_weakref", init_weakref},
	{"_testcapi", init_testcapi},
	{"_random", init_random},
	{"collections", initcollections},
	{"itertools", inititertools},
	{"strop", initstrop},
	{"unicodedata", initunicodedata},
	{"fcntl", initfcntl},
	{"pwd", initpwd},
	{"grp", initgrp},
	{"select", initselect},
	{"_csv", init_csv},
	{"_socket", init_socket},
	{"xxsubtype", initxxsubtype},

/* -- ADDMODULE MARKER 2 -- */

	/* This module lives in marshal.c */
	{"marshal", PyMarshal_Init},

	/* This lives in import.c */
	{"imp", initimp},

	/* These entries are here for sys.builtin_module_names */
	{"__main__", NULL},
	{"__builtin__", NULL},
	{"sys", NULL},
	{"exceptions", NULL},

	/* This lives in gcmodule.c */
	{"gc", initgc},

	/* Sentinel */
	{0, 0}
};
