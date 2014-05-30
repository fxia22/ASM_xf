#! python
#   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
#   *                                                                       *
#   *   *   *          http://members.lycos.co.uk/bdeck             *   *   *
#   *                                                                       *
#############################################################################
# 2003 DJGPP mail Release 1.0, deckerben, http://members.lycos.co.uk/bdeck
# 
# Sample csv script for importing Yahoo addressbook csv format into abook

import ccsv

p = ccsv.parser()

a = 3
file = open("Yahoo_ab.csv")
file2 = open("abook", "w")
while 1:
    line = file.readline()
    if not line:
        break
    fields = p.parse(line)
    if not fields:
        # multi-line record
        continue
    # process the fields
    file2.write("\n[%s]\n" % a)
    file2.write("name=%s %s\n" % (fields[1], fields[3]))
    file2.write("email=%s\n" % fields[55])
    a = a + 1
file.close()
file2.close()
