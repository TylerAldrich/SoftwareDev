#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore

# Class for labels used as error messages in GUI
class ErrorMsgLabel(QtGui.QLabel):
  def __init__(self, label_text):
    QtGui.QLabel.__init__(self, label_text)
    