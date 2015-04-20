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

  def __init__(self, window, slide_attrs, lookzone_attrs, saved_slide, saved_lookzone):
    QtGui.QWidget.__init__(self)
    self.slide_attrs = slide_attrs
    self.lookzone_attrs = lookzone_attrs
    self.saved_slide = saved_slide
    self.saved_lookzone = saved_lookzone
    self.window = window
    self.initUI()

  def initUI(self):
    layout = QtGui.QVBoxLayout(self)

    # Set up the Attribute Type tabs
    tabsWidget = QtGui.QTabWidget()
    self.slideMetricsTab = SlideMetricsAttrListsComponent(self.window, self.slide_attrs, self.saved_slide)
    self.lookzoneTab = LookzoneAttrListsComponent(self.window, self.lookzone_attrs, self.saved_lookzone)

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
    # Save state of lists in view
    self.slideMetricsTab.saveState()
    self.lookzoneTab.saveState()
    selected_slide_attrs = self.slideMetricsTab.getChosenAttrs()
    selected_lookzone_attrs = self.lookzoneTab.getChosenAttrs()
    self.window.showSaveFilesView(selected_slide_attrs, selected_lookzone_attrs)
