#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sys import argv
from PyQt4 import QtGui, QtCore, QtWebKit
from autocomplete import CompletionTextEdit 

test_attributes = [
	'Total time tracked',
	'Total time shown',
	'Total tracking lost',
	'Pupil x diameter std dev',
	'Pupil y diameter std dev',
	'Average pupil x diameter'
	]

class AttributeCompleter(QtGui.QCompleter):
	def __init__(self, parent=None):
		QtGui.QCompleter.__init__(self, test_attributes, parent)

class LoadFileWidget(QtGui.QWidget):
	procNext = QtCore.pyqtSignal()

	def __init__(self, window):
		QtGui.QWidget.__init__(self)
		self.window = window
		self.initUI()

	def initUI(self):
		layout = QtGui.QVBoxLayout(self)

		titleLabel = QtGui.QLabel('Upload Excel File', self)
		subtitleLabel = QtGui.QLabel('Click browse to select an expirement to upload', self)

		layout.addStretch(1)
		layout.addWidget(titleLabel)
		layout.addWidget(subtitleLabel)

		browseFileLayout = QtGui.QHBoxLayout(self)
		browseFileLayout.addStretch(1)

		self.fileTextEdit = QtGui.QLineEdit()
		browseButton = QtGui.QPushButton('Browse')
		browseFileLayout.addWidget(self.fileTextEdit)
		browseFileLayout.addWidget(browseButton)
		browseButton.clicked.connect(self.selectFile)

		layout.addLayout(browseFileLayout)
		self.button = QtGui.QPushButton('Next')
		layout.addWidget(self.button)
		self.button.clicked.connect(self.switchViews)

	def switchViews(self):
		fileName = self.fileTextEdit.text()
		self.window.switchToB(fileName)

	def selectFile(self):
		self.fileTextEdit.setText(QtGui.QFileDialog.getOpenFileName())

class LoadConfigFile(QtGui.QWidget):
	procNext = QtCore.pyqtSignal()

	def __init__(self, window, msg):
		QtGui.QWidget.__init__(self)
		self.window = window
		self.msg = msg
		self.initUI()

	def initUI(self):
		layout = QtGui.QVBoxLayout(self)
		label = QtGui.QLabel(self.msg, self)
		completer = AttributeCompleter() 
		attributeEdit = CompletionTextEdit()
		attributeEdit.setCompleter(completer)
		self.button = QtGui.QPushButton('Second Button')
		layout.addWidget(label)
		layout.addWidget(attributeEdit)
		layout.addWidget(self.button)
		self.button.clicked.connect(self.switchViews)

	def switchViews(self):
		self.window.switchToA();

class Window(QtGui.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.initUI()

	def initUI(self):
		self.resize(400, 400)
		self.center()
		self.setWindowTitle('Quit')
		self.show()
		self.switchToA()

	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def closeEvent(self, event):
		reply = QtGui.QMessageBox.question(self, 'Message',
			"Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def switchToB(self, msg):
		newClass = LoadConfigFile(self, msg)
		self.setCentralWidget(newClass)

	def switchToA(self):
		firstClass = LoadFileWidget(self)
		self.setCentralWidget(firstClass)

def main():

	app = QtGui.QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
