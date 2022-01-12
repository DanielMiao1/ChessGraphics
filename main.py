"""
main.py
Chess Game Main File
"""
import math

try:
	from PyQt5.QtGui import *
except ModuleNotFoundError:
	print("The PyQt5 library is not installed. Use the 'pip3 install PyQt5' bash command to install it.")
	exit()

try:
	import chess
	chess.Game()
except:
	__import__("os").system("pip3 install git+https://github.com/DanielMiao1/chess")


from PyQt5.QtCore import *
from PyQt5.QtTest import *
from PyQt5.QtWidgets import *

import twoplayers


class PushButton(QPushButton):
	def __init__(self, parent, text="", clicked=None):
		super(PushButton, self).__init__(parent)
		self.setText(text)
		self.clicked, self.setting_color = clicked, True
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-SemiBold.ttf"))[0], 15))
		self.setStyleSheet("color: transparent; background-color: transparent; border: 15px solid transparent;")

	def enterEvent(self, event: QEvent) -> None:
		if self.setting_color:
			return
		self.setStyleSheet("color: white; background-color: #6400CF; border: 15px solid #6400CF;")
		super(PushButton, self).enterEvent(event)

	def leaveEvent(self, event: QEvent) -> None:
		if self.setting_color:
			return
		self.setStyleSheet("color: white; background-color: #8400FF; border: 15px solid #8400FF;")
		super(PushButton, self).leaveEvent(event)

	def mousePressEvent(self, event: QMouseEvent) -> None:
		if self.setting_color:
			return
		self.setStyleSheet("color: white; background-color: #4F00A6; border: 15px solid #4F00A6;")
		super(PushButton, self).mousePressEvent(event)
		if self.clicked is not None:
			self.clicked()

	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		if self.setting_color:
			return
		self.setStyleSheet("color: white; background-color: #6400CF; border: 15px solid #6400CF;")
		super(PushButton, self).mouseReleaseEvent(event)

	def animationFinished(self):
		self.setting_color = False
		self.setStyleSheet("color: white; background-color: #8400FF; border: 15px solid #8400FF;")

	def setColor(self, color: QColor):
		if color.getRgb() in [(0, 0, 0, 0), (0, 0, 1, 1), (1, 0, 2, 2), (1, 0, 3, 3), (2, 0, 4, 4), (2, 0, 4, 4), (2, 0, 5, 5), (3, 0, 6, 6), (3, 0, 7, 7), (4, 0, 8, 8), (4, 0, 9, 9), (5, 0, 9, 9)]:
			return
		self.setStyleSheet(f"color: white; background-color: rgba({color.getRgb()[0]}, {color.getRgb()[1]}, {color.getRgb()[2]}, {color.getRgb()[3]});")

	color = pyqtProperty(QColor, fset=setColor)


class Label(QLabel):
	def __init__(self, parent, text=""):
		super(Label, self).__init__(parent=parent)
		self.setText(text)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)

	def setColor(self, color):
		palette = self.palette()
		palette.setColor(self.foregroundRole(), color)
		self.setPalette(palette)

	color = pyqtProperty(QColor, fset=setColor)


class QuitButton(QPushButton):
	def __init__(self, parent):
		super(QuitButton, self).__init__(parent=parent)
		self.setText("×")
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.pressed.connect(QApplication.quit)
		self.status_tip = Label(parent, text="Quit")
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


class OptionsButton(QPushButton):
	def __init__(self, text, parent, pressed_function=None):
		super(OptionsButton, self).__init__(parent=parent)
		self.pressed_function = pressed_function
		self.text = Label(self, text)
		self.text.resize(self.size())
		self.text.setWordWrap(True)
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
	
	def resizeEvent(self, event):
		self.text.resize(event.size())
		super(OptionsButton, self).resizeEvent(event)
	
	def enterEvent(self, event) -> None:
		if self.styleSheet().split()[1] == "white;":
			self.setStyleSheet("background-color: #EEEEEE; border: 12px solid #EEEEEE; color: black")
		super(OptionsButton, self).enterEvent(event)
	
	def leaveEvent(self, event) -> None:
		if self.styleSheet().split()[1] == "#EEEEEE;":
			self.setStyleSheet("background-color: white; border: 12px solid white; color: black")
		super(OptionsButton, self).leaveEvent(event)
	
	def mousePressEvent(self, event) -> None:
		if self.pressed_function is not None:
			self.pressed_function(self.text.text())
		super(OptionsButton, self).mousePressEvent(event)
	

class StartGame(QPushButton):
	def __init__(self, parent, text, pressed_function=None):
		super(StartGame, self).__init__(parent=parent)
		self.pressed_function = pressed_function
		self.setText(text)
		self.setFixedHeight(75)
		self.setStyleSheet("background-color: white; border: 5px solid white; color: black;")
		self.setCursor(Qt.CursorShape.PointingHandCursor)
	
	def enterEvent(self, event) -> None:
		self.setStyleSheet("background-color: #EEEEEE; border: 5px solid #EEEEEE; color: black;")
		super(StartGame, self).enterEvent(event)

	def leaveEvent(self, event) -> None:
		self.setStyleSheet("background-color: white; border: 5px solid white; color: black;")
		super(StartGame, self).leaveEvent(event)
	
	def mousePressEvent(self, event) -> None:
		self.setStyleSheet("background-color: black; border: 5px solid black; color: white;")
		if self.pressed_function is not None:
			self.pressed_function()
		super(StartGame, self).mousePressEvent(event)
	
	def mouseReleaseEvent(self, event) -> None:
		self.setStyleSheet("background-color: white; border: 5px solid white; color: black;")
		super(StartGame, self).mouseReleaseEvent(event)


class OptionButton(QPushButton):
	def __init__(self, parent, text=""):
		super(OptionButton, self).__init__(text, parent=parent)
		self.setStyleSheet("width: 100%; height: 30px; background-color: transparent;")
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.selected = False
	
	def enterEvent(self, event) -> None:
		self.setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.2);")
		super(OptionButton, self).enterEvent(event)
	
	def leaveEvent(self, event) -> None:
		if not self.selected:
			self.setStyleSheet("width: 100%; height: 30px; background-color: transparent;")
		else:
			self.setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.4);")
		super(OptionButton, self).leaveEvent(event)
	
	def mousePressEvent(self, event) -> None:
		self.selected = not self.selected
		self.setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.4);")
		super(OptionButton, self).mousePressEvent(event)
	
	def mouseReleaseEvent(self, event) -> None:
		if not self.selected:
			self.setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.2);")
		super(OptionButton, self).mouseReleaseEvent(event)
	

class FENInput(QLineEdit):
	def __init__(self, parent, key_press_function=None):
		super(FENInput, self).__init__(parent=parent)
		self.key_press_function = key_press_function
	
	def keyPressEvent(self, event) -> None:
		if self.key_press_function is not None:
			self.key_press_function()
		super(FENInput, self).keyPressEvent(event)


class PGNInput(QTextEdit):
	def __init__(self, parent, key_press_function=None):
		super(PGNInput, self).__init__(parent=parent)
		self.key_press_function = key_press_function
	
	def keyPressEvent(self, event) -> None:
		if self.key_press_function is not None:
			self.key_press_function()
		super(PGNInput, self).keyPressEvent(event)


class MainPage(QWidget):
	def __init__(self, parent, two_player_mode_function=None):
		super(MainPage, self).__init__(parent=parent)
		self.select_mode_label_animation, self.two_player_mode_animation = None, None
		self.two_player_mode_function = two_player_mode_function
		self.quit_button = QuitButton(self)
		self.quit_button.hide()
		self.animated = False
		self.options = None
		self.options_widgets = None
		self.title = Label(self, text="Chess")
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
		self.select_mode_label = Label(self, text="Select a mode")
		self.select_mode_label.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-Bold.ttf"))[0], 30))
		self.select_mode_animation = QPropertyAnimation(self.select_mode_label, b"color")
		self.select_mode_animation.setLoopCount(1)
		self.select_mode_animation.setDuration(20000)
		self.select_mode_animation.setStartValue(QColor("#CC00FF"))
		self.select_mode_animation.setEndValue(QColor("#1B00FF"))
		self.select_mode_animation.finished.connect(lambda: self.changeAnimationDirection(self.select_mode_animation))
		self.two_player_mode_button = PushButton(self, text="2 Player Mode", clicked=self.twoPlayers)
		self.select_mode_label.setColor(QColor("transparent"))

	@staticmethod
	def changeAnimationDirection(animation):
		animation.setDirection(int(not animation.direction()))
		animation.start()
	
	def twoPlayers(self):
		def styleTimeControlButtons(text):
			nonlocal time_control_total, time_control_total_increment, time_control_move, time_control_selected, time_control_widget_total, time_control_widget_total_increment, time_control_widget_move, time_control_display
			time_control_total.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			time_control_total_increment.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			time_control_move.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			time_control_unlimited.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			time_control_selected = text
			time_control_display.setText("10.0m+0s")
			if text == "Total Time":
				time_control_widget_total_increment.hide()
				time_control_widget_move.hide()
				time_control_widget_total.show()
				time_control_total.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			elif text == "Total Time + Increment Per Move":
				time_control_widget_total.hide()
				time_control_widget_move.hide()
				time_control_widget_total_increment.show()
				time_control_total_increment.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			elif text == "Unlimited":
				time_control_display.setText("unlimited")
				time_control_widget_total.hide()
				time_control_widget_move.hide()
				time_control_widget_total_increment.hide()
				time_control_unlimited.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			else:
				time_control_widget_total.hide()
				time_control_widget_total_increment.hide()
				time_control_widget_move.show()
				time_control_move.setStyleSheet("background-color: black; border: 12px solid black; color: white;")

		def styleVariantButtons(text):
			nonlocal variant_standard, variant_antichess, variant_threecheck, variant_selected
			variant_standard.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			variant_antichess.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			variant_threecheck.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			variant_selected = text
			if text == "Standard":
				variant_standard.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			elif text == "Antichess":
				variant_antichess.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			else:
				variant_threecheck.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		
		def stylePositionButtons(text):
			nonlocal position_fen, position_pgn, selected_position, position_widget_fen, position_widget_pgn
			position_fen.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			position_pgn.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			selected_position = text
			if text == "FEN":
				position_widget_pgn.hide()
				position_widget_fen.show()
				position_fen.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			else:
				position_widget_pgn.show()
				position_widget_fen.hide()
				position_pgn.setStyleSheet("background-color: black; border: 12px solid black; color: white;")

		def updatePositionText():
			nonlocal position_widget_fen, position_widget_pgn, selected_position, position_text
			if selected_position == "FEN":
				position_text = position_widget_fen.text()
			else:
				position_text = position_widget_pgn.toPlainText()

		def changeTimeDisplay(slider, value):
			nonlocal time_control_display, time_control_widget_total_increment_total, time_control_widget_total_increment_increment
			if slider == "total":
				time_control_display.setText(str(value / 10) + "m" + "+0s")
			elif slider == "inc_total":
				if "+" not in time_control_display.text():
					time_control_display.setText(str(time_control_widget_total_increment_total.value()) + "+" + str(time_control_widget_total_increment_increment.value()))
				time_control_display.setText(str(value / 10) + "m+" + str(time_control_widget_total_increment_increment.value()) + "s")
			elif slider == "inc_inc":
				if "+" not in time_control_display.text():
					time_control_display.setText(str(time_control_widget_total_increment_total.value()) + "+" + str(time_control_widget_total_increment_increment.value()))
				time_control_display.setText(str(time_control_widget_total_increment_total.value() / 10) + "m+" + str(value) + "s")
			else:
				time_control_display.setText(str(value) + "s")

		def startGame():
			nonlocal time_control_display, variant_selected, selected_position, position_text
			updatePositionText()
			self.two_player_mode_function(time_control_display.text(), variant_selected, selected_position, position_text)
			self.options.deleteLater()
			self.options = self.options_widgets = None

		# Options scroll area
		self.options = QGroupBox(self)
		options_layout = QVBoxLayout()
		# Title
		title = Label(self.options, "New 2 Player Game")
		title.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-Bold.ttf"))[0], 20))
		# Add space
		spacing = QWidget(self.options)
		spacing.setFixedSize(QSize(1, 30))
		# Time control section
		time_control_button = OptionButton(self, "Time Control")
		time_control_group = QGroupBox(self.options)
		time_control_group.setStyleSheet("background-color: #AAA;")
		time_control_button.pressed.connect(lambda time_control_group=time_control_group: time_control_group.show() if time_control_group.isHidden() else time_control_group.hide())
		time_control_group.setFixedHeight(math.floor(self.height() / 6))
		time_control_group_layout = QGridLayout()
		time_control_group_layout.setSpacing(0)
		time_control_display = Label(time_control_group, "10.0m+0s")
		time_control_selected = "Total Time"
		time_control_buttons = QGroupBox(time_control_group)
		time_control_buttons_layout = QHBoxLayout()
		time_control_buttons_layout.setSpacing(0)
		time_control_total = OptionsButton("Total Time", time_control_buttons, styleTimeControlButtons)
		time_control_total.setFixedSize(QSize(self.width() // 12, self.height() // 17))
		time_control_total.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		time_control_total_increment = OptionsButton("Total Time + Increment Per Move", time_control_buttons, styleTimeControlButtons)
		time_control_total_increment.setFixedSize(QSize(self.width() // 12, self.height() // 17))
		time_control_move = OptionsButton("Time Per Move", time_control_buttons, styleTimeControlButtons)
		time_control_move.setFixedSize(QSize(self.width() // 12, self.height() // 17))
		time_control_unlimited = OptionsButton("Unlimited", time_control_buttons, styleTimeControlButtons)
		time_control_unlimited.setFixedSize(QSize(self.width() // 12, self.height() // 17))
		time_control_buttons_layout.addStretch()
		time_control_buttons_layout.addWidget(time_control_total)
		time_control_buttons_layout.addSpacing(5)
		time_control_buttons_layout.addWidget(time_control_total_increment)
		time_control_buttons_layout.addSpacing(5)
		time_control_buttons_layout.addWidget(time_control_move)
		time_control_buttons_layout.addSpacing(5)
		time_control_buttons_layout.addWidget(time_control_unlimited)
		time_control_buttons_layout.addStretch()
		time_control_buttons.setLayout(time_control_buttons_layout)
		time_control_widget = QGroupBox(time_control_group)
		time_control_widget_layout = QVBoxLayout()
		time_control_widget_layout.setSpacing(0)
		time_control_widget_total = QSlider(Qt.Orientation.Horizontal, time_control_widget)
		time_control_widget_total.setRange(1, 750)
		time_control_widget_total.setValue(100)
		time_control_widget_total.valueChanged.connect(lambda value: changeTimeDisplay("total", value))
		time_control_widget_total_increment = QGroupBox()
		time_control_widget_total_increment_layout = QVBoxLayout()
		time_control_widget_total_increment_layout.setSpacing(0)
		time_control_widget_total_increment_total = QSlider(Qt.Orientation.Horizontal, time_control_widget_total_increment)
		time_control_widget_total_increment_total.valueChanged.connect(lambda value: changeTimeDisplay("inc_total", value))
		time_control_widget_total_increment_total.setRange(0, 500)
		time_control_widget_total_increment_increment = QSlider(Qt.Orientation.Horizontal, time_control_widget_total_increment)
		time_control_widget_total_increment_increment.valueChanged.connect(lambda value: changeTimeDisplay("inc_inc", value))
		time_control_widget_total_increment_increment.setRange(0, 100)
		time_control_widget_total_increment_layout.addWidget(time_control_widget_total_increment_total)
		time_control_widget_total_increment_layout.addWidget(time_control_widget_total_increment_increment)
		time_control_widget_total_increment_layout.addStretch()
		time_control_widget_total_increment.setLayout(time_control_widget_total_increment_layout)
		time_control_widget_total_increment.hide()
		time_control_widget_move = QSlider(Qt.Orientation.Horizontal, time_control_widget)
		time_control_widget_move.valueChanged.connect(lambda value: changeTimeDisplay("move", value))
		time_control_widget_move.hide()
		time_control_widget_layout.addWidget(time_control_widget_total)
		time_control_widget_layout.addWidget(time_control_widget_total_increment)
		time_control_widget_layout.addWidget(time_control_widget_move)
		time_control_widget.setLayout(time_control_widget_layout)
		time_control_group_layout.addWidget(time_control_display, 1, 1)
		time_control_group_layout.addWidget(time_control_buttons, 2, 1)
		time_control_group_layout.addWidget(time_control_widget, 3, 1)
		time_control_group.setLayout(time_control_group_layout)
		time_control_group.hide()
		# Variant section
		variant_selected = "Standard"
		variant_button = OptionButton(self, "Chess Variant")
		variant_group = QGroupBox(self.options)
		variant_group.setStyleSheet("background-color: #AAA;")
		variant_button.pressed.connect(lambda variant_group=variant_group: variant_group.show() if variant_group.isHidden() else variant_group.hide())
		variant_group.setFixedHeight(math.floor(self.height() / 15))
		variant_group_layout = QGridLayout()
		variant_group_layout.setSpacing(5)
		variant_standard = OptionsButton("Standard", variant_group, styleVariantButtons)
		variant_standard.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		variant_antichess = OptionsButton("Antichess", variant_group, styleVariantButtons)
		variant_threecheck = OptionsButton("Three Check", variant_group, styleVariantButtons)
		variant_group_layout.addWidget(variant_standard, 1, 1)
		variant_group_layout.addWidget(variant_antichess, 1, 2)
		variant_group_layout.addWidget(variant_threecheck, 2, 1)
		variant_group.setLayout(variant_group_layout)
		variant_group.hide()
		# Position section
		selected_position = "FEN"
		position_text = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
		position_button = OptionButton(self, "FEN/PGN")
		position_group = QGroupBox(self.options)
		position_group.setStyleSheet("background-color: #AAA;")
		position_button.pressed.connect(lambda position_group=position_group: position_group.show() if position_group.isHidden() else position_group.hide())
		position_group.setFixedHeight(math.floor(self.height() / 8))
		position_group_layout = QVBoxLayout()
		position_group_layout.setSpacing(0)
		position_buttons = QGroupBox(time_control_group)
		position_buttons_layout = QHBoxLayout()
		position_buttons_layout.setSpacing(5)
		position_fen = OptionsButton("FEN", position_buttons, stylePositionButtons)
		position_fen.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		position_pgn = OptionsButton("PGN", position_buttons, stylePositionButtons)
		position_buttons_layout.addWidget(position_fen)
		position_buttons_layout.addWidget(position_pgn)
		position_buttons.setLayout(position_buttons_layout)
		position_widget = QGroupBox(position_group)
		position_widget_layout = QVBoxLayout()
		position_widget_layout.setSpacing(0)
		position_widget_fen = FENInput(self, key_press_function=updatePositionText)
		position_widget_fen.setAttribute(Qt.WA_MacShowFocusRect, 0)
		position_widget_fen.setStyleSheet("background-color: #999; border: 3px solid #999;")
		position_widget_pgn = PGNInput(self, key_press_function=updatePositionText)
		position_widget_pgn.setStyleSheet("background-color: #999; border: 3px solid #999;")
		position_widget_pgn.hide()
		position_widget_layout.addWidget(position_widget_fen)
		position_widget_layout.addWidget(position_widget_pgn)
		position_widget_layout.addStretch()
		position_widget.setLayout(position_widget_layout)
		position_group_layout.addWidget(position_buttons)
		position_group_layout.addWidget(position_widget)
		position_group.setLayout(position_group_layout)
		position_group.hide()
		# Add widgets to options
		start_game = StartGame(self.options, "Start Game", startGame)
		options_layout.setSpacing(0)
		options_layout.addWidget(title)
		options_layout.addWidget(spacing)
		options_layout.addWidget(time_control_button)
		options_layout.addWidget(time_control_group)
		options_layout.addWidget(variant_button)
		options_layout.addWidget(variant_group)
		options_layout.addWidget(position_button)
		options_layout.addWidget(position_group)
		options_layout.addStretch()
		options_layout.addWidget(start_game)
		self.options.setStyleSheet("background-color: white; border: none;")
		self.options.setLayout(options_layout)
		self.options.setFixedSize(QSize(math.floor(self.width() / 1.5), math.floor(self.height() / 1.5)))
		self.options.move(QPoint((self.width() - self.options.width()) // 2, (self.height() - self.options.height()) // 2))
		self.options.show()
		self.options_widgets = {"tc_total": time_control_total, "tc_total_increment": time_control_total_increment, "tc_move": time_control_move, "tc_unlimited": time_control_unlimited}

	def resizeEvent(self, event: QResizeEvent) -> None:
		if event.size().width() > event.size().height():
			min_size = event.size().height()
		else:
			min_size = event.size().width()
		if event.size().width() > 1500:
			self.title.setFont(QFont("Impact", self.width() // 15, italic=True))
		else:
			self.title.setFont(QFont("Impact", 100, italic=True))
		self.title.move((event.size().width() - self.title.width()) // 2, event.size().height() // 20)
		self.select_mode_label.move((event.size().width() - self.select_mode_label.width()) // 2, (event.size().height() // 20) + 200)
		self.two_player_mode_button.move((event.size().width() - self.two_player_mode_button.width()) // 2, (event.size().height() // 20) + 250)
		if self.options is not None:
			self.options.setFixedSize(QSize(math.floor(self.width() / 1.5), math.floor(self.height() / 1.5)))
			self.options.move(QPoint((self.width() - self.options.width()) // 2, (self.height() - self.options.height()) // 2))
			if event.size().width() < 970 or event.size().height() < 612:
				self.options_widgets["tc_total"].setFixedSize(QSize(97, 51))
				self.options_widgets["tc_total_increment"].setFixedSize(QSize(97, 51))
				self.options_widgets["tc_move"].setFixedSize(QSize(97, 51))
				self.options_widgets["tc_unlimited"].setFixedSize(QSize(97, 51))
			else:
				self.options_widgets["tc_total"].setFixedSize(QSize(event.size().width() // 10, event.size().height() // 12))
				self.options_widgets["tc_total_increment"].setFixedSize(QSize(event.size().width() // 10, event.size().height() // 12))
				self.options_widgets["tc_move"].setFixedSize(QSize(event.size().width() // 10, event.size().height() // 12))
				self.options_widgets["tc_unlimited"].setFixedSize(QSize(event.size().width() // 10, event.size().height() // 12))
		if min_size > 720:
			self.quit_button.resize(QSize(min_size // 20, min_size // 20))
		else:
			self.quit_button.resize(QSize(36, 36))
		if not self.animated:
			self.title_opening_animation.setEndValue(QSize(self.title.maximumWidth(), 200))
			self.title_opening_animation.setStartValue(QSize(self.title.maximumWidth(), 0))
			self.title_opening_animation.start()
			self.animated = True
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
		self.setMinimumSize(QSize(720, 500))
		self.stacked_pages, self.stacks = QStackedWidget(self), {"main-page": MainPage(self, two_player_mode_function=self.twoPlayerMode), "two-players": twoplayers.TwoPlayers(self)}
		self.stacked_pages.addWidget(self.stacks["main-page"])
		self.stacked_pages.addWidget(self.stacks["two-players"])
		self.showFullScreen()
		self.stacked_pages.move(0, 0)
		self.stacked_pages.setFixedSize(self.size())

	def twoPlayerMode(self, time_control, variant, position_type, position):
		self.stacks["two-players"].setTimeControl(time_control)
		self.stacks["two-players"].setupBoard(variant, position_type, position)
		self.setIndex(1, self.stacks["two-players"])
		self.stacks["two-players"].startClocks()
		self.setWindowTitle("2-Player Chess Game: White to move")

	def resetTwoPlayerGame(self):
		self.stacks["two-players"].deleteLater()
		self.stacks["two-players"] = twoplayers.TwoPlayers(self)
		self.stacked_pages.addWidget(self.stacks["two-players"])

	def setIndex(self, index, widget):
		self.stacked_pages.setCurrentIndex(index)
		widget.animation.start()

	def resizeEvent(self, event: QResizeEvent) -> None:
		self.stacks["main-page"].resize(event.size())
		super(Window, self).resizeEvent(event)


application, window = QApplication([]), Window()
application.exec_()
