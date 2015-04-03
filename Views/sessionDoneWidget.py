#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from navigation import NavigationWidget

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
      slideFilePathLabel = QtGui.QLabel(self.slideFilePath, self)
      layout.addWidget(slideFileMsgLabel)
      layout.addWidget(slideFilePathLabel)

    if len(self.lookzoneFilePath):
      lookzoneFileMsgLabel = QtGui.QLabel('Output file generated successfully with chosen <b>LookZone</b> data from given files. See generated ouput at:', self)
      lookzoneFilePathLabel = QtGui.QLabel(self.lookzoneFilePath, self)
      layout.addWidget(lookzoneFileMsgLabel)
      layout.addWidget(lookzoneFilePathLabel)

    if len(self.configFilePath):
      configFileMsgLabel = QtGui.QLabel('Your chosen data attributes from this session has been saved as a iPatch <b>Configuration</b> file at:', self)
      configFilePathLabel = QtGui.QLabel(self.configFilePath, self)    
      layout.addWidget(configFileMsgLabel)
      layout.addWidget(configFilePathLabel)

    # TODO: Refactor this code to use NavigationWidget
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
