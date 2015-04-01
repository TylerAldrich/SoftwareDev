#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from navigation import NavigationWidget

# Widget that has user browse for an input file
class LoadFileWidget(QtGui.QWidget):
	procNext = QtCore.pyqtSignal()

	def __init__(self, window):
		QtGui.QWidget.__init__(self)
		self.window = window
		self.initUI()

	def initUI(self):
		# Create initial vertical layout
		layout = QtGui.QVBoxLayout(self)
		layout.setAlignment(QtCore.Qt.AlignTop)

		titleLabel = QtGui.QLabel('Upload Excel File', self)
		subtitleLabel = QtGui.QLabel('Click browse to select an experiment to upload', self)

		# Add two labels to layout
		layout.addWidget(titleLabel)
		layout.addWidget(subtitleLabel)

		# Horizontal layout is for the text box and browse button
		browseFileLayout = QtGui.QHBoxLayout(self)

		# Init text edit box for file path and browse button to
		# find the file.  Set browse button on click to selectFile function
		self.fileTextEdit = QtGui.QLineEdit()
		browseButton = QtGui.QPushButton('Browse')
		browseFileLayout.addWidget(self.fileTextEdit)
		browseFileLayout.addWidget(browseButton)
		browseButton.clicked.connect(self.selectFile)

		# Add horizontal layout to overall layout
		layout.addLayout(browseFileLayout)

		self.errorMsgLabel = QtGui.QLabel('')
		layout.addWidget(self.errorMsgLabel)
		navigation = NavigationWidget(self.window, None, self.switchViews)
		layout.addWidget(navigation)

	# go to next view to select data attributes
	def switchViews(self):
		fileName = self.fileTextEdit.text()
		# TODO: Make application open file path at this point and validate input so we can show error on this screen
		if len(fileName):
			self.window.showLoadConfigView(fileName)
		else:
			self.errorMsgLabel.setText('<b style="color:red">No input file was selected. Please choose an input Excel file to continue.</b>')

	# open a file dialog to pick an xlsx input file
	def selectFile(self):
		self.fileTextEdit.setText(QtGui.QFileDialog.getOpenFileName())
