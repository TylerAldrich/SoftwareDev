#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from sys import argv
from PyQt4 import QtGui, QtCore
import time
from workbook_reader import WorkbookReader
from configuration import Configuration
from Views.selectAttributes import SelectAttributesWidget
from navigation import NavigationWidget
from heading_label import HeadingLabel
from ipatch_exception import IPatchException
from error_msg_label import ErrorMsgLabel

# Widget that shows a progress bar for loading and reading files to get attributes
class LoadProgress(QtGui.QWidget):
  def __init__(self, window, experimentFilePaths, parent=None):
    super(LoadProgress, self).__init__(parent)
    self.window = window
    self.experimentFilePaths = experimentFilePaths

    layout = QtGui.QVBoxLayout(self)
    # Make a heading label for the top of layout
    heading = HeadingLabel('Please wait...this could take up to a few minutes.')
    layout.addWidget(heading)
    layout.addStretch()
    self.error_msg_label = ErrorMsgLabel('')
    layout.addWidget(self.error_msg_label)
    # Make the progress bar
    self.progressBar = QtGui.QProgressBar(self)
    self.progressBar.setRange(0,100)
    layout.addWidget(self.progressBar)
    # Make progress text to go with progress bar
    self.progress_text_label = QtGui.QLabel('Analyzing input files...', self)
    self.progress_text_label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(self.progress_text_label)
    layout.addStretch()

    # Add naviagation to go back
    navigation = NavigationWidget(self.window, self.goBack, None)
    layout.addWidget(navigation)

    # Connect callbacks for progress
    self.loadingFilesTask = ReadInputFilesThread(experimentFilePaths, self.window.configFilePath)
    self.loadingFilesTask.notifyProgress.connect(self.onProgress)
    self.loadingFilesTask.notifyFinished.connect(self.onFinished)
    self.loadingFilesTask.notifyError.connect(self.onError)

    self.onStart()
    self.error_occured = False

  # Start the task we want to keep progress of
  def onStart(self):
    self.loadingFilesTask.start()

  # Updates UI when progress on task is made
  def onProgress(self, i):
    self.progressBar.setValue(i)
    progressText = "Analyzing input files: " + str(i) + "%"
    self.progress_text_label.setText(progressText)

  # Updates UI when task is complete
  def onFinished(self, i):
    if not self.error_occured:
      # save workbook reader objects to window to use for writing output later
      self.window.all_readers = self.loadingFilesTask.get_all_readers()
      self.showSelectAttributesView()

  # Updates UI when an error was thrown
  def onError(self, e):
    self.error_msg_label.setText(e)
    self.error_occured = True

  # Function to show the screen for selecting attributes
  def showSelectAttributesView(self):
    selectAttributesWidget = SelectAttributesWidget(self.window, self.loadingFilesTask.get_slide_attrs(), self.loadingFilesTask.get_lookzone_attrs(), self.loadingFilesTask.get_saved_slide_attrs(), self.loadingFilesTask.get_saved_lookzone_attrs())
    self.window.setCentralWidget(selectAttributesWidget)

  # Go back to the load file screen
  def goBack(self):
    self.window.showLoadFileView()

# Class to run opening and reading of input files in a separate thread
class ReadInputFilesThread(QtCore.QThread):
  notifyProgress = QtCore.pyqtSignal(int)
  notifyFinished = QtCore.pyqtSignal(int)
  notifyError = QtCore.pyqtSignal(str)

  def __init__(self, experimentFilePaths, configFilePath=None):
    super(ReadInputFilesThread, self).__init__()
    self.all_readers = []
    self.saved_slide = set()
    self.saved_lookzone = set()
    self.slide_attrs = []
    self.lookzone_attrs = []
    self.experimentFilePaths = experimentFilePaths
    self.configFilePath = configFilePath or ''

  def get_all_readers(self):
    return self.all_readers

  def get_saved_slide_attrs(self):
    return list(self.saved_slide)

  def get_saved_lookzone_attrs(self):
    return list(self.saved_lookzone)

  def get_slide_attrs(self):
    return list(self.slide_attrs)

  def get_lookzone_attrs(self):
    return list(self.lookzone_attrs)

  # open and read input Excel files to get attributes
  def load_input_files(self):
    # keep track of how much progress we've made opening/reading files
    opened_files = 0
    num_files = len(self.experimentFilePaths)
    # For each file in the list of files, create a reader and get all of its attributes
    try:
      for filePath in self.experimentFilePaths:
        # First parse the experiment from the saved file path
        reader = WorkbookReader(str(filePath))

        self.all_readers.append(reader)

        # get the lookzone and slide attributes from the reader
        attrs = reader.get_attributes()
        self.lookzone_attrs = attrs['lookzone'];
        self.slide_attrs = attrs['slide'];

        # update progress bar on successful file open
        opened_files += 1
        ratio = opened_files / float(num_files)
        percent_done = ratio * 100

        self.notifyProgress.emit(percent_done)

      # Then if there is a config file to load, load it
      if len(self.configFilePath):
        saved_attrs = Configuration.read_config_file(self.configFilePath)
        self.saved_slide.update(saved_attrs['slide'])
        self.saved_lookzone.update(saved_attrs['lookzone'])
    except IPatchException as e:
      self.notifyError.emit(str(e))

  def run(self):
    self.load_input_files()
    # notify the GUI that the task is done
    self.notifyFinished.emit(1)
