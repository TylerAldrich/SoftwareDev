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

	def __init__(self, window):
		QtGui.QWidget.__init__(self)
		self.window = window
		self.initUI()

	def initUI(self):
		layout = QtGui.QVBoxLayout(self)

		# Set up the Attribute Type tabs
		tabsWidget = QtGui.QTabWidget()
		self.slideMetricsTab = SlideMetricsAttrListsComponent(self.window)
		self.lookzoneTab = LookzoneAttrListsComponent(self.window)

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
		# TODO: change following to output config view
		self.window.showLoadFileView()
		# Save state of lists in view
		self.slideMetricsTab.saveState()
		self.lookzoneTab.saveState()
