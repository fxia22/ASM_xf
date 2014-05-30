#!/usr/bin/python -O
#
# A fast replacement for xmlrpclib
#
#


import _xmlrpc


# begin by importing all available functions
#
from xmlrpclib import *


# override xmlrpclib classes with _xmlrpc alternatives
#
Boolean	= _xmlrpc.boolean
True = Boolean(1)
False = Boolean(0)
DateTime = _xmlrpc.dateTime
Binary = _xmlrpc.base64


# override the Marshaller class with a (much) simpler version
#
class Marshaller:
	def __init__(self):
			pass

	def dumps(self, values):
		if ((isinstance(values, Fault))
		or  (isinstance(values, Fault))):
			d = { 'faultString' : values.faultString,
				  'faultCode' : values.faultCode }
			return ('<fault>\n%s</fault>\n' % _xmlrpc.encode(d))
		else:
			l = ['<params>\n']
			for item in values:
				l.append('\t<param>\n\t\t')
				l.append(_xmlrpc.encode(item))
				l.append('\n\t</param>\n')
			l.append('</params>\n')
			return string.join(l, '')


# override the Marshaller class with a (much) faster version
#
class Parser:
	def __init__(self, target):
		self.result = None
		self.target = target
		self.file = StringIO()

	def feed(self, s):
		self.file.write(s)

	def close(self):
		v = self.file.getvalue()
		self.target.set_data(v)


# ensure that we use our fast parser
#
FastParser = Parser


# override the Marshaller class with a (much) faster version
#
class Unmarshaller:
	def __init__(self):
		self.data = None
		self.method = None
		self.value = None

	def set_data(self, data):
		self.data = data

	def close(self):
		s = string.lstrip(self.data)
		if s[:7] == '<value>':
			self.value = _xmlrpc.decode(data)
		elif ((s[:21] == "<?xml version='1.0'?>")
		or    (s[:21] == '<?xml version="1.0"?>')):
			s = string.lstrip(s[21:])
			if s[:16] == '<methodResponse>':
				try:
					s = ("HTTP/1.0 200 OK\r\n"
					     "Content-length: %d\r\n\r\n"
					     "%s" % (len(self.data),self.data))
					self.value = _xmlrpc.parseResponse(s)[0]
				except _xmlrpc.fault:
					v = sys.exc_value
					raise Fault(v.faultCode, v.faultString)
			elif s[:12] == '<methodCall>':
				(self.method, self.value) = _xmlrpc.parseCall(self.data)
		if self.value == None:
			raise TypeError, "unrecognized data: %.40s..." % s
		return self.value

	def getmethodname(self):
		return self.method


if __name__ == "__main__":
	server = Server('http://localhost:23456')
	print server
	print server.echo('blah')
