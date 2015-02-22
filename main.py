#!/usr/bin/python
import xlrd
import sys
import pprint
from workbook import Workbook


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Must give this program a workbook to open"
        sys.exit(1)

    workbook_file = sys.argv[1]
    workbook = Workbook(workbook_file)

    stat_sheets = workbook.get_sheets()
    data_dict = workbook.get_data(stat_sheets[0])
    workbook.write_workbook("Example.xls", "Width", "Appears", "Gazepoint count")
    print "File created: Example.xls"
