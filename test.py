#!/usr/bin/python
import xlrd
import unittest
from workbook import Workbook

TEST_WORKBOOK_1 = 'sample_inputs/191144- ATT 2 NEG.xlsx'
TEST_WORKBOOK_2 = 'sample_inputs/191150- ATT 2 NEG.xlsx'
TEST_WORKBOOK_3 = 'test_xls/test_sheet_count.xls'

class TestWorkbookMethods(unittest.TestCase):

    def setUp(self):
        self.workbook1 = Workbook(TEST_WORKBOOK_1)
        self.workbook2 = Workbook(TEST_WORKBOOK_2)
        self.workbook3 = Workbook(TEST_WORKBOOK_3)

        self.wb1_sheets = self.workbook1.get_sheets()
        self.wb2_sheets = self.workbook2.get_sheets()
        self.wb3_sheets = self.workbook3.get_sheets()

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

    def test_grab_attributes(self):
        # make sure the number of attributes is correct
        hsh_len = 2
        slide_len = 38
        lookzone_len = 120

        attrs1 = self.workbook1.grab_attributes()
        attrs2 = self.workbook2.grab_attributes()
        self.assertEqual(len(attrs1),hsh_len)
        self.assertEqual(len(attrs2),hsh_len)
        self.assertEqual(len(attrs1["slide"]), slide_len)
        self.assertEqual(len(attrs2["slide"]), slide_len)
        self.assertEqual(len(attrs1["lookzone"]), lookzone_len)
        self.assertEqual(len(attrs2["lookzone"]), lookzone_len)


if __name__ == '__main__':
    unittest.main()
