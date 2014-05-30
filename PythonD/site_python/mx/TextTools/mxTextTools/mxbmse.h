#ifndef MXBMSE_H
#define MXBMSE_H
/* 
  mxbmse -- Fast Boyer Moore Search Algorithm (Version 0.8)

  The implementation is reentrant and thread safe. While the
  general idea behind the Boyer Moore algorithm are in the public
  domain, this implementation falls under the following copyright:

  Copyright (c) 1997-2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
  Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com

                        All Rights Reserved

  See the documentation for copying information or contact the author
  (mal@lemburg.com).

*/

#ifdef __cplusplus
extern "C" {
#endif

/* sanity check switches */
/*#define SAFER 1*/

/* [X]SHIFT must have enough bits to store len(match) 
   - using 'char' here makes the routines run 15% slower than
     with 'int', on the other hand, 'int' is at least 4 times
     larger than 'char'
*/
#define SHIFT_TYPE int
#define XSHIFT_TYPE char

typedef struct {
    char *match;
    int len_match;
    char *eom;
    char *pt;
    SHIFT_TYPE shift[256]; /* char-based shift table */
} mxbmse_data;

/* Boyer-Moore Algorithm */

extern mxbmse_data *bm_init(char *match,
			      int len_match);
extern void bm_free(mxbmse_data *c);
extern int bm_search(mxbmse_data *c,
		     char *text,
		     int start,
		     int len_text);
extern int bm_tr_search(mxbmse_data *c,
			char *text,
			int start,
			int len_text,
			char *tr);

/* EOF */
#ifdef __cplusplus
}
#endif
#endif
