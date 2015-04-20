#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from collections import OrderedDict

# set up UI for two list horizontally aligned listviews
# to display attributes to choose and chosen ones.
class AttributeListsComponent(QtGui.QWidget):
  def __init__(self, window):
    QtGui.QWidget.__init__(self)
    self.window = window
    self.loadState()
    self.attributes_are_chosen = self.initAttributesState()
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
    # filter on initial load in case loading a prior state
    self.filterAttributes()

  # initialize a dict keeping track of whether each attribute is chosen or not
  def initAttributesState(self):
    attrs_are_chosen = OrderedDict()
    num_attrs = len(self.attributes)
    for i in xrange(num_attrs):
      attrs_are_chosen[self.attributes[i]] = False

    num_selected_attrs = len(self.selectedAttributes)
    for i in xrange(num_selected_attrs):
      attrs_are_chosen[self.selectedAttributes[i]] = True
    
    return attrs_are_chosen

  # construct and return a widget containing a filter box
  def makeSearch(self, filterFunction, filter):
    # Search bar for attributes
    search_bar = QtGui.QLineEdit()
    search_bar.setPlaceholderText('Search')
    # set the filter text if we have past GUI state to restore
    if len(filter) > 0:
      search_bar.setText(filter)
    search_bar.textChanged.connect(filterFunction)
    return search_bar

  # construct and return layout containing choose attrs list and filterbox
  def makeChooseAttrsList(self):
    ## setup list view test
    attributesLayout = QtGui.QVBoxLayout(self)

    # build filter searchbox
    self.attributeSearchBar = self.makeSearch(self.filterAttributes, self.filter)

    # Add label and search bar for selecting attributes
    attributesLabel = QtGui.QLabel('Select Attributes', self)
    attributesLayout.addWidget(attributesLabel)
    attributesLayout.addWidget(self.attributeSearchBar)
    # build list widget and add to layout
    self.chooseListWidget = self.createListWidget(self.attributes, self.buttonTextAdd)
    self.filterAttributes()
    attributesLayout.addWidget(self.chooseListWidget)
    return attributesLayout

  # construct and return layout containing selected attrs list
  def makeSelectedAttrsList(self):
    selectedLayout = QtGui.QVBoxLayout(self)

    # build filter searchbox
    self.chosen_search_bar = self.makeSearch(self.filterChosen, self.chosen_filter)

    # Build the clear all button
    self.clear_all_button = QtGui.QPushButton('Clear All')
    self.clear_all_button.clicked.connect(self.clearAllAttrs)

    # label for list
    selectedLabel = QtGui.QLabel('Selected Attributes', self)
    selectedLayout.addWidget(selectedLabel)
    selectedLayout.addWidget(self.chosen_search_bar)
    # build selected attributes list and add to layout
    self.selectedListWidget = self.createListWidget(self.attributes, self.buttonTextRemove)
    self.filterChosen()
    selectedLayout.addWidget(self.selectedListWidget)
    selectedLayout.addWidget(self.clear_all_button)
    return selectedLayout

  # construct and return list widget with given attributes as items and responding
  # to click events with the given onClicked function
  def createListWidget(self, attributes, onClicked):
    listWidget = QtGui.QListWidget(self)
    # sort list of attributes before adding
    attributes.sort()
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
    for i in selectedItems:
      self.attributes_are_chosen[str(i.text())] = True
    self.filterAttributes()
    self.filterChosen()

  # move selected attrs in selected list to the choose list
  def removeAttribute(self):
    selectedItems = self.selectedListWidget.selectedItems()
    removedList = []
    for i in selectedItems:
      self.attributes_are_chosen[str(i.text())] = False
    self.filterAttributes()
    self.filterChosen()

  # save GUI state (lists and filterbox) to the window
  def saveState(self):
    self.window.guiState[self.__class__.guiStateKey]['selectedAttrsItems'] = self.getChosenAttrs()
    self.window.guiState[self.__class__.guiStateKey]['filter'] = self.attributeSearchBar.text()
    self.window.guiState[self.__class__.guiStateKey]['chosen_filter'] = self.chosen_search_bar.text()

  # load the GUI state if available
  def loadState(self):
    # if there is no saved state, create a new one for this view
    if not self.window.guiState.has_key(self.__class__.guiStateKey):
      self.window.guiState[self.__class__.guiStateKey] = { 'selectedAttrsItems': self.__class__.saved_attrs, 'filter': '' , 'chosen_filter' : ''}

    # keep reference to full attribute list for ourselves to use in this class
    self.attributes = self.__class__.attr_list

    self.filter = self.window.guiState[self.__class__.guiStateKey]['filter']
    self.chosen_filter = self.window.guiState[self.__class__.guiStateKey]['chosen_filter']
    self.selectedAttributes = self.window.guiState[self.__class__.guiStateKey]['selectedAttrsItems']

  # clears window saved GUI state for this view
  def clearState(self):
    if self.window.guiState.has_key(self.__class__.guiStateKey):
      del self.window.guiState[self.__class__.guiStateKey]

  # returns list of strings of chosen attributes for output from the given list widget
  def getChosenAttrs(self):
    chosen_attributes = []
    for attr, chosen in self.attributes_are_chosen.items():
      if chosen is True:
        chosen_attributes.append(attr)

    return chosen_attributes

  # sets the filter to the given string query
  def setFilter(self, query):
    self.attributeSearchBar.setText(query)

  # On typing change, filter attributes
  def filterAttributes(self):
    searchedItems = self.chooseListWidget.findItems(self.attributeSearchBar.text(), QtCore.Qt.MatchContains)

    # Iterate through list of attributes we have and hide any that aren't being searched for
    # but don't show attributes hidden due to being visible in the selected list
    for index in xrange(self.chooseListWidget.count()):
      listItem = self.chooseListWidget.item(index)
      isHidden = listItem not in searchedItems or self.attributes_are_chosen[str(listItem.text())]
      self.chooseListWidget.setItemHidden(listItem, isHidden)

  # Filter the chose attributes
  def filterChosen(self):
    searchedItems = self.selectedListWidget.findItems(self.chosen_search_bar.text(), QtCore.Qt.MatchContains)

    # Iterate through list of attributes we have and hide any that aren't being searched for
    # but don't show attributes hidden due to being visible in the selected list
    for index in xrange(self.selectedListWidget.count()):
      listItem = self.selectedListWidget.item(index)
      isHidden = listItem not in searchedItems or not self.attributes_are_chosen[str(listItem.text())]
      self.selectedListWidget.setItemHidden(listItem, isHidden)

  # Clears all of the selected attributes
  def clearAllAttrs(self):
    for i in xrange(self.selectedListWidget.count()):
      item = self.selectedListWidget.item(i)
      self.attributes_are_chosen[str(item.text())] = False
    self.filterAttributes()
    self.filterChosen()
