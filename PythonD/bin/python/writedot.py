#!python


# $Id: writedot.py,v 1.4 2003/03/27 09:54:57 jfasch Exp $

from libconfix.repo import ModuleRepository
from libconfix.depgraph import DependencyGraph
from libconfix.error import Error
from libconfix.helper_automake import automake_name
import sys

def write_graph(depgraph, name):

    lines = []

    lines.append('digraph '+name+' {')

    # nodes

    for n in depgraph.nodes():
        lines.append('  '+automake_name('_'.join(n.module().name()))+';')

    lines.append('')

    # edges

    for n in depgraph.nodes():
        for (succnode, reasons) in n.successors():
            lines.append('  '+automake_name('_'.join(n.module().name()))+' -> '+automake_name('_'.join(succnode.module().name()))+';')

    lines.append('}')

    return lines


def main():
    try:
        repo = ModuleRepository(sys.argv[1])
        depgraph = DependencyGraph(repo.modules())
        print '\n'.join(write_graph(depgraph, 'test'))

    except Error, e:
        print `e`

if __name__ == "__main__":
    main()


