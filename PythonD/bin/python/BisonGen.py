#!python
"""
A Bison input file generator
WWW: http://4suite.com/BisonGen        e-mail: support@4suite.com

Copyright (c) 1999 Fourthought Inc., USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string

from xml.dom import Node
from xml.dom.ext.reader import Sax
import os, string, getopt

ReservedWords = {'class':'_class'
                 }

g_nonTerminalList = []

if os.environ.has_key('BGENCONFIGDIR'):
    g_makeConfigDir = os.environ['BGENCONFIGDIR']
else:
    g_makeConfigDir = '/dev/env/DJDIR/etc/4Suite/'


def GenFiles(fileName, genMapping, genNestedTuple):
    dom = Sax.FromXmlFile(fileName, validate=0)
    GenNonTerminalList(dom)
    GenBison(dom)
    GenHeader(dom)
    GenSwigHeader(dom)
    GenSwigC(dom)
    GenSwigI(dom)
    GenMakeFile(dom)
    GenParser(dom)
    GenMapping and GenMapping(dom)
    GenNestedTuple and GenNestedTuple(dom)
    return


def TranslatePythonKeyword(inWord):
    if inWord in ReservedWords.keys():
        return ReservedWords[inWord]
    return inWord


def GenNonTerminalList(dom):
    global g_nonTerminalList
    nts = dom.getElementsByTagName('NON_TERMINAL')
    for n in nts:
        g_nonTerminalList.append(n.firstChild.data)


def GenMapping(dom):
    genName = dom.documentElement.getAttribute('NAME')
    projectName = dom.documentElement.getAttribute('PROJECT')
    if not projectName:
        projectName = genName
    outFile = open('%sParseTreeMapping.py' % genName,'w')
    outFile.write("import %s\n" % genName)
    outFile.write("import %sParserBase\n" % genName)

    outFile.write("from Ft.Lib import TraceOut\n")

    outFile.write("trace = TraceOut.TraceOut(['%s.Parsers.%sParserImp', '%s.Parsers', '%s'])\n" % (projectName,genName,projectName,projectName))

    outFile.write("from %sParserBase import SyntaxException\n" % genName)
    outFile.write("from %sParserBase import ParseTreeException\n" % genName)
    outFile.write("from %sParserBase import PrintSyntaxException\n" % genName)
    outFile.write("from %sParserBase import PrintParseTreeException\n" % genName)

    outFile.write("class %sParseTreeMapping(%sParserBase.%sParserBase):\n" % (genName,genName,genName))
    outFile.write("\tdef __init__(self):\n")
    outFile.write("\t\t%sParserBase.%sParserBase.__init__(self)\n" % (genName,genName))

    rule_sets = dom.getElementsByTagName('RULE_SET')
    for rule_set in rule_sets:
        numGen = -1
        rules = rule_set.getElementsByTagName('RULE')
        for rule in rules:
            symbols = rule.getElementsByTagName('SYMBOL')
            gen = rule.getElementsByTagName('PYTHON_CALLBACK')
            if len(gen) == 0:
                continue
            if len(symbols) > numGen:
                numGen = len(symbols)
        if numGen == -1:
            continue
        #Define the function def
        nt = rule_set.getElementsByTagName('NON_TERMINAL')[0].childNodes[0].data
        outFile.write('\tdef %s(self' % TranslatePythonKeyword(nt))
        for ctr in range(numGen):
            outFile.write(', arg%d = None' % ctr)
        outFile.write('):\n')

        #Write the traceout command
        outFile.write("\t\ttrace('%s called with " % nt)
        for ctr in range(numGen):
            outFile.write('%s ')

        outFile.write("' % (")
        for ctr in range(numGen):
            if ctr == 0:
                outFile.write('str(arg%d)' % ctr)
            else:
                outFile.write(', str(arg%d)' % ctr)
        outFile.write("))\n")

        #Create a new struct
        outFile.write("\t\tnewNode = {}\n")
        outFile.write("\t\tnewNode['TYPE'] = '%s'\n" % string.upper(nt))

        r = range(numGen)
        r.reverse()
        for ctr in r:
            outFile.write("\t\tif arg%d == '%%%%FT-NT%%%%':\n" % ctr)
            outFile.write("\t\t\tnewNode[%d] = self.pop()\n" % ctr)
            outFile.write("\t\telse:\n")
            outFile.write("\t\t\tnewNode[%d] = arg%d\n" % (ctr,ctr))
            
        outFile.write("\t\tself.push(newNode)\n\n")

    outFile.write('\n');
    outFile.write("if __name__ == '__main__':\n")
    outFile.write("\tfrom Ft.Lib import DumpBgMapping\n")
    outFile.write("\timport sys\n")
    outFile.write("\trt = []\n")
    outFile.write("\tp = %sParseTreeMapping()\n" % genName)
    outFile.write("\tif len(sys.argv)==2:\n")
    outFile.write("\t\tl = open(sys.argv[1],'r').read()\n")
    outFile.write("\telse:\n")
    outFile.write('\t\tl = raw_input(">>>")\n')
    outFile.write('\ttry:\n')
    outFile.write("\t\trt = p.parse(l)\n")
    outFile.write("\t\tDumpBgMapping.Dump(rt)\n")
    outFile.write('\texcept ParseTreeException, e:\n')
    outFile.write('\t\tPrintParseTreeException(e)\n')
    outFile.write('\texcept SyntaxException, e:\n')
    outFile.write('\t\tPrintSyntaxException(e)\n')

    outFile.close()


def GenNestedTuple(dom):
    genName = dom.documentElement.getAttribute('NAME')
    projectName = dom.documentElement.getAttribute('PROJECT')
    if not projectName:
        projectName = genName
    outFile = open('%sParseTreeTuple.py' % genName,'w')
    outFile.write("import %s\n" % genName)
    outFile.write("import %sParserBase\n" % genName)

    outFile.write("from Ft.Lib import TraceOut\n")

    outFile.write("trace = TraceOut.TraceOut(['%s.Parsers.%sParserImp', '%s.Parsers', '%s'])\n" % (projectName,genName,projectName,projectName))

    outFile.write("from %sParserBase import SyntaxException\n" % genName)
    outFile.write("from %sParserBase import ParseTreeException\n" % genName)
    outFile.write("from %sParserBase import PrintSyntaxException\n" % genName)
    outFile.write("from %sParserBase import PrintParseTreeException\n" % genName)

    outFile.write("class %sParseTreeTuple(%sParserBase.%sParserBase):\n" % (genName,genName,genName))
    outFile.write("\tdef __init__(self):\n")
    outFile.write("\t\t%sParserBase.%sParserBase.__init__(self)\n" % (genName,genName))

    rule_sets = dom.getElementsByTagName('RULE_SET')
    for rule_set in rule_sets:
        numGen = -1
        rules = rule_set.getElementsByTagName('RULE')
        for rule in rules:
            symbols = rule.getElementsByTagName('SYMBOL')
            gen = rule.getElementsByTagName('PYTHON_CALLBACK')
            if len(gen) == 0:
                continue
            if len(symbols) > numGen:
                numGen = len(symbols)
        if numGen == -1:
            continue
        #Define the function def
        nt = rule_set.getElementsByTagName('NON_TERMINAL')[0].childNodes[0].data
        outFile.write('\tdef %s(self' % TranslatePythonKeyword(nt))
        for ctr in range(numGen):
            outFile.write(', arg%d = None' % ctr)
        outFile.write('):\n')

        #Write the traceout command
        outFile.write("\t\ttrace('%s called with " % nt)
        for ctr in range(numGen):
            outFile.write('%s ')

        outFile.write("' % (")
        for ctr in range(numGen):
            if ctr == 0:
                outFile.write('str(arg%d)' % ctr)
            else:
                outFile.write(', str(arg%d)' % ctr)
        outFile.write("))\n")

        #Create a non-terminal node
        outFile.write("\t\tnewNode = []\n")
        outFile.write("\t\tnewNode[0:0] = ['%s']\n" % string.upper(nt))

        r = range(numGen)
        r.reverse()
        for ctr in r:
            outFile.write("\t\tif arg%d == '%%%%FT-NT%%%%':\n" % ctr)
            outFile.write("\t\t\tnewNode[%d:%d] = [self.pop()]\n" % (ctr+1, ctr+1))
            outFile.write("\t\telse:\n")
            outFile.write("\t\t\tnewNode[%d:%d] = [arg%d]\n" % (ctr+1,ctr+1,ctr))

        outFile.write("\t\tself.push(tuple(newNode))\n\n")

    outFile.write('\n')
    outFile.write("if __name__ == '__main__':\n")
    outFile.write("\tfrom Ft.Lib import DumpBgTuple\n")
    outFile.write("\timport sys\n")
    outFile.write("\trt = []\n")
    outFile.write("\tp = %sParseTreeTuple()\n" % genName)
    outFile.write("\tif len(sys.argv)==2:\n")
    outFile.write("\t\tl = open(sys.argv[1],'r').read()\n")
    outFile.write("\telse:\n")
    outFile.write('\t\tl = raw_input(">>>")\n')
    outFile.write('\ttry:\n')
    outFile.write("\t\trt = p.parse(l)\n")
    outFile.write("\t\tDumpBgTuple.Dump(rt)\n")
    outFile.write('\texcept ParseTreeException, e:\n')
    outFile.write('\t\tPrintParseTreeException(e)\n')
    outFile.write('\texcept SyntaxException, e:\n')
    outFile.write('\t\tPrintSyntaxException(e)\n')

    outFile.close()


def GenParser(dom):
    genName = dom.documentElement.getAttribute('NAME')
    outFile = open('%sParserBase.py' % genName,'w')
    outFile.write("import %s\n" % genName)

    outFile.write("class SyntaxException:\n")
    outFile.write("\tdef __init__(self,loc,prodNum):\n")
    outFile.write("\t\tself.loc = loc\n")
    outFile.write("\t\tself.prodNum = prodNum\n")
    outFile.write("class ParseTreeException:\n")

    outFile.write("\tdef __init__(self,loc,prodNum,errorType,errorValue,errorTraceback):\n")
    outFile.write("\t\tself.loc = loc\n")
    outFile.write("\t\tself.prodNum = prodNum\n")
    outFile.write("\t\tself.errorType = errorType\n")
    outFile.write("\t\tself.errorValue = errorValue\n")
    outFile.write("\t\tself.errorTraceback = errorTraceback\n")

    outFile.write("class %sParserBase:\n" % genName)
    outFile.write("\tdef __init__(self):\n")
    outFile.write("\t\tself.initialize()\n")
    outFile.write("\tdef initialize(self):\n")
    outFile.write("\t\tself.prodNum = -1\n")
    outFile.write("\t\tself.results = None\n")
    outFile.write("\t\tself.__stack = []\n")
    outFile.write("\t\t%s.cvar.g_errorOccured = 0\n" % genName)
    outFile.write("\tdef parse(self,st):\n")
    outFile.write("\t\tself.initialize()\n")
    outFile.write("\t\trt = %s.my_yyparse(self,st)\n" % genName)
    outFile.write("\t\tif %s.cvar.g_errorOccured == 1:\n" % genName)
    outFile.write("\t\t\traise SyntaxException(%s.cvar.g_errorLocation, self.prodNum)\n" % genName)
    outFile.write("\t\tif %s.cvar.g_errorOccured == 2:\n" % genName)
    outFile.write("\t\t\traise ParseTreeException(%s.cvar.g_errorLocation, self.prodNum, %s.cvar.g_errorType,%s.cvar.g_errorValue, %s.cvar.g_errorTraceback)\n" % (genName,genName,genName,genName))
    outFile.write("\t\treturn self.__stack\n")

    outFile.write("\tdef pop(self):\n")
    outFile.write("\t\tif len(self.__stack) == []:\n")
    outFile.write("\t\t\tself.raiseException('Pop with 0 stack length')\n")
    outFile.write("\t\trt = self.__stack[-1]\n")
    outFile.write("\t\tdel self.__stack[-1]\n")
    outFile.write("\t\treturn rt\n")
    outFile.write("\tdef push(self,item):\n")
    outFile.write("\t\tself.__stack.append(item)\n")
    outFile.write("\tdef empty(self):\n")
    outFile.write("\t\treturn len(self.__stack) == 0\n")
    outFile.write("\tdef size(self):\n")
    outFile.write("\t\treturn len(self.__stack)\n")
    outFile.write("\tdef raiseException(self,message):\n")
    outFile.write('\t\traise message + ": EBNF Prod Num:",self.prodNum\n')
    outFile.write("\t#------Callback methods------\n")
    outFile.write("\tdef setEbnfProductionNumber(self,num):\n")
    outFile.write("\t\tprint 'Set Prod Num to %s' % str(num)\n")
    outFile.write("\t\tself.prodNum = num\n")

    rule_sets = dom.getElementsByTagName('RULE_SET')
    for rule_set in rule_sets:
        numGen = -1
        rules = rule_set.getElementsByTagName('RULE')
        for rule in rules:
            symbols = rule.getElementsByTagName('SYMBOL')
            gen = rule.getElementsByTagName('PYTHON_CALLBACK')
            if len(gen) == 0:
                continue
            if len(symbols) > numGen:
                numGen = len(symbols)
        if numGen == -1:
            continue
        nt = rule_set.getElementsByTagName('NON_TERMINAL')[0].childNodes[0].data
        outFile.write('\tdef %s(self' % TranslatePythonKeyword(nt))
        for ctr in range(numGen):
            outFile.write(', arg%d = None' % ctr)
        outFile.write('):\n')
        outFile.write("\t\tprint '%s called with " % nt)
        for ctr in range(numGen):
            outFile.write('%s ')

        outFile.write("' % (")
        for ctr in range(numGen):
            if ctr == 0:
                outFile.write('str(arg%d)' % ctr)
            else:
                outFile.write(', str(arg%d)' % ctr)
        outFile.write(")\n")

    outFile.write('\n\n');
    outFile.write('def PrintSyntaxException(e):\n')
    outFile.write('\tprint "**************Syntax Exception ******"\n')
    outFile.write('\tprint "Syntax Exception at or near \'" + e.loc + "\' on line number %%d" %% %s.cvar.lineNum\n'%genName)
    outFile.write('\tprint "\\tException occured when processing production number %s" % str(e.prodNum) \n')

    outFile.write('def PrintParseTreeException(e):\n')
    outFile.write('\tprint "**************Exception in Python Callback******"\n')
    outFile.write('\tprint "Exception at or near \'" + e.loc + "\' on line number %%d" %% %s.cvar.lineNum\n'%genName)
    outFile.write('\tprint "\\tException occured when processing production number %s" % str(e.prodNum) \n')
    outFile.write('\tprint "Python Exception \'" + str(e.errorType) + "\'"\n')
    outFile.write('\timport traceback\n')
    outFile.write('\ttraceback.print_tb(e.errorTraceback)\n')

    outFile.write("if __name__ == '__main__':\n")
    outFile.write("\timport sys\n")
    outFile.write("\tp = %sParserBase()\n" % genName)
    outFile.write("\tif len(sys.argv)==2:\n")
    outFile.write("\t\tl = open(sys.argv[1],'r').read()\n")
    outFile.write("\telse:\n")
    outFile.write('\t\tl = raw_input(">>>")\n')
    outFile.write('\ttry:\n')
    outFile.write("\t\tp.parse(l)\n")
    outFile.write('\texcept ParseTreeException, e:\n')
    outFile.write('\t\tPrintParseTreeException(e)\n')
    outFile.write('\texcept SyntaxException, e:\n')
    outFile.write('\t\tPrintSyntaxException(e)\n')

    outFile.close()


def GenMakeFile(dom):
    genName = dom.documentElement.getAttribute('NAME')
    outFile = open('Setup.in', 'w')
    outFile.write('*shared*\n')
    outFile.write("%sc %sSwig.c %s_wrap.c %s.tab.c lex.%s.c -lfl\n" % (genName,genName,genName,genName,genName))
    outFile.close()

    os.system('cp '+g_makeConfigDir+'Makefile.pre.in Makefile.pre.in')
    outFile = open('Makefile.pre.in', 'a')
    outFile.write('\n#Rules specific to the %s parser: generated by BisonGen\n' % genName)
    outFile.write('bgclean: distclean\n')
    outFile.write('\trm -f lex.%s.c\n' % genName)
    outFile.write('\trm -f %s.py\n' % genName)
    outFile.write('\trm -f %s.tab.*\n' % genName)
    outFile.write('\trm -f %s_wrap.*\n' % genName)
    outFile.write('\trm -f *.o\n')
    outFile.write('\trm -f *.so\n')
    outFile.write('\trm -f *.pyc\n')
    outFile.write('\trm -f %s.output\n' % genName)
    outFile.write('\trm -f %sDebug\n' % genName)
    outFile.write('\trm -f %s.y\n\n' % genName)

    outFile.write("%s_wrap.c: %s.i %s.tab.h\n" % (genName,genName,genName))
    outFile.write('\tswig -python -shadow -dascii %s.i\n\n' % genName)
    outFile.write('lex.%s.c: %s.l %s.tab.h\n' % (genName,genName,genName))
    outFile.write('\tflex %s.l\n\n' % (genName))
    outFile.write('\tmv lex.yy.c lex.%s.c\n\n' % (genName))
    outFile.write("%s.tab.c %s.tab.h: %s.y\n" % (genName,genName,genName))
    outFile.write("\tbison -d %s.y\n\n" % genName)
    outFile.write("%sSwig.c: %s.tab.h\n\n" % (genName, genName))
    outFile.write("debug: %sDebug\n\n" % genName)
    outFile.write("add_debug:\n")
    outFile.write("\tbison -d -v -t %s.y\n" % genName) 
    outFile.write("\tflex -d %s.l\n\n" % (genName))
    outFile.write('\tmv lex.yy.c lex.%s.c\n\n' % (genName))
    outFile.write("%sDebug: %s.tab.c %s.tab.h lex.%s.c add_debug\n" % (genName,genName,genName,genName))
    outFile.write("\t$(CC) -o %sDebug %s.tab.c lex.%s.c -lfl -DPARSE_DEBUG\n\n" % (genName,genName,genName))
    outFile.close()

    #Make the scanner instruction file
    outFile = open('scanner.%s.txt'%(genName), 'w')
    yys_member_elem = dom.documentElement.getElementsByTagName('YYSTYPE_MEMBER')[0]
    yystype = yys_member_elem.getAttribute('TYPE')
    outFile.write('''
You will need the following C code in your scanner file.

define YYSTYPE %s
#include <stdio.h>
#include "%s.tab.h"
#include "%s.h"
#undef yywrap

The easiest way is to use FLEX and place the above along with any other
relevant C code in between %%{ %%} in the LEX definitions section.
'''%(yystype, genName, genName))
    outFile.close()
    

def GenSwigI(dom):
    genName = dom.documentElement.getAttribute('NAME')
    outFile = open('%s.i'% genName,'w')
    outFile.write('%%module %s\n' % genName)
    outFile.write('%{\n')
    outFile.write('#include "%s.tab.h"\n'%genName)
    outFile.write('#include "%sSwig.h"\n' % genName)
    outFile.write('%}\n')
    outFile.write('%typemap(python,in) PyObject *parser {\n')
    outFile.write('\t$target = $source;\n')
    outFile.write('}\n')

    outFile.write('%typemap(python,out) PyObject * {\n')
    outFile.write('\t$target = $source;\n')
    outFile.write('}\n')

    outFile.write('%%include "%sSwig.h"\n'%genName)
    outFile.write('%%include "%s.tab.h"\n'%genName)
    outFile.close()


def GenSwigC(dom):
    genName = dom.documentElement.getAttribute('NAME')
    outFile = open('%sSwig.c'% genName,'w')
    outFile.write('#include "%s.tab.h"\n' % genName)
    outFile.write("#include <stdio.h>\n")
    outFile.write("#include <math.h>\n")
    outFile.write('#include "Python.h"\n');
    outFile.write('#include "%s.h"\n'%genName)
    outFile.write('#include "%sSwig.h"\n'%genName)

    outFile.write('PyObject* g_parser;\n')
    outFile.write('char *g_str = NULL;\n')
    outFile.write('char * g_start = NULL;\n')
    outFile.write('char *g_end = NULL;\n')
    outFile.write('extern int yyparse(void);\n')
    outFile.write('extern int g_errorOccured;\n')
    outFile.write('extern char *g_errorLocation;\n')
    outFile.write('extern int lineNum;\n')

    outFile.write('#define min(a,b) (a) < (b) ? (a) : (b)\n')

    outFile.write('long my_yyparse(PyObject *parser, char *str) {\n')
    outFile.write('\tg_parser = parser;\n')
    outFile.write('\tg_str = g_start = str;\n')
    outFile.write('\tg_end = g_start + strlen(g_str);\n')
    outFile.write('\tg_errorOccured = 0;\n')
    outFile.write('\tyyparse();\n')
    outFile.write('\treturn ~g_errorOccured;\n');
    outFile.write('}\n')

    outFile.write('int my_yyinput(char *buf, int max_size) {\n')
    outFile.write('\tint n=min(max_size,g_end - g_start);\n')
    outFile.write('\tif (n > 0) {\n')
    outFile.write('\t\tmemcpy(buf,g_start,n);\n')
    outFile.write('\t\tg_start += n;\n')
    outFile.write('\t}\n')
    outFile.write('\treturn n;\n')
    outFile.write('}\n')

    outFile.close()


def GenSwigHeader(dom):
    genName = dom.documentElement.getAttribute('NAME')
    outFile = open('%sSwig.h'% genName,'w')

    outFile.write('#ifndef __%sSWIG_MODULE_H\n' % string.upper(genName))
    outFile.write('#define __%sSWIG_MODULE_H\n' % string.upper(genName))

    outFile.write('long my_yyparse(PyObject *parser,char *str);\n')

    outFile.write('char *g_errorLocation;\n')
    outFile.write('int g_errorOccured;\n')

    outFile.write('PyObject *g_errorType;\n')
    outFile.write('PyObject *g_errorValue;\n')
    outFile.write('PyObject *g_errorTraceback;\n')
    outFile.write('extern int lineNum;\n')

    outFile.write('#endif\n')


def GenHeader(dom):
    genName = dom.documentElement.getAttribute('NAME')
    outFile = open('%s.h'% genName,'w')

    outFile.write('#ifndef __%s_MODULE_H\n' % string.upper(genName))
    outFile.write('#define __%s_MODULE_H\n' % string.upper(genName))

    outFile.write('#ifndef PARSE_DEBUG\n')
    outFile.write('#include "Python.h"\n')
    outFile.write('extern PyObject* g_parser;\n')

    outFile.write('extern int g_errorOccured;\n')
    outFile.write('extern  char* g_errorLocation;\n')

    outFile.write('extern PyObject *g_errorType, *g_errorValue, *g_errorTraceback;\n')

    outFile.write('extern int yynerrs;\n')

    outFile.write('extern int my_yyinput(char *buf, int max_size);\n')
    outFile.write('#undef YY_INPUT\n')
    outFile.write('#define YY_INPUT(b,r,ms) (r = my_yyinput(b,ms))\n')
    outFile.write('#endif\n')

    outFile.write('#endif\n')
    
    outFile.close()


def GenBison(dom):
    genName = dom.documentElement.getAttribute('NAME')
    outFile = open(genName + '.y','w')
    #See if the user has thier own definition section
    defin = dom.getElementsByTagName('DEFINITION')
    outFile.write('%{\n')
    if len(defin):
        outFile.write(defin[0].childNodes[0].data)
        outFile.write('\n')

    #Add our stuff
    outFile.write('#ifdef PARSE_DEBUG\n')
    outFile.write('#include "stdarg.h"\n')
    outFile.write('void PyObject_CallMethod(int inst, char *method, char *format, ...);\n')
    outFile.write('int g_parser;\n')
    outFile.write('#else\n')
    outFile.write('#include "%s.h"\n' % genName)
    outFile.write('#endif\n')
    outFile.write('extern char *yytext;\n')
    outFile.write('int CheckError();\n')
    outFile.write('void yyerror(char *s);\n')

    #Add our stuff to the def file
    #Add yystype stuff
    yystypes = dom.getElementsByTagName('YYSTYPE_MEMBER')

    has_types = 0
    if len(yystypes) == 1:
        #The easy stuff
        outFile.write('#define YYSTYPE %s\n' % yystypes[0].getAttribute('TYPE'))
        outFile.write('%}\n')
    else:
        has_types = 1
        outFile.write('%}\n')
        outFile.write('%union {\n')
        for yType in yystypes:
            outFile.write('\t %s %s;\n' % (yType.getAttribute('TYPE'),yType.childNodes[0].data))
        outFile.write('}\n')

    #Add token stuff
    tokens = dom.getElementsByTagName('TOKEN')
    for t in tokens:
        if has_types == 1:
            outFile.write('%%token <%s> %s\n' % (t.getAttribute('TYPE'),t.childNodes[0].data))
        else:
            outFile.write('%%token %s\n' % (t.childNodes[0].data))

    #Add the prededence stuff
    precs = dom.getElementsByTagName('PRECEDENCE')
    if len(precs):
        prec = precs[0]
        for p in prec.childNodes:
            if p.nodeType != Node.ELEMENT_NODE:
                continue
            if p.tagName == 'ASSOCIATIVE':
                outFile.write('%%%s ' % string.lower(p.getAttribute('TYPE')))
                for o in p.getElementsByTagName('OPERATOR'):
                    outFile.write('%s ' % o.childNodes[0].data)
                outFile.write('\n')
            if p.tagName == 'NONASSOCIATIVE':
                outFile.write('%%nonassoc %s\n' % p.childNodes[0].data)

    #Add the type stuff
    if has_types:
        nts = dom.getElementsByTagName('NON_TERMINAL')
        for nt in nts:
            outFile.write('%%type <%s> %s\n' % (nt.getAttribute('TYPE'),nt.childNodes[0].data))

    outFile.write('%%\n')

    #The meat, add the rules
    rule_sets = dom.getElementsByTagName('RULE_SET')
    for rule_set in rule_sets:
        prodNum = rule_set.getAttribute('NAME')
        nts = rule_set.getElementsByTagName('NON_TERMINAL')
        outFile.write('%s: ' % nts[0].childNodes[0].data)
        rules = rule_set.getElementsByTagName('RULE')
        first = 1
        for rule in rules:
            if not first:
                outFile.write('\t | ');
            first = 0
            symbols = rule.getElementsByTagName('SYMBOL')
            for symbol in symbols:
                outFile.write('%s ' % symbol.childNodes[0].data)
            outFile.write('\n\t{\n')

            def writeGenerated(file,prodNum,symbols,nt):
                global g_nonTerminalList
                file.write('\tPyObject_CallMethod(g_parser,"setEbnfProductionNumber","s","%s");\n' % prodNum)
                if len(symbols) == 0:
                    file.write('\tPyObject_CallMethod(g_parser, %s, NULL);\n' % TranslatePythonKeyword(nt.childNodes[0].data))
                else:
                    typeStr = ''
                    for s in symbols:
                        t = s.getAttribute('TYPE')
                        typeStr = typeStr + t
                    file.write('\tPyObject_CallMethod(g_parser, "%s", "%s"' % (TranslatePythonKeyword(nt.childNodes[0].data),typeStr))
                    ctr = 1
                    for s in symbols:
                        if s.childNodes[0].data[0] in ['"',"'"]:
                            file.write(', "%s"' % s.childNodes[0].data[1:-1])
                        elif s.childNodes[0].data in g_nonTerminalList:
                            file.write(', "%%FT-NT%%"')
                        else:
                            file.write(', $%d' % ctr)
                        ctr = ctr + 1
                    file.write(');\n')
                file.write('\tif (CheckError() == 0) {\n')
                file.write('\t\tYYABORT;\n')
                file.write('\t\t}\n')

            codes = rule.getElementsByTagName('CODE')
            if len(codes) == 1:
                for child in codes[0].childNodes:
                    if child.nodeType != Node.ELEMENT_NODE:
                        continue
                    if child.tagName == 'PYTHON_CALLBACK':
                        writeGenerated(outFile,prodNum,symbols,nts[0])
                    if child.tagName == 'CODE_SNIPPET':
                        for c in child.childNodes:
                            outFile.write('\t' + c.data)
                        outFile.write('\n')
                
            outFile.write('\t}\n')
        outFile.write('\t;\n')
    outFile.write('%%\n')

    #User def section
    outFile.write('#ifndef PARSE_DEBUG\n')
    outFile.write('int CheckError() {\n')
    outFile.write("\tif (PyErr_Occurred() != NULL) {\n")
    outFile.write("\t\tyynerrs++;\n")
    outFile.write("\t\tg_errorOccured = 2;\n")
    outFile.write("\t\tg_errorLocation = yytext;\n")
    outFile.write("\t\tPyErr_Fetch(&g_errorType,&g_errorValue, &g_errorTraceback);\n")
    outFile.write("\t\treturn 0;\n")
    outFile.write("\t\t}\n")
    outFile.write("\t return 1;\n")
    outFile.write('}\n')
    outFile.write('#else\n')
    outFile.write('int CheckError() {\n')
    outFile.write('\t return 1;\n')
    outFile.write('}\n')

    outFile.write('void PyObject_CallMethod(int parser,char *method, char *format, ...) {\n')
    outFile.write('\tprintf("Call Method %s\n", method);\n')
    outFile.write('}\n')

    ur = dom.getElementsByTagName('USER_ROUTINE')
    genMain = 1
    genError = 1
    if len(ur):
        if ur[0].getAttribute('NO_MAIN'):
            genMain = 0
        if ur[0].getAttribute('NO_YYERROR'):
            genError = 0
    if genMain:
        outFile.write('int main() {\n')
        outFile.write('yydebug = 1;\n')
        outFile.write('\tyyparse();\n')
        outFile.write('}\n')
    outFile.write('#endif\n')

    if genError:
        outFile.write('void yyerror(char *s){\n')
        outFile.write('\t#ifdef PARSE_DEBUG\n')
        outFile.write('\tprintf("%s at or before %s...\\n", s, yytext);\n')
        outFile.write('\t#else\n')
        outFile.write('\tg_errorOccured = 1;\n')
        outFile.write('\tg_errorLocation = yytext;\n')
        outFile.write('\t#endif\n')
        outFile.write('}\n')
    if len(ur):
        outFile.write(ur[0].childNodes[0].data)
    outFile.close()


if __name__ == '__main__':
    import sys
    usage = """
Usage:

BisonGen.py [-c<config_dir>] [-m | -n] [<XML input file>]
    -c<config_dir>    Specify the configuration directory [default %s]
    -m Generate parse tree as mapping
    -n Generate parse tree as nested tuples
    """%(g_makeConfigDir)

    optlist, args = getopt.getopt(sys.argv[1:], 'c:mn')

    command_line_error = 0
    if len(args) == 0:
        command_line_error = 1
    else:
        spec_file = args[0]

    genMapping = 0
    genNestedTuple = 0

    for op in optlist:
        if op[0] == "-c":
            g_makeConfigDir = op[1]
        elif op[0] == '-m':
            genMapping = 1
        elif op[0] == '-n':
            genNestedTuple = 1
        else:
            command_line_error = 1
    if g_makeConfigDir[-1] != '/':
        g_makeConfigDir = g_makeConfigDir + '/'

    if command_line_error:
        print usage
        sys.exit(1)

    GenFiles(spec_file, genMapping, genNestedTuple)

