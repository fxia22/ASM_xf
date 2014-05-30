#!/usr/local/bin/python

""" Words - tag words in a string (Version 0.2)
    
    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""

from mx.TextTools import *

lcwords = []
cwords = []

lower_case_word = (lcwords,AppendToTag+Table,
        (# first char in word
         (None,IsIn,a2z+umlaute),
         # all other chars (if there are any)
         (None,AllIn,german_alpha,MatchOk))
       )

capital_word = (cwords,AppendToTag+Table,
        (# first char in word
         (None,IsIn,A2Z+Umlaute),
         # all other chars (if there are any)
         (None,AllIn,german_alpha,MatchOk))
       ) 

tag_words = (lower_case_word+(+1,+2),
             capital_word+(+1,),
             (None,AllIn,white+newline,+1),
             (None,AllNotIn,german_alpha+white+newline,+1), # uninteresting
             (None,EOF,Here,-4)) # EOF

if __name__ == '__main__':
    
    import sys

    # read in a file
    f = open(sys.argv[1])
    text = f.read()

    t = TextTools._timer()

    t.start()
    # don't need a taglist, so pass None
    result, taglist, nextindex = tag(text,tag_words,0,len(text))
    t = t.stop()
    
    print result, nextindex

    print 'lower case words:'
    for n,l,r,d in lcwords:
        print ' ',text[l:r]
    print
    print 'capital letter words:'
    for n,l,r,d in cwords:
        print ' ',text[l:r]
    print
    print 'found',len(lcwords)+len(cwords),'words in',t[0],'sec (scanned',len(text),'bytes)'
