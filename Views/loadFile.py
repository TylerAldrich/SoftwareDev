#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from filePathWidget import FilePathWidget
from navigation import NavigationWidget

# Widget that has user browse for an input file
class LoadFileWidget(QtGui.QWidget):
  procNext = QtCore.pyqtSignal()

  def __init__(self, window):
    QtGui.QWidget.__init__(self)
    self.window = window
    self.initUI()

  def initUI(self):
    # Create initial vertical layout
    layout = QtGui.QVBoxLayout(self)
    layout.setAlignment(QtCore.Qt.AlignTop)

    titleLabel = QtGui.QLabel('Upload Excel File', self)
    subtitleLabel = QtGui.QLabel('Click browse to select an experiment to upload', self)

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
    browseButton.clicked.connect(self.selectFile)

    # Add horizontal layout to overall layout
    layout.addLayout(browseFileLayout)

    # Add vertical layout that will contain list of files
    self.files_list_layout = QtGui.QVBoxLayout(self)
    layout.addLayout(self.files_list_layout)

    self.errorMsgLabel = QtGui.QLabel('')
    layout.addWidget(self.errorMsgLabel)

    # Add navigation to layout
    navigation = NavigationWidget(self.window, None, self.switchViews)
    layout.addWidget(navigation)

  # go to next view to select data attributes
  def switchViews(self):
    # TODO: Make application open file path at this point and validate input so we can show error on this screen
    if len(self.file_names):
      self.window.showLoadConfigView(self.file_names)
    else:
      self.errorMsgLabel.setText('<b style="color:red">No input file was selected. Please choose an input Excel file to continue.</b>')

  # open a file dialog to pick an xlsx input file
  def selectFile(self):
    select_dialog = QtGui.QFileDialog(self)
    select_dialog.setFileMode(QtGui.QFileDialog.AnyFile)
    self.file_names = map(str, select_dialog.getOpenFileNames())

    # If there is only one file, fill the text box with the path
    # otherwise show all files below text box
    if len(self.file_names) > 1:
      self.fileTextEdit.setText("")
      self.updateListOfFiles()
    else:
      self.fileTextEdit.setText(self.file_names[0])

  # Method to update the view of all the files
  def updateListOfFiles(self):
    # First clear out all views already there
    for i in reversed(range(self.files_list_layout.count())):
      self.files_list_layout.itemAt(i).widget().setParent(None)

    # Then add each file path to the view
    for file_path in self.file_names:
      file_label = FilePathWidget(file_path, self)
      self.files_list_layout.addWidget(file_label)

  # Method to remove a given file name
  def removeFile(self, file_path):
    # Remove the file name from the list and update the view
    self.file_names.remove(file_path)
    self.updateListOfFiles()
