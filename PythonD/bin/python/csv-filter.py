#! python
#   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
#   *                                                                       *
#   *   *   *          http://members.lycos.co.uk/bdeck             *   *   *
#   *                                                                       *
#############################################################################
# 2003 DJGPP mail Release 1.0, deckerben, http://members.lycos.co.uk/bdeck
# 
# Sample csv script for reading csv, filtering columns and writing output.
# 
# Usage example:
#     cvs-filter.py /dev/d/files/file.cvs "Customer Name" custAddr > cust.txt
    

import ccsv
p = ccsv.parser()

def csvfilter(csvfile, keys):
    output = ""
    file = open(csvfile)
    # First line normally holds the 'key' for fields.
    line = file.readline()
    fields = p.parse(line)
    if not fields:
        # File blank!
        raise IOError, "Error in csv_filter: file blank."
        return
    names = fields
    # Set desired fields:
    index = 0
    columns = []
    for field in fields:
        if field in keys:
            columns.append(index)
        index += 1
    #print "Columns desired: %s %s" % (columns, keys)
    # Use this next line if you want to create a python list of results:
    output = output + "["
    while 1:
        line = file.readline()
        if not line:
            break
        fields = p.parse(line)
        if not fields:
            # multi-line record
            continue
        # process the fields. This is where output is tailored.
        # 'columns' is a list of row numbers where we want the csv data.
        for column in columns:
            # With each record element (here: store as string):
            output = output + "\"" + fields[column] + "\""
        # After each record line:
        output = output + ","

    # Use this next line if you want to create a python list of results:
    output = output + "]"
    # We are done. Close the file.    
    file.close()
    return output


if __name__ == "__main__":
        import sys
        keys = tuple([arg for arg in sys.argv[2:]])
        print csvfilter(sys.argv[1], keys)
