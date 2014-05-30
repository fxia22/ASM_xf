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

file = open("ADSL orphans 15-07-04_0.csv")
file2 = open("list.txt", "w")
file2.write("[")
while 1:
    line = file.readline()
    if not line:
        break
    fields = p.parse(line)
    if not fields:
        # multi-line record
        continue
    # process the fields
    file2.write("\"%s\"," % (fields[0]))
file2.write("]")
file.close()
file2.close()
