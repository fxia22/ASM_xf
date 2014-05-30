#!/usr/local/bin/python

""" mysplit - an alternative split implementation (Version 0.1)
    
    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""
from mx.TextTools import *

mysplit_table = (
    # Match all whitespace
    (None,AllInSet,whitespace_set,+1),
    # Match and tag all non-whitespace
    ('text',AllInSet + AppendMatch,nonwhitespace_set,+1),
    # Loop until EOF
    (None,EOF,Here,-2),
    )

def mysplit(text,

            table=mysplit_table,tag=tag):

    return tag(text,table)[1]

###

import exceptions

stoplist = {'abc':1, 'def':1}

class KeywordFound(exceptions.StandardError):
    def __init__(self, taglist):
        self.taglist = taglist

def callable(taglist,text,l,r,subtags):

    taglist.append(text[l:r])
    if stoplist.has_key(text[l:r]):
        raise KeywordFound(taglist)

mysplitex_table = (
    # Match all whitespace
    (None,AllInSet,whitespace_set,+1),
    # Match and tag all non-whitespace
    (callable,AllInSet + CallTag,nonwhitespace_set,+1),
    # Loop until EOF
    (None,EOF,Here,-2),
    )

def mysplitex(text,

              table=mysplitex_table,tag=tag,KeywordFound=KeywordFound):

    try:
        return tag(text,table)[1]
    except KeywordFound,data:
        return data.taglist

###

if __name__ == '__main__':

    import time
    from string import split

    tries = tuple(range(100000))
    probe = 'abc def ghi jkjkjl asfwer sdfswer sfasgwer svasdwer'

    print 'mysplit:',
    t = time.clock()
    for i in tries:
        l = mysplit(probe)
    print time.clock() - t,'sec.'

    print 'mysplit (calling tag() directly):',
    t = time.clock()
    for i in tries:
        l = tag(probe,mysplit_table)[1]
    print time.clock() - t,'sec.'

    print 'setsplit:',
    t = time.clock()
    sp = setsplit
    ws = whitespace_set
    for i in tries:
        l = sp(probe,ws)
    print time.clock() - t,'sec.'
        
    print 'string.split:',
    t = time.clock()
    for i in tries:
        l = split(probe)
    print time.clock() - t,'sec.'
        
