"""
main.py
Chess Game Main File
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Window(QMainWindow):
	"""Main Window"""
	def __init__(self):
		super(Window, self).__init__()
		self.title = QLabel("Chess", self)
		self.showFullScreen()
		self.show()
	
	def resizeEvent(self, event: QResizeEvent) -> None:
		self.title.move((event.size().width() // 2) - (self.title.width() // 2), 100)
		super(Window, self).resizeEvent(event)


application, window = QApplication([]), Window()
application.exec_()
