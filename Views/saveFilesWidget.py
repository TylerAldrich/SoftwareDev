#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re, os
from sys import argv
from PyQt4 import QtGui, QtCore
from navigation import NavigationWidget

# Widget that has user browse for an input file
class SaveFileWidget(QtGui.QWidget):
  procNext = QtCore.pyqtSignal()

  def __init__(self, window, slide_attrs, lookzone_attrs):
    QtGui.QWidget.__init__(self)
    self.window = window
    self.slide_attrs = slide_attrs
    self.lookzone_attrs = lookzone_attrs
    self.slideFileName = ''
    self.lookzoneFileName = ''
    self.configFileName = ''
    self.initUI()

  def initUI(self):
    # Create initial vertical layout
    layout = QtGui.QVBoxLayout(self)
    layout.setAlignment(QtCore.Qt.AlignTop)

    # Get the current directory to prepopulate the file lines
    self.current_directory = os.path.join(os.path.expanduser('~'), 'Desktop') + '/'

		## Save Slide metrics section
    if len(self.slide_attrs) > 0:
      layout.addLayout(self.makeSlideBrowseOutput())

    ## Save lookzone section
    if len(self.lookzone_attrs) > 0:
      lookTitleLabel = QtGui.QLabel('Save Lookzone File', self)
      lookSubtitleLabel = QtGui.QLabel('Click browse to select a location to save your LookZone data', self)

      # Add two labels to layout
      layout.addWidget(lookTitleLabel)
      layout.addWidget(lookSubtitleLabel)

      # Horizontal layout is for the text box and browse button
      browseLookzoneFileLayout = QtGui.QHBoxLayout(self)

      # Init text edit box for file path and browse button to
      # find the file.  Set browse button on click to selectFile function
      self.lookzoneFileEdit = QtGui.QLineEdit()
      self.lookzoneFileEdit.setText(self.current_directory + 'lookzone.xls')
      browseLookzoneButton = QtGui.QPushButton('Browse')
      browseLookzoneFileLayout.addWidget(self.lookzoneFileEdit)
      browseLookzoneFileLayout.addWidget(browseLookzoneButton)
      browseLookzoneButton.clicked.connect(self.selectLookzoneLoc)
      # Add horizontal layout to overall layout
      layout.addLayout(browseLookzoneFileLayout)

      self.lookzone_error_msg_label = QtGui.QLabel('')
      layout.addWidget(self.lookzone_error_msg_label)

    ## Save config file section
    configTitleLabel = QtGui.QLabel('Make Configurations File <b>(Optional)</b>', self)
    configSubtitleLabel = QtGui.QLabel('Choose a location to create a configurations file to save these selected attributes for a later experiment', self)
    # configSubtitleLabel = QtGui.QLabel('Choose a location to create a configurations file to save these selected attributes for a later experiment. This is recommended in order to save you time in the future - simply load this configuration file next time you start a session and all your chosen attributes will be pre-selected for you.', self)

    # Add two labels to layout
    layout.addWidget(configTitleLabel)
    layout.addWidget(configSubtitleLabel)

    # Horizontal layout is for the text box and browse button
    browseConfigFileLayout = QtGui.QHBoxLayout(self)

    # Init text edit box for file path and browse button to
    # find the file.  Set browse button on click to selectFile function
    self.configFileEdit = QtGui.QLineEdit()
    browseConfigButton = QtGui.QPushButton('Browse')
    browseConfigFileLayout.addWidget(self.configFileEdit)
    browseConfigFileLayout.addWidget(browseConfigButton)
    browseConfigButton.clicked.connect(self.selectConfigLoc)
    # Add horizontal layout to overall layout
    layout.addLayout(browseConfigFileLayout)

    navigation = NavigationWidget(self.window, self.goBack, self.switchViews)
    layout.addWidget(navigation)

  def makeSlideBrowseOutput(self):
    layout = QtGui.QVBoxLayout(self)

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
    self.fileTextEdit.setText(self.current_directory + 'slide.xls')
    browseButton = QtGui.QPushButton('Browse')
    browseFileLayout.addWidget(self.fileTextEdit)
    browseFileLayout.addWidget(browseButton)
    browseButton.clicked.connect(self.selectSlideLoc)

    layout.addLayout(browseFileLayout)

    self.slide_error_msg_label = QtGui.QLabel('')
    layout.addWidget(self.slide_error_msg_label)

    return layout

  def writeOutputs(self):
    output_file_paths = {}
    output_file_paths['slide_metrics_path'] = ''
    output_file_paths['lookzone_data_path'] = ''
    output_file_paths['config_file_path'] = ''
    if len(self.slide_attrs):
      output_file_paths['slide_metrics_path'] = self.slideFileName

    if len(self.lookzone_attrs):
      output_file_paths['lookzone_data_path'] = self.lookzoneFileName

    self.configFileName = self.configFileEdit.text()
    if len(self.configFileName):
      output_file_paths['config_file_path'] = self.configFileName

    self.window.showWriteProgressView(output_file_paths, self.slide_attrs, self.lookzone_attrs)

  # go back to attribute selection view
  def goBack(self):
    self.window.showSelectAttributesView()

  def validateInputs(self):
    foundError = False

    regex_format = re.compile(".*\.xls$")
    if len(self.slide_attrs):
      self.slideFileName = self.fileTextEdit.text()

      if not len(self.slideFileName) or not regex_format.match(self.slideFileName):
        self.slide_error_msg_label.setText('<b style="color:red">You must select a valid output location for Slide Metrics.</b>')
        foundError = True

      if os.path.isfile(self.slideFileName):


    if len(self.lookzone_attrs):
      self.lookzoneFileName = self.lookzoneFileEdit.text()

      if not len(self.lookzoneFileName) or not regex_format.match(self.lookzoneFileName):
        self.lookzone_error_msg_label.setText('<b style="color:red">You must select a valid output location for LookZone Data.</b>')
        foundError = True

    return not foundError

  # go to next view to select data attributes
  def switchViews(self):
    if self.validateInputs():
      self.writeOutputs()

  # open a file dialog to pick an xlsx input file for lookzone data
  def selectLookzoneLoc(self):
    save_lookzone_dialog = self.createSaveExcelDialog()
    if save_lookzone_dialog.exec_():
      files = list(save_lookzone_dialog.selectedFiles())
      self.lookzoneFileEdit.setText(str(files[0]))

  # open a file dialog to choose a location for the configurations file
  def selectConfigLoc(self):
    save_config_dialog = QtGui.QFileDialog(self)
    save_config_dialog.setFileMode(QtGui.QFileDialog.AnyFile)
    save_config_dialog.setNameFilter(self.tr("iPatch (*.ipatch)"))
    save_config_dialog.setDefaultSuffix("ipatch")
    if save_config_dialog.exec_():
      files = list(save_config_dialog.selectedFiles())
      self.configFileEdit.setText(str(files[0]))

  # open a file dialog to pick an xlsx input file for slide data
  def selectSlideLoc(self):
    save_slide_dialog = self.createSaveExcelDialog()
    if save_slide_dialog.exec_():
      files = list(save_slide_dialog.selectedFiles())
      self.fileTextEdit.setText(str(files[0]))

  # Function to create a save dialog
  def createSaveExcelDialog(self):
    save_dialog = QtGui.QFileDialog(self)
    save_dialog.setFileMode(QtGui.QFileDialog.AnyFile)
    save_dialog.setNameFilter(self.tr("Excel (*.xls)"))
    save_dialog.setDefaultSuffix("xls")
    return save_dialog

  # Function to show the user an error occured while saving the type of file
  def set_error(self, attr_type, e):
    if attr_type == 'slide':
      self.slide_error_msg_label.setText(e)
    else:
      self.lookzone_error_msg_label.setText(e)

