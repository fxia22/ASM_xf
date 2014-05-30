#!/usr/bin/env python

"""
$Id: py2wsdl.py,v 1.10 2003/10/10 05:36:34 uid1057114584 Exp $

Container module for all Python->WSDL conversion.

Requires wsdllib in PYTHONPATH.
"""


import sys, types, inspect
import epydoc.objdoc
from epydoc.markup import epytext
from xml.dom.ext import PrettyPrint

import wsdllib
import wsdlutil


DEF_BASE_URI = "http://au-dev-0001.flow.com.au:9876/"

DEF_NAMESPACES = (
    ("xmlns", "http://schemas.xmlsoap.org/wsdl/"),
    #("xmlns:soap", "http://schemas.xmlsoap.org/wsdl/soap/"),
    ("xmlns:xsd", "http://www.w3.org/2001/XMLSchema"),
    ("xmlns:SOAP-ENC", "http://schemas.xmlsoap.org/soap/encoding/"),
)


class Generator:
    """
    Generator base class.  All subclasses must override generate().
    It is likely that subclasses will have different function signatures
    for their generate() methods.

    Note:
    Accessing the WSDL content in the __init__ can be hazardous to
    your health.  If a streaming parser (eg, SAX) is being used the WSDL
    will be validated as the instance is created.  This could result in
    a parse exception that would, in turn, result in failure to create
    the instance.  Not goot.
    """
    def __init__(self):
        pass

    def generate(self):
        raise NotImplementedError, "generate()"


class MessageGenerator(Generator):
    """
    Base class for the various messages.  All subclassees must override
    the generate() method.

    Using the supplied package and WSDL, subclasses should generate
    and return a valid message instance.  A message can be thought
    of as a WSDL abstraction of the data supplied to or received from
    an operation.
    """
    def __init__(self, package, wsdl, debug=0):
        self.package = package
        self.wsdl = wsdl
        self.debug = debug
        Generator.__init__(self)


class RequestMessageGenerator(MessageGenerator):
    def generate(self, classInstance, methodInstance):
        """
        Creates a request message, where the name is of the form:
        
            <class name>.<method name>.request
        
        Populates the request message with the parts, including their
        names, types, and documentation.  Returns the request message
        instance.
        """
        docmap = epydoc.objdoc.DocMap()
        uid = epydoc.objdoc.make_uid(methodInstance)
        docmap.add_one(uid)
        epyFunc = docmap.popitem()[1]
        requestName = "%s.%s.request" % (classInstance.__name__,
            methodInstance.__name__)
        requestMessage = self.wsdl.messages.addMessage(requestName)
        populateRequestMessageFromEpyFunc(requestMessage, epyFunc)
        return requestMessage


class ResponseMessageGenerator(MessageGenerator):
    def generate(self, classInstance, methodInstance):
        """
        Creates a response message, where the name is of the form:
        
            <class name>.<method name>.response
        
        The WSDL for the response messages will always be of the form:
        
            <wsdl:message name="foo">

        Returns the response message instance.
        """
        responseName = "%s.%s.response" % (classInstance.__name__,
            methodInstance.__name__)
        responseMessage = self.wsdl.messages.addMessage(responseName)
        return responseMessage


class BindingOperationGenerator(Generator):
    """
    Supplied the package and a WSDL binding instance.  Used to generate
    operation instances that are child elements of the supplied binding
    instance.
    """
    def __init__(self, package, binding, debug=0):
        self.package = package
        self.binding = binding
        self.debug = debug
        Generator.__init__(self)

    def generate(self, method):
        """
        Build an operation for the binding.  We assume that all
        operations involve both an input and an output (ie, they all
        use the request-response transmission primitive).  Returns
        the generated operation instance.
        """
        parsed = epytext.parse(method.__doc__)
        doc = parsed.firstChild.firstChild.firstChild.data
        operation = self.binding.addOperation(method.__name__, doc)
        operation.addSoap({"soapAction" : ""})
        # FIXME Should support different uses, not just "encoded"
        input = operation.setInput()
        input.addSoap({
            "use" : "encoded",
            "encodingStyle" : "http://schemas.xmlsoap.org/soap/encoding/",
        })
        output = operation.setOutput()
        output.addSoap({
            "use" : "encoded",
            "encodingStyle" : "http://schemas.xmlsoap.org/soap/encoding/",
        })
        # FIXME Need to generate faults
        return operation


class BindingGenerator(Generator):
    """
    Supplied the package and a WSDL instance.  Used to generate binding
    instances that are child elements of the supplied WSDL instance.
    """
    def __init__(self, package, wsdl,
            bindingOperationGeneratorClass=BindingOperationGenerator,
            debug=0):
        self.package = package
        self.wsdl = wsdl
        self.bindingOperationGeneratorClass = bindingOperationGeneratorClass
        self.debug = debug
        Generator.__init__(self)

    def generate(self, classInstance):
        """
        Build a binding for the WSDL.  Each binding represents a class.
        Its documentation child element represents the class doc string.
        Returns the generated binding instance.
        """
        bindingType = "tns:%sPortType" % classInstance.__name__
        bindingDoc = getattr(self.package, classInstance.__name__).__doc__
        bindingDoc = flattenString(bindingDoc)
        binding = self.wsdl.bindings.addBinding(classInstance.__name__,
            bindingType, bindingDoc)
        # FIXME Should support different styles, not just "rpc"
        binding.addSoap({
            "style" : "rpc",
            "transport" : "http://schemas.xmlsoap.org/soap/http",
        })
        # Generate a binding operation for every method
        bindingOperationGenerator = self.bindingOperationGeneratorClass(
            self.package, binding, debug=self.debug)
        methodList = getMethods(getattr(self.package, classInstance.__name__))
        for methodInstance in methodList:
            bindingOperationGenerator.generate(methodInstance)
        return binding


class PortTypeOperationGenerator(Generator):
    """
    Supplied the package and a WSDL portType instance.  Used to generate
    operation instances that are child elements of the supplied portType
    instance.
    """
    def __init__(self, package, portType, debug=0):
        self.package = package
        self.portType = portType
        self.debug = debug
        Generator.__init__(self)

    def generate(self, methodInstance):
        """
        Build an operation for the portType.  We assume that all
        operations involve both an input and an output (ie, they all
        use the request-response transmission primitive).  The input
        refers to the corresponding request message.  The output refers
        to the corresponding response message.  Returns the generated
        operation instance.
        """
        operation = self.portType.addOperation(methodInstance.__name__)
        requestRef = "tns:%s.%s.request" % (self.portType.name,
            methodInstance.__name__)
        responseRef = "tns:%s.%s.response" % (self.portType.name,
            methodInstance.__name__)
        operation.setInput(requestRef)
        operation.setOutput(responseRef)
        # FIXME Need to generate faults
        return operation


class PortTypeGenerator(Generator):
    """
    Supplied the package and a WSDL instance.  Used to generate portType
    instances that are child elements of the supplied WSDL instance.
    """
    def __init__(self, package, wsdl,
            portTypeOperationGeneratorClass=PortTypeOperationGenerator,
            debug=0):
        self.package = package
        self.wsdl = wsdl
        self.portTypeOperationGeneratorClass = portTypeOperationGeneratorClass
        self.debug = debug
        Generator.__init__(self)

    def generate(self, classInstance):
        """
        Build a portType for the WSDL.  Each portType represents a class.
        Its documentation child element represents the class doc string.
        Returns the generated portType instance.
        """
        portTypeName = classInstance.__name__ + "PortType"
        portType = self.wsdl.portTypes.addPortType(portTypeName)
        # Generate a portType operation for every method
        portTypeOperationGenerator = self.portTypeOperationGeneratorClass(
            self.package, portType, debug=self.debug)
        methodList = getMethods(getattr(self.package, classInstance.__name__))
        for methodInstance in methodList:
            portTypeOperationGenerator.generate(methodInstance)
        return portType


class WSDLGenerator(Generator):
    """
    Supplied the package.  Coordinates the various generators to generate
    a WSDL instance.
    """
    def __init__(self, targetNamespace=DEF_BASE_URI,
            bindingGeneratorClass=BindingGenerator,
            bindingOperationGeneratorClass=BindingOperationGenerator,
            portTypeGeneratorClass=PortTypeGenerator,
            portTypeOperationGeneratorClass=PortTypeOperationGenerator,
            requestMessageGeneratorClass=RequestMessageGenerator,
            responseMessageGeneratorClass=ResponseMessageGenerator,
            debug=0):
        self.targetNamespace = targetNamespace
        self.bindingGeneratorClass = bindingGeneratorClass
        self.bindingOperationGeneratorClass = bindingOperationGeneratorClass
        self.portTypeGeneratorClass = portTypeGeneratorClass
        self.portTypeOperationGeneratorClass = portTypeOperationGeneratorClass
        self.requestMessageGeneratorClass = requestMessageGeneratorClass
        self.responseMessageGeneratorClass = responseMessageGeneratorClass
        self.debug = debug

    def generate(self, package):
        """
        Supplied the package.  Coordinates the various generators to
        generate a WSDL instance.  Returns the WSDL instance.
        """
        wsdl = wsdllib.Wsdl()
        wsdl.setName(package.__name__)

        wsdlDocumentation = getPackageDocumentation(package)
        wsdlDocumentation = flattenString(wsdlDocumentation)
        wsdl.setDocumentation(wsdlDocumentation)

        # FIXME I have a *very* strong feeling that this is the wrong
        # FIXME way to do this.  I suspect wsdllib will actually do
        # FIXME this for me if I build the WSDL elements some other way.
        wsdl.setTargetNamespace(self.targetNamespace)
        wsdl.addNamespace("xmlns:tns", self.targetNamespace)
        for name, uri in DEF_NAMESPACES:
            wsdl.addNamespace(name, uri)

        bindingGenerator = self.bindingGeneratorClass(package, wsdl,
            self.bindingOperationGeneratorClass, self.debug)
        portTypeGenerator = self.portTypeGeneratorClass(package, wsdl,
            self.portTypeOperationGeneratorClass, self.debug)
        for classInstance in getClasses(package):
            bindingGenerator.generate(classInstance)
            portTypeGenerator.generate(classInstance)
            # Generate a request message and a response message for
            # every method
            requestMessageGenerator = self.requestMessageGeneratorClass(
                package, wsdl, self.debug)
            responseMessageGenerator = self.responseMessageGeneratorClass(
                package, wsdl, self.debug)
            methodList = getMethods(getattr(package, classInstance.__name__))
            for methodInstance in methodList:
                requestMessageGenerator.generate(classInstance, methodInstance)
                responseMessageGenerator.generate(classInstance, methodInstance)

        return wsdl


def populateRequestMessageFromEpyFunc(message, epyFunc):
    """
    Each part is added to the supplied message along with its
    documentation and type information.
    """
    for p in epyFunc.parameters():
        paramDesc = None
        paramType = None
        if p.name() == "self":
            continue
        if p.descr():
            paramDesc = p.descr().to_plaintext(None)
        if p.type():
            paramType = p.type().to_plaintext(None)
        part = message.addPart(p.name(), paramDesc)
        part.type = paramType


def populateResponseMessageFromEpyFunc(message, epyFunc):
    """
    The return part is added to the supplied message along with its
    documentation and type information.
    """
    r = epyFunc.returns()
    returnDesc = None
    returnType = None
    if not r:
        return
    if r.descr():
        returnDesc = r.descr().to_plaintext(None)
    if r.type():
        returnType = r.type().to_plaintext(None)
    part = message.addPart(r.name(), returnDesc)
    part.type = returnType


def getPackageSchemas(package):
    """
    The "<types>...</types>" WSDL data is in the __init__ doc string
    and contains the WSDL schemas.  The doc string also contains the
    WSDL documentation.

    Extracts and returns the portion of the doc string that represents
    the WSDL schemas.
    """
    if not package.__doc__:
        return ""
    start = package.__doc__.find("<types>")
    end = package.__doc__.find("</types>")
    if (start == -1) or (end == -1):
        return ""
    start += len("<types>")
    return package.__doc__[start:end]


def getPackageDocumentation(package):
    """
    The documentation is in the __init__ doc string.  The doc string also
    contains "<types>...</types>" data.  That data is not considered part
    of the package documentation.  Instead, it is more akin to "#include".
    
    Extracts the portion of the doc string that represents the WSDL
    documentation.  Removes all newline characters and returns the result.
    """
    if not package.__doc__:
        return ""
    documentation = package.__doc__.split("<types>", 1)[0]
    return flattenString(documentation)


def getClasses(package):
    """
    It just so happens that the class names are the same as the module
    names (in packages produced by wsdl2py).  This may not always be
    the case.  Nyer nyer.
    """
    classes = []
    packageAttributeNames = dir(package)
    for attributeName in packageAttributeNames:
        if attributeName[0] == "_":
            continue
        attribute = getattr(package, attributeName)
        if type(attribute) == types.ClassType:
            classes.append(attribute)
    return classes


def getMethods(classInstance):
    """
    Determines all the members of a given class and returns those members
    that are methods (types.MethodType) with names that do not begin with
    "_".

    Transforms a list of tuples of the form:
        [ (methodName, methodInstance), (methodName, methodInstance) ... ]

    to a simple list of method instances.  Returns the list of method
    instances.
    """
    methods = inspect.getmembers(classInstance)
    methods = filter(lambda m: m[0] and m[0][0] != "_", methods)
    methods = filter(lambda m: type(m[1]) == types.MethodType, methods)
    methods = map(lambda m: m[1], methods)
    return methods


def flattenString(s):
    """
    Removes all newline characters and indentation from the supplied
    string, s.  Returns the "flattened" version.

    >>> flattenString("")
    ''
    >>> flattenString("test")
    'test'
    >>> flattenString("this\\nis\\na\\ntest")
    'this is a test'
    >>> flattenString("this\\r\\nis\\r\\nanother\\r\\ntest")
    'this is another test'
    """
    lines = s.split("\n")
    lines = map(lambda l: l.strip(), lines)
    lines = filter(None, lines)
    return " ".join(lines)


if __name__ == "__main__":
    try:
        package = __import__(sys.argv[1])
        filename = sys.argv[2]
    except IndexError:
        sys.stderr.write("Usage: py2wsdl <package> <wsdl file>\n")
        sys.exit(1)
    except ImportError, reason:
        sys.stderr.write("%s\n" % reason)
        sys.exit(1)

    w = WSDLGenerator()
    wsdl = w.generate(package)
    wsdlString = wsdlutil.wsdlToString(wsdl, schemas=getPackageSchemas(package))
    wsdlFile = open(filename, "w")
    wsdlFile.write(wsdlString)
    wsdlFile.close()
