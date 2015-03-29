import xlwt
from metrics import Metrics, Lookzone, Slidemetrics
from workbook_reader import WorkbookReader

class WorkbookWriter():
    def __init__(self, readers, output, attributes):
        """ Instantiated with a list of workbook_readers, filename for lookzone output, and
        filename for slide metrics output, and a list of attributes"""
        self.readers = readers
        self.output = output
        self.attributes = attributes
        self.book = xlwt.Workbook() # Create the book
        self.attribute_sheets = {}
        self.header_to_col_num = {}

    def write_reader(self, reader):
        """Writes data for individual reader"""
        # Abstract Stub
        return

    def write_headers(self, sheet):
        """ Write header for sheet """
        # TODO: We will have to separate writing header and data in Iteration 2
        pass

    def write_readers(self):
        self.write_headers(self.readers)
        row_num = 1
        for reader in self.readers:
            self.write_reader(reader, row_num)
            row_num += 1

    def write_first_reader(self):
        """ This method prints only the first reader of the writer """
        self.write_reader(self.readers[0])

class LookzoneWriter(WorkbookWriter):

    def __init__(self, readers, output, attrs):
        """ Initialize instance of a lookzone writer.
        @Params: readers - Listof WorkbookReader
                output - String: Path to output file
                attrs - (Listof String): Desired Attributes
        """
        WorkbookWriter.__init__(self,readers,output,attrs)


    def write_headers(self, readers):
        """ Write header for sheet """
        for attribute in self.attributes: # Create sheet for each attribute
            sheet_name = attribute.replace('/', "'d") # Sheet names do not support slashes
            if len(sheet_name) > 31:
              sheet_name = sheet_name[:26]
              sheet_name += '...'
            write_sheet = self.book.add_sheet(sheet_name) # Create the sheet
            self.attribute_sheets[attribute] = write_sheet # store right sheet to get later

            # Set up sheets headers
            write_sheet.write(0, 0, 'SubjectID')
            row_num = 0
            col_num = 1
            col_names = set()
            for reader in readers:
                current_lookzone_num = 1
                for stat in reader._stat_sheets:
                    for lookzone in reader.get_lookzones(stat):
                        col_name = self.__get_header(stat, lookzone, current_lookzone_num)
                        current_lookzone_num += 1

                        if col_name not in col_names:
                            col_names.add(col_name)

                    current_lookzone_num = 1

            col_names = sorted(list(col_names))
            for col_name in col_names:
                write_sheet.write(row_num, col_num, col_name)
                if attribute not in self.header_to_col_num:
                    self.header_to_col_num[attribute] = {}
                self.header_to_col_num[attribute][col_name] = col_num
                col_num += 1

    def __get_header(self, stat, lookzone, lz_num):
        """ Returns header for a given stat sheet and lookzone object """
        sheet_name = stat.name.split('.')[0]

        if "OUTSIDE" in lookzone.name: # last lookzone of the file
            col_name = "%s_outside" % sheet_name
        else:
            col_name = "%s_LZ%s" % (sheet_name, str(lz_num))

        return col_name


    def write_reader(self, reader, row_num):
        """ Write data for individual reader.
        @Params: reader - WorkbookReader """
        subject_id = reader.get_subject_id()
        for attribute in self.attributes: # Create sheet for each attribute
            write_sheet = self.attribute_sheets[attribute]

            # Add data for the subject
            write_sheet.write(row_num, 0, subject_id)
            current_lookzone_num = 1
            for stat in reader._stat_sheets:
                for lookzone in reader.get_lookzones(stat):
                    if lookzone.has_attribute(attribute): # only add if attr exists
                        col_name = self.__get_header(stat, lookzone, current_lookzone_num)
                        col_num = self.header_to_col_num[attribute][col_name]
                        write_sheet.write(row_num,col_num,lookzone.value_for_attribute(attribute))
                    current_lookzone_num += 1
                current_lookzone_num = 1
        self.book.save(self.output)
"""
mapping from column header -> column number
get column header for each lookzone we go through
get column number to write that data to
repeat
"""

class SlideMetricWriter(WorkbookWriter):
    def __init__(self, readers, output, attrs):
        """ Initialize instance of a lookzone writer.
        @Params: readers - Listof WorkbookReader
                output - String: Path to output file
                attrs - (Listof String): Desired Attributes
        """
        WorkbookWriter.__init__(self,readers,output,attrs)

    def __get_header(self, stat):
        """ Returns header for a given stat sheet and lookzone object """
        sheet_name = stat.name.split('.')[0]
        return sheet_name

    def write_headers(self, readers):
        for attribute in self.attributes:
            sheet_name = attribute.replace('/', "'d") # Sheet names do not support slashes
            if len(sheet_name) > 31:
              sheet_name = sheet_name[:26]
              sheet_name += '...'
            write_sheet = self.book.add_sheet(sheet_name) # Create the sheet
            self.attribute_sheets[attribute] = write_sheet # store right sheet to get later

            # Set up sheets headers
            write_sheet.write(0, 0, 'SubjectID')
            col_names = set()
            for reader in readers:
                for stat in reader._stat_sheets:
                    col_name = self.__get_header(stat)
                    col_names.add(col_name)

            col_num = 1
            row_num = 0
            for col_name in col_names:
                write_sheet.write(row_num, col_num, col_name)
                if attribute not in self.header_to_col_num:
                    self.header_to_col_num[attribute] = {}
                self.header_to_col_num[attribute][col_name] = col_num
                col_num += 1

    def write_reader(self, reader, row_num):
        """ Write data for individual reader.
        @Params: reader - WorkbookReader """
        subject_id = reader.get_subject_id()
        for attribute in self.attributes:
            write_sheet = self.attribute_sheets[attribute]
            # Add data for the subject
            write_sheet.write(row_num, 0, subject_id)
            col_num = 1
            for stat in reader._stat_sheets:
                slidemetric = reader.get_slidemetrics(stat)
                if slidemetric.has_attribute(attribute): # only add if attr exists
                    col_name = self.__get_header(stat)
                    col_num = self.header_to_col_num[attribute][col_name]
                    write_sheet.write(row_num,col_num,slidemetric.value_for_attribute(attribute))
        self.book.save(self.output)

