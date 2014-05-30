#!/usr/local/bin/python

""" RTF - tag a RTF string (Version 0.2)
    
    This version does recursion using the TableInList cmd.
    
    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""

import sys,string

# engine + constants
from mx.TextTools import *

# list of tables (hack to be able to do recursion)
tables = []
# indices
rtf_index = 0

numeral = (# sign ?
           (None,Is,'-',+1),
           (None,AllIn,number)
          )

# XXX: doesn't know how to handle \bin et al. with embedded {}

ctrlword = (# name
            ('name',AllIn,a2z),
            # delimiter
            (None,Is,' ',+1,MatchOk),
            (None,IsIn,number+'-',MatchOk),
             (None,Skip,-1),
             ('param',Table,numeral,+0,MatchOk),
             (None,Is,' ',+1,MatchOk),
              (None,Skip,-1)
           )

hex = set(number+'abcdefABCDEF')
notalpha = set(alpha,0)

ctrlsymbol = (# hexquote
              (None,Is,"'",+3),
               (None,IsInSet,hex),
               (None,IsInSet,hex),
              # other
              (None,IsInSet,notalpha,+1,MatchOk)
             )

rtf = (# control ?
       (None,Is,'\\',+3),
        # word
        ('word',Table,ctrlword,+1,-1),
        # symbol
        ('symbol',Table,ctrlsymbol,+1,-2),
       # closing group
       (None,Is,'}',+2),
        (None,Skip,-1,0,MatchOk),
       # nested group
       (None,Is,'{',+4),
        # recurse
        ('group',TableInList,(tables,rtf_index)),
        (None,Is,'}'),
        (None,Jump,To,-8),
       # document text
       ('text', AllNotIn, '\\{}',+1,-9),
       # EOF
       ('eof',EOF,Here)
      )

# add tables to list
tables.append(rtf)

# note:
# TableInList,(tables,rtf_index)) means: use table tables[rtf_index]

if __name__ == '__main__':

    t = TextTools._timer()

    # read file
    f = open(sys.argv[1])
    text = f.read()

    # tag text
    t.start()
    result, taglist, nextindex = tag(text,rtf)
    t = t.stop()[0]

    print result, nextindex, t,'sec ... hit return to see the tags'
    raw_input()
    print
    print_tags(text,taglist)
