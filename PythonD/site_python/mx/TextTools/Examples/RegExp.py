#!/usr/local/bin/python

""" RegExp - tag a string using regexps (Version 0.1)
    
    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""

# engine + constants
from mx.TextTools import *

# special matching function
def match_regexp(text,position,len_text,regexpr):
    position = position + max(0,regexpr.match(text,position))
    return position

# create a table in the sense re_1\|re_2\|...\|re_N where
# re_i \in regexps
def or_regexps(regexps):
    # regexps = list of compiled regexps
    l = []
    for i in range(len(regexps)):
        l.append((i,CallArg,(match_regexp,regexps[i]),+1,MatchOk))
    l.append((None,Fail,Here))
    return tuple(l)

if __name__ == '__main__':

    # create some simple regexps
    import regex
    regexps = [ 'spam*', 'ham*', 'eggs' ]
    regexps = map(regex.compile,regexps)
    table = or_regexps(regexps)

    text = raw_input('type some words: ')
    result, taglist, nextindex = tag(text,table)

    if result:
        print 'subexpr nr.',taglist[0][0],'matched:',taglist[0]
    else:
        print 'no match'

    if nextindex < len(text): 
        print 'rest of unparsed input:',text[nextindex:]
