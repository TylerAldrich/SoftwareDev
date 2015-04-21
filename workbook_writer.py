import xlwt
from metrics import Metrics, Lookzone, Slidemetrics
from workbook_reader import WorkbookReader
from ipatch_exception import IPatchException

MAX_SHEET_NAME_LENGTH = 31

class WorkbookWriter():
    def __init__(self, readers, output, attributes, listener=None):
        """ Instantiated with a list of workbook_readers, filename for lookzone output, and
        filename for slide metrics output, and a list of attributes

        WorkbookWriter is a parent class to LookzoneWriter and SlideMetricWriter,
        which handle writing output workbook sheets, headers, keys, and data from
        the given WorkbookReaders
        """
        self.readers = readers
        self.output = output
        self.attributes = attributes
        self.listener = listener
        self.book = xlwt.Workbook() # Create the book
        self.attribute_sheets = {}
        self.header_to_col_num = {}
        self.sheet_names = {}

    def write_reader(self, reader):
        """Writes data for individual reader"""
        # Abstract Stub
        return

    def write_headers(self, sheet):
        """ Write header for sheet """
        pass

    def write_readers(self):
        self.write_headers(self.readers)
        row_num = 1
        for reader in self.readers:
            self.write_reader(reader, row_num)
            try:
                self.listener.notifier(row_num)
            except Exception as e:
                print('encountered exception in notifier:')
                print(str(e))
                pass
            row_num += 1

        self.write_key()
        self.book.save(self.output)

    def write_key(self):
        """ Writes mapping from sheet # -> full sheet name """
        key_sheet = self.book.add_sheet("Key")

        row_num = 1
        try:
            key_sheet.write(0, 0, 'Key')
            key_sheet.write(0, 1, 'Full Sheet Name')
        except:
            raise IPatchException("Could not write to Key sheet")
        for key, name in self.sheet_names.iteritems():
            key_sheet.write(row_num, 0, str(key))
            key_sheet.write(row_num, 1, name)
            row_num += 1

    def write_first_reader(self):
        """ This method prints only the first reader of the writer """
        self.write_reader(self.readers[0])


class LookzoneWriter(WorkbookWriter):

    def __init__(self, readers, output, attrs, listener=None):
        """ Initialize instance of a lookzone writer.
        @Params: readers - Listof WorkbookReader
                output - String: Path to output file
                attrs - (Listof String): Desired Attributes
        """
        WorkbookWriter.__init__(self, readers, output, attrs, listener)


    def write_headers(self, readers):
        """ Write header for sheet """
        sheet_count = 0
        for attribute in self.attributes: # Create sheet for each attribute
            sheet_count += 1
            self.sheet_names[sheet_count] = attribute # store original sheet name for Key
            sheet_name = attribute.replace('/', "") # Sheet names do not support slashes
            sheet_name = "%s-%s" % (str(sheet_count), sheet_name)
            if len(sheet_name) > MAX_SHEET_NAME_LENGTH:
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
                for stat in reader.get_sheet_names():
                    for lookzone in reader.get_lookzones(stat):
                        col_name = self.__get_header(stat, lookzone, current_lookzone_num)
                        current_lookzone_num += 1

                        if col_name not in col_names:
                            col_names.add(col_name)

                    current_lookzone_num = 1

            col_names = sorted(list(col_names))
            for col_name in col_names:
                try:
                    write_sheet.write(row_num, col_num, col_name)
                except:
                    raise IPatchException("Could not write header: {0}".format(col_name))
                if attribute not in self.header_to_col_num:
                    self.header_to_col_num[attribute] = {}
                self.header_to_col_num[attribute][col_name] = col_num
                col_num += 1

    def __get_header(self, stat, lookzone, lz_num):
        """ Returns header for a given stat sheet and lookzone object """
        sheet_name = stat.split('.')[0]

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
            for stat in reader.get_sheet_names():
                for lookzone in reader.get_lookzones(stat):
                    if lookzone.has_attribute(attribute): # only add if attr exists
                        col_name = self.__get_header(stat, lookzone, current_lookzone_num)
                        col_num = self.header_to_col_num[attribute][col_name]
                        try:
                            write_sheet.write(row_num,col_num,lookzone.value_for_attribute(attribute))
                        except:
                            raise IPatchException("Could not write attribute: {0}".format(attribute))
                    current_lookzone_num += 1
                current_lookzone_num = 1


class SlideMetricWriter(WorkbookWriter):
    def __init__(self, readers, output, attrs, listener=None):
        """ Initialize instance of a lookzone writer.
        @Params: readers - Listof WorkbookReader
                output - String: Path to output file
                attrs - (Listof String): Desired Attributes
        """
        WorkbookWriter.__init__(self, readers, output, attrs, listener)

    def __get_header(self, stat):
        """ Returns header for a given stat sheet and lookzone object """
        sheet_name = stat.split('.')[0]
        return sheet_name

    def write_headers(self, readers):
        sheet_count = 0
        for attribute in self.attributes: # Create sheet for each attribute
            sheet_count += 1
            self.sheet_names[sheet_count] = attribute # store original sheet name for Key
            sheet_name = attribute.replace('/', "") # Sheet names do not support slashes
            sheet_name = "%s-%s" % (str(sheet_count), sheet_name)
            if len(sheet_name) > MAX_SHEET_NAME_LENGTH:
              sheet_name = sheet_name[:26]
              sheet_name += '...'
            write_sheet = self.book.add_sheet(sheet_name) # Create the sheet
            self.attribute_sheets[attribute] = write_sheet # store right sheet to get later

            # Set up sheets headers
            write_sheet.write(0, 0, 'SubjectID')
            col_names = set()
            for reader in readers:
                for stat in reader.get_sheet_names():
                    col_name = self.__get_header(stat)
                    col_names.add(col_name)

            col_num = 1
            row_num = 0
            for col_name in col_names:
                try:
                    write_sheet.write(row_num, col_num, col_name)
                except:
                    raise IPatchException("Could not write header: {0}".format(col_name))
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
            for stat in reader.get_sheet_names():
                slidemetric = reader.get_slidemetrics(stat)
                if slidemetric.has_attribute(attribute): # only add if attr exists
                    col_name = self.__get_header(stat)
                    col_num = self.header_to_col_num[attribute][col_name]
                    try:
                        write_sheet.write(row_num,col_num,slidemetric.value_for_attribute(attribute))
                    except:
                        raise IPatchException("Could not write value for attribute: {0}".format(attribute))

