#!/usr/bin/python
import xlrd
import sys
import pprint
from workbook_reader import WorkbookReader
from workbook_writer import LookzoneWriter
from workbook_writer import SlideMetricWriter

#Checks that the command line contains the necessary arguments and throws an error if not
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Must give this program a workbook to open, a filename to save as Look Zones, and a filename to save as Slide Metrics"
        sys.exit(1)

    #Sets the command line arguments
    workbook_file = sys.argv[1]
    lookzone_output  = sys.argv[2]
    slide_metric_output = sys.argv[3]

    # placeholder attributes
    lookzone_attrs = ["Width", "Appears", "Gazepoint count"]
    slide_attrs = ["Percent time tracked", "Average pupil area", "Number of fixations"]

    # create reader(s)
    workbook_reader = WorkbookReader(workbook_file)

    # create writers
    lookzone_writer = LookzoneWriter([workbook_reader], lookzone_output, lookzone_attrs)
    slide_metric_writer = SlideMetricWriter([workbook_reader], slide_metric_output, slide_attrs)

    #Writes the two workbooks and prints a success message for each file created
    for writer in [lookzone_writer, slide_metric_writer]:
        writer.write_first_reader()
        print "File created: " + writer.output



