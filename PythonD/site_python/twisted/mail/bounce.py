# -*- test-case-name: twisted.test.test_bounce -*-
#
# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
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

import rfc822, string, time, os

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from twisted.protocols import smtp

def generateBounce(message, failedFrom, failedTo, transcript=''):
    if not transcript:
        transcript = '''\
I'm sorry, the following address has permanent errors: %(failedTo)s.
I've given up, and I will not retry the message again.
''' % vars()
    boundary = "%s_%s_%s" % (time.time(), os.getpid(), 'XXXXX')
    fp = StringIO.StringIO()
    failedAddress = rfc822.AddressList(failedTo)[0][1]
    failedDomain = string.split(failedAddress, '@', 1)[1]
    fp.write('From: postmaster@'+failedDomain+'\n')
    fp.write('To: '+failedFrom+'\n')
    fp.write('Subject: Returned Mail: see transcript for details\n')
    fp.write('Message-ID: %s' % (smtp.messageid(uniq='bounce'),))
    fp.write('Content-Type: multipart/report; report-type=delivery-status; boundary="%s"\n' % boundary)
    fp.write('\n')
    fp.write('--%s\n' % boundary)
    fp.write('\n')
    fp.write(transcript)
    fp.write('\n')
    fp.write('--%s\n' % boundary)
    fp.write('Content-Type: message/delivery-status')
    fp.write('\n')
    fp.write('Arrival-Date: %s\n' % time.ctime(time.time()))
    fp.write('\n')
    fp.write('Final-Recipient: RFC822; ' + failedTo + '\n')
    orig = message.tell()
    message.seek(2, 0)
    sz = message.tell()
    message.seek(0, orig)
    if sz > 10000:
        while 1:
            line = message.readline()
            if len(line)<=1:
                break
            fp.write(line)
    else:
        fp.write(message.read())
    return '', failedFrom, fp.getvalue()
