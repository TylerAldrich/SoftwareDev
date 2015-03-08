#!/usr/bin/python
import xlrd
import sys
import pprint
from workbook import Workbook


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Must give this program a workbook to open and a filename to save as"
        sys.exit(1)

    workbook_file = sys.argv[1]
    filename  = sys.argv[2]
    workbook = Workbook(workbook_file)

    workbook.write_workbook(filename, "Width", "Appears", "Gazepoint count")
    #workbook.write_slidemetrics_workbook(filename)
    print "File created: " + filename

