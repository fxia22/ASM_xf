
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

"""Mail support for twisted python.
"""

import os
import stat
import socket
import time
import md5

from twisted.protocols import pop3
from twisted.protocols import smtp
from twisted.persisted import dirdbm
from twisted.python import components
from twisted.mail import mail
from twisted.internet import defer

from twisted import cred
import twisted.cred.portal
import twisted.cred.credentials
import twisted.cred.checkers
import twisted.cred.error

INTERNAL_ERROR = '''\
From: Twisted.mail Internals
Subject: An Error Occurred

  An internal server error has occurred.  Please contact the
  server administrator.
'''

class _MaildirNameGenerator:
    """Utility class to generate a unique maildir name
    """
    n = 0
    p = os.getpid()
    s = socket.gethostname()

    def generate(self):
        self.n = self.n + 1
        t = str(int(time.time()))
        return '%s.%s_%s.%s' % (t, self.p, self.n, self.s)

_generateMaildirName = _MaildirNameGenerator().generate

def initializeMaildir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
        for subdir in ['new', 'cur', 'tmp', '.Trash']:
            os.mkdir(os.path.join(dir, subdir))
        for subdir in ['new', 'cur', 'tmp']:
            os.mkdir(os.path.join(dir, '.Trash', subdir))
        # touch
        open(os.path.join(dir, '.Trash', 'maildirfolder'), 'w').close()


class AbstractMaildirDomain:
    """Abstract maildir-backed domain.
    """

    def __init__(self, service, root):
        """Initialize.
        """
        self.root = root

    def userDirectory(self, user):
        """Get the maildir directory for a given user

        Override to specify where to save mails for users.
        Return None for non-existing users.
        """
        return None

    ##
    ## IDomain
    ##
    def exists(self, user):
        """Check for existence of user in the domain
        """
        if self.userDirectory(user.dest.local) is not None:
            return defer.succeed(user)
        else:
            return defer.fail(smtp.SMTPBadRcpt(user))

    def startMessage(self, user):
        """Save a message for a given user
        """
        name, domain = user.dest.local, user.dest.domain
        dir = self.userDirectory(name)
        fname = _generateMaildirName()
        filename = os.path.join(dir, 'tmp', fname)
        fp = open(filename, 'w')
        fp.write("Delivered-To: %(name)s@%(domain)s\n" % vars())
        return mail.FileMessage(fp, filename, os.path.join(dir, 'new', fname))


class MaildirMailbox(pop3.Mailbox):
    """Implement the POP3 mailbox semantics for a Maildir mailbox
    """

    def __init__(self, path):
        """Initialize with name of the Maildir mailbox
        """
        self.path = path
        self.list = []
        self.deleted = {}
        initializeMaildir(path)
        for name in ('cur', 'new'):
            for file in os.listdir(os.path.join(path, name)):
                self.list.append(os.path.join(path, name, file))

    def listMessages(self, i=None):
        """Return a list of lengths of all files in new/ and cur/
        """
        if i is None:
            ret = []
            for mess in self.list:
                if mess:
                    ret.append(os.stat(mess)[stat.ST_SIZE])
                else:
                    ret.append(0)
            return ret
        return os.stat(self.list[i])[stat.ST_SIZE]

    def getMessage(self, i):
        """Return an open file-pointer to a message
        """
        return open(self.list[i])

    def getUidl(self, i):
        """Return a unique identifier for a message

        This is done using the basename of the filename.
        It is globally unique because this is how Maildirs are designed.
        """
        # Returning the actual filename is a mistake.  Hash it.
        base = os.path.basename(self.list[i])
        return md5.md5(base).hexdigest()

    def deleteMessage(self, i):
        """Delete a message

        This only moves a message to the .Trash/ subfolder,
        so it can be undeleted by an administrator.
        """
        trashFile = os.path.join(
            self.path, '.Trash', 'cur', os.path.basename(self.list[i])
        )
        os.rename(self.list[i], trashFile)
        self.deleted[self.list[i]] = trashFile
        self.list[i] = 0

    def undeleteMessages(self):
        """Undelete any deleted messages it is possible to undelete

        This moves any messages from .Trash/ subfolder back to their
        original position, and empties out the deleted dictionary.
        """
        for (real, trash) in self.deleted.items():
            try:
                os.rename(trash, real)
            except OSError, (err, estr):
                import errno
                # If the file has been deleted from disk, oh well!
                if err != errno.ENOENT:
                    raise
                # This is a pass
            else:
                try:
                    self.list[self.list.index(0)] = real
                except ValueError:
                    self.list.append(real)
        self.deleted.clear()


class StringListMailbox:
    __implements__ = (pop3.IMailbox,)
    
    def __init__(self, msgs):
        self.msgs = msgs
    
    def listMessages(self, i=None):
        if i is None:
            return map(len, self.msgs)
        return len(self.msgs[i])
    
    def getMessage(self, i):
        return StringIO.StringIO(self.msgs[i])
    
    def getUidl(self, i):
        return md5.new(self.msgs[i]).hexdigest()
    
    def deleteMessage(self, i):
        pass
    
    def undeleteMessages(self):
        pass
    
    def sync(self):
        pass
     
class MaildirDirdbmDomain(AbstractMaildirDomain):
    """A Maildir Domain where membership is checked by a dirdbm file
    """
    
    __implements__ = (cred.portal.IRealm,)
    
    portal = None
    _credcheckers = None
    
    def __init__(self, service, root, postmaster=0):
        """Initialize

        The first argument is where the Domain directory is rooted.
        The second is whether non-existing addresses are simply
        forwarded to postmaster instead of outright bounce

        The directory structure of a MailddirDirdbmDomain is:

        /passwd <-- a dirdbm file
        /USER/{cur,new,del} <-- each user has these three directories
        """
        AbstractMaildirDomain.__init__(self, service, root)
        dbm = os.path.join(root, 'passwd')
        if not os.path.exists(dbm):
            os.makedirs(dbm)
        self.dbm = dirdbm.open(dbm)
        self.postmaster = postmaster

    def userDirectory(self, name):
        """Get the directory for a user

        If the user exists in the dirdbm file, return the directory
        os.path.join(root, name), creating it if necessary.
        Otherwise, returns postmaster's mailbox instead if bounces
        go to postmaster, otherwise return None
        """
        if not self.dbm.has_key(name):
            if not self.postmaster:
                return None
            name = 'postmaster'
        dir = os.path.join(self.root, name)
        if not os.path.exists(dir):
            initializeMaildir(dir)
        return dir

    ##
    ## IDomain
    ##
    def addUser(self, user, password):
        self.dbm[user] = password
        # Ensure it is initialized
        self.userDirectory(user)
    
    def getCredentialsCheckers(self):
        if self._credcheckers is None:
            self._credcheckers = [DirdbmDatabase(self.dbm)]
        return self._credcheckers

    ##
    ## IRealm
    ##
    def requestAvatar(self, avatarId, mind, *interfaces):
        if pop3.IMailbox not in interfaces:
            raise NotImplementedError("No interface")
        if avatarId == cred.checkers.ANONYMOUS:
            mbox = StringListMailbox([INTERNAL_ERROR])
        else:
            mbox = MaildirMailbox(os.path.join(self.root, avatarId))
                
        return (
            pop3.IMailbox,
            mbox,
            lambda: None
        )

class DirdbmDatabase:
    __implements__ = (cred.checkers.ICredentialsChecker,)
    
    credentialInterfaces = (cred.credentials.IUsernamePassword,)
    
    def __init__(self, dbm):
        self.dirdbm = dbm
    
    def requestAvatarId(self, credentials):
        if credentials.username in self.dirdbm:
            if credentials.checkPassword(self.dirdbm[credentials.username]):
                return credentials.username
        raise cred.error.UnauthorizedLogin()
