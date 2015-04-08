#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore

# Class for label used as placeholder in empty list view
class EmptyListLabel(QtGui.QLabel):
  def __init__(self, label_text):
    QtGui.QLabel.__init__(self, label_text)
    self.setAlignment(QtCore.Qt.AlignCenter)
