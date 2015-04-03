#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from Views.selectAttributes import SelectAttributesWidget
from Views.loadFile import LoadFileWidget
from Views.saveFilesWidget import SaveFileWidget
from Views.sessionDoneWidget import SessionDoneWidget
from Views.loadConfig import LoadConfigWidget
from Views.slideMetricsAttrLists import SlideMetricsAttrListsComponent
from Views.lookzoneAttrLists import LookzoneAttrListsComponent
from workbook_reader import WorkbookReader
from workbook_writer import SlideMetricWriter, LookzoneWriter
from configuration import Configuration

# The main class that starts and enables flow through
# the different views of the application
class Window(QtGui.QMainWindow):

  def __init__(self):
    super(Window, self).__init__()
    self.appName = 'iPatch'
    self.appVersion = 'v0.1'
    # save a Dict that caches the state of certain GUI elements 
    self.guiState = {}
    self.configFilePath = ''
    self.initUI()

  def initUI(self):
    self.resize(700, 500)
    self.center()
    self.setWindowTitle(self.appName + ' ' + self.appVersion)
    self.show()
    # Load up the Load file view
    self.showLoadFileView()

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

  # Function to show the screen for selecting attributes 
  def showSelectAttributesView(self):
    # For each file in the list of files, create a reader and get all of its attributes
    saved_slide = set()
    saved_lookzone = set()
    self.all_readers = []
    for filePath in self.experimentFilePaths:
      print str(filePath)
      # First parse the experiment from the saved file path
      reader = WorkbookReader(str(filePath))
      self.all_readers.append(reader)

      # get the lookzone and slide attributes from the reader
      attrs = reader.get_attributes()
      lookzone_attrs = attrs['lookzone'];
      slide_attrs = attrs['slide'];

      # Then if there is a config file to load, load it
      if len(self.configFilePath):
        saved_attrs = Configuration.read_config_file(self.configFilePath)
        saved_slide.update(saved_attrs['slide'])
        saved_lookzone.update(saved_attrs['lookzone'])

    self.selectAttributesWidget = SelectAttributesWidget(self, list(lookzone_attrs), list(slide_attrs), saved_slide, saved_lookzone)
    self.setCentralWidget(self.selectAttributesWidget)

  # Function to show the screen for selecting a configuration file
  def showLoadConfigView(self, experimentFilePaths=None):
    if experimentFilePaths:
      self.experimentFilePaths = experimentFilePaths
    loadConfig = LoadConfigWidget(self)
    self.setCentralWidget(loadConfig)

  # Function to show the screen for loading a new excel file
  def showLoadFileView(self):
    firstClass = LoadFileWidget(self)
    self.setCentralWidget(firstClass)

  ## Function to show the save file screen
  def showSaveFilesView(self, slide_attrs, lookzone_attrs):
    saveFilesView = SaveFileWidget(self, slide_attrs, lookzone_attrs)
    self.setCentralWidget(saveFilesView)

  def showDoneView(self, slideFilePath, lookzoneFilePath, configFilePath):
    doneView = SessionDoneWidget(self, slideFilePath, lookzoneFilePath, configFilePath)
    self.setCentralWidget(doneView)

  ## Function to save slide metric attributes
  def saveSlideMetricsData(self, filePath, attrs):
    if len(attrs) > 0:
      slide_writer = SlideMetricWriter(self.all_readers, filePath, attrs)
      slide_writer.write_readers()

  ## Function to save lookzone attributes
  def saveLookzoneData(self, filePath, attrs):
    if len(attrs) > 0:
      lookzone_writer = LookzoneWriter(self.all_readers, filePath, attrs)
      lookzone_writer.write_readers()

	## Function to save the configuration file
  def saveConfigFile(self, filePath, slide_attrs, lookzone_attrs):
    config = Configuration(filePath, lookzone_attrs, slide_attrs)
    config.print_config_file()

  ## Function to clear the state of the attributes screen after saving
  def clearAttributesState(self):
    if self.guiState.has_key(SlideMetricsAttrListsComponent.guiStateKey):
      del self.guiState[SlideMetricsAttrListsComponent.guiStateKey]

    if self.guiState.has_key(LookzoneAttrListsComponent.guiStateKey):
      del self.guiState[LookzoneAttrListsComponent.guiStateKey]

# Main function to run everything
def main():
  app = QtGui.QApplication(sys.argv)
  window = Window()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
