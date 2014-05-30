#!/usr/bin/python
#
# A wrapper for the python module _xmlrpc (which was written in C)
#
# Copyright (C) 2001, Shilad Sen, Sourcelight Technologies, Inc.
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307
# 
# The author can be reached at:
#
# shilad.sen@sourcelight.com
#
# Shilad Sen
# Sourcelight Technologies, Inc.
# 906 University Place, Suite B-211
# Evanston, IL 60201
# 
# Thanks to Chris Jensen for the windows port and Pat Szuta for DateTime
# and Base64 objects.
#
#


import sys
import _xmlrpc


VERSION		= _xmlrpc.VERSION
LIBRARY		= _xmlrpc.LIBRARY

ACT_INPUT	= _xmlrpc.ACT_INPUT
ACT_OUTPUT	= _xmlrpc.ACT_OUTPUT
ACT_EXCEPT	= _xmlrpc.ACT_EXCEPT

ONERR_KEEP_DEF	= _xmlrpc.ONERR_KEEP_DEF
ONERR_KEEP_WORK	= _xmlrpc.ONERR_KEEP_WORK

DATE_FORMAT_US		= _xmlrpc.DATE_FORMAT_US
DATE_FORMAT_EUROPE	= _xmlrpc.DATE_FORMAT_EUROPE


# An xmlrpc server object
#
# addMethods(dict):
#		"Registers" commands.  Commands take a dictionary where
#		keys are command names and values are the functions to call.
#		Each function must take 4 args (serv, src, uri, method, params)
#		and return the value to be returned to the client.  If an error
#		is raised, a fault response is created, and the client will (in
#		this client implementation) raise the same error.  Note that the
#		the server can delay responding until a later time by raising
#		a xmlrpc.postpone error.  See queueResponse and queueFault.
#
# activeFds():
#		Returns a 3-tuple of the active file descriptor sets for
#		They are: (input_fds, output_fds, exception_fds)
#
# bindAndListen(port, queue=DEF_QUEUE):
#		Bind the server to a port and start listening.  This function
#		takes the port to bind to and an optional queue size.
#
# setOnErr(onErr):
#		Set an error handler for server errors.  (For example, for bad
#		requests).  Each error handler should take the server and the
#		source that caused the error.  Error handlers must return an
#		integer, that is composed of the following values bitwise
#		or'ed together:
#		ONERR_KEEP_DEF:		do default error handling
#					(consists of printing traceback and
#					dropping the client)
#		ONERR_KEEP_WORK:	don't raise this exception any higher
#
# work(timeout=-1.0):
#		Process requests for some period of time
#		All internal errors (such as bad requests) are raised here.
#		You should set an error handler using server.setOnErr() if
#		this is not your desired behavior
#
# setFdAndListen(port, queue=5):
#		The same as bindAndListen, but uses a supplied socket fd.
#		Useful mainly for inetd servers inheriting a socket through
#		stdin.
#
# setAuth(authFunc):
#		Set a handler used for basic authentication.  The handler
#		will get three arguments: (uri, name, password) and return
#		a two-tuple of a 1 or 0 (1 indicating success) and the
#		domain the authentication should apply to.  Note that the
#		domain is not currently used.
#
# addSource(src):
#		Monitor a source into the server's file descriptor event loop.
#
# delSource(src):
#		Remove a source from the server's file descriptor event loop.
#
# queueResponse(src, result):
#		This function is only useful if the response has been delayed
#		by raising a xmlrpc.postpone exception.  This function will
#		complete the response to the given client (source).
#
# queueFault(src, faultCode, faultString):
#		Same as queueResponse but raises a fault.
#
class server:
	def __init__(self):
		self._o = _xmlrpc.server()
		self.comtab = {}

	def addMethods(self, dict):
		d = {}
		for (name, func) in dict.items():
			d[name] = self.dispatch
			self.comtab[name] = func
		self._o.addMethods(d)

	def dispatch(self, serv, src, uri, method, params):
		return self.comtab[method](self, src, uri, method, params)

	def bindAndListen(self, port, queue=5):
		self._o.bindAndListen(port, queue)

	def close(self):
		self._o.close()

	def setFdAndListen(self, fd, queue=5):
		self._o.setFdAndListen(fd, queue)

	def work(self, timeout=-1.0):
		self._o.work(timeout)

	def exit(self):
		self._o.exit()

	def activeFds(self):
		return self._o.activeFds()

	def setAuth(self, authFunc):
		self._o.setAuth(authFunc)

	def setOnErr(self, onErr):
		self._o.setOnErr(onErr)

	def addSource(self, src):
		self._o.addSource(src._o)

	def delSource(self, src):
		self._o.delSource(src._o)

	def queueResponse(self, src, response):
		self._o.queueResponse(src, response)

	def queueFault(self, src, faultCode, faultString):
		self._o.queueFault(src, faultCode, faultString)

# An xmlrpc client class
#
# activeFds():
#		Returns a 3-tuple of the active file descriptor sets for
#		They are: (input_fds, output_fds, exception_fds)
#
# close():
#		Free any file descriptors associated with the client
#
# execute(method, params, timeout=-1.0):
#		Execute a command on a remote host that has been connected to.
#		If the server generates a fault response, an exception is
#		raised.
#
# nbExecute(method, params, pyfunc, extArgs):
#		Queue up a command for execution when "work()" is called.
#
# setOnErr(onErr):
#		Set an error handler for internal client errors (i.e. read
#		failed).  This is only if you use nbExecute.  Each error
#		handler should take the server and the source that caused the
#		error.  Error handlers must return an integer that is composed
#		of the following values bitwise or'ed together:
#		ONERR_KEEP_DEF:		do default error handling
#					(consists of printing traceback and
#					dropping the client)
#		ONERR_KEEP_WORK:	don't raise this exception any higher
#
# work(timeout=-1.0):
#		Process requests for some period of time
#		All internal errors (such as bad requests) are raised here.
#		You should set an error handler using client.setOnErr() if
#		this is not your desired behavior
#
class client:
	def __init__(self, host, port, url='/', serv=None):
		if serv:
			self._o = _xmlrpc.clientFromServer(
				host, port, url, serv._o)
		else:
			self._o = _xmlrpc.client(host, port, url)

	def activeFds(self):
		return self._o.activeFds()

	def close(self):
		self._o.close()

	def execute(self, method, params, timeout=-1.0, name=None, passw=None):
		return self._o.execute(method, params, timeout, name, passw)

	def fdState(self):
		return self._o.fdState()

	def nbExecute(self, method, params, pyfunc,
	              extArgs=None, name=None, passw=None):
		self._o.nbexecute(method, params, self.nbDispatch,
				(pyfunc, extArgs), name, passw)

	def nbDispatch(self, src, response, (pyfunc, extArgs)):
		pyfunc(self, response, extArgs)

	def work(self, timeout=-1.0):
		self._o.work(timeout)

	def setOnErr(self, onErr):
		self._o.setOnErr(onErr)


# An xmlrpc source.  This is not documented yet.
#
# setOnErr(onErr):
#		Set an error handler for server errors.  (For example, for bad
#		requests).  Each error handler should take the server and the
#		source that caused the error.  Error handlers must return an
#		integer, that is composed of the following values bitwise
#		or'ed together:
#		ONERR_KEEP_DEF:		do default error handling
#					(consists of printing traceback and
#					dropping the client)
#		ONERR_KEEP_WORK:	don't raise this exception any higher
#
class source:
	def __init__(self, fd):
		self._o = _xmlrpc.source(fd)

	def getDesc(self):
		return self._o.getDesc()

	def setDesc(self, desc):
		self._o.setDesc(desc)

	def setOnErr(self, onErr):
		self._o.setOnErr(onErr)

	def setCallback(self, func, actions, params):
		self._o.setCallback(self.marshaller, actions, params)
		self._func = func

	def marshaller(self, src, actions, args):
		return self._func(self, actions, args)


# module wide definitions
#
def setLogLevel(level):
	_xmlrpc.setLogLevel(level)

def setLogger(file):
	_xmlrpc.setLogger(file)

def getDateFormat():
	return _xmlrpc.getDateFormat()

def setDateFormat(format):
	_xmlrpc.setDateFormat(format)


# boolean data type; constructor takes 0 or 1; value can be used in logic exp
#
boolean = _xmlrpc.boolean
booleanType = type(boolean(0))


# dateTime data type; constructor takes 6 tuple
#
dateTime = _xmlrpc.dateTime
dateTimeType = type(dateTime(1,1,1,1,1,1))


# base64 data type; constructor takes binary sting
#
base64 = _xmlrpc.base64
base64Type = type(base64(''))


# fault data type
#
fault = _xmlrpc.fault


# A postpone error can be raised by a server's handler function to notify
# the client that a response will be returned LATER
#
postpone = _xmlrpc.postpone


# xml encode an xmlrpc data value
#
def encode(value):
	return _xmlrpc.encode(value)


# decode xml representing an xmlrpc data value
# returns a tuple of the value an any unused portion of the xml string
#
def decode(xml):
	return _xmlrpc.decode(xml)


# build a string representing a xmlrpc request
# method must be a string which is the name of the remote function
# params must be a sequence of some sort
# addInfo is a dictionary of additional header information
#
def buildRequest(uri, method, params, addInfo={}):
	return _xmlrpc.buildRequest(uri, method, params, addInfo)


# build a string representing a xmlrpc response
# result is the result object to be returned to the client
# addInfo is a dictionary of additional header information
#
def buildResponse(result, addInfo={}):
	return _xmlrpc.buildResponse(result, addInfo)


# build a string representing a xmlrpc fault
# errCode is an integer representing the error
# errStr is a string representing the error
# addInfo is a dictionary of additional header information
#
def buildFault(errCode, errStr, addInfo={}):
	return _xmlrpc.buildFault(errCode, errStr, addInfo)


# parse a string representing a xmlrpc response
# a tuple of the result and any additional header info are included
# if a fault page is parsed, a corresponding exception is raised
#
def parseResponse(response):
	return _xmlrpc.parseResponse(response)


# parse a string representing a xmlrpc request
# a tuple of the method name, params, and additional header info are included
#
def parseRequest(request):
	return _xmlrpc.parseRequest(request)
