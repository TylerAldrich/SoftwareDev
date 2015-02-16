#!/usr/bin/python
import xlrd

workbook = xlrd.open_workbook('sample_inputs/191137- ATT 2 NEG.xlsx')
print workbook.sheet_names()
