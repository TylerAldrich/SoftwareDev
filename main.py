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

    stat_sheets = workbook.get_sheets()
    data_dict = workbook.get_data(stat_sheets[0])
    workbook.write_workbook(filename, "Width", "Appears", "Gazepoint count")
    #workbook.write_slidemetrics_workbook(filename)
    print "File created: " + filename
