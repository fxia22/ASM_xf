from mx.TextTools.Examples.HTML import *
from mx.TextTools.Constants.TagTables import *

# tag()
print 'Tagging Engine:'
text = open('../Doc/mxTextTools.html').read()
print ' parsing HTML documentation...'
utext = upper(text)
result, taglist, nextindex = tag(utext,htmltable)
assert result == 1
print ' done.'

print ' testing some tag table semantics...'
table = ((None,Word,'Word'),)
assert tag('Word',table)[0] == 1
assert tag('word',table)[0] == 0
assert tag('xyz',table)[0] == 0

table = ((None,Word,'Word',MatchFail),)
assert tag('Word',table)[0] == 1
assert tag('word',table)[0] == 0
assert tag('xyz',table)[0] == 0

table = ((None,Word,'Word',MatchOk),)
assert tag('Word',table)[0] == 1
assert tag('word',table)[0] == 1
assert tag('xyz',table)[0] == 1

table = ((None,Word,'Word',MatchOk,MatchFail),)
assert tag('Word',table)[0] == 0
assert tag('word',table)[0] == 1
assert tag('xyz',table)[0] == 1

print ' done.'

# splitat()
print 'splitat()'
assert splitat('Hello','l') == ('He', 'lo')
assert splitat('Hello','l',2) == ('Hel', 'o')
assert splitat('Hello','l',-1) == ('Hel', 'o')
assert splitat('Hello','l',-2) == ('He', 'lo')

# suffix
print 'suffix()'
assert suffix('abc.html/',('.htm','abc','.html','/'),0,3) == 'abc'
assert suffix('abc.html/',('.htm','abc','.html','/'),0,4) == None
assert suffix('abc.html/',('.htm','abc','.html','/'),0,8) == '.html'

# prefix
print 'prefix()'
assert prefix('abc.html/',('.htm','abc','.html','/'),0,3) == 'abc'
assert prefix('abc.html/',('.htm','abc','.html','/'),1,4) == None
assert prefix('abc.html/',('.htm','abc','.html','/'),3,9) == '.htm'

# join
print 'join()'
assert join(('a','b','c')) == 'abc'
assert join(['a','b','c']) == 'abc'
assert join(('a','b','c'),' ') == 'a b c'
assert join(['a','b','c'],' ') == 'a b c'
assert join((('abc',0,1),('abc',1,2),('abc',2,3))) == 'abc'
assert join((('abc',0,1),'b',('abc',2,3))) == 'abc'
assert join((('abc',0,3),)) == 'abc'

# isascii
print 'isascii()'
assert isascii('abc') == 1
assert isascii('abcäöü') == 0
assert isascii('abcäöüdef') == 0
assert isascii('.,- 1234') == 1
try:
    unicode
except NameError:
    pass
else:
    assert isascii(unicode('abc')) == 1
    assert isascii(unicode('abcäöü', 'latin-1')) == 0
    assert isascii(unicode('abcäöüdef', 'latin-1')) == 0
    assert isascii(unicode('.,- 1234')) == 1

# XXX Do some more tests...

print
print 'Works.'
