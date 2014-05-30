#!/usr/local/bin/python

""" Python - tag table for Python (Version 0.6)

    * 0.5->0.6: changed the names of the tags !
                fixed bug in match_str()

    XXX can't handle (lambda ...) and misses not in 'if x is not'

    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""
# engine + constants
from mx.TextTools import *

# helper for correct string matching (with \quotes):

def match_str(s,x,len_text,c):

    while x < len_text and s[x] != c:
        if s[x] == '\\' and s[x+1] == c: 
            x = x + 2
            continue
        x = x + 1
    return x

comment = ('comment',Table,
            ((None,Is,'#'),
             (None,AllNotIn,'\n\r',MatchOk))
          )

whitespace = (None,AllIn,' \t')
opt_whitespace = whitespace + (+1,)

identifier = ('identifier',Table,
              ((None,IsIn,alpha+'_'),
               (None,AllIn,alpha+'_'+number,MatchOk))
             )

string = ('str',Table,
          (# hints
           (None,IsIn,'\"\''),
           (None,Skip,-1),
           # now let's see what we have...
           (None,Word,'"""',+4),
            ('string',NoWord,'"""',+1),
            (None,Word,'"""'),
            (None,Jump,To,MatchOk),
           (None,Word,"'''",+4),
            ('string',NoWord,"'''",+1),
            (None,Word,"'''"),
            (None,Jump,To,MatchOk),
           (None,Is,'"',+4),
            ('string',CallArg,(match_str,'"'),+1),
            (None,Word,'"'),
            (None,Jump,To,MatchOk),
           (None,Is,"'"),
            ('string',CallArg,(match_str,"'"),+1),
            (None,Word,"'"),
            (None,Jump,To,MatchOk))
         )

skw = ["del", "from", "lambda", "return", "and", "elif",
"global", "not", "try", "break", "else", "if", "or", "while",
"except", "import", "pass", "continue", "finally", "in", "print",
"for", "is", "raise"]
keywords = word_in_list(skw)

# note: '=lambda x:...' and '(lambda x:...' are not recognized,
#       yet '= lambda x:...' and '( lambda x:...' are (just like in
#       emacs python-mode) !

keyword = ('kw',Table,
           ((None,AllIn,' \t\n\r'),
            # hints
            (None,IsIn,alpha),
            (None,Skip,-1),
            # one in the list keywords
            ('keyword',Table,keywords,+3),
              (None,IsIn,': \t\n\r'),
              (None,Jump,To,MatchOk),
            # a function declaration
            ('keyword',Word,'def',+12),
              whitespace,
              identifier,
              (None,Is,'('),
              # scan parameters
              ('parameter',AllNotIn,'(),',+2),
              # are there more ?
              (None,Is,',',+1,-1),
              # tuple in param-list ?
              (None,Is,'(',+1,-2),
              # maybe we're done
              (None,Is,')'),
              # to make sure...
              (None,Is,',',+1,-4),
              (None,Is,')',+1),
              # test for correct syntax
              (None,IsIn,': \t\n\r'),
              (None,Jump,To,MatchOk),
            # a class declaration:
            ('keyword',Word,'class'),
              whitespace,
              identifier,
              (None,Is,'(',MatchOk),
              # scan base-classes
              ('baseclass',AllNotIn,'),',+2),
              # are there more ?
              (None,Is,',',+1,-1),
              # we're done
              (None,Is,')'),
              (None,IsIn,': \t\n\r'))
           )

python_script = (comment+(+1,-0),
                 string+(+1,-1),
                 keyword+(+1,-2),
                 # end-of-file ?
                 (None,EOF,Here,+1,MatchOk),
                 # skip uninteresting chars and restart
                 (None,IsIn,any),
                 (None,AllNotIn,'#\'\"_ \n\r\t',-5,-5)
                )

if __name__ == '__main__':

    ### testing

    import sys

    # open file
    text = open(sys.argv[-1]).read()
    print 'read',len(text),'bytes...'
    taglist = []
    t = TextTools._timer()

    # parse file
    t.start()
    result, taglist, next = tag(text,python_script,0,len(text),taglist)
    print 'tag:',t.stop(),'sec.'

    # run against Just's PyFontify if available
    try: 
        import PyFontify # URL: ftp://starship.python.net/pub/crew/just/PyFontify.py
        t.start()
        PyFontify.fontify(text)
        print 'PyFontify:',t.stop(),'sec.'
    except ImportError:
        pass
        
    print 'hit return...'
    raw_input()
    print result
    if result:
        print_tags(text,taglist)
