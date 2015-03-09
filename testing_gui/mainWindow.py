#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore, QtWebKit
from autocomplete import CompletionTextEdit
from selectSlideAttributes import SelectSlideMetricsWidget
from loadFile import LoadFileWidget

class Window(QtGui.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.initUI()

	def initUI(self):
		self.resize(400, 400)
		self.center()
		self.setWindowTitle('Quit')
		self.show()
		## Load up the Load file view
		self.showLoadFileView()

	## Function to center the window on screen
	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	## Function to show dialog for when window is closed
	def closeEvent(self, event):
		reply = QtGui.QMessageBox.question(self, 'Message',
			"Are you sure you want to quit?", QtGui.QMessageBox.Yes |
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	## Function to show the screen for selecting slide metric attributes 
	def showSlideMetricsView(self, filePath):
		newClass = SelectSlideMetricsWidget(self, filePath)
		self.setCentralWidget(newClass)

	## Function to show the screen for loading a new excel file
	def showLoadFileView(self):
		firstClass = LoadFileWidget(self)
		self.setCentralWidget(firstClass)

## Main function to run everything
def main():

	app = QtGui.QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
