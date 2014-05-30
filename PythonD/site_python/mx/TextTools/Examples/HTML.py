#!/usr/local/bin/python

""" HTML - tag a HTML string (Version 0.6)
    
    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""

import sys,string

# constants + engine
from mx.TextTools import *

# ErrorTag
error = '*syntax error'                 # error tag obj

tagname_set = set(alpha+'-'+number)
tagattrname_set = set(alpha+'-'+number)
tagvalue_set = set('"\'> ',0)
white_set = set(' \r\n\t')

tagname_set = set(alpha+'-'+number)
tagattrname_set = set(alpha+'-'+number)
tagvalue_set = set('"\'> ',0)
white_set = set(' \r\n\t')

tagattr = (
       # name
       ('name',AllInSet,tagattrname_set),
       # with value ?
       (None,Is,'=',MatchOk),
       # skip junk
       (None,AllInSet,white_set,+1),
       # unquoted value
       ('value',AllInSet,tagvalue_set,+1,MatchOk),
       # double quoted value
       (None,Is,'"',+5),
         ('value',AllNotIn,'"',+1,+2),
         ('value',Skip,0),
         (None,Is,'"'),
         (None,Jump,To,MatchOk),
       # single quoted value
       (None,Is,'\''),
         ('value',AllNotIn,'\'',+1,+2),
         ('value',Skip,0),
         (None,Is,'\'')
       )

valuetable = (
    # ignore whitespace + '='
    (None,AllInSet,set(' \r\n\t='),+1),
    # unquoted value
    ('value',AllInSet,tagvalue_set,+1,MatchOk),
    # double quoted value
    (None,Is,'"',+5),
     ('value',AllNotIn,'"',+1,+2),
     ('value',Skip,0),
     (None,Is,'"'),
     (None,Jump,To,MatchOk),
    # single quoted value
    (None,Is,'\''),
     ('value',AllNotIn,'\'',+1,+2),
     ('value',Skip,0),
     (None,Is,'\'')
    )

allattrs = (
    # look for attributes
    (None,AllInSet,white_set,+4),
     (None,Is,'>',+1,MatchOk),
     ('tagattr',Table,tagattr),
     (None,Jump,To,-3),
    (None,Is,'>',+1,MatchOk),
    # handle incorrect attributes
    (error,AllNotIn,'> \r\n\t'),
    (None,Jump,To,-6)
    )

htmltag = (
    (None,Is,'<'),
    # is this a closing tag ?
    ('closetag',Is,'/',+1),
    # a coment ?
    ('comment',Is,'!',+8),
     (None,Word,'--',+4),
     ('text',sWordStart,FS('-->'),+1),
     (None,Skip,3),
     (None,Jump,To,MatchOk),
     # a SGML-Tag ?
     ('other',AllNotIn,'>',+1),
      (None,Is,'>'),
     (None,Jump,To,MatchOk),
    # XMP-Tag ?
    ('tagname',Word,'xmp',+5),
     (None,Is,'>'),
     ('text',sWordStart,FS('</xmp>',to_lower)),
     (None,Skip,len('</xmp>')),
     (None,Jump,To,MatchOk),
    # get the tag name
    ('tagname',AllInSet,tagname_set),
    # look for attributes
    (None,AllInSet,white_set,+4),
     (None,Is,'>',+1,MatchOk),
     ('tagattr',Table,tagattr),
     (None,Jump,To,-3),
     (None,Is,'>',+1,MatchOk),
    # handle incorrect attributes
    (error,AllNotIn,'> \n\r\t'),
    (None,Jump,To,-6)
    )

htmltable = (# HTML-Tag
             ('htmltag',Table,htmltag,+1,+4),
             # not HTML, but still using this syntax: error or inside XMP-tag !
             (error,Is,'<',+3),
              (error,AllNotIn,'>',+1),
              (error,Is,'>'),
             # normal text
             ('text',AllNotIn,'<',+1),
             # end of file
             ('eof',EOF,Here,-5),
            )

if __name__ == '__main__':

    t = TextTools._timer()

    # read file
    f = open(sys.argv[1])
    text = f.read()

    try:
        count = string.atoi(sys.argv[2])
    except:
        count = 1000
    
    print 'Starting to parse the file %i times...' % count

    # parse file
    t.start()
    for i in range(count):
        utext = upper(text)
        result, taglist, nextindex = tag(utext,htmltable)
        if not result:
            print ' parsing failed; aborting'
            break
    t = t.stop()[0]

    mean = t/count
    print result, nextindex, mean*1000,'msec',nextindex/mean,'bytes/sec.'
    print
    print 'Hit return to see the tags...'
    raw_input()
    print
    print_tags(text,taglist)
