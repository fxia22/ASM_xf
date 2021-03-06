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
"""\"I'm Feeling Lucky\" with U{Google<http://google.com>}.
"""
import urllib
from twisted.internet import protocol, reactor, defer
from twisted.protocols import http

class GoogleChecker(http.HTTPClient):

    def connectionMade(self):
        self.sendCommand('GET', self.factory.url)
        self.sendHeader('Host', self.factory.host)
        self.sendHeader('User-Agent', self.factory.agent)
        self.endHeaders()

    def handleHeader(self, key, value):
        key = key.lower()
        if key == 'location':
            self.factory.gotLocation(value)

    def handleStatus(self, version, status, message):
        if status != '302':
            self.factory.noLocation(ValueError("bad status"))

    def handleEndHeaders(self):
        self.factory.noLocation(ValueError("no location"))

    def handleResponsePart(self, part):
        pass

    def handleResponseEnd(self):
        pass

    def connectionLost(self, reason):
        self.factory.noLocation(reason)


class GoogleCheckerFactory(protocol.ClientFactory):

    protocol = GoogleChecker

    def __init__(self, words):
        self.url = ('/search?q=%s&btnI=%s' %
	            (urllib.quote_plus(' '.join(words)),
	             urllib.quote_plus("I'm Feeling Lucky")))
        self.agent="Twisted/GoogleChecker"
        self.host = "www.google.com"
        self.deferred = defer.Deferred()

    def clientConnectionFailed(self, _, reason):
        self.noLocation(reason)

    def gotLocation(self, location):
        if self.deferred:
            self.deferred.callback(location)
            self.deferred = None

    def noLocation(self, error):
        if self.deferred:
            self.deferred.errback(error)
            self.deferred = None


def checkGoogle(words):
    """Check google for a match.

    @returns: a Deferred which will callback with a URL or errback with a
        Failure.
    """
    factory = GoogleCheckerFactory(words)
    reactor.connectTCP('www.google.com', 80, factory)
    return factory.deferred
