#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from filePathWidget import FilePathWidget
from navigation import NavigationWidget
from heading_label import HeadingLabel
from empty_list_label import EmptyListLabel
from error_msg_label import ErrorMsgLabel

# Widget that has user browse for an input file
class LoadFileWidget(QtGui.QWidget):
  guiStateKey = 'loadFile'
  procNext = QtCore.pyqtSignal()

  def __init__(self, window):
    QtGui.QWidget.__init__(self)
    self.window = window
    self.file_names = []
    self.initUI()
    self.load_state()
    self.updateListOfFiles()

  def initUI(self):
    # Create initial vertical layout
    layout = QtGui.QVBoxLayout(self)
    layout.setAlignment(QtCore.Qt.AlignTop)

    title_label = HeadingLabel('Choose Experiment Files')
    subtitle_label = QtGui.QLabel('Click browse to select at least one experiment (Excel file). Shift or Ctrl click to select multiple.', self)
    title_label.setWordWrap(True)
    subtitle_label.setWordWrap(True)

    # Add two labels to layout
    layout.addWidget(title_label)
    layout.addWidget(subtitle_label)

    # Horizontal layout is for the text box and browse button
    browse_file_layout = QtGui.QHBoxLayout(self)

    # Init text edit box for file path and browse button to
    # find the file.  Set browse button on click to selectFile function
    self.fileTextEdit = QtGui.QLineEdit()
    browse_button = QtGui.QPushButton('Browse')
    browse_file_layout.addWidget(self.fileTextEdit)
    browse_file_layout.addWidget(browse_button)
    browse_button.clicked.connect(self.selectFile)

    # Add horizontal layout to overall layout
    layout.addLayout(browse_file_layout)

    # Add vertical layout that will contain list of files
    scroll_view = QtGui.QScrollArea(self)
    scroll_view.setWidgetResizable(True)
    scroll_view_contents = QtGui.QWidget(scroll_view)
    scroll_view.setWidget(scroll_view_contents)

    self.files_list_layout = QtGui.QVBoxLayout(scroll_view_contents)
    self.no_files_label = EmptyListLabel('No input files yet')
    self.files_list_layout.addWidget(self.no_files_label)
    layout.addWidget(scroll_view)

    # Section for clear all buttons and add more files button
    add_remove_layout = QtGui.QHBoxLayout(self)
    self.clear_all_button = QtGui.QPushButton('Clear All')
    self.clear_all_button.clicked.connect(self.clearAllFiles)
    self.add_file_button = QtGui.QPushButton('Add Another File')
    self.add_file_button.clicked.connect(self.addAnotherFile)
    self.clear_all_button.hide()
    self.add_file_button.hide()

    # Add buttons to layout and layout to view
    add_remove_layout.addWidget(self.clear_all_button)
    add_remove_layout.addWidget(self.add_file_button)
    layout.addLayout(add_remove_layout)

    self.showLoadConfigCheckbox = QtGui.QCheckBox('Load attributes from iPatch configuration file')
    self.showLoadConfigCheckbox.stateChanged.connect(self.showLoadConfig)

    layout.addWidget(self.showLoadConfigCheckbox)

    self.loadConfig = self.makeLoadConfig()
    layout.addWidget(self.loadConfig)

    self.error_msg_label = ErrorMsgLabel('')
    layout.addWidget(self.error_msg_label)

    # Add navigation to layout
    navigation = NavigationWidget(self.window, None, self.switchViews)
    layout.addWidget(navigation)

  def selectConfigFile(self):
    self.configFileTextEdit.setText(QtGui.QFileDialog.getOpenFileName())

  def makeLoadConfig(self):
    widget = QtGui.QWidget(self)
    # Create initial vertical layout
    layout = QtGui.QVBoxLayout(widget)
    layout.setAlignment(QtCore.Qt.AlignTop)

    subtitleLabel = QtGui.QLabel('Click browse to select a previously saved configurations file', self)
    layout.addWidget(subtitleLabel)

    # Horizontal layout is for the text box and browse button
    browseFileLayout = QtGui.QHBoxLayout(self)

    # Init text edit box for file path and browse button to
    # find the file.  Set browse button on click to selectFile function
    self.configFileTextEdit = QtGui.QLineEdit()
    if len(self.window.configFilePath):
      self.configFileTextEdit.setText(self.window.configFilePath)
    browseButton = QtGui.QPushButton('Browse')
    browseFileLayout.addWidget(self.configFileTextEdit)
    browseFileLayout.addWidget(browseButton)
    browseButton.clicked.connect(self.selectConfigFile)

    # Add horizontal layout to overall layout
    layout.addLayout(browseFileLayout)
    widget.hide()
    return widget

  def showLoadConfig(self, state):
    if state == QtCore.Qt.Checked:
      # show the load config file widgets
      self.loadConfig.show()
    else:
      self.loadConfig.hide()

  # go to next view to select data attributes
  def switchViews(self):
    # TODO: Make application open file path at this point and validate input so we can show error on this screen
    self.window.configFilePath = '' # reset config file path just in case it was unchecked
    if len(self.file_names):
      # self.window.showLoadConfigView(self.file_names)
      configFilePath = self.configFileTextEdit.text()
      if len(configFilePath) and self.showLoadConfigCheckbox.isChecked():
        self.window.configFilePath = configFilePath

      self.save_state()
      self.window.showSelectAttributesView(self.file_names)
    else:
      self.error_msg_label.setText('No input file was selected. Please choose at least one input file to continue.')

  # open a file dialog to pick an xlsx input file
  def selectFile(self):
    self.clearErrorMessage()

    self.file_names = self.showFileDialog()

    self.fileTextEdit.setText("")
    self.updateListOfFiles()

  # Method to show a file dialog and returns a list of chosen file names
  def showFileDialog(self):
    select_dialog = QtGui.QFileDialog(self)
    select_dialog.setFileMode(QtGui.QFileDialog.AnyFile)
    files = map(str, select_dialog.getOpenFileNames())
    return files

  # Method to update the view of all the files
  def updateListOfFiles(self):
    # First clear out all views already there
    for i in reversed(range(self.files_list_layout.count())):
      self.files_list_layout.itemAt(i).widget().setParent(None)

    # Then add each file path to the view
    for file_path in self.file_names:
      file_label = FilePathWidget(file_path, self)
      self.files_list_layout.addWidget(file_label)

    # Check length of file list, if none, hide clear all and add buttons
    if len(self.file_names) == 0:
      self.clear_all_button.hide()
      self.add_file_button.hide()
      self.files_list_layout.addWidget(self.no_files_label)
    else:
      self.clear_all_button.show()
      self.add_file_button.show()

  # Method to remove a given file name
  def removeFile(self, file_path):
    self.clearErrorMessage()

    # Remove the file name from the list and update the view
    self.file_names.remove(file_path)
    self.updateListOfFiles()

  # Method to clear all of the added files
  def clearAllFiles(self):
    self.clearErrorMessage()

    # Clear out the list of file names then update the view
    del self.file_names[:]
    self.updateListOfFiles()

  # Method to add another file to the already chosen list
  def addAnotherFile(self):
    self.clearErrorMessage()

    added_files = self.showFileDialog()

    # If the added file has already been added, yell at them
    for added_file in added_files:
      if added_file in self.file_names:
        # throw error
        self.error_msg_label.setText('File has already been added, cannot add same file twice.')
      else:
        self.file_names.append(added_file)

    # update the view of course!
    self.updateListOfFiles()

  # Method to just clear out the error message after another click occurs
  def clearErrorMessage(self):
    self.error_msg_label.setText('')

  # Method to show an error occured while opening and parsing the file
  def show_error_on_file(self, e):
    self.error_msg_label.setText(e)

  # Method to save the current state of the screen
  def save_state(self):
    self.window.guiState[self.__class__.guiStateKey]['chosenFiles'] = self.file_names
    self.window.guiState[self.__class__.guiStateKey]['configFile'] = self.configFileTextEdit.text()

  # Method to load the current state of the view if there is one
  def load_state(self):
    if not self.window.guiState.has_key(self.__class__.guiStateKey):
      self.window.guiState[self.__class__.guiStateKey] = { 'chosenFiles': self.file_names, 'configFile': self.configFileTextEdit.text() }

    self.file_names = self.window.guiState[self.__class__.guiStateKey]['chosenFiles']
    self.configFileTextEdit.setText(self.window.guiState[self.__class__.guiStateKey]['configFile'])

  # Method to clear out the state
  def clear_state(self):
    if self.window.guiState.has_key(self.__class__.guiStateKey):
      del self.window.guiState[self.__class__.guiStateKey]
