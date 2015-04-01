#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore

# Provides widget for navigating to previous and next steps in app
# expects the main window and two callback functions for "back"
# and "next" clicks. If either is not provided, its respective button
# is also not included in the widget.
# TODO: Refactor this code to allow customization like placement, custom text, etc.
class NavigationWidget(QtGui.QWidget):
	procNext = QtCore.pyqtSignal()

	def __init__(self, window, prevClicked=None, nextClicked=None):
		QtGui.QWidget.__init__(self)
		self.window = window
		self.prevClicked = prevClicked
		self.nextClicked = nextClicked
		self.initUI()

	def initUI(self):
		navigationLayout = QtGui.QHBoxLayout(self)
		if not self.prevClicked is None:
			self.back = QtGui.QPushButton('Back')
			navigationLayout.addWidget(self.back)
			self.back.clicked.connect(self.prevClicked)
		if not self.nextClicked is None:
			navigationLayout.addStretch(1)
			self.next = QtGui.QPushButton('Next')
			navigationLayout.addWidget(self.next)
			self.next.clicked.connect(self.nextClicked)
