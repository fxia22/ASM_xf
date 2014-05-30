#!/usr/local/bin/python

""" pytag - tag strings given a table of things to look for (Version 0.6)
    
    * includes the Python version pytag() of the tagging engine
    * this module includes a debugger for tag tables; to enable it,
      call pytag.use_debugger(); when the debugger prompts, enter 'h'
      to see a help screen
    * it also allows for verbose output while trying to tag a string;
      call pytag.set_verbosity(1) to see the whole process of tagging

      XXX: doesn't know anything about the new commands introduced in
          the C version !!!

      XXX: NOT SUPPORTED ANYMORE (well, at least for now)

    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2001, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
    
"""

import sys,string

# globals 
verbose = 0
debugging = 0
breakpoints = []

# some useful constants
from mx.TextTools import *

import types
strtype = types.StringType
tabletype = types.TupleType
fcttype = types.FunctionType

MatchError = 'MatchError'

not_set = 0

#
# Python version of tag():
#

def pytag(text,table,startindex=0,len_text=not_set,taglist=not_set):

    """Tag text[startindex:len_text] using the Tag Table given in table.
       - returns a tuple (success, taglist, nextindex)
       - if taglist == None, then no taglist is created
    """
    if len_text is not_set:
        # use all chars in text
        len_text = len(text)
    if taglist is not_set:
        # create a fresh new list
        taglist = []
    if verbose: print '\ntag()-call'
    i = 0
    x = startindex
    loopcounter = -1

    while i < len(table):

        entry = table[i]
        lentry = len(entry)
        if verbose:
            print 'text[%i]:table[%i]\tentry\t%s'%(x,i,format_entry(table,i))
            print '\t\t\tin\t%s'%(repr(text[x:len_text])[:40])
        if lentry == 4:
            tagobj, cmd, match, jne = entry
            je = +1
        elif lentry == 5:
            tagobj, cmd, match, jne, je = entry
        else:
            tagobj, cmd, match = entry
            jne = 0
            je = +1

        if debugging:
            if debugging == 3 and (x not in breakpoints):
                pass
            else:
                global debugging
                debugging,x,i = debugger(text,x,len_text,table,i,loopcounter,taglist)

        subtags = None
        flags = cmd & ~0xFF
        cmd = cmd & 0xFF
            
        if cmd == AllIn:
            if type(match) != strtype: raise TypeError,'match must be a string'
            start = x
            while x < len_text and text[x] in match:
                x = x + 1
            if start == x:
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                if verbose: print '\nAllIn matched',repr(tagobj),start,':',x,repr(text[start:x])[:40]

        elif cmd == AllNotIn:
            if type(match) != strtype: raise TypeError,'match must be a string'
            start = x
            while x < len_text and text[x] not in match:
                x = x + 1
            if start == x:
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                if verbose: print '\nAllNotIn matched',repr(tagobj),start,':',x,repr(text[start:x])[:40]

        elif cmd == Is:
            if type(match) != strtype: raise TypeError,'match must be a string'
            start = x
            if x < len_text and text[x] == match:
                x = x + 1
            if start == x:
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                if verbose: print '\nIs matched',repr(tagobj),start,':',x,repr(text[start:x])[:40]

        elif cmd == IsIn:
            if type(match) != strtype: raise TypeError,'match must be a string'
            start = x
            if x < len_text and text[x] in match:
                x = x + 1
            if start == x:
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                if verbose: print '\nIsIn matched',repr(tagobj),start,':',x,repr(text[start:x])[:40]

        elif cmd == IsNotIn:
            if type(match) != strtype: raise TypeError,'match must be a string'
            start = x
            if x < len_text and text[x] not in match:
                x = x + 1
            if start == x:
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                if verbose: print '\nIsNotIn matched',repr(tagobj),start,':',x,repr(text[start:x])[:40]

        elif cmd == Word:
            if type(match) != strtype: raise TypeError,'match must be a string'
            start = x
            if text[x:x+len(match)] == match and x < len_text:
                x = x + len(match)
            if start == x:
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                if verbose: print '\nWord matched',repr(tagobj),start,':',x,repr(text[start:x])[:40]

        elif cmd == NoWord:
            if type(match) != strtype: raise TypeError,'match must be a string'
            start = x
            lw = len(match)
            while x < len_text and text[x:x+lw] != match:
                x = x + 1
            if start == x:
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                if verbose: print '\nNoWord matched',repr(tagobj),start,':',x,repr(text[start:x])[:40]

        elif cmd == Table:
            if type(match) != tabletype: raise TypeError,'match must be a table'
            start = x

            if debugging == 2:
                global debugging
                d = debugging
                debugging = 0
                result, subtags, nextindex = tag(text,match,x,len_text,[])
                debugging = d
            else:
                result, subtags, nextindex = tag(text,match,x,len_text,[])

            if not result:
                if verbose: print '\nTable did not match\n'
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                x = nextindex
                if verbose: print '\nTable matched',repr(tagobj),start,':',x,repr(text[x:nextindex])[:40]

        elif cmd == TableInList:
            start = x
            tablelist, entry = match

            if debugging == 2:
                global debugging
                d = debugging
                debugging = 0
                result, subtags, nextindex = tag(text,tablelist[entry],x,len_text,[])
                debugging = d
            else:
                result, subtags, nextindex = tag(text,tablelist[entry],x,len_text,[])

            if not result:
                if verbose: print '\nTableInList did not match\n'
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                x = nextindex
                if verbose: print '\nTableInList matched',repr(tagobj),start,':',x,repr(text[x:nextindex])[:40]

        elif cmd == Call:
            start = x
            x = match(text,start,len_text)
            if start == x:
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                if verbose: print '\nCall matched',repr(tagobj),start,':',x,repr(text[start:x])[:40]

        elif cmd == CallArg:
            start = x
            try:
                fct, arg = match
            except:
                raise TypeError,'match must be a tuple (fct,arg)'
            x = fct(text,start,len_text,arg)
            if start == x:
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                if verbose: print '\nCallArg matched',repr(tagobj),start,':',x,repr(text[start:x])[:40]

        elif cmd == Loop:
            start = x
            # loop-construct
            if loopcounter > 0:
                # next
                loopcounter = loopcounter - 1
            elif loopcounter < 0:
                # init
                loopcounter = match
                loopstartpos = x
            if verbose: print '\nLoop count =',loopcounter,' startpos =',loopstartpos
            if loopcounter == 0:
                # end
                loopcounter = -1
                # matched
                start = loopstartpos
                if verbose: print '\nLoop matched',repr(tagobj),start,':',x,repr(text[start:x])[:40]
                je = jne
            else:
                # continue loops
                i = i + je
                continue

        elif cmd == LoopControl:
            loopcounter = match
            i = i + je
            continue

        elif cmd == EOF:
            # match end-of-string
            if len_text > x:
                # not matched
                if not jne:
                    # match failed
                    return (0,taglist,x)
                # try an other entry
                i = i + jne
                continue
            else:
                # matched
                x = len_text
                if verbose: print '\nmatched EOF'
                je = MatchOk

        elif cmd == Fail:
            if not jne:
                # match failed
                return (0,taglist,x)
            # try an other entry
            i = i + jne
            continue

        elif cmd == Skip:
            # skip match bytes (back or forward) in text
            x = x + match
            if verbose:
                if match > 0: y,z = x - match,x
                else:         y,z = x,x - match
                print '\nSkip ',repr(tagobj),'to',x,'skipped:',repr(text[y:z])[:40]

        else:
            raise TypeError,'tag-command unknown: '+repr(cmd)

        # append to taglist
        if tagobj is not None:
            if flags > 0:
                if flags & CallTag:
                    tagobj(taglist,text,start,x,subtags)
                elif flags & AppendToTag:
                    tagobj.append((start,x,subtags))
                else:
                    raise TypeError,'tag-command-flag unknown: '+repr(flag)
            else:
                if taglist is not None:
                    taglist.append((tagobj,start,x,subtags))

        if verbose: print 72*'-'

        # goto next table entry
        i = i + je

    # table matched ok
    return (1,taglist,x)

#
# Override the C version
#
TextTools.tag = pytag

#
# get all the goodies from TextTools
#
from mx.TextTools import *

#
# setup functions for the Python version pytag()
#

def set_verbosity(level = 1):
    """ set verbosity for tagging: 0=off 1=on """
    global verbose
    verbose = level
    
def use_debugger(bp=[]):
    """ use the tag table debugger
        * bp can be a list of preset breakpoints (bytes into text)
    """
    global debugging, breakpoints
    debugging = 1
    breakpoints = bp


def debugger(text,x,len_text,table,i,loopvar,taglist):
    """ the tag table debugger front end
        * returns (rc,x,i)
          with rc = 0 ... stop debugging   #
                  = 1 ... do one step      #
                  = 2 ... step over table  #
    """
    rc = -1
    print 75*'_'
    print '| table[%i]=(%s)'%(i,format_entry(table,i))
    print '| text[%i:]=%s'%(x,repr(text[x:len_text])[:55])
    print '| h = help; vars: loop counter =',loopvar
    print 75*'-'
    while rc < 0:
        s = raw_input('tag-debugger >>> ')
        try:
            if len(s) > 0:
                c = s[0]
            else:
                c = 's' # hitting return is like entering 's'
            if c == 's':
                rc = 1
            elif c == 'n':
                rc = 2
            elif c == 'w':
                print 'table[',i,']=(',format_entry(table,i),')'
                print 'text [',x,']:',repr(text[x:len_text])[:55]
                print 'vars: loop counter =',loopvar
            elif c == 'q':
                rc = 0
            elif c == 'r':
                rc = 3
            elif c == 'b':
                global breakpoints
                breakpoints.append(string.atoi(s[1:]))
            elif c == 'c':
                global breakpoints
                breakpoints.remove(string.atoi(s[1:]))
            elif c == 'l':
                print 'breakpoints:'
                for b in breakpoints:
                    print ' ',b,'text =',repr(text[b:])[:60]
            elif c == 'g':
                x = string.atoi(s[1:])
            elif c == 'v':
                global verbose
                verbose = 1 - verbose
            elif c == 't':
                print 'taglist:'
                print_tags(text,taglist)
            elif c == 'm':
                print 'current matching table:'
                print format_table(table,i)
            elif c == 'p':
                y = string.atoi(s[1:])
                print 'text[',y,']:',repr(text[y:len_text])[:60]
            else:
                raise 'help'
        except 'help':
            print 'Commands:'
            print 's = step next entry  | return = step'
            print 'w = where are we     | q = run without debugging'
            print 'b*= add breakpoint * | c*= delete breakpoint *'
            print 'l = list breakpoints | v = switch verbosity on/off'
            print 't = show taglist     | r = run to next breakpoint/end'
            print 'n = step over table  | p*= print text from byte *'
            print 'g*= goto position *  | m = show current matching table'
            print
            print '*...these take an argument, e.g. b1200 or p 1200'
        except:
            print 'Internal Debugger Error -- last request not processed !'
    if verbose: print 72*'_'
    return rc,x,i
