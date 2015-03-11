import xlrd
import pprint
import pdb
from metrics import Metrics, Lookzone, Slidemetrics

class WorkbookReader():
    """ Wraps the xlrd Book object """
    def __init__(self, workbook_file):
        self.workbook = xlrd.open_workbook(workbook_file)
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
        filename = self.workbook_filename.split('/')[-1]
        return filename.split('-')[0].strip()

    def get_attributes(self):
        """returns a hash of a set of attributes for lookzone attributes and slide attributes
        OUTPUT: {'lookzone' : (Setof String), 'slide' : (Setof String)} """
        lookzone_attrs = set()
        slide_attrs = set()
        for sheet in self._stat_sheets:
            row = 0
            # Loop through slide metrics
            while sheet.cell_value(row,0) != "LOOKZONE METRICS:":
                if sheet.cell_type(row,0) == 1 : # Found a slide metric
                    slide_attrs.add(sheet.cell_value(row,0)) # add that slide metric
                row += 1
            row += 1  # increment one more time for next section
            # loop through rest of file (lookzones)
            while row < sheet.nrows:
                if sheet.cell_type(row,0) == 1: # Found a lookzone
                    lookzone_attrs.add(sheet.cell_value(row,0))
                row += 1

        return {"lookzone" : lookzone_attrs, "slide" : slide_attrs} # return as hash


    ##### Sheet Methods ####

    def get_lookzones(self,sheet):
        """ Return an Array of Lookzones for the given sheet """
        row = 0
        lookzones = []
        while sheet.cell_value(row,0) != "LOOKZONE METRICS:": # Loop until first lookzone
            row = row + 1
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
        while sheet.cell_value(row,0) != "SLIDE METRICS:": # Loop until first slide metric
            row = row + 1
        row = row + 1

        while sheet.cell_value(row,0) != "LOOKZONE METRICS:":
            if sheet.cell_type(row,0) == 1 : # Found a slide metric
                slidemetric.add_value_for_attribute(sheet.cell_value(row,5),sheet.cell_value(row,0))
            #elif sheet.cell_type(row,0) == 1:

            row = row + 1
        return slidemetric
