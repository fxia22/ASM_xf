# Twisted, the Framework of Your Internet
# Copyright (C) 2001-2002 Matthew W. Lefkowitz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
"""wxPython support for Twisted.

To use::

    | # given a wxApp instance called myWxAppInstance:
    | from twisted.internet import wxsupport
    | wxsupport.install(myWxAppInstance)
    
Use Twisted's APIs for running and stopping the event loop, don't use
wxPython's methods.

API Stability: stable

Maintainer: U{Itamar Shtull-Trauring<mailto:twisted@itamarst.org>}
"""

# wxPython imports
from wxPython.wx import wxApp

# twisted imports
from twisted.internet import reactor


class wxRunner:
    """Make sure GUI events are handled."""
    
    def __init__(self, app):
        self.app = app
        
    def run(self):
        """
        Execute pending WX events followed by WX idle events and
        reschedule.
        """
        # run wx events
        while self.app.Pending():
            self.app.Dispatch()
        
        # run wx idle events
        self.app.ProcessIdle()
        reactor.callLater(0.02, self.run)


def install(app):
    """Install the wxPython support, given a wxApp instance"""
    runner = wxRunner(app)
    reactor.callLater(0.02, runner.run)


__all__ = ["install"]
