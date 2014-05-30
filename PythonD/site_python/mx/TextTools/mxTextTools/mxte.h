#ifndef MXTE_H
#define MXTE_H

/* 
  mxte -- a table driven tagging engine for Python (Version 0.7)

  Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
  Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
*/

#ifdef __cplusplus
extern "C" {
#endif

/* fast_tag: a table driven parser engine
   
 * return codes:
   rc = 2: match ok; rc = 1: match failed; rc = 0: error
 * doesn't check type of passed arguments: my only be called by tag()
 * doesn't increment reference counts of passed objects ! 
*/

/* commands in cmd; see tagconst.py for details */

/* jumps */
#define MATCH_FAIL		0
#define MATCH_JUMP 		MATCH_FAIL

#define MATCH_EOF 		1
#define MATCH_SKIP 		2
#define MATCH_MOVE		3

#define MATCH_MAX_SPECIALS	9

/* low-level string matching, using the same simple logic:
   - match has to be a string 
   - they only modify x (the current position in text)
*/
#define MATCH_ALLIN 		11
#define MATCH_ALLNOTIN 		12
#define MATCH_IS 		13
#define MATCH_ISIN 		14
#define MATCH_ISNOTIN 		15

#define MATCH_WORD 		21
#define MATCH_WORDSTART       	22
#define MATCH_WORDEND		23
#define MATCH_NOWORD		MATCH_SWORDSTART

#define MATCH_MAX_LOWLEVEL	99

/* higher-level string matching, having their own logic */

#define MATCH_ALLINSET 		31
#define MATCH_ISINSET		32

#define MATCH_SWORDSTART	111
#define MATCH_SWORDEND		112
#define MATCH_SFINDWORD		113

/* special commands */
#define MATCH_CALL 		201
#define MATCH_CALLARG 		202
#define MATCH_TABLE 		203
#define MATCH_SUBTABLE 		207
#define MATCH_TABLEINLIST 	204
#define MATCH_SUBTABLEINLIST 	208
#define MATCH_LOOP 		205
#define MATCH_LOOPCONTROL	206

/* flags set in cmd (>=256) */
#define MATCH_CALLTAG		(1 << 8)
#define MATCH_APPENDTAG 	(1 << 9)
#define MATCH_APPENDTAGOBJ	(1 << 10)
#define MATCH_APPENDMATCH	(1 << 11)
#define MATCH_LOOKAHEAD		(1 << 12)

/* special argument integers */
#define MATCH_THISTABLE		999

extern 
int fast_tag(PyObject *pytext,  	/* must be a Python string */
	     char *text,		/* text of that string */
	     int len_text,		/* length of the Python string */
	     PyObject *table,		/* must be a tuple (this is *not* checked) */
	     int start,			/* start position in text */
	     PyObject *taglist,		/* must be a Python list */
	     int *next);       		/* output: next position in text */

/* EOF */
#ifdef __cplusplus
}
#endif
#endif
