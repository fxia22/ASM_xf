#!python


# Copyright (C) 2002 Salomon Automation
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# $Id: confix.py,v 1.60 2003/04/02 10:01:40 lmjohns3 Exp $

import sys
import os

import libconfix.const
import libconfix.todo
import libconfix.args

from libconfix.error import Error

def main():
    CONFIGFILES = libconfix.const.ARG_CONFIGFILES
    PROFILE = libconfix.const.ARG_PROFILE

    try:
        # bootstrap (:-) the args first time, only to get configfile
        # and profile name.
        tmp_todo = []
        confargs = libconfix.args.defaults()
        def_config = confargs[CONFIGFILES][:]
        confargs.update(libconfix.args.getopts(tmp_todo))

        # using update() on a dictionary replaces elements with the new values.
        # we need to prepend a list (of config files, in this case) to the old
        # list.
        confargs[CONFIGFILES] = def_config + confargs[CONFIGFILES]

        confargs = libconfix.args.subst_path(confargs)

        # second time, now for real.
        the_todo = []
        the_args = libconfix.args.defaults()
        the_args.update(\
            libconfix.args.conffile(confargs[CONFIGFILES], confargs[PROFILE]))
        the_args.update(libconfix.args.getopts(the_todo))
        the_args.update(libconfix.args.postprocess(the_args))
        the_args = libconfix.args.subst_path(the_args)

        # tell 'em what todo.
        libconfix.todo.TODO = the_todo
        libconfix.todo.ARGS = the_args

        # normally todo failures will throw exceptions, but this is in here just
        # as a safety measure.
        if libconfix.todo.todo():
            sys.exit(1)

    except Error, e:
        print `e`
        sys.exit(1)

if __name__ == "__main__":
    main()
