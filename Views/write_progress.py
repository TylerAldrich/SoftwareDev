#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from sys import argv
from PyQt4 import QtGui, QtCore
import time
from workbook_writer import SlideMetricWriter, LookzoneWriter
from configuration import Configuration
from Views.selectAttributes import SelectAttributesWidget
from heading_label import HeadingLabel
from ipatch_exception import IPatchException

# Widget that shows a progress bar for loading and reading files to get attributes
class WriteProgress(QtGui.QWidget):
  def __init__(self, window, output_file_paths, slide_attrs, lookzone_attrs, parent=None):
    super(WriteProgress, self).__init__(parent)
    self.window = window
    self.output_file_paths = output_file_paths
    self.slide_attrs = slide_attrs
    self.lookzone_attrs = lookzone_attrs

    layout = QtGui.QVBoxLayout(self)
    # Make a heading label for the top of layout
    heading = HeadingLabel('Please wait...this could take up to a few minutes.')
    layout.addWidget(heading)
    layout.addStretch()
    # Make the progress bar
    self.progressBar = QtGui.QProgressBar(self)
    self.progressBar.setRange(0,100)
    layout.addWidget(self.progressBar)
    # Make progress text to go with progress bar
    self.progress_text_label = QtGui.QLabel('Writing Slide Metric data...', self)
    self.progress_text_label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(self.progress_text_label)
    layout.addStretch()

    # Connect callbacks for progress
    self.writingFilesTask = WriteOutputFilesThread(self.window.all_readers, self.output_file_paths, self.slide_attrs, self.lookzone_attrs)
    self.writingFilesTask.notifyProgress.connect(self.onSlideProgress)
    self.writingFilesTask.notifyFinished.connect(self.onFinished)

    self.onStart()

  # Start the task we want to keep progress of
  def onStart(self):
    self.writingFilesTask.start()

  # Updates UI on progress in writing slide metric data 
  def onSlideProgress(self, i):
    self.progressBar.setValue(i)
    progressText = "Writing Slide Metric data: " + str(i) + "%"
    self.progress_text_label.setText(progressText)

  # Updates UI on progress in writing lookzone data 
  def onLookzoneProgress(self, i):
    self.progressBar.setValue(i)
    progressText = "Writing LookZone data: " + str(i) + "%"
    self.progress_text_label.setText(progressText)

  # Updates UI when task is complete
  def onFinished(self, i):
    if (i == 1):
      # done writing slide metrics, reset progress bar to show writing lookzone data
      self.progressBar.setValue(0)
      self.progress_text_label.setText('Writing LookZone data...')
      self.writingFilesTask.notifyProgress.disconnect()
      self.writingFilesTask.notifyProgress.connect(self.onLookzoneProgress)
    if (i == 2):
      # done writing lookzone data
      # We want to clear the chosen attributes when starting a new session
      self.window.clearGuiState()
      # show the final success screen
      self.window.showDoneView(self.output_file_paths['slide_metrics_path'], self.output_file_paths['lookzone_data_path'], self.output_file_paths['config_file_path'])

# Class to run opening and reading of input files in a separate thread
class WriteOutputFilesThread(QtCore.QThread):
  notifyProgress = QtCore.pyqtSignal(int)
  notifyFinished = QtCore.pyqtSignal(int)

  def __init__(self, all_readers, output_file_paths, slide_attrs, lookzone_attrs):
    super(WriteOutputFilesThread, self).__init__()
    self.slide_metrics_path = ''
    self.lookzone_data_path = ''
    self.slide_attrs = slide_attrs
    self.lookzone_attrs = lookzone_attrs

    self.all_readers = all_readers
    self.num_readers = len(self.all_readers)

    if output_file_paths.has_key('slide_metrics_path'):
      self.slide_metrics_path = output_file_paths['slide_metrics_path']
    if output_file_paths.has_key('lookzone_data_path'):
      self.lookzone_data_path = output_file_paths['lookzone_data_path']
    if output_file_paths.has_key('config_file_path'):
      self.config_file_path = output_file_paths['config_file_path']

  # Function to save slide metric attributes
  def write_slide_metrics(self):
    if len(self.slide_attrs) > 0:
      try:
        slide_writer = SlideMetricWriter(self.all_readers, self.slide_metrics_path, self.slide_attrs, self)
        slide_writer.write_readers()
      except IPatchException as e:
        print('error in write_slide_metrics')
        # self.save_files_view.set_error('slide', str(e))

  # Function to save lookzone attributes
  def write_lookzone_data(self):
    if len(self.lookzone_attrs) > 0:
      try:
        lookzone_writer = LookzoneWriter(self.all_readers, self.lookzone_data_path, self.lookzone_attrs, self)
        lookzone_writer.write_readers()
      except IPatchException as e:
        print('error in write_lookzone_data')
        # self.save_files_view.set_error('lookzone', str(e))
  
  # Function to save the configuration file
  def write_config_file(self):
    if len(self.config_file_path) > 0:
      config = Configuration(self.config_file_path, self.lookzone_attrs, self.slide_attrs)
      config.print_config_file()
  
  # Called by workbook writer when we want to indicate progress by saying how many rows we've finished writing
  def notifier(self, num_done):
    ratio = num_done / float(self.num_readers)
    percent_done = ratio * 100
    self.notifyProgress.emit(percent_done)

  def run(self):
    self.write_slide_metrics()
    # notify the GUI that we are done writing slide metrics
    self.notifyFinished.emit(1)
    self.write_lookzone_data()
    self.write_config_file()
    # notify the GUI that we are done writing lookzone
    self.notifyFinished.emit(2)
