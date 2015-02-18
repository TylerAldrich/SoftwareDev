#!/usr/bin/python
import xlrd
import sys


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

    def generate_contents(self, sheet):
        """ Put the contents of each cell into a dictionary.
            If the cell name is already in the dict, add to a list
            of values for that statistic. """
        # XXX TODO - Need to keep track of where the values in each
        # list come from (different lookzones and shit)

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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Must give this program a workbook to open"
        sys.exit(1)

    workbook_file = sys.argv[1]
    workbook = Workbook(workbook_file)

    stat_sheets = workbook.get_sheets()
    data_dict = workbook.get_data(stat_sheets[0])
    print data_dict
