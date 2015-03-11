#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from Views.selectAttributes import SelectAttributesWidget
from Views.loadFile import LoadFileWidget
from Views.saveFilesWidget import SaveFileWidget
from workbook_reader import WorkbookReader
from workbook_writer import SlideMetricWriter, LookzoneWriter

# The main class that starts and enables flow through
# the different views of the application
class Window(QtGui.QMainWindow):

  def __init__(self):
    super(Window, self).__init__()
    self.appName = 'iPatch'
    self.appVersion = 'v0.1'
    # save a Dict that caches the state of certain GUI elements 
    self.guiState = {}
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

  # Function to show the screen for selecting slide metric attributes 
  def showSlideMetricsView(self, filePath):
    self.reader = WorkbookReader(str(filePath))
    attrs = self.reader.get_attributes()
    lookzone_attrs = attrs['lookzone'];
    slide_attrs = attrs['slide'];
    newClass = SelectAttributesWidget(self, list(lookzone_attrs), list(slide_attrs))
    self.setCentralWidget(newClass)

  # Function to show the screen for loading a new excel file
  def showLoadFileView(self):
    firstClass = LoadFileWidget(self)
    self.setCentralWidget(firstClass)

  ## Function to show the save file screen
  def showSaveFilesView(self, slide_attrs, lookzone_attrs):
    saveFilesView = SaveFileWidget(self, slide_attrs, lookzone_attrs)
    self.setCentralWidget(saveFilesView)

  ## Function to save slide metric attributes
  def saveSlideMetricsData(self, filePath, attrs):
    if len(attrs) > 0:
      slide_writer = SlideMetricWriter([self.reader], filePath, attrs)
      slide_writer.write_first_reader()
      self.showLoadFileView()

  ## Function to save lookzone attributes
  def saveLookzoneData(self, filePath, attrs):
    if len(attrs) > 0:
      lookzone_writer = LookzoneWriter([self.reader], filePath, attrs)
      lookzone_writer.write_first_reader()

# Main function to run everything
def main():
  app = QtGui.QApplication(sys.argv)
  window = Window()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
