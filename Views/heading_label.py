#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore

# Class for labels used as top level headings in app
class HeadingLabel(QtGui.QLabel):
  def __init__(self, label_text):
    # formatted_str = self.format_label(label_text)
    QtGui.QLabel.__init__(self, label_text)
    