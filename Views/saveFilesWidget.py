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

		# Save Slide metrics section
    if len(self.slide_attrs) > 0:
      layout.addLayout(self.makeSlideBrowseOutput())

    # Save lookzone section
    if len(self.lookzone_attrs) > 0:
      lookTitleLabel = QtGui.QLabel('<b>Save Lookzone File</b>', self)
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
      browseLookzoneButton.setCursor(QtCore.Qt.PointingHandCursor)
      browseLookzoneFileLayout.addWidget(self.lookzoneFileEdit)
      browseLookzoneFileLayout.addWidget(browseLookzoneButton)
      browseLookzoneButton.clicked.connect(self.selectLookzoneLoc)
      # Add horizontal layout to overall layout
      layout.addLayout(browseLookzoneFileLayout)

      self.lookzone_error_msg_label = QtGui.QLabel('')
      layout.addWidget(self.lookzone_error_msg_label)


    self.showSaveConfigCheckbox = QtGui.QCheckBox('Save attributes to iPatch configuration file')
    self.showSaveConfigCheckbox.stateChanged.connect(self.showSaveConfig)
    self.showSaveConfigCheckbox.setToolTip('Make a <b>*.ipatch</b> config file to automatically save all the saved attributes to use in other sessions')

    layout.addWidget(self.showSaveConfigCheckbox)

    self.saveConfigView = self.makeSaveConfigView()
    layout.addWidget(self.saveConfigView)

    navigation = NavigationWidget(self.window, self.goBack, self.switchViews)
    layout.addWidget(navigation)

  # show or hide the save config file view
  def showSaveConfig(self, state):
    if state == QtCore.Qt.Checked:
      # show the load config file widgets
      self.saveConfigView.show()
    else:
      self.saveConfigView.hide()

  # build save config file view (hidden initially until checked)
  def makeSaveConfigView(self):
    widget = QtGui.QWidget(self)
    # Create initial vertical layout
    layout = QtGui.QVBoxLayout(widget)
    layout.setAlignment(QtCore.Qt.AlignTop)

    configSubtitleLabel = QtGui.QLabel('Choose a location to create a configurations file to save these selected attributes for a later experiment. This is recommended in order to save you time in the future - simply load this configuration file next time you start a session and all your chosen attributes will be pre-selected for you.', self)
    configSubtitleLabel.setWordWrap(True)
    layout.addWidget(configSubtitleLabel)

    # Horizontal layout is for the text box and browse button
    browseConfigFileLayout = QtGui.QHBoxLayout(self)

    self.configFileEdit = QtGui.QLineEdit()
    self.configFileEdit.setText(self.current_directory + 'config.ipatch')
    browseConfigButton = QtGui.QPushButton('Browse')
    browseConfigButton.setCursor(QtCore.Qt.PointingHandCursor)
    browseConfigFileLayout.addWidget(self.configFileEdit)
    browseConfigFileLayout.addWidget(browseConfigButton)
    browseConfigButton.clicked.connect(self.selectConfigLoc)
    # Add horizontal layout to overall layout
    layout.addLayout(browseConfigFileLayout)

    widget.hide()
    return widget

  # make slide metrics output save view
  def makeSlideBrowseOutput(self):
    layout = QtGui.QVBoxLayout(self)

    titleLabel = QtGui.QLabel('<b>Save Slide Metrics File</b>', self)
    subtitleLabel = QtGui.QLabel('Click browse to select a location to save your Slide Metrics data', self)

    # Add two labels to layout
    layout.addWidget(titleLabel)
    layout.addWidget(subtitleLabel)

    # Horizontal layout is for the text box and browse button
    browseFileLayout = QtGui.QHBoxLayout(self)
    # Init text edit box for file path and browse button
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

  # write the output files
  def writeOutputs(self):
    output_file_paths = {}
    output_file_paths['slide_metrics_path'] = ''
    output_file_paths['lookzone_data_path'] = ''
    output_file_paths['config_file_path'] = ''
    if len(self.slide_attrs):
      output_file_paths['slide_metrics_path'] = self.slideFileName

    if len(self.lookzone_attrs):
      output_file_paths['lookzone_data_path'] = self.lookzoneFileName

    if len(self.configFileName) and self.saveConfigView.isVisible():
      output_file_paths['config_file_path'] = self.configFileName

    self.window.showWriteProgressView(output_file_paths, self.slide_attrs, self.lookzone_attrs)

  # go back to attribute selection view
  def goBack(self):
    self.window.showSelectAttributesView()

  # check that input paths are valid
  def validateInputs(self):
    foundError = False

    regex_format = re.compile(".*\.xls$")

    if len(self.slide_attrs):
      self.slideFileName = self.fileTextEdit.text()

      if not len(self.slideFileName) or not regex_format.match(self.slideFileName):
        self.slide_error_msg_label.setText('<b style="color:red">You must select a valid output location for Slide Metrics.</b>')
        foundError = True

      if os.path.isfile(self.slideFileName):
        file_split = self.slideFileName.split('\\')
        file_name = file_split[-1]
        foundError = self.showOverwriteMessage(file_name)

        # If they selected to not overwrite the file, return immediately
        if foundError:
          return not foundError

    if len(self.lookzone_attrs):
      self.lookzoneFileName = self.lookzoneFileEdit.text()

      if not len(self.lookzoneFileName) or not regex_format.match(self.lookzoneFileName):
        self.lookzone_error_msg_label.setText('<b style="color:red">You must select a valid output location for LookZone Data.</b>')
        foundError = True

      if os.path.isfile(self.lookzoneFileName):
        file_split = self.lookzoneFileName.split('\\')
        file_name = file_split[-1]
        foundError = self.showOverwriteMessage(file_name)

        # If they selected to not overwrite the file, return immediately
        if foundError:
          return not foundError

    self.configFileName = self.configFileEdit.text()

    if self.saveConfigView.isVisible() and len(self.configFileName):
      if os.path.isfile(self.configFileName):
        file_split = self.configFileName.split('\\')
        file_name = file_split[-1]
        foundError = self.showOverwriteMessage(file_name)

        # If they selected to not overwrite the file, return immediately
        if foundError:
          return not foundError

    return not foundError

  # Show error message for file already saved in that location
  def showOverwriteMessage(self, file_name):
    message = file_name + ' Already exists in this location, do you want to overwrite it?'
    reply = QtGui.QMessageBox.question(self, 'Message',
      message, QtGui.QMessageBox.Yes |
      QtGui.QMessageBox.No, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.No:
      return True
    else:
      return False

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

