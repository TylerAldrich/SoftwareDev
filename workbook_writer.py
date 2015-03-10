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

    def write_reader(self, reader):
        """Writes data for individual reader"""
        # Abstract Stub
        return

    def write_headers(self, sheet):
        """ Write header for sheet """
        # TODO: We will have to separate writing header and data in Iteration 2
        pass

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

    def write_reader(self, reader):
        """ Write data for individual reader.
        @Params: reader - WorkbookReader """
        book = xlwt.Workbook() # Create the book
        subject_id = reader.get_subject_id()
        for attribute in self.attributes: # Create sheet for each attribute
            write_sheet = book.add_sheet(attribute) # Create the sheet

            # Set up sheets headers
            write_sheet.write(0, 0, 'SubjectID')
            row_num = 0
            col_num = 1
            current_lookzone_num = 1
            for stat in reader._stat_sheets:
                for lookzone in reader.get_lookzones(stat):
                    sheet_name = stat.name.split('.')[0]

                    if "OUTSIDE" in lookzone.name: # last lookzone of the file
                        col_name = "%s_outside" % sheet_name
                    else:
                        col_name = "%s_LZ%s" % (sheet_name, str(current_lookzone_num))
                        current_lookzone_num += 1

                    write_sheet.write(row_num, col_num, col_name)
                    col_num += 1
                current_lookzone_num = 1

            # Add data for the subject
            write_sheet.write(1, 0, subject_id)
            row_num = 1
            col_num = 1
            for stat in reader._stat_sheets:
                for lookzone in reader.get_lookzones(stat):
                    if lookzone.has_attribute(attribute): # only add if attr exists
                        write_sheet.write(row_num,col_num,lookzone.value_for_attribute(attribute))
                    col_num += 1
        book.save(self.output)

class SlideMetricWriter(WorkbookWriter):
    def __init__(self, readers, output, attrs):
        """ Initialize instance of a lookzone writer.
        @Params: readers - Listof WorkbookReader
                output - String: Path to output file
                attrs - (Listof String): Desired Attributes
        """
        WorkbookWriter.__init__(self,readers,output,attrs)

    def write_reader(self, reader):
        """ Write data for individual reader.
        @Params: reader - WorkbookReader """
        book = xlwt.Workbook() # Create the book
        subject_id = reader.get_subject_id()

        for attribute in self.attributes: # Create sheet for each attribute
            sheet_name = attribute
            if len(sheet_name) > 31:
              sheet_name = sheet_name[:26]
              sheet_name += '...'
            write_sheet = book.add_sheet(sheet_name) # Create the sheet
            #slidemetric = get_slidemetrics(self, write_sheet)
            # Set up sheets headers
            write_sheet.write(0, 0, 'SubjectID')
            row_num = 0
            col_num = 1
            current_slidemetric_num = 1
            for stat in reader._stat_sheets:
                sheet_name = stat.name.split('.')[0]
                col_name =  sheet_name
                current_slidemetric_num += 1
                write_sheet.write(row_num, col_num, col_name)
                col_num += 1
                current_lookzone_num = 1

            # Add data for the subject
            write_sheet.write(1, 0, subject_id)
            row_num = 1
            col_num = 1
            for stat in reader._stat_sheets:
                slidemetric = reader.get_slidemetrics(stat)
                if slidemetric.has_attribute(attribute): # only add if attr exists
                    write_sheet.write(row_num,col_num,slidemetric.value_for_attribute(attribute))
                col_num += 1
        book.save(self.output)
   	
