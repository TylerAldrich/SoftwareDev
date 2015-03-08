#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore, QtWebKit
from autocomplete import CompletionTextEdit 

## Mock attributes to use for now
test_attributes = [
	'Total time tracked',
	'Total time shown',
	'Total tracking lost',
	'Pupil x diameter std dev',
	'Pupil y diameter std dev',
	'Average pupil x diameter'
	]

## Complete class, we'll probably need a second for lookzone
class AttributeCompleter(QtGui.QCompleter):
	def __init__(self, parent=None):
		QtGui.QCompleter.__init__(self, test_attributes, parent)

class SelectSlideMetricsWidget(QtGui.QWidget):
	procNext = QtCore.pyqtSignal()

	def __init__(self, window, filePath):
		QtGui.QWidget.__init__(self)
		self.window = window
		## File path won't be needed, just was using it to 
		## test passing strings and data around
		self.filePath = filePath
		self.initUI()

	def initUI(self):
		layout = QtGui.QVBoxLayout(self)
		label = QtGui.QLabel(self.filePath, self)

		## set up auto complete for text field
		completer = AttributeCompleter()
		attributeEdit = CompletionTextEdit()
		attributeEdit.setCompleter(completer)

		self.button = QtGui.QPushButton('Go back to first page')
		layout.addWidget(label)
		layout.addWidget(attributeEdit)
		layout.addWidget(self.button)
		self.button.clicked.connect(self.switchViews)

	def switchViews(self):
		## Just switches the view back to the inital screen for now
		self.window.showLoadFileView();
