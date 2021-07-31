"""
main.py
Chess Game Main File
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
from PyQt5.QtWidgets import *

import twoplayers

class PushButton(QPushButton):
	def __init__(self, parent, text = "", clicked = None):
		super(PushButton, self).__init__(parent)
		self.setText(text)
		self.clicked, self.setting_color = clicked, False
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-SemiBold.ttf"))[0], 15))
		self.setStyleSheet("color: transparent; background-color: transparent; border: 15px solid transparent;")
	
	def enterEvent(self, event: QEvent) -> None:
		if self.setting_color: return
		self.setStyleSheet("color: white; background-color: #6400CF; border: 15px solid #6400CF;")
		super(PushButton, self).enterEvent(event)
	
	def leaveEvent(self, event: QEvent) -> None:
		if self.setting_color: return
		self.setStyleSheet("color: white; background-color: #8400FF; border: 15px solid #8400FF;")
		super(PushButton, self).leaveEvent(event)
	
	def mousePressEvent(self, event: QMouseEvent) -> None:
		if self.setting_color: return
		self.setStyleSheet("color: white; background-color: #4F00A6; border: 15px solid #4F00A6;")
		super(PushButton, self).mousePressEvent(event)
		if self.clicked is not None: self.clicked()
	
	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		if self.setting_color: return
		self.setStyleSheet("color: white; background-color: #6400CF; border: 15px solid #6400CF;")
		super(PushButton, self).mouseReleaseEvent(event)
	
	def animationFinished(self):
		self.setting_color = False
		self.setStyleSheet("color: white; background-color: #8400FF; border: 15px solid #8400FF;")
	
	def setColor(self, color: QColor):
		self.setting_color = True
		if color.getRgb() in [(0, 0, 0, 0), (0, 0, 1, 1), (1, 0, 2, 2), (1, 0, 3, 3), (2, 0, 4, 4), (2, 0, 4, 4), (2, 0, 5, 5), (3, 0, 6, 6), (3, 0, 7, 7), (4, 0, 8, 8), (4, 0, 9, 9), (5, 0, 9, 9)]: return
		self.setStyleSheet(f"color: white; background-color: rgba({color.getRgb()[0]}, {color.getRgb()[1]}, {color.getRgb()[2]}, {color.getRgb()[3]});")
	
	color = pyqtProperty(QColor, fset = setColor)

class Label(QLabel):
	def __init__(self, parent, text = ""):
		super(Label, self).__init__(parent = parent)
		self.setText(text)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
		
	def setColor(self, color):
		palette = self.palette()
		palette.setColor(self.foregroundRole(), color)
		self.setPalette(palette)
		
	color = pyqtProperty(QColor, fset = setColor)
	
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
		self.select_mode_label_animation, self.two_player_mode_animation = None, None
		self.quit_button = QuitButton(self)
		self.quit_button.hide()
		self.title = Label(self, text = "Chess")
		self.title_animation = QPropertyAnimation(self.title, b"color")
		self.title_animation.setLoopCount(1)
		self.title_animation.setDuration(20000)
		self.title_animation.setStartValue(QColor("#1B00FF"))
		self.title_animation.setEndValue(QColor("#CC00FF"))
		self.title_animation.finished.connect(lambda: self.changeAnimationDirection(self.title_animation))
		self.title_animation.start()
		self.title_opening_animation = QPropertyAnimation(self.title, b"size")
		self.title_opening_animation.setDuration(750)
		self.title_opening_animation.finished.connect(self.titleAnimationFinished)
		self.select_mode_label = Label(self, text = "Select a mode")
		self.select_mode_label.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-Bold.ttf"))[0], 30))
		self.select_mode_animation = QPropertyAnimation(self.select_mode_label, b"color")
		self.select_mode_animation.setLoopCount(1)
		self.select_mode_animation.setDuration(20000)
		self.select_mode_animation.setStartValue(QColor("#CC00FF"))
		self.select_mode_animation.setEndValue(QColor("#1B00FF"))
		self.select_mode_animation.finished.connect(lambda: self.changeAnimationDirection(self.select_mode_animation))
		self.two_player_mode_button = PushButton(self, text = "2 Player Mode", clicked = two_player_mode_function)
		self.select_mode_label.setColor(QColor("transparent"))
	
	@staticmethod
	def changeAnimationDirection(animation):
		animation.setDirection(int(not animation.direction()))
		animation.start()
	
	def resizeEvent(self, event: QResizeEvent) -> None:
		self.title.setFont(QFont("Impact", self.width() // 15, italic = True))
		self.title.move(QPoint(self.title.pos().x(), 10))
		self.title_opening_animation.setEndValue(QSize(self.title.maximumWidth(), 200))
		self.title_opening_animation.setStartValue(QSize(self.title.maximumWidth(), 0))
		self.title_opening_animation.start()
		super(MainPage, self).resizeEvent(event)
		
	def titleAnimationFinished(self):
		self.quit_button.show()
		self.quit_button.raise_()
		QTest.qWait(250)
		self.select_mode_label.move(QPoint(self.select_mode_label.pos().x(), self.select_mode_label.pos().y() + 100))
		self.select_mode_label_animation = QPropertyAnimation(self.select_mode_label, b"color")
		self.select_mode_label_animation.setDuration(250)
		self.select_mode_label_animation.setStartValue(QColor("transparent"))
		self.select_mode_label_animation.setEndValue(QColor("#CC00FF"))
		self.select_mode_label_animation.start()
		self.select_mode_label_animation.finished.connect(self.twoPlayerModeAnimation)
	
	def twoPlayerModeAnimation(self):
		self.select_mode_animation.start()
		self.two_player_mode_button.move(QPoint(self.two_player_mode_button.pos().x(), self.two_player_mode_button.pos().y() + 100))
		self.two_player_mode_animation = QPropertyAnimation(self.two_player_mode_button, b"color")
		self.two_player_mode_animation.setDuration(250)
		self.two_player_mode_animation.setStartValue(QColor("transparent"))
		self.two_player_mode_animation.setEndValue(QColor("#8400FF"))
		self.two_player_mode_animation.start()
		self.two_player_mode_animation.finished.connect(self.two_player_mode_button.animationFinished)
		
class Window(QMainWindow):
	"""Main Window"""
	def __init__(self) -> None:
		super(Window, self).__init__()
		self.setWindowTitle("Chess")
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
