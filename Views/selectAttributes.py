#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore
from slideMetricsAttrLists import SlideMetricsAttrListsComponent
from lookzoneAttrLists import LookzoneAttrListsComponent
from navigation import NavigationWidget

class SelectAttributesWidget(QtGui.QWidget):
  procNext = QtCore.pyqtSignal()

  def __init__(self, window, lookzone_attrs, slide_attrs):
    QtGui.QWidget.__init__(self)
    self.lookzone_attrs = lookzone_attrs
    self.slide_attrs = slide_attrs
    self.window = window
    self.initUI()

  def initUI(self):
    layout = QtGui.QVBoxLayout(self)

    # Set up the Attribute Type tabs
    tabsWidget = QtGui.QTabWidget()
    self.slideMetricsTab = SlideMetricsAttrListsComponent(self.window, self.slide_attrs)
    self.lookzoneTab = LookzoneAttrListsComponent(self.window, self.lookzone_attrs)

    tabsWidget.addTab(self.slideMetricsTab, "Slide Metrics")
    tabsWidget.addTab(self.lookzoneTab, "LookZone Data")
    # Add tabs and content within tabs into layout
    layout.addWidget(tabsWidget)

    # set up back and next buttons on the bottom separate from tabs
    navigation = NavigationWidget(self.window, self.goToSetupView, self.goToOutputConfigView)
    layout.addWidget(navigation)

  # Switches back to loading input file view
  def goToSetupView(self):
    self.window.showLoadFileView()
    # Since going back to file selection requires file analysis before
    # coming back to this screen, clear state of chosen attributes
    self.slideMetricsTab.clearState()
    self.lookzoneTab.clearState()

  # Switches to output config view
  def goToOutputConfigView(self):
    selected_slide_attrs = self.slideMetricsTab.getItemsFromListView(self.slideMetricsTab.selectedListWidget)
    selected_lookzone_attrs = self.lookzoneTab.getItemsFromListView(self.lookzoneTab.selectedListWidget)
    self.window.showSaveFilesView(selected_slide_attrs, selected_lookzone_attrs)
    # Save state of lists in view
    self.slideMetricsTab.saveState()
    self.lookzoneTab.saveState()
