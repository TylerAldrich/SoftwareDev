#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from autocomplete import CompletionTextEdit 
from navigation import NavigationWidget

# Widget that has user browse for an input file
class SaveFileWidget(QtGui.QWidget):
  procNext = QtCore.pyqtSignal()

  def __init__(self, window, slide_attrs, lookzone_attrs):
    QtGui.QWidget.__init__(self)
    self.window = window
    self.slide_attrs = slide_attrs
    self.lookzone_attrs = lookzone_attrs
    self.initUI()

  def initUI(self):
    # Create initial vertical layout
    layout = QtGui.QVBoxLayout(self)
    layout.setAlignment(QtCore.Qt.AlignTop)

    titleLabel = QtGui.QLabel('Save Slide Metrics File', self)
    subtitleLabel = QtGui.QLabel('Click browse to select a location to save your Slide Metrics data', self)

    # Add two labels to layout
    layout.addWidget(titleLabel)
    layout.addWidget(subtitleLabel)

    # Horizontal layout is for the text box and browse button
    browseFileLayout = QtGui.QHBoxLayout(self)

    # Init text edit box for file path and browse button to
    # find the file.  Set browse button on click to selectFile function
    self.fileTextEdit = QtGui.QLineEdit()
    browseButton = QtGui.QPushButton('Browse')
    browseFileLayout.addWidget(self.fileTextEdit)
    browseFileLayout.addWidget(browseButton)
    browseButton.clicked.connect(self.selectSlideLoc)

    # Add horizontal layout to overall layout
    layout.addLayout(browseFileLayout)
    navigation = NavigationWidget(self.window, None, self.switchViews)
    layout.addWidget(navigation)

  # go to next view to select data attributes
  def switchViews(self):
    fileName = self.fileTextEdit.text()
    self.window.saveSlideMetricsData(fileName, self.slide_attrs)

  # open a file dialog to pick an xlsx input file
  def selectSlideLoc(self):
    save_slide_dialog = QtGui.QFileDialog(self)
    save_slide_dialog.setFileMode(QtGui.QFileDialog.AnyFile)
    save_slide_dialog.setNameFilter(self.tr("Excel (*.xlsx)"))
    save_slide_dialog.setDefaultSuffix("xlsx")
    if save_slide_dialog.exec_():
      files = list(save_slide_dialog.selectedFiles())
      self.fileTextEdit.setText(str(files[0]))
