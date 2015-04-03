#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
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

		## Save Slide metrics section
    if len(self.slide_attrs) > 0:
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

      layout.addLayout(browseFileLayout)

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
      browseLookzoneButton = QtGui.QPushButton('Browse')
      browseLookzoneFileLayout.addWidget(self.lookzoneFileEdit)
      browseLookzoneFileLayout.addWidget(browseLookzoneButton)
      browseLookzoneButton.clicked.connect(self.selectLookzoneLoc)
      # Add horizontal layout to overall layout
      layout.addLayout(browseLookzoneFileLayout)

    ## Save config file section
    configTitleLabel = QtGui.QLabel('Make Configurations File <b>(Optional)</b>', self)
    configSubtitleLabel = QtGui.QLabel('Choose a location to create a configurations file to save these selected attributes for a later experiment', self)
    # TODO: swap previous line with next one once we figure out QLabel wrapping
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

  def writeOutputs(self):
    if len(self.slide_attrs) > 0:
      self.slideFileName = self.fileTextEdit.text()
      # Save slide metrics data
      self.window.saveSlideMetricsData(self.slideFileName, self.slide_attrs)

    if len(self.lookzone_attrs) > 0:
      self.lookzoneFileName = self.lookzoneFileEdit.text()
      # Save Lookzone metrics data
      self.window.saveLookzoneData(self.lookzoneFileName, self.lookzone_attrs)

    self.configFileName = self.configFileEdit.text()
    if len(self.configFileName):
      # Save the attributes in a configuration file
      self.window.saveConfigFile(self.configFileName, self.slide_attrs, self.lookzone_attrs)

  # go back to attribute selection view
  def goBack(self):
    self.window.showSelectAttributesView()
  
  # go to next view to select data attributes
  def switchViews(self):
    self.writeOutputs()
    # We want to clear the chosen attributes when starting a new session
    self.window.clearAttributesState()
    # TODO: We would show progress bar view instead, which would go to Done only on success
    self.window.showDoneView(self.slideFileName, self.lookzoneFileName, self.configFileName)

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

