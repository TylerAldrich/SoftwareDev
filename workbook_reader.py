import xlrd
import pprint
import pdb
import re
import os
from metrics import Metrics, Lookzone, Slidemetrics
from ipatch_exception import IPatchException

LOOKZONE_STRING = "LOOKZONE METRICS:"
SLIDE_STRING    = "SLIDE METRICS:"

class WorkbookReader():
    """ Wraps the xlrd Book object """
    def __init__(self, workbook_file):
        try:
            self.workbook = xlrd.open_workbook(workbook_file)
        except IOError as e:
            raise IPatchException("File does not exist")
        except:
            raise IPatchException("File could not be opened")
        self._stat_sheets = []
        self._data_dict = {}
        self.workbook_filename = workbook_file
        self.get_sheets()

    def get_sheets(self):
        """ Return needed sheets from the workbook (end in STAT) """
        if not self._stat_sheets:
            stat_sheet_names = filter(lambda w: w.endswith('STAT'), self.workbook.sheet_names())
            self._stat_sheets = [self.workbook.sheet_by_name(sheet) for sheet in stat_sheet_names]

        return self._stat_sheets

    def get_subject_id(self):
        """ Return subject id (first numbers in file name)"""
        # get xls filename (end of path x/y/z/123-foo.xls)
        filename = self.workbook_filename.split(os.sep)[-1]
        return filename.split('-')[0].strip()

    def get_attributes(self):
        """returns a hash of a set of attributes for lookzone attributes and slide attributes
        OUTPUT: {'lookzone' : (Setof String), 'slide' : (Setof String)} """
        lookzone_attrs = set()
        slide_attrs = set()
        for sheet in self._stat_sheets:
            row = 0
            # Loop through slide metrics
            while sheet.cell_value(row,0) != LOOKZONE_STRING:
                if sheet.cell_type(row,0) == 1 : # Found a slide metric
                    value = sheet.cell_value(row,0)
                    if self._valid_slidemetric_value(value):
                        slide_attrs.add(value) # add that slide metric
                row += 1
            row += 1  # increment one more time for next section
            # loop through rest of file (lookzones)
            while row < sheet.nrows:
                if sheet.cell_type(row,0) == 1: # Found a lookzone
                    value = sheet.cell_value(row,0)
                    if self._valid_lookzone_value(value):
                        lookzone_attrs.add(value)
                row += 1

        lookzone_attrs = sorted(list(lookzone_attrs))
        slide_attrs = sorted(list(slide_attrs))
        return {"lookzone" : lookzone_attrs, "slide" : slide_attrs} # return as hash


    def _valid_lookzone_value(self, v):
        return not re.match("ATT_.*|LookZone.*|LOOKZONE.*|Vertex.*", v)

    def _valid_slidemetric_value(self, v):
        return v != SLIDE_STRING

    ##### Sheet Methods ####

    def get_lookzones(self,sheet):
        """ Return an Array of Lookzones for the given sheet """
        row = 0
        lookzones = []
        while sheet.cell_value(row,0) != LOOKZONE_STRING: # Loop until first lookzone
            row = row + 1
            if row >= sheet.nrows: # looped through entire sheet
                raise IPatchException("Incorrectly Formated Worksheet") # don't loop forever
        row = row + 1

        while row < sheet.nrows:
            lookzone_count = -1 # Start adding in Lookzones
            if sheet.cell_type(row,1) == 1 : # Found a lookzone
                lookzones.append(Lookzone(sheet.cell_value(row,1))) # name that lookzone
                lookzone_count += 1
            elif sheet.cell_type(row,0) == 1:  # attribute
                lookzones[lookzone_count].add_value_for_attribute(sheet.cell_value(row,5),sheet.cell_value(row,0))
            row = row + 1
        return lookzones


    def get_slidemetrics(self, sheet):
        """Return the slide metric object for the given sheet"""
        row = 0
        slidemetric = Slidemetrics("blah")
        while sheet.cell_value(row,0) != SLIDE_STRING: # Loop until first slide metric
            row = row + 1
            if row >= sheet.nrows: # means we looped through entire sheet
                raise IPatchException("Incorrectly Formated Worksheet") # don't loop forever
        row = row + 1

        while sheet.cell_value(row,0) != LOOKZONE_STRING:
            if sheet.cell_type(row,0) == 1 : # Found a slide metric
                slidemetric.add_value_for_attribute(sheet.cell_value(row,5),sheet.cell_value(row,0))
            #elif sheet.cell_type(row,0) == 1:

            row = row + 1
        return slidemetric
