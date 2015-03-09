#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore, QtWebKit
from autocomplete import CompletionTextEdit 

class LoadFileWidget(QtGui.QWidget):
	procNext = QtCore.pyqtSignal()

	def __init__(self, window):
		QtGui.QWidget.__init__(self)
		self.window = window
		self.initUI()

	def initUI(self):
		## Create initial vertical layout
		layout = QtGui.QVBoxLayout(self)

		titleLabel = QtGui.QLabel('Upload Excel File', self)
		subtitleLabel = QtGui.QLabel('Click browse to select an expirement to upload', self)

		## Add two labels to layout
		layout.addStretch(1)
		layout.addWidget(titleLabel)
		layout.addWidget(subtitleLabel)

		## Horizontal layout is for the text box and browse button
		browseFileLayout = QtGui.QHBoxLayout(self)
		browseFileLayout.addStretch(1)

		## Init text edit box for file path and browse button to
		## find the file.  Set browse button on click to selectFile function
		self.fileTextEdit = QtGui.QLineEdit()
		browseButton = QtGui.QPushButton('Browse')
		browseFileLayout.addWidget(self.fileTextEdit)
		browseFileLayout.addWidget(browseButton)
		browseButton.clicked.connect(self.selectFile)

		## Add horizontal layout to overall layout
		layout.addLayout(browseFileLayout)
		self.button = QtGui.QPushButton('Next')
		layout.addWidget(self.button)
		self.button.clicked.connect(self.switchViews)

	def switchViews(self):
		fileName = self.fileTextEdit.text()
		self.window.showSlideMetricsView(fileName)

	def selectFile(self):
		self.fileTextEdit.setText(QtGui.QFileDialog.getOpenFileName())
