#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from autocomplete import CompletionTextEdit

class AttributeCompleter(QtGui.QCompleter):
	def __init__(self, parent=None):
		QtGui.QCompleter.__init__(self, ['a', 'b', 'c'], parent)

# set up UI for two list horizontally aligned listviews
# to display attributes to choose and chosen ones.
class AttributeListsComponent(QtGui.QWidget):
	def __init__(self, window):
		QtGui.QWidget.__init__(self)
		self.window = window
		self.loadState()
		self.initUI()

	def initUI(self):
		layout = QtGui.QVBoxLayout(self)

		# create horizontal view to hold all attributes list
		# and selected attributes list
		attributesView = QtGui.QHBoxLayout(self)

		chooseAttrsList = self.makeChooseAttrsList()
		selectedAttrsList = self.makeSelectedAttrsList()
		# add choose attrs list view
		attributesView.addLayout(chooseAttrsList)
		# Add/Remove attributes button
		self.addAttributeButton = QtGui.QPushButton('Add')
		self.addAttributeButton.setMinimumWidth(100)
		attributesView.addWidget(self.addAttributeButton)
		self.addAttributeButton.clicked.connect(self.moveAttributes)
		# add selected attrs list view
		attributesView.addLayout(selectedAttrsList)

		layout.addLayout(attributesView)

	# construct and return a widget containing a filter box 
	def makeSearch(self):
		completer = AttributeCompleter()
		attributeEdit = CompletionTextEdit()
		attributeEdit.setCompleter(completer)
		return attributeEdit

	# construct and return layout containing choose attrs list and filterbox
	def makeChooseAttrsList(self):
		## setup list view test
		attributesLayout = QtGui.QVBoxLayout(self)

		# build filter searchbox
		searchboxView = self.makeSearch()

		# Add label and search bar for selecting attributes
		attributesLabel = QtGui.QLabel('Select Attributes', self)
		attributesLayout.addWidget(attributesLabel)
		attributesLayout.addWidget(searchboxView)
		# build list widget and add to layout
		self.chooseListWidget = self.createListWidget(self.attributes, self.buttonTextAdd)
		attributesLayout.addWidget(self.chooseListWidget)
		return attributesLayout

	# construct and return layout containing selected attrs list
	def makeSelectedAttrsList(self):
		selectedLayout = QtGui.QVBoxLayout(self)

		# label for list
		selectedLabel = QtGui.QLabel('Selected Attributes', self)
		selectedLayout.addWidget(selectedLabel)
		# build selected attributes list and add to layout
		self.selectedListWidget = self.createListWidget(self.selectedAttributes, self.buttonTextRemove)
		selectedLayout.addWidget(self.selectedListWidget)
		return selectedLayout

	# construct and return list widget with given attributes as items and responding
	# to click events with the given onClicked function
	def createListWidget(self, attributes, onClicked):
		listWidget = QtGui.QListWidget(self)
		listWidget.addItems(attributes)
		listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		listWidget.clicked.connect(onClicked)
		return listWidget

	# set button text to indicate removal functionality
	def buttonTextRemove(self):
		self.addAttributeButton.setText('Remove')

	# set button text to indicate addition functionality
	def buttonTextAdd(self):
		self.addAttributeButton.setText('Add')

	# Add or remove attribute from lists depending on button type
	def moveAttributes(self):
		if self.addAttributeButton.text() == 'Add':
			self.addAttribute()
		else:
			self.removeAttribute()

	# move selected attrs in choose list to the selected list
	def addAttribute(self):
		selectedItems = self.chooseListWidget.selectedItems()
		selectedList = []
		for i in list(selectedItems):
			selectedList.append(str(i.text()))
			self.chooseListWidget.takeItem(self.chooseListWidget.row(i))
		self.selectedListWidget.addItems(selectedList)

	# move selected attrs in selected list to the choose list
	def removeAttribute(self):
		selectedItems = self.selectedListWidget.selectedItems()
		removedList = []
		for i in list(selectedItems):
			removedList.append(str(i.text()))
			self.selectedListWidget.takeItem(self.selectedListWidget.row(i))
		self.chooseListWidget.addItems(removedList)

	# save GUI state (lists and filterbox) to the window
	def saveState(self):
		self.window.guiState[self.__class__.guiStateKey]['chooseAttrsItems'] = self.getItemsFromListView(self.chooseListWidget)
		self.window.guiState[self.__class__.guiStateKey]['selectedAttrsItems'] = self.getItemsFromListView(self.selectedListWidget)

	# load the GUI state if available
	def loadState(self):
		# if there is no saved state, create a new one for this view
		if not self.window.guiState.has_key(self.__class__.guiStateKey):
			# TODO: change test_attributes to actual ones from file
			self.window.guiState[self.__class__.guiStateKey] = { 'chooseAttrsItems': self.__class__.test_attributes, 'selectedAttrsItems': [], 'filter': '' }

		self.attributes = self.window.guiState[self.__class__.guiStateKey]['chooseAttrsItems']
		self.selectedAttributes = self.window.guiState[self.__class__.guiStateKey]['selectedAttrsItems']

	# clears window saved GUI state for this view
	def clearState(self):
		if self.window.guiState.has_key(self.__class__.guiStateKey):
			del self.window.guiState[self.__class__.guiStateKey]

	# returns a list of the text items from the given list widget
	def getItemsFromListView(self, widget):
		items = []
		for index in xrange(widget.count()):
			items.append(widget.item(index))
		labels = [i.text() for i in items]
		return labels
