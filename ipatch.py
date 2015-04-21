#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from sys import argv
from PyQt4 import QtGui, QtCore
from Views.selectAttributes import SelectAttributesWidget
from Views.loadFile import LoadFileWidget
from Views.saveFilesWidget import SaveFileWidget
from Views.sessionDoneWidget import SessionDoneWidget
from Views.loadConfig import LoadConfigWidget
from Views.slideMetricsAttrLists import SlideMetricsAttrListsComponent
from Views.lookzoneAttrLists import LookzoneAttrListsComponent
from Views.load_progress import LoadProgress
from Views.write_progress import WriteProgress
from workbook_reader import WorkbookReader
from workbook_writer import SlideMetricWriter, LookzoneWriter
from configuration import Configuration
from ipatch_exception import IPatchException

# The main class that starts and enables flow through
# the different views of the application
class Window(QtGui.QMainWindow):

  def __init__(self):
    super(Window, self).__init__()
    self.appName = 'iPatch'
    self.appVersion = 'v1.0'
    self.appWidth = 700
    self.appHeight = 500
    # save a Dict that caches the state of certain GUI elements
    self.guiState = {}
    self.attribute_cache = {}
    # save the reader objects from reading input files
    self.all_readers = []
    # the config file should persist through views so save it in window
    self.configFilePath = ''
    self.set_style()
    self.initUI()

  def initUI(self):
    self.resize(self.appWidth, self.appHeight)
    self.center()
    self.setWindowTitle(self.appName + ' ' + self.appVersion)
    self.setWindowIcon(QtGui.QIcon('eyecon.png'))
    self.show()
    # Load up the Load file view
    self.showLoadFileView()

    # Add a menu bar where the user can start over or quit
    menu = self.menuBar().addMenu('File')
    menu.addAction('New Session', self.start_new)
    menu.addAction('Quit', self.closeApp)

  def set_style(self):
    try:
        current_path = sys._MEIPASS
    except Exception:
        current_path = os.path.dirname(os.path.realpath(__file__))
    stylesheet = os.path.join(current_path, 'ipatch_style.stylesheet')
    f = open(stylesheet, 'r')
    self.style_data = f.read()
    f.close()
    self.setStyleSheet(self.style_data)

  # Function to center the window on screen
  def center(self):
    qr = self.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

  # Function to show dialog for when window is closed
  def closeEvent(self, event):
    reply = QtGui.QMessageBox.question(self, 'Message',
      "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
      QtGui.QMessageBox.No, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
      event.accept()
    else:
      event.ignore()

  # close the application window
  def closeApp(self):
    self.close()

  # clear state and start a new session
  def start_new(self):
    reply = QtGui.QMessageBox.question(self, 'Message',
      "Are you sure you want to start a new session?", QtGui.QMessageBox.Yes |
      QtGui.QMessageBox.No, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
      self.clearGuiState()
      self.showLoadFileView()

  # Function to show the screen for selecting a configuration file
  def showLoadConfigView(self, experimentFilePaths=None):
    if experimentFilePaths:
      self.experimentFilePaths = experimentFilePaths
    loadConfig = LoadConfigWidget(self)
    self.setCentralWidget(loadConfig)

  # Function to show the screen for loading a new excel file
  def showLoadFileView(self):
    self.load_file_view = LoadFileWidget(self)
    self.setCentralWidget(self.load_file_view)

  # Function to show load inputs progress bar
  def showLoadProgressView(self, experimentFilePaths):
    self.setCentralWidget(LoadProgress(self, experimentFilePaths))

  # Function to show the screen for selecting attributes (only on going back from save view)
  def showSelectAttributesView(self):
    selectAttributesWidget = SelectAttributesWidget(self, self.attribute_cache['slide_attrs'], self.attribute_cache['lookzone_attrs'], self.attribute_cache['saved_slide_attrs'], self.attribute_cache['saved_lookzone_attrs'])
    self.setCentralWidget(selectAttributesWidget)

  # Function to show write outputs progress bar
  def showWriteProgressView(self, output_file_paths, slide_attrs, lookzone_attrs):
    self.setCentralWidget(WriteProgress(self, output_file_paths, slide_attrs, lookzone_attrs))

  # Function to show the save file screen
  def showSaveFilesView(self, slide_attrs, lookzone_attrs):
    self.save_files_view = SaveFileWidget(self, slide_attrs, lookzone_attrs)
    self.setCentralWidget(self.save_files_view)

  def showDoneView(self, slideFilePath, lookzoneFilePath, configFilePath):
    doneView = SessionDoneWidget(self, slideFilePath, lookzoneFilePath, configFilePath)
    self.setCentralWidget(doneView)

  # Function to save slide metric attributes
  def saveSlideMetricsData(self, filePath, attrs):
    if len(attrs) > 0:
      try:
        slide_writer = SlideMetricWriter(self.all_readers, filePath, attrs)
        slide_writer.write_readers()
      except IPatchException as e:
        self.save_files_view.set_error('slide', str(e))

  # Function to save lookzone attributes
  def saveLookzoneData(self, filePath, attrs):
    if len(attrs) > 0:
      try:
        lookzone_writer = LookzoneWriter(self.all_readers, filePath, attrs)
        lookzone_writer.write_readers()
      except IPatchException as e:
        self.save_files_view.set_error('lookzone', str(e))

	# Function to save the configuration file
  def saveConfigFile(self, filePath, slide_attrs, lookzone_attrs):
    config = Configuration(filePath, lookzone_attrs, slide_attrs)
    config.print_config_file()

  # Function to clear all saved state in GUI including selected config file and attributes
  def clearGuiState(self):
    self.clearAttributesState()
    self.configFilePath = ''
    self.all_readers = []
    self.attribute_cache = {}

  # Function to clear the state of the attributes screen after saving
  def clearAttributesState(self):
    self.guiState = {}

# Main function to run everything
def main():
  app = QtGui.QApplication(sys.argv)
  window = Window()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
