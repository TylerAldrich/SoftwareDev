import xlrd
import xlwt
import pprint
from lookzone import Lookzone

class Workbook():
    """ Wraps the xlrd Book object """
    def __init__(self, workbook_file):
        self.workbook = xlrd.open_workbook(workbook_file)
        self._stat_sheets = []
        self._data_dict = {}

    def get_sheets(self):
        """ Return needed sheets from the workbook (end in STAT) """
        if not self._stat_sheets:
            stat_sheet_names = filter(lambda w: w.endswith('STAT'), self.workbook.sheet_names())
            self._stat_sheets = [self.workbook.sheet_by_name(sheet) for sheet in stat_sheet_names]

        return self._stat_sheets
    def get_subject_id():
        # TODO: Is this the number before the sheetname?
        pass

    # Don't think we need this anymore
    def generate_contents(self, sheet):
         """ Put the contents of each cell into a dictionary.
             If the cell name is already in the dict, add to a list
             of values for that statistic. """
         # TODO(KingTyler) - Need to keep track of where the values in each
         # list come from (different lookzones)
         if sheet.name in self._data_dict:
            # already generated contents for this sheet
            return

         self._data_dict[sheet.name] = {}
         data = self._data_dict[sheet.name]

         for row_num in xrange(sheet.nrows):
             row = sheet.row(row_num)

             row_key = None
             for cell_num in xrange(sheet.ncols):
                 # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date
                 #             4=Boolean, 5=Error, 6=Blank
                 cell_type = sheet.cell_type(row_num, cell_num)

                 if cell_type == 0: # skip blank rows
                     continue

                 cell_value = sheet.cell_value(row_num, cell_num)
                 if cell_type == 1: # add this as row key
                     row_key = cell_value
                 if cell_type == 2 and row_key:
                     if row_key in data and not isinstance(data[row_key], list):
                         data[row_key] = [data[row_key], cell_value]
                     elif row_key in data:
                         data[row_key].append(cell_value)
                     else:
                         data[row_key] = cell_value

    def get_data(self, sheet):
        """ Returns dictionary of data from the sheet.
            If its not generated, we generate it here """
        if sheet.name not in self._data_dict:
            self.generate_contents(sheet)
        return self._data_dict[sheet.name]

    def get_lookzones(self,sheet):
        """ Return an Array of Lookzones for the given sheet """
        row = 0
        lookzones = []
        while sheet.cell_value(row,0) != "LOOKZONE METRICS:": # Loop until first lookzone
            row = row + 1
        row = row + 1

        while row < sheet.nrows:
            lookzone_count = 0 # Start adding in Lookzones
            if sheet.cell_type(row,1) == 1 : # Found a lookzone
                lookzones.append(Lookzone(sheet.cell_value(row,1))) # name that lookzone
            elif sheet.cell_type(row,0) == 1:  # attribute
                lookzones[lookzone_count].add_value_for_attribute(sheet.cell_value(row,5),sheet.cell_value(row,0))
            else: # end of lookzone
                lookzone_count = lookzone_count + 1 # increments
            row = row + 1
        return lookzones

    def grab_attributes(self):
        """returns a hash of a set of attributes for lookzone attributes and slide attributes
        OUTPUT: {'lookzone' : (Setof String), 'slide' : (Setof String)} """
        lookzone_attrs = set() 
        slide_attrs = set()
        for sheet in self._stat_sheets:
            row = 0
            while sheet.cell_value(row,0) != "LOOKZONE METRICS:":
                if sheet.cell_type(row,0) == 1 : # Found a slide metric
                    slide_attrs.add(sheet.cell_value(row,0)) # add that slide metric
                row += 1
            row += 1  # increment one more time for next section
            while row < sheet.nrows: # loop through rest of file (lookzones)
                if sheet.cell_type(row,0) == 1: # Found a lookzone
                    lookzone_attrs.add(sheet.cell_value(row,0))
                row += 1

        return {"lookzone" : lookzone_attrs, "slide" : slide_attrs} # return as hash

    def write_workbook(self, filename, *attrs):
        """ Prints sheets containing given attributes to filename. """
        book = xlwt.Workbook() # Create the book
        for attribute in attrs: # Creat sheet for each attribute
            write_sheet = book.add_sheet(attribute) # Create the sheet
            for row_count, subject in enumerate(self._stat_sheets): # loop through subjects
                for col_count, lookzone in enumerate(self.get_lookzones(subject)):
                    if lookzone.has_attribute(attribute): # only add if attr exists
                        write_sheet.write(row_count,col_count,lookzone.value_for_attribute(attribute))

        book.save(filename)


