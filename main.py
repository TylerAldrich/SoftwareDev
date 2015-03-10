#!/usr/bin/python
import xlrd
import sys
import pprint
from workbook import Workbook

#Checks that the command line contains the necessary arguments and throws an error if not
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Must give this program a workbook to open, a filename to save as Look Zones, and a filename to save as Slide Metrics"
        sys.exit(1)

#Sets the command line arguments
    workbook_file = sys.argv[1]
    filename  = sys.argv[2]
    filename2 = sys.argv[3]
    workbook = Workbook(workbook_file)

#Writes the two workbooks and prints a success message
    workbook.write_lookzone_workbook(filename, "Width", "Appears", "Gazepoint count")
    workbook.write_slidemetrics_workbook(filename2, "Percent time tracked", "Average pupil area", "Number of fixations")
    print "Files created: " + filename + " and " + filename2



