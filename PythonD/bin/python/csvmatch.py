#! python
#   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
#   *                                                                       *
#   *   *   *                http://www.caddit.net                  *   *   *
#   *                                                                       *
#############################################################################
# 2003 DJGPP mail Release 1.0, deckerben, http://members.lycos.co.uk/bdeck
# 
# Sample csv script for importing Yahoo addressbook csv format into abook

import ccsv

p = ccsv.parser()


# Build a dictionary of CIDR arrays which store selected attribute fields
cidrs = {}
# Keep a list of all errors
errorlist = []
# file is a csv from ops2 with: cidr, 1count, lastcount, 1in, lastin
file = open("users.csv")
while 1:
  line = file.readline()
  if not line:
    break
  fields = p.parse(line)
  if not fields:
    # multi-line record
    continue
  # process the fields
  #file2.write("\"%s\"," % (fields[0]))
  # Write dictionary of interesting CIDRs discriminating users less than 2M
  #if (fields[2] > 2000000.0):
  cidrs[fields[0]] = fields[2]
file.close()


# file is csv from IPDB asciidump2: name, service#, cidr, fullname
file = open("asciidump2.csv")
print "customer",",","CIDR",",","servicenumber",",","usage in octets"
while 1:
  line = file.readline()
  if not line:
    break
  fields = p.parse(line)
  if not fields:
    continue
  try:
    if cidrs.has_key(fields[2]):
      print fields[3],",",fields[2],",",fields[1],",",cidrs[fields[2]]
  except:
    errorlist.append(fields)


file.close()
print "ERRORS:"
for error in errorlist:
  if type(error) == type([]):
    for item in error:
      print item,",",
    print
  else:
    print error
