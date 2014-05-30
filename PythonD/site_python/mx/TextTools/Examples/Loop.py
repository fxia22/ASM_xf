#!/usr/local/bin/python

""" Loop - loop examples (Version 0.1)
    
    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""

import sys,string

# engine + constants
from mx.TextTools import *

# use Loop to match a certain number of subtags
table1 = ((None,Word,'loop '),
         # match <= 5 stars
         ('loop',Loop,5,+4),
          (None,Is,'*',+1,-1),
          (None,LoopControl,Break),
          (None,Jump,To,-3),
         # must end with a dot
         (None,Is,'.'))

# use Loop to tag subsections of a tagging table, i.e.
# emulate a Table-match
table2 = (('presection',AllNotIn,'(',+1),
          # match a group of characters enclosed in ()
          ('section',Loop,1,+4),
           (None,Is,'('),
           (None,AllNotIn,')'),
           (None,Is,')',0,-3),
         # must end with a dot
         (None,Is,'.'))

# read in all chars and then do lots of null loops
table3 = (('Loops',Loop,10000,MatchOk),
          (None,AllNotIn,'',-1,-1))

text = raw_input('loop-example (e.g. "loop *."): ')
result, taglist, nextindex = tag(text,table1)
print 'result =',result,'-- rest of text:',text[nextindex:]
if result:print_tags(text,taglist)

text = raw_input('section-example( e.g. "myfun(params)."): ')
result, taglist, nextindex = tag(text,table2)
print 'result =',result,'-- rest of text:',text[nextindex:]
if result:print_tags(text,taglist)

text = raw_input('null-loops-example (e.g. "some chars"): ')
result, taglist, nextindex = tag(text,table3)
print 'result =',result,'-- rest of text:',text[nextindex:]
if result:print_tags(text,taglist)
