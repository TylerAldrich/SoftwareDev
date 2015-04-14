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
from Views.load_progress import ReadInputFilesThread
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
    self.appVersion = 'v0.1'
    self.appWidth = 700
    self.appHeight = 500
    # save a Dict that caches the state of certain GUI elements
    self.guiState = {}
    # the config file should persist through views so save it in window
    self.configFilePath = ''
    self.set_style()
    self.initUI()

  def initUI(self):
    self.resize(self.appWidth, self.appHeight)
    self.center()
    self.setWindowTitle(self.appName + ' ' + self.appVersion)
    self.show()
    # Load up the Load file view
    self.showLoadFileView()

    # Add a menu bar where the user can start over or quit
    menu = self.menuBar().addMenu('File')
    menu.addAction('New Experiment', self.start_new)
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

  def closeApp(self):
    self.close()

  def start_new(self):
    reply = QtGui.QMessageBox.question(self, 'Message',
      "Are you sure you want to start a new session?", QtGui.QMessageBox.Yes |
      QtGui.QMessageBox.No, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
      self.clearAttributesState()
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

  # Function to clear the state of the attributes screen after saving
  def clearAttributesState(self):
    if self.guiState.has_key(SlideMetricsAttrListsComponent.guiStateKey):
      del self.guiState[SlideMetricsAttrListsComponent.guiStateKey]

    if self.guiState.has_key(LookzoneAttrListsComponent.guiStateKey):
      del self.guiState[LookzoneAttrListsComponent.guiStateKey]

    if self.guiState.has_key(LoadFileWidget.guiStateKey):
      del self.guiState[LoadFileWidget.guiStateKey]

# Main function to run everything
def main():
  app = QtGui.QApplication(sys.argv)
  window = Window()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
