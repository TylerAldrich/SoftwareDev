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

		## Search bar for attributes
		self.attributeSearchBar = QtGui.QLineEdit()
		self.attributeSearchBar.setPlaceholderText('Search')
		self.attributeSearchBar.textChanged.connect(self.filterAttributes)

		## create horizontal view to hold all attributes list
		## and selected attributes list
		attributesView = QtGui.QHBoxLayout(self)
		attributesView.addStretch(1)

		## setup list view test
		attributesLayout = QtGui.QVBoxLayout(self)

		## Add label and search bar for selecting attributes
		attributesLabel = QtGui.QLabel('Select Slide Metric Attributes', self)
		attributesLayout.addWidget(attributesLabel)
		attributesLayout.addWidget(self.attributeSearchBar)

		self.listOfAttributes = self.createListWidget(attributesLayout, test_attributes, self.buttonTextAdd)
		attributesView.addLayout(attributesLayout)

		## Add attributes button
		self.addAttributeButton = QtGui.QPushButton('Add')
		attributesView.addWidget(self.addAttributeButton)
		self.addAttributeButton.clicked.connect(self.moveAttributes)

		## Selected attributes
		selectedLayout = QtGui.QVBoxLayout(self)

		## Create label for selected attributes
		selectedLabel = QtGui.QLabel('Selected Slide Metric Attributes', self)
		selectedLayout.addWidget(selectedLabel)

		## Create list of selected attributes
		self.selectedAttributes = self.createListWidget(selectedLayout, [], self.buttonTextRemove)
		attributesView.addLayout(selectedLayout)

		layout.addLayout(attributesView)

		self.button = QtGui.QPushButton('Go back to first page')
		layout.addWidget(label)
		layout.addWidget(self.button)
		self.button.clicked.connect(self.switchViews)

	## Function to create the list widgets
	def createListWidget(self, layout, attributes, onClicked):
		listWidget = QtGui.QListWidget(self)
		listWidget.addItems(attributes)
		listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		listWidget.clicked.connect(onClicked)
		layout.addWidget(listWidget)
		return listWidget

	def switchViews(self):
		## Just switches the view back to the inital screen for now
		self.window.showLoadFileView();

	def buttonTextRemove(self):
		self.addAttributeButton.setText('Remove')

	def buttonTextAdd(self):
		self.addAttributeButton.setText('Add')

	def moveAttributes(self):
		if self.addAttributeButton.text() == 'Add':
			self.addAttribute()
		else:
			self.removeAttribute()

	def addAttribute(self):
		selectedItems = self.listOfAttributes.selectedItems()
		selectedList = []
		for i in list(selectedItems):
			selectedList.append(str(i.text()))
			self.listOfAttributes.takeItem(self.listOfAttributes.row(i))
		self.selectedAttributes.addItems(selectedList)

	def removeAttribute(self):
		selectedItems = self.selectedAttributes.selectedItems()
		removedList = []
		for i in list(selectedItems):
			removedList.append(str(i.text()))
			self.selectedAttributes.takeItem(self.selectedAttributes.row(i))
		self.listOfAttributes.addItems(removedList)

	## On typing change, filter attributes
	def filterAttributes(self):
		searchedItems = self.listOfAttributes.findItems(self.attributeSearchBar.text(), QtCore.Qt.MatchContains)

		## Iterate through list of attributes we have and hide any that aren't being searched for
		for index in xrange(self.listOfAttributes.count()):
			listItem = self.listOfAttributes.item(index)
			isHidden = listItem not in searchedItems
			self.listOfAttributes.setItemHidden(listItem, isHidden)
