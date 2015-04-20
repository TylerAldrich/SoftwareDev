#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from navigation import NavigationWidget
from clickable_qlabel import ClickableQLabel

# Widget that has user browse for an input file
class SessionDoneWidget(QtGui.QWidget):
  procNext = QtCore.pyqtSignal()

  def __init__(self, window, slideFilePath, lookzoneFilePath, configFilePath):
    QtGui.QWidget.__init__(self)
    self.window = window
    self.slideFilePath = slideFilePath
    self.lookzoneFilePath = lookzoneFilePath
    self.configFilePath = configFilePath
    self.initUI()

  def initUI(self):
    # Create initial vertical layout
    layout = QtGui.QVBoxLayout(self)
    layout.setAlignment(QtCore.Qt.AlignTop)

    titleLabel = QtGui.QLabel('<b style="font-size: 24px">Success!</b>', self)
    layout.addWidget(titleLabel)

    if len(self.slideFilePath):
      slideFileMsgLabel = QtGui.QLabel('Output file generated successfully with chosen <b>Slide Metric</b> data from given files. See generated ouput at:', self)
      slideFilePathLabel = ClickableQLabel(self.slideFilePath, self)
      self.connect(slideFilePathLabel, QtCore.SIGNAL('clicked()'), self.openSlideOutput)
      slideFilePathLabel.setCursor(QtCore.Qt.PointingHandCursor)
      layout.addWidget(slideFileMsgLabel)
      layout.addWidget(slideFilePathLabel)

    if len(self.lookzoneFilePath):
      lookzoneFileMsgLabel = QtGui.QLabel('Output file generated successfully with chosen <b>LookZone</b> data from given files. See generated ouput at:', self)
      lookzoneFilePathLabel = ClickableQLabel(self.lookzoneFilePath, self)
      self.connect(lookzoneFilePathLabel, QtCore.SIGNAL('clicked()'), self.openLookzoneOutput)
      lookzoneFilePathLabel.setCursor(QtCore.Qt.PointingHandCursor)
      layout.addWidget(lookzoneFileMsgLabel)
      layout.addWidget(lookzoneFilePathLabel)

    if len(self.configFilePath):
      configFileMsgLabel = QtGui.QLabel('Your chosen data attributes from this session has been saved as a iPatch <b>Configuration</b> file at:', self)
      configFilePathLabel = QtGui.QLabel(self.configFilePath, self)    
      layout.addWidget(configFileMsgLabel)
      layout.addWidget(configFilePathLabel)

    navigationWidgetWrapper = QtGui.QWidget(self) 
    navigationLayout = QtGui.QHBoxLayout(navigationWidgetWrapper)
    self.quitBtn = QtGui.QPushButton('Quit iPatch')
    navigationLayout.addWidget(self.quitBtn)
    self.quitBtn.clicked.connect(self.window.closeApp)
    navigationLayout.addWidget(self.quitBtn)

    navigationLayout.addStretch(1)
    self.newSessionBtn = QtGui.QPushButton('Start new session')
    navigationLayout.addWidget(self.newSessionBtn)
    self.newSessionBtn.clicked.connect(self.window.showLoadFileView)
    layout.addWidget(navigationWidgetWrapper)

  def openSlideOutput(self):
    outputPath = QtCore.QUrl("file:///" + self.slideFilePath, QtCore.QUrl.TolerantMode)
    result = QtGui.QDesktopServices.openUrl(outputPath);

  def openLookzoneOutput(self):
    outputPath = QtCore.QUrl("file:///" + self.lookzoneFilePath, QtCore.QUrl.TolerantMode)
    result = QtGui.QDesktopServices.openUrl(outputPath);
