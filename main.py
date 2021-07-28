"""
main.py
Chess Game Main File
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import twoplayers

class PushButton(QPushButton):
	def __init__(self, parent, text = ""):
		super(PushButton, self).__init__(parent)
		self.setText(text)
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setStyleSheet("color: white; background-color: #8400FF; border: 4px solid #8400FF;")
	
	def enterEvent(self, event: QEvent) -> None:
		self.setStyleSheet("color: white; background-color: #6400CF; border: 4px solid #6400CF;")
		super(PushButton, self).enterEvent(event)
	
	def leaveEvent(self, event: QEvent) -> None:
		self.setStyleSheet("color: white; background-color: #8400FF; border: 4px solid #8400FF;")
		super(PushButton, self).leaveEvent(event)
	
	def mousePressEvent(self, event: QMouseEvent) -> None:
		self.setStyleSheet("color: white; background-color: #4F00A6; border: 4px solid #4F00A6;")
		super(PushButton, self).mousePressEvent(event)
	
	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		self.setStyleSheet("color: white; background-color: #6400CF; border: 4px solid #6400CF;")
		super(PushButton, self).mouseReleaseEvent(event)

class Label(QLabel):
	def __init__(self, parent, text = ""):
		super(Label, self).__init__(parent = parent)
		self.setText(text)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class QuitButton(QPushButton):
	def __init__(self, parent):
		super(QuitButton, self).__init__(parent = parent)
		self.setText("×")
		self.setFixedSize(QSize(40, 40))
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.pressed.connect(QApplication.quit)
		self.status_tip = Label(parent, text = "Quit")
		self.status_tip.setFixedWidth(40)
		self.status_tip.move(QPoint(self.pos().x(), self.pos().y() + 40))
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
	
	def enterEvent(self, event: QEvent) -> None:
		self.status_tip.show()
		self.setStyleSheet("color: black; background-color: red; border: none;")
		super(QuitButton, self).enterEvent(event)
	
	def leaveEvent(self, event: QEvent) -> None:
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
		super(QuitButton, self).leaveEvent(event)

class MainPage(QWidget):
	def __init__(self, parent, two_player_mode_function = None):
		super(MainPage, self).__init__(parent = parent)
		self.quit_button = QuitButton(self)
		self.title = Label(self, text = "Chess")
		self.title.setFont(QFont("Helvetica", 35))
		self.title.setFixedHeight(50)
		self.select_mode_label = Label(self, text = "Select a mode")
		self.select_mode_label.setFont(QFont("Helvetica"))
		self.two_player_mode_button = PushButton(self, text = "2 Player Mode")
		if two_player_mode_function is not None: self.two_player_mode_button.pressed.connect(two_player_mode_function)

class Window(QMainWindow):
	"""Main Window"""
	def __init__(self):
		super(Window, self).__init__()
		self.stacked_pages, self.stacks = QStackedWidget(self), {"main-page": MainPage(self, two_player_mode_function = lambda: self.stacked_pages.setCurrentIndex(1)), "two-players": twoplayers.TwoPlayers(self)}
		self.stacked_pages.addWidget(self.stacks["main-page"])
		self.stacked_pages.addWidget(self.stacks["two-players"])
		self.showFullScreen()
		self.stacked_pages.move(0, 0)
		self.stacked_pages.setFixedSize(self.size())
		self.show()
		self.setMinimumSize(QSize(self.width(), self.height() - 20))
	
	def resetTwoPlayerGame(self):
		self.stacks["two-players"].deleteLater()
		self.stacks["two-players"] = twoplayers.TwoPlayers(self)
		self.stacked_pages.addWidget(self.stacks["two-players"])
	
	def resizeEvent(self, event: QResizeEvent) -> None:
		self.move(0, 20)
		self.stacks["main-page"].title.move((event.size().width() - self.stacks["main-page"].title.width()) // 2, 100)
		self.stacks["main-page"].select_mode_label.move((event.size().width() - self.stacks["main-page"].select_mode_label.width()) // 2, 200)
		self.stacks["main-page"].two_player_mode_button.move((event.size().width() - self.stacks["main-page"].two_player_mode_button.width()) // 2, 250)
		super(Window, self).resizeEvent(event)


application, window = QApplication([]), Window()
application.exec_()
