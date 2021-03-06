#!/usr/bin/python
import xlrd
import unittest
from workbook_reader import WorkbookReader
from workbook_writer import WorkbookWriter, SlideMetricWriter, LookzoneWriter

TEST_WORKBOOK_1 = 'sample_inputs/191144- ATT 2 NEG.xlsx'
TEST_WORKBOOK_2 = 'sample_inputs/191150- ATT 2 NEG.xlsx'
TEST_WORKBOOK_3 = 'test_xls/test_sheet_count.xls'

TEST_PARTIAL_1 = 'Test_Files/69420 - TestInputOne.xls'
TEST_PARTIAL_2 = 'Test_Files/42069 - TestInputTwo.xls'

class TestWorkbookMethods(unittest.TestCase):

    def setUp(self):
        self.workbook1 = WorkbookReader(TEST_WORKBOOK_1)
        self.workbook2 = WorkbookReader(TEST_WORKBOOK_2)
        self.workbook3 = WorkbookReader(TEST_WORKBOOK_3)
        self.partial1  = WorkbookReader(TEST_PARTIAL_1)
        self.partial2  = WorkbookReader(TEST_PARTIAL_2)

        self.wb1_sheets = self.workbook1.get_sheet_names()
        self.wb2_sheets = self.workbook2.get_sheet_names()
        self.wb3_sheets = self.workbook3.get_sheet_names()

    def sheets_equal(self, sheet1, sheet2):
        # Internal method:  Determine if the two given sheets are equivalent
        for row in xrange(sheet1.nrows):
            for col in xrange(sheet1.ncols):
                if sheet1.cell_value(row,col) != sheet2.cell_value(row,col):
                    return False
        return True

    def books_equal(self,book1,book2):
        # Internal method: Determine if two workbooks are equal
        book1_sheets = book1.sheets() # list of sheet
        book2_sheets = book2.sheets()

        for i in xrange(len(book1_sheets)):
            if not self.sheets_equal(book1_sheets[i],book2_sheets[i]):
                return False
        return True

    def test_sheets_returned(self):
        # make sure the number of STAT sheets in the workbook is correct.
        # 'correct' numbers found by opening test workbooks in Excel
        workbook1_answer = 36
        workbook2_answer = 36
        workbook3_answer = 3

        workbook1_number = len(self.wb1_sheets)
        workbook2_number = len(self.wb2_sheets)
        workbook3_number = len(self.wb3_sheets)

        self.assertEqual(workbook1_number, workbook1_answer)
        self.assertEqual(workbook2_number, workbook2_answer)
        self.assertEqual(workbook3_number, workbook3_answer)

    def test_get_lookzones(self):
        # make sure lookzones are returned from the workbook for each sheet.
        # there is usually 2-3 lookzones, but always more than 0
        # TODO make sure this is actually true... also maybe its always >=2?
        for sheet in self.wb1_sheets:
            self.assertTrue(self.workbook1.get_lookzones(sheet) > 0)
        for sheet in self.wb2_sheets:
            self.assertTrue(self.workbook2.get_lookzones(sheet) > 0)

    def test_get_slide_metrics(self):
        # make sure slidemetrics are returned from the workbook for each sheet.
        checked_attr = "Percent time tracked" # I believe they all have this
        for sheet in self.wb1_sheets:
            self.assertTrue(self.workbook1.get_slidemetrics(sheet).has_attribute(checked_attr))
        for sheet in self.wb2_sheets:
            self.assertTrue(self.workbook2.get_slidemetrics(sheet).has_attribute(checked_attr))

    def test_get_attributes(self):
        # Test that the hash includes two values: slide and lookzone.
        # Verify that each of these contains a set with the correct
        # number of values
        hsh_len = 2
        slide_len = 37
        lookzone_len = 40

        attrs1 = self.workbook1.get_attributes()
        attrs2 = self.workbook2.get_attributes()
        self.assertEqual(len(attrs1),hsh_len)
        self.assertEqual(len(attrs2),hsh_len)
        self.assertEqual(len(attrs1["slide"]), slide_len)
        self.assertEqual(len(attrs2["slide"]), slide_len)
        self.assertEqual(len(attrs1["lookzone"]), lookzone_len)
        self.assertEqual(len(attrs2["lookzone"]), lookzone_len)

    def test_subject_id(self):
        # make sure the correct subject id is returned
        workbook1_id = self.workbook1.get_subject_id()
        workbook2_id = self.workbook2.get_subject_id()

        self.assertEqual(workbook1_id, '191144')
        self.assertEqual(workbook2_id, '191150')

    def test_write_lookzones(self):
        # Test the output of LookZoneWriter to that of an
        # Expected output file
        output_path = "./Test_Files/TestLookzoneOutput.xls"
        expected_output_path = "./Test_Files/ExpectedLookzoneOutput.xls"
        lookzone_writer = LookzoneWriter([self.workbook1],output_path,["Width", "Appears"])
        lookzone_writer.write_readers()
        expected_book = xlrd.open_workbook(expected_output_path)
        resulting_book = xlrd.open_workbook(output_path)

        self.assertTrue(self.books_equal(expected_book,resulting_book))

    def test_write_slide_metrics(self):
        # Test the output of SlideMetricWriter to that of an
        # Expected output file
        output_path = "./Test_Files/TestSlideMetricOutput.xls"
        expected_output_path = "./Test_Files/ExpectedSlideMetricOutput.xls"
        test_attrs = ["Percent time tracked", "Average pupil area", "Number of fixations"]
        slide_writer = SlideMetricWriter([self.workbook1],output_path,test_attrs)
        slide_writer.write_readers()
        expected_book = xlrd.open_workbook(expected_output_path)
        resulting_book = xlrd.open_workbook(output_path)

        self.assertTrue(self.books_equal(expected_book,resulting_book))

    def test_write_multiple_lookzones(self):
        # Test the output of LookZoneWriter to that of an
        # Expected output file
        output_path = "./Test_Files/TestMultiLookzoneOutput.xls"
        expected_output_path = "./Test_Files/ExpectedMultiLookzoneOutput.xls"
        test_attrs = ["Width", "Appears", "Gazepoint count"]
        lookzone_writer = LookzoneWriter([self.workbook1, self.workbook2], output_path, test_attrs)
        lookzone_writer.write_readers()
        expected_book = xlrd.open_workbook(expected_output_path)
        resulting_book = xlrd.open_workbook(output_path)

        self.assertTrue(self.books_equal(expected_book,resulting_book))

    def test_write_multiple_slide_metrics(self):
        # Test the output of SlideMetricWriter to that of an
        # Expected output file
        output_path = "./Test_Files/TestMultiSlideMetricOutput.xls"
        expected_output_path = "./Test_Files/ExpectedMultiSlideMetricOutput.xls"
        test_attrs = ["Percent time tracked", "Average pupil area", "Number of fixations"]
        slide_writer = SlideMetricWriter([self.workbook1, self.workbook2], output_path, test_attrs)
        slide_writer.write_readers()
        expected_book = xlrd.open_workbook(expected_output_path)
        resulting_book = xlrd.open_workbook(output_path)

        self.assertTrue(self.books_equal(expected_book,resulting_book))

    def test_write_partial_slide_metrics(self):
        # Test output of SlideMetricWrtier when input files dont all contain the same
        # fields, have partially missing data
        output_path = "./Test_Files/TestPartialSlideMetricOutput.xls"
        expected_output_path = "./Test_Files/PartialSlideMetricOutput.xls"
        test_attrs = ["Bananas Per Second", "Grapes Per Second"]
        slide_writer = SlideMetricWriter([self.partial2, self.partial1], output_path, test_attrs)
        slide_writer.write_readers()
        expected_book = xlrd.open_workbook(expected_output_path)
        resulting_book = xlrd.open_workbook(output_path)

        self.assertTrue(self.books_equal(expected_book,resulting_book))

    def test_write_partial_lookzones(self):
        # Test output of LookzoneWrtier when input files dont all contain the same
        # fields, have partially missing data
        output_path = "./Test_Files/TestPartialLookzoneOutput.xls"
        expected_output_path = "./Test_Files/PartialLookzoneOutput.xls"
        test_attrs = ["Apple", "Banana", "Grape", "Orange"]
        lookzone_writer = LookzoneWriter([self.partial2, self.partial1], output_path, test_attrs)
        lookzone_writer.write_readers()
        expected_book = xlrd.open_workbook(expected_output_path)
        resulting_book = xlrd.open_workbook(output_path)

        self.assertTrue(self.books_equal(expected_book,resulting_book))

if __name__ == '__main__':
    unittest.main()
