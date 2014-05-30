#!/usr/bin/env python

"""
$Id: wsdl2py.py,v 1.6 2003/07/23 06:37:03 david Exp $

Container module for all WSDL->Python code generator bases.
"""


import os, sys, types
from xml.dom.ext import PrettyPrint, SplitQName
from wsdlutil import unqualifiedName


NO_DOCUMENTATION = "N/A"
DEF_INDENT = "    "


class Generator:
    """
    Generator base class.  All subclasses must override toString().

    Note:
    Accessing the WSDL content in the __init__ can be hazardous to
    your health.  If a streaming parser (eg, SAX) is being used the WSDL
    will be validated as the instance is created.  This could result in
    a parse exception that would, in turn, result in failure to create
    the instance.  Not goot.
    """

    TEMPLATE = ""

    def __init__(self):
        pass

    def toString(self):
        raise NotImplementedError, "toString()"


class MethodGenerator(Generator):
    """
    Supplied the WSDL, the Binding, and the Operation within that WSDL for
    which a method will be generated.  It is necessary to supply all
    as the WSDL is not hierarchical.  That is, an operation does not
    contain the operation parts necessary to determine method parameters.
    The operation parts are defined separately in messages with names
    of the form:
    
        <binding name>.<operation name>.request
        <binding name>.<operation name>.response
    """

    TEMPLATE = \
        "    def %(name)s(self, %(parameters)s):\n" \
        "        \"\"\"\n" \
        "%(documentation)s\n" \
        "        \"\"\"\n" \
        "        result = None\n" \
        "        return result\n"

    def __init__(self, wsdl, binding, operation, debug=0):
        self.wsdl = wsdl
        self.binding = binding
        self.operation = operation
        self.debug = debug
        Generator.__init__(self)

    def toString(self):
        """
        Returns a string representation of a method, including parameters,
        doc string, and some stub code.
        """
        name = self.operation.name
        if self.debug:
            sys.stdout.write("Generating method: %s\n" % name)
        parameters = buildMethodParameterString(self.wsdl, self.binding,
            self.operation)
        documentation = buildMethodDocString(self.wsdl, self.binding,
            self.operation)
        return self.TEMPLATE % locals()


class ClassGenerator(Generator):
    """
    Supplied the WSDL and the Binding within that WSDL for which a
    class will be generated.  It is necessary to supply both as the
    WSDL is not hierarchical.  That is, a binding does not contain the
    operation parts necessary to determine method parameters.
    """

    TEMPLATE = \
        "class %(name)s:\n" \
        "    \"\"\"\n" \
        "%(documentation)s\n" \
        "    \"\"\"\n" \
        "%(methods)s\n"

    def __init__(self, wsdl, binding, methodGeneratorClass=MethodGenerator,
            debug=0):
        self.wsdl = wsdl
        self.binding = binding
        self.methodGeneratorClass = methodGeneratorClass
        self.debug = debug
        Generator.__init__(self)

    def toString(self):
        """
        Returns a string representation of a class, including a doc
        string and all methods.
        """
        name = self.binding.name
        if self.debug:
            sys.stdout.write("Generating class: %s\n" % name)
        documentation = buildClassDocString(self.binding)
        methodList = []
        for operation in self.binding.operations.values():
            # Supply the WSDL and the Binding so the generator can extract
            # the parameters (message parts) for each method (operation)
            methodGenerator = self.methodGeneratorClass(self.wsdl,
                self.binding, operation, debug=self.debug)
            method = methodGenerator.toString()
            methodList.append(method)
        methods = "\n".join(methodList)
        return self.TEMPLATE % locals()


class ModuleGenerator(Generator):
    """
    Supplied the WSDL and the Binding within that WSDL for which a
    module will be generated.  It is necessary to supply both as the
    WSDL is not hierarchical.  That is, a binding does not contain the
    operation parts necessary to determine method parameters.
    """

    TEMPLATE = \
        "#!/usr/bin/env python\n" \
        "\n" \
        "__all__ = [\"%(name)s\"]\n" \
        "\n" \
        "%(classes)s\n"

    def __init__(self, wsdl, binding,
            classGeneratorClass=ClassGenerator,
            methodGeneratorClass=MethodGenerator,
            debug=0):
        self.wsdl = wsdl
        self.binding = binding
        self.classGeneratorClass = classGeneratorClass
        self.methodGeneratorClass = methodGeneratorClass
        self.debug = debug

    def toString(self):
        """
        Returns a string representation of a module containing a class
        of the same name.
        """
        name = self.binding.name
        if self.debug:
            sys.stdout.write("Generating module: %s\n" % name)
        # Supply both the WSDL and the Binding so that the generator can
        # extract the parameters (message parts) for each method (operation)
        classGenerator = self.classGeneratorClass(self.wsdl, self.binding,
            self.methodGeneratorClass, debug=self.debug)
        classes = classGenerator.toString()
        return self.TEMPLATE % locals()


class InitGenerator(Generator):
    TEMPLATE = \
        "#!/usr/bin/env python\n" \
        "\n" \
        "\"\"\"\n" \
        "%(documentation)s\n" \
        "\"\"\"\n" \
        "\n" \
        "%(imports)s\n"

    IMPORT_TEMPLATE = "from %s import *"

    def __init__(self, wsdl, additionalImports=[], debug=0):
        self.wsdl = wsdl
        self.debug = debug
        # FIXME
        # Should support additional imports
        if additionalImports:
            sys.stderr.write("WARNING: Additional imports not yet supported\n")
        Generator.__init__(self)

    def _extractImports(self):
        """
        Determines every module as defined by the bindings, builds an
        import for each, and returns a string representing all imports.
        """
        moduleList = self.wsdl.bindings.keys()
        importList = map(lambda m, t=self.IMPORT_TEMPLATE: t % m, moduleList)
        return "\n".join(importList)

    def toString(self):
        """
        Returns a string representation of an __init__.py, containing
        an import for each module and class.
        """
        if self.debug:
            sys.stdout.write("Generating __init__\n")
        name = self.wsdl.name
        documentation = buildInitDocString(self.wsdl)
        imports = self._extractImports()
        return self.TEMPLATE % locals()


class PackageBuilder:
    README_TEMPLATE = \
        "README generated by %(name)s\n" \
        "\n" \
        "%(documentation)s\n"

    def __init__(self, wsdl, base="",
            initGeneratorClass=InitGenerator,
            moduleGeneratorClass=ModuleGenerator,
            classGeneratorClass=ClassGenerator,
            methodGeneratorClass=MethodGenerator,
            debug=0):
        self.wsdl = wsdl
        self.base = base
        self.initGeneratorClass = initGeneratorClass
        self.moduleGeneratorClass = moduleGeneratorClass
        self.classGeneratorClass = classGeneratorClass
        self.methodGeneratorClass = methodGeneratorClass
        self.debug = debug
 
    def build(self):
        os.mkdir(os.path.join(self.base, self.wsdl.name))
        self.writeREADME()
        self.writeModules()
        self.writeInit()

    def writeREADME(self):
        if self.debug:
            sys.stdout.write("Generating README\n")
        name = "%s:%s" % (self.__module__, self.__class__)
        documentation = indentAndWrapLine(self.wsdl.documentation
            or NO_DOCUMENTATION)
        readmePath = os.path.join(self.base, self.wsdl.name, "README")
        readme = open(readmePath, "w")
        readme.write(self.README_TEMPLATE % locals())
        readme.close()

    def writeInit(self):
        initGenerator = self.initGeneratorClass(self.wsdl, debug=self.debug)
        initPath = os.path.join(self.base, self.wsdl.name, "__init__.py")
        init = open(initPath, "w")
        init.write(initGenerator.toString())
        init.close()

    def writeModules(self):
        for binding in self.wsdl.bindings.values():
            moduleGenerator = self.moduleGeneratorClass(self.wsdl, binding,
                self.classGeneratorClass, self.methodGeneratorClass,
                debug=self.debug)
            moduleName = "%s.py" % binding.name
            modulePath = os.path.join(self.base, self.wsdl.name, moduleName)
            module = open(modulePath, "w")
            module.write(moduleGenerator.toString())
            module.close()


def buildMethodParameterString(wsdl, binding, operation):
    """
    Determines every parameter as defined by the parts of an operation's
    message.  Returns the parameters as a comma-separated string.
    """
    requestName = getRequestName(wsdl, binding, operation)
    requestMessage = wsdl.messages[requestName]
    parameterList = requestMessage.parts.keys()
    return ", ".join(parameterList)


def buildClassDocString(binding, indentWidth=DEF_INDENT):
    """
    Simply returns the binding documentation as a formatted string
    suitable for use as a doc string.

    The addition of doc string quotes is left to the caller, allowing
    the caller to choose between \'\'\' and \"\"\".
    """
    return indentAndWrapLine(binding.documentation or NO_DOCUMENTATION,
        firstIndent=indentWidth, bodyIndent=indentWidth)


def buildInitDocString(wsdl, indentWidth=DEF_INDENT):
    """
    Returns a string containing the WSDL documentation and the WSDL
    schemas.

    The addition of doc string quotes is left to the caller, allowing
    the caller to choose between \'\'\' and \"\"\".
    """
    docString = indentAndWrapLine(wsdl.documentation or NO_DOCUMENTATION) + "\n"
    if wsdl.types.definitions:
        schemas = "\n".join(wsdl.types.definitions)
        docString += "\n<types>%s</types>" % schemas
    return docString


def buildMethodRequestDocString(requestMessage, indentWidth=DEF_INDENT):
    """
    Accepts a request message instance.  Extracts each part name,
    documentation, and type.  Builds a string in epydoc format suitable
    for use in a method doc string.  Returns the formatted string.
    """
    s = ""
    firstIndent = indentWidth * 2
    bodyIndent = indentWidth * 3

    for part in requestMessage.parts.values():
        parameterDoc = "@parameter %s: %s" % (part.name, part.documentation)
        s += indentAndWrapLine(parameterDoc, firstIndent, bodyIndent)
        s += "\n"
        parameterType = "@type %s: %s" % (part.name, part.type)
        s += indentAndWrapLine(parameterType, firstIndent, bodyIndent)
        s += "\n"

    return s


def buildMethodResponseDocString(responseMessage, indentWidth=DEF_INDENT):
    """
    Accepts a response message instance.  Extracts the name,
    documentation, and type for the part.  Currently we support, at most,
    one part in a response message.  Builds a string in epydoc format
    suitable for use in a method doc string.  Returns the formatted
    string.
    """
    assert len(responseMessage.parts.values()) in (0, 1), \
        "Only 0 or 1 response part supported"

    if len(responseMessage.parts.values()) == 0:
        return ""

    s = ""
    firstIndent=indentWidth * 2
    bodyIndent=indentWidth * 3

    part = responseMessage.parts.values()[0]
    returnDoc = "@return: %s" % (part.documentation or NO_DOCUMENTATION)
    s += indentAndWrapLine(returnDoc, firstIndent, bodyIndent)
    s += "\n"
    returnType = "@rtype: %s" % part.type
    s += indentAndWrapLine(returnType, firstIndent, bodyIndent)
    s += "\n"

    return s


def buildMethodDocString(wsdl, binding, operation, indentWidth=DEF_INDENT):
    """
    Determines every parameter and its type as defined by the parts of
    an operation's message.  Returns the docString contents as a string.
    The addition of doc string quotes is left to the caller, allowing
    the caller to choose between \'\'\' and \"\"\".
    """
    docString = indentAndWrapLine(operation.documentation or NO_DOCUMENTATION,
        indentWidth * 2, indentWidth * 2)
    docString += "\n\n"

    requestName = getRequestName(wsdl, binding, operation)
    requestMessage = wsdl.messages[requestName]
    docString += buildMethodRequestDocString(requestMessage, indentWidth)

    responseName = getResponseName(wsdl, binding, operation)
    responseMessage = wsdl.messages[responseName]
    docString += buildMethodResponseDocString(responseMessage, indentWidth)

    return docString


def indentAndWrapLine(line, firstIndent="", bodyIndent="", length=80):
    """
    Returns the indented and wrapped version of line.  Does not lose
    any content.
    """
    assert type(line) in types.StringTypes, "Line"
    assert length > len(firstIndent) and length > len(bodyIndent), "Length"

    buf = []
    indent = firstIndent
    indentedLine = indent + line
    while len(indentedLine) > length:
        index = indentedLine.rfind(" ", len(indent), length)
        # We cannot find a space to use as a wrap point in
        # indentedLine[len(indent):length] so we look for the
        # first space in indentedLine[length:]
        if index == -1:
            index = indentedLine.find(" ", length, len(indentedLine))
            # We cannot find a space to use as a wrap point so we,
            # of course, will not wrap
            if index == -1:
                index = len(indentedLine)
        buf.append(indentedLine[0:index])
        indent = bodyIndent
        indentedLine = indent + indentedLine[index:].strip()
    # Verify that the last indented line has something worth storing
    if indentedLine.strip():
        buf.append(indentedLine)

    return "\n".join(buf)


def getMessageName(wsdl, binding, operation, type):
    """         
    Extracts and returns the name of a message.  The type must be "input",
    "output", or "fault".  From the binding we determine the name of the
    portType containing the message definitions.  Using the operation
    name and type ("input", "output", or "fault") we can inspect the
    portType/operation pair and extract the name of the message.
    """
    assert type in ("input", "output", "fault"), "Invalid type: %s" % type

    portTypeName = unqualifiedName(binding.type)
    portType = wsdl.portTypes[portTypeName]
    portOperation = portType.operations[operation.name]
    messageName = getattr(portOperation, type).message
    return unqualifiedName(messageName)


def getRequestName(wsdl, binding, operation):
    """
    Extracts and returns the name of the request message.
    """
    return getMessageName(wsdl, binding, operation, "input")


def getResponseName(wsdl, binding, operation):
    """
    Extracts and returns the name of the response message.
    """
    return getMessageName(wsdl, binding, operation, "output")


if __name__ == "__main__":
    import wsdllib
    try:
        wsdlFile = open(sys.argv[1], "r")
    except (IndexError, OSError):
        sys.stderr.write("Usage: wsdl2py <WSDL file>\n")
        sys.exit(1)
    wsdl = wsdllib.ReadFromStream(wsdlFile)
    p = PackageBuilder(wsdl, debug=1)
    p.build()
