#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore

class FilePathWidget(QtGui.QWidget):

  def __init__(self, file_path, parent):
    QtGui.QWidget.__init__(self)
    self.parent = parent
    self.file_path = file_path
    self.initUI()

  def initUI(self):
    layout = QtGui.QHBoxLayout(self)

    remove_button = QtGui.QPushButton('Remove')
    layout.addWidget(remove_button)
    remove_button.clicked.connect(self.removeFile)

    file_label = QtGui.QLabel(self.file_path)
    layout.addWidget(file_label)


  def removeFile(self):
    self.parent.removeFile(self.file_path)
