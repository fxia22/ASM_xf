# Twisted, the Framework of Your Internet
# Copyright (C) 2003 Matthew W. Lefkowitz
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

"""
Serial port support for Windows.

Requires PySerial and win32all, and needs to be used with win32event
reactor.

This code probably works but is currently untested by the maintainers.
"""

# system imports
import os
import serial
from serial import PARITY_NONE, PARITY_EVEN, PARITY_ODD
from serial import STOPBITS_ONE, STOPBITS_TWO
from serial import FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
import win32file, win32event

# twisted imports
from twisted.protocols import basic
from twisted.internet import abstract
from twisted.python import log

# sibling imports
from serialport import BaseSerialPort


class SerialPort(BaseSerialPort, abstract.FileDescriptor):
    """A select()able serial device, acting as a transport."""

    connected = 1

    def __init__(self, protocol, deviceNameOrPortNumber, reactor, 
        baudrate = 9600, bytesize = EIGHTBITS, parity = PARITY_NONE,
        stopbits = STOPBITS_ONE, xonxoff = 0, rtscts = 0):
        self._serial = serial.Serial(deviceNameOrPortNumber, baudrate=baudrate,
                                     bytesize=bytesize, parity=parity,
                                     stopbits=stopbits, timeout=None,
                                     xonxoff=xonxoff, rtscts=rtscts)
        self.flushInput()
        self.flushOutput()
        self.reactor = reactor
        self.protocol = protocol
        self.outQueue = []
        self.closed = 0
        self.closedNotifies = 0
        self.writeInProgress = 0
        
        self.protocol = protocol
        self.protocol.makeConnection(self)
        self._overlappedRead = win32file.OVERLAPPED()
        self._overlappedRead.hEvent = win32event.CreateEvent(None, 0, 0, None)
        self._overlappedWrite = win32file.OVERLAPPED()
        self._overlappedWrite.hEvent = win32event.CreateEvent(None, 0, 0, None)
        
        self.reactor.addEvent(self._overlappedRead.hEvent, self, self.serialReadEvent)
        self.reactor.addEvent(self._overlappedWrite.hEvent, self, self.serialWriteEvent)

        flags, comstat = win32file.ClearCommError(self._serial.hComPort)
        rc, self.read_buf = win32file.ReadFile(self._serial.hComPort,
                                               win32file.AllocateReadBuffer(1),
                                               self._overlappedRead)

    def serialReadEvent(self):
        #get that character we set up
        n = win32file.GetOverlappedResult(self._serial.hComPort, self._overlappedRead, 0)
        if n:
            first = str(self.read_buf[:n])
            #now we should get everything that is already in the buffer
            flags, comstat = win32file.ClearCommError(self._serial.hComPort)
            rc, buf = win32file.ReadFile(self._serial.hComPort,
                                         win32file.AllocateReadBuffer(comstat.cbInQue),
                                         self._overlappedRead)
            n = win32file.GetOverlappedResult(self._serial.hComPort, self._overlappedRead, 1)
            #handle all the received data:
            self.protocol.dataReceived(first + str(buf[:n]))

        #set up next one
        rc, self.read_buf = win32file.ReadFile(self._serial.hComPort,
                                               win32file.AllocateReadBuffer(1),
                                               self._overlappedRead)

    def write(self, data):
        if self.writeInProgress:
            self.outQueue.append(data)
        else:
            self.writeInProgress = 1
            win32file.WriteFile(self._serial.hComPort, data, self._overlappedWrite)

    def serialWriteEvent(self):
        try:
            dataToWrite = self.outQueue.pop(0)
        except IndexError:
            self.writeInProgress = 0
            return
        else:
            win32file.WriteFile(self._serial.hComPort, dataToWrite, self._overlappedWrite)
    
    def connectionLost(self, reason):
        self.reactor.removeEvent(self._overlappedRead.hEvent)
        self.reactor.removeEvent(self._overlappedWrite.hEvent)
        abstract.FileDescriptor.connectionLost(self, reason)
        self._serial.close()
