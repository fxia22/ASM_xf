#! python
#   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
#   *                                                                       *
#   *   *   *          http://members.lycos.co.uk/bdeck             *   *   *
#   *                                                                       *
#############################################################################
# 2004 DJGPP mail Release 1.0, deckerben, http://members.lycos.co.uk/bdeck
# 
# csv script for breaking down csv entries into individual text files

import sys, os
import ccsv

p = ccsv.parser()



def toFile(fields=[], key=[], folder = 'csv2file'):
    elNum = 0
    try:
        txtFile = open(os.path.join(folder, fields[3]), 'w')
    except IOError:
        raise IOError, "There was an error trying to write the file."
        return
    for element in fields:
        if len(key) >= elNum + 1:
            txtFile.write("%s   ::   %s\n" % (key[elNum], element))
        else:
            txtFile.write("unknown #%i   ::   %s" % (elNum, element))
        elNum += 1
    txtFile.close()
    del txtFile
    
    
def readCsv(csvFile):
    folder = 'csv2file'
    os.mkdir(folder)
    try:
        csvFile = open(csvFile, "r")
    except IOError:
        raise IOError, "There was an error trying to write the file."
        return
    keyLine = csvFile.readline()
    key = p.parse(keyLine)
    while 1:
        line = csvFile.readline()
        if not line:
            break
        fields = p.parse(line)
        if not fields:
            # multi-line record
            continue
        # process the fields
        toFile(fields, key, folder) 
    csvFile.close()


if __name__ == "__main__":
    cmdarg = sys.argv[1]
    readCsv(cmdarg)



