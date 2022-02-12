# -*- coding: utf-8 -*-

"""
main.py
Chess Game Main File
"""
try:
	from PyQt5.QtGui import *
except ModuleNotFoundError:
	print("The PyQt5 library is not installed. Use the 'pip3 install PyQt5' bash command to install it.")
	exit()

try:
	import chess
	chess.Game()
except (AttributeError, ModuleNotFoundError):
	__import__("os").system("pip3 install git+https://github.com/DanielMiao1/chess")
	import chess


from PyQt5.QtSvg import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
from PyQt5.QtWidgets import *

import math
import computer
import settings
import twoplayers


def PGNValid(PGN):
	contains_moves = False
	for i in PGN.splitlines():
		if i.strip() == "" or (i.startswith("[") and i.endswith("]") and " " in i):
			continue
		if i.startswith("1."):
			contains_moves = True
			continue
		return False
	return contains_moves


class PushButton(QPushButton):
	def __init__(self, parent, text="", clicked=None):
		super(PushButton, self).__init__(parent)
		self.setText(text)
		self.clicked, self.setting_color = clicked, True
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-SemiBold.ttf"))[0], 15))
		self.setStyleSheet("color: transparent; background-color: transparent; border: 15px solid transparent;")
		self.setFocusPolicy(Qt.StrongFocus)

	def focusInEvent(self, event) -> None:
		if event.reason() <= 2:
			if self.setting_color:
				return
			self.setStyleSheet("color: white; background-color: #6400CF; border: 15px solid #6400CF;")
		super(PushButton, self).focusInEvent(event)

	def focusOutEvent(self, event) -> None:
		if event.reason() <= 2:
			if self.setting_color:
				return
			self.setStyleSheet("color: white; background-color: #8400FF; border: 15px solid #8400FF;")
		super(PushButton, self).focusOutEvent(event)

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
		if self.clicked is not None:
			self.clicked()
		self.pressed.emit()

	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		if self.setting_color:
			return
		self.setStyleSheet("color: white; background-color: #6400CF; border: 15px solid #6400CF;")
		super(PushButton, self).mouseReleaseEvent(event)

	def keyPressEvent(self, event) -> None:
		if event.key() in [Qt.Key_Enter, Qt.Key_Return] and self.parent().two_player_mode_options is None and self.parent().computer_mode_options is None:
			self.pressed.emit()
		if event.key() == Qt.Key_Space:
			self.pressed.emit()
		super(PushButton, self).keyPressEvent(event)

	def animationFinished(self):
		self.setting_color = False
		self.setStyleSheet("color: white; background-color: #8400FF; border: 15px solid #8400FF;")

	def setColor(self, color: QColor):
		if color.getRgb() in [(0, 0, 0, 0), (0, 0, 1, 1), (1, 0, 2, 2), (1, 0, 3, 3), (2, 0, 4, 4), (2, 0, 4, 4), (2, 0, 5, 5), (3, 0, 6, 6), (3, 0, 7, 7), (4, 0, 8, 8), (4, 0, 9, 9), (5, 0, 9, 9)]:
			return
		self.setStyleSheet(f"color: white; background-color: rgba({color.getRgb()[0]}, {color.getRgb()[1]}, {color.getRgb()[2]}, {color.getRgb()[3]});")

	color = pyqtProperty(QColor, fset=setColor)


class Label(QLabel):
	def __init__(self, parent, text="", selectable=True):
		super(Label, self).__init__(parent=parent)
		self.setText(text)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
		if selectable:
			self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

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
		self.setFocusPolicy(Qt.StrongFocus)

	def focusInEvent(self, event) -> None:
		if event.reason() <= 2:
			self.status_tip.show()
			self.setStyleSheet("color: black; background-color: red; border: none;")
		super(QuitButton, self).focusInEvent(event)

	def focusOutEvent(self, event) -> None:
		if event.reason() <= 2:
			self.status_tip.hide()
			self.setStyleSheet("color: black; background-color: white; border: none;")
		super(QuitButton, self).focusOutEvent(event)

	def enterEvent(self, event: QEvent) -> None:
		self.status_tip.show()
		self.setStyleSheet("color: black; background-color: red; border: none;")
		super(QuitButton, self).enterEvent(event)

	def leaveEvent(self, event: QEvent) -> None:
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
		super(QuitButton, self).leaveEvent(event)


class OptionsButton(QPushButton):
	def __init__(self, text, parent, pressed_function=None, center_text=False, border=True, size=False):
		super(OptionsButton, self).__init__(parent=parent)
		self.pressed_function = pressed_function
		self.text = QLabel(text, self)
		if center_text:
			self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.text.resize(self.size())
		self.text.setWordWrap(True)
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.border = border
		if size:
			self.setFixedSize(size)
		if self.border:
			self.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
		else:
			self.setStyleSheet("background-color: white; border: none; color: black;")

	def resizeEvent(self, event):
		self.text.resize(event.size())
		super(OptionsButton, self).resizeEvent(event)

	def enterEvent(self, event) -> None:
		if self.styleSheet().split()[1] == "white;":
			if self.border:
				self.setStyleSheet("background-color: #EEEEEE; border: 12px solid #EEEEEE; color: black")
			else:
				self.setStyleSheet("background-color: #EEEEEE; border: none; color: black")
		super(OptionsButton, self).enterEvent(event)

	def leaveEvent(self, event) -> None:
		if self.styleSheet().split()[1] == "#EEEEEE;":
			if self.border:
				self.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			else:
				self.setStyleSheet("background-color: white; border: none; color: black;")
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
		self.setCursor(Qt.CursorShape.PointingHandCursor)

	def mousePressEvent(self, event) -> None:
		if self.pressed_function is not None:
			self.pressed_function()
		super(StartGame, self).mousePressEvent(event)


class OptionButton(QPushButton):
	def __init__(self, parent, text=""):
		super(OptionButton, self).__init__(text, parent=parent)
		self.setStyleSheet("width: 100%; height: 30px; background-color: transparent;")
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.selected = False

	def focusInEvent(self, event):
		if event.reason() <= 2:
			self.setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.2);")
		super(OptionButton, self).focusInEvent(event)

	def focusOutEvent(self, event):
		if event.reason() <= 2:
			self.setStyleSheet("width: 100%; height: 30px; background-color: transparent;")
		super(OptionButton, self).focusOutEvent(event)

	def keyPressEvent(self, event: QKeyEvent):
		if event.text() == " ":
			if not self.selected:
				self.setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.4);")
			else:
				self.setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.2);")
			self.selected = not self.selected
		super(OptionButton, self).keyPressEvent(event)

	def enterEvent(self, event: QEnterEvent) -> None:
		self.setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.2);")
		super(OptionButton, self).enterEvent(event)

	def leaveEvent(self, event) -> None:
		if not self.selected:
			self.setStyleSheet("width: 100%; height: 30px; background-color: transparent;")
		else:
			self.setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.4);")
		super(OptionButton, self).leaveEvent(event)

	def mousePressEvent(self, event) -> None:
		if event.button() == Qt.MouseButton.LeftButton:
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


class SettingsButton(PushButton):
	def __init__(self, parent):
		super(SettingsButton, self).__init__(parent=parent)
		self.resize(QSize(64, 64))
		self.svg = QSvgWidget(self)
		self.svg.renderer().load(bytearray('<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"><path d="M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 1.987l.169.311c.446.82.023 1.841-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705 1.987-1.987l-.169-.311a1.464 1.464 0 0 1 .872-2.105l.34-.1c1.4-.413 1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 0 0 1-2.105-.872l-.1-.34zM8 10.93a2.929 2.929 0 1 1 0-5.86 2.929 2.929 0 0 1 0 5.858z"/></svg>', encoding='utf-8'))
		self.setStyleSheet("background-color: transparent; border: none;")
		self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

	def focusInEvent(self, event) -> None:
		self.setStyleSheet("background-color: #CCC; border: none;")
		super(SettingsButton, self).focusInEvent(event)

	def focusOutEvent(self, event) -> None:
		self.setStyleSheet("background-color: transparent; border: none;")
		super(SettingsButton, self).focusOutEvent(event)

	def enterEvent(self, event) -> None:
		self.setStyleSheet("background-color: #CCC; border: none;")
		super(SettingsButton, self).enterEvent(event)

	def leaveEvent(self, event) -> None:
		self.setStyleSheet("background-color: transparent; border: none;")
		super(SettingsButton, self).leaveEvent(event)

	def mousePressEvent(self, event) -> None:
		self.pressed.emit()

	def resizeEvent(self, event) -> None:
		self.svg.move(QPoint((event.size().width() - 16) // 2, (event.size().height() - 16) // 2))
		super(SettingsButton, self).resizeEvent(event)


class MainPage(QWidget):
	def __init__(self, parent, two_player_mode_function, computer_mode_function):
		super(MainPage, self).__init__(parent=parent)
		self.select_mode_label_animation = self.two_player_mode_animation = self.computer_mode_button_animation = None
		self.two_player_mode_function = two_player_mode_function
		self.computer_mode_function = computer_mode_function
		self.quit_button = QuitButton(self)
		self.quit_button.hide()
		self.animated = False
		self.two_player_mode_options = self.two_player_mode_options_widgets = self.two_player_mode_options_close = self.computer_mode_options = self.computer_mode_options_widgets = self.computer_mode_options_close = None
		self.title = Label(self, text="Chess", selectable=False)
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
		self.two_player_mode_button = PushButton(self, text="2 Player Mode")
		self.two_player_mode_button.pressed.connect(self.twoPlayers)
		self.computer_mode_button = PushButton(self, text="Player-Computer Mode")
		self.computer_mode_button.pressed.connect(self.computer)
		self.select_mode_label.setColor(QColor("transparent"))
		self.settings_button = SettingsButton(self)
		self.settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
		self.settings_button.pressed.connect(self.settings)

	@staticmethod
	def changeAnimationDirection(animation):
		animation.setDirection(int(not animation.direction()))
		animation.start()

	def settings(self):
		self.parent().parent().setIndex(2, self.parent().parent().stacks["settings"])

	def computer(self):
		def styleLevelButtons(text):
			nonlocal computer_level_0, computer_level_1, computer_level_2, computer_level_3, computer_custom, computer_level, computer_path
			computer_level_0.setStyleSheet("background-color: white; border: none; color: black;")
			computer_level_1.setStyleSheet("background-color: white; border: none; color: black;")
			computer_level_2.setStyleSheet("background-color: white; border: none; color: black;")
			computer_level_3.setStyleSheet("background-color: white; border: none; color: black;")
			computer_custom.setStyleSheet("background-color: white; border: none; color: black;")
			if text == "0":
				computer_path = False
				computer_level_0.setStyleSheet("background-color: black; border: none; color: white;")
			elif text == "1":
				computer_path = False
				computer_level_1.setStyleSheet("background-color: black; border: none; color: white;")
			elif text == "2":
				computer_path = False
				computer_level_2.setStyleSheet("background-color: black; border: none; color: white;")
			elif text == "3":
				computer_path = False
				computer_level_3.setStyleSheet("background-color: black; border: none; color: white;")
			else:
				computer_custom.setStyleSheet("background-color: black; border: none; color: white;")
			computer_level = text

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
				if position_text.strip() == "" or chess.functions.FENvalid(position_text.strip()):
					position_widget_fen.setStyleSheet("background-color: #999; border: 3px solid #999;")
				else:
					position_widget_fen.setStyleSheet("background-color: #ff7e7e; border: 3px solid #ff7e7e;")
			else:
				position_text = position_widget_pgn.toPlainText()
				if position_text.strip() == "" or PGNValid(position_text):
					position_widget_pgn.setStyleSheet("background-color: #999; border: 3px solid #999;")
				else:
					position_widget_pgn.setStyleSheet("background-color: #ff7e7e; border: 3px solid #ff7e7e;")

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
			nonlocal time_control_display, selected_position, position_text, computer_level, computer_path
			updatePositionText()
			if selected_position == "FEN" and position_text.strip() == "":
				position_text = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
			close_dialog()
			self.computer_mode_function("level" if computer_level else "path", computer_level if computer_level else computer_path, time_control_display.text(), selected_position, position_text.strip())

		def close_dialog():
			self.computer_mode_options.deleteLater()
			self.computer_mode_options_close.deleteLater()
			self.computer_mode_options = self.computer_mode_options_widgets = self.computer_mode_options_close = None

		def setupCustomEngine():
			nonlocal computer_level_0, computer_custom, computer_level, computer_path
			file = QFileDialog.getOpenFileName(None, "Select Engine File")
			if not file[0] and not file[1]:
				computer_level = "0"
				computer_custom.setStyleSheet("background-color: white; border: none; color: black;")
				computer_level_0.setStyleSheet("background-color: black; border: none; color: white;")
				return
			computer_level = False
			computer_path = file[0]

		# Options scroll area
		self.computer_mode_options = QGroupBox(self)
		options_layout = QVBoxLayout()
		# Title and close button
		title = Label(self.computer_mode_options, "New Player vs Computer Game")
		title.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-Bold.ttf"))[0], 20))
		self.computer_mode_options_close = QPushButton("×", self)
		self.computer_mode_options_close.pressed.connect(close_dialog)
		self.computer_mode_options_close.setCursor(Qt.CursorShape.PointingHandCursor)
		self.computer_mode_options_close.setStyleSheet("QPushButton { background-color: white; border: 12px solid white; } QPushButton:hover, QPushButton:focus { background-color: #EEE; border: 12px solid #EEE; }")
		self.computer_mode_options_close.show()
		# Add space
		spacing = QWidget(self.computer_mode_options)
		spacing.setFixedSize(QSize(1, 30))
		# Computer level section
		computer_path = False
		computer_level = "0"
		computer_level_button = OptionButton(self, "Computer Level")
		computer_level_group = QGroupBox(self.computer_mode_options)
		computer_level_group.setStyleSheet("background-color: #AAA;")
		computer_level_button.pressed.connect(lambda computer_level_group=computer_level_group: computer_level_group.show() if computer_level_group.isHidden() else computer_level_group.hide())
		computer_level_group.setFixedHeight(math.floor(self.height() / 6))
		computer_level_group_layout = QHBoxLayout()
		computer_level_group_layout.setSpacing(2)
		computer_level_0 = OptionsButton("0", self, pressed_function=styleLevelButtons, center_text=True, border=False, size=QSize(40, 40))
		computer_level_0.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		computer_level_1 = OptionsButton("1", self, pressed_function=styleLevelButtons, center_text=True, border=False, size=QSize(40, 40))
		computer_level_2 = OptionsButton("2", self, pressed_function=styleLevelButtons, center_text=True, border=False, size=QSize(40, 40))
		computer_level_3 = OptionsButton("3", self, pressed_function=styleLevelButtons, center_text=True, border=False, size=QSize(40, 40))
		computer_custom = OptionsButton("Custom Engine...", self, pressed_function=styleLevelButtons, center_text=True, border=False, size=QSize(150, 40))
		computer_custom.pressed.connect(setupCustomEngine)
		computer_level_group_layout.addStretch()
		computer_level_group_layout.addWidget(computer_level_0)
		computer_level_group_layout.addWidget(computer_level_1)
		computer_level_group_layout.addWidget(computer_level_2)
		computer_level_group_layout.addWidget(computer_level_3)
		computer_level_group_layout.addSpacing(10)
		computer_level_group_layout.addWidget(computer_custom)
		computer_level_group_layout.addStretch()
		computer_level_group.setLayout(computer_level_group_layout)
		computer_level_group.hide()
		# Time control section
		time_control_button = OptionButton(self, "Time Control")
		time_control_group = QGroupBox(self.computer_mode_options)
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
		time_control_total = OptionsButton("Total Time", time_control_buttons, styleTimeControlButtons, center_text=True, size=QSize(120, 50))
		time_control_total.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		time_control_total_increment = OptionsButton("Total Time + Increment Per Move", time_control_buttons, styleTimeControlButtons, center_text=True, size=QSize(120, 50))
		time_control_move = OptionsButton("Time Per Move", time_control_buttons, styleTimeControlButtons, center_text=True, size=QSize(120, 50))
		time_control_unlimited = OptionsButton("Unlimited", time_control_buttons, styleTimeControlButtons, center_text=True, size=QSize(120, 50))
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
		time_control_widget_total_increment_total.setRange(0, 500)
		time_control_widget_total_increment_total.valueChanged.connect(lambda value: changeTimeDisplay("inc_total", value))
		time_control_widget_total_increment_increment = QSlider(Qt.Orientation.Horizontal, time_control_widget_total_increment)
		time_control_widget_total_increment_increment.setRange(1, 100)
		time_control_widget_total_increment_increment.valueChanged.connect(lambda value: changeTimeDisplay("inc_inc", value))
		time_control_widget_total_increment_layout.addWidget(time_control_widget_total_increment_total)
		time_control_widget_total_increment_layout.addWidget(time_control_widget_total_increment_increment)
		time_control_widget_total_increment_layout.addStretch()
		time_control_widget_total_increment.setLayout(time_control_widget_total_increment_layout)
		time_control_widget_total_increment.hide()
		time_control_widget_move = QSlider(Qt.Orientation.Horizontal, time_control_widget)
		time_control_widget_move.setRange(1, 100)
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
		# Position section
		selected_position = "FEN"
		position_text = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
		position_button = OptionButton(self, "FEN/PGN")
		position_group = QGroupBox(self.computer_mode_options)
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
		position_widget_fen.textChanged.connect(updatePositionText)
		position_widget_pgn = PGNInput(self, key_press_function=updatePositionText)
		position_widget_pgn.setStyleSheet("background-color: #999; border: 3px solid #999;")
		position_widget_pgn.textChanged.connect(updatePositionText)
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
		start_game = StartGame(self.computer_mode_options, "Start Game", startGame)
		start_game.setStyleSheet("StartGame { background-color: white; border: 5px solid white; color: black; } StartGame:hover, StartGame:focus { background-color: #EEEEEE; border: 5px solid #EEEEEE; color: black; }")
		options_layout.setSpacing(0)
		options_layout.addWidget(title)
		options_layout.addWidget(spacing)
		options_layout.addWidget(computer_level_button)
		options_layout.addWidget(computer_level_group)
		options_layout.addWidget(time_control_button)
		options_layout.addWidget(time_control_group)
		options_layout.addWidget(position_button)
		options_layout.addWidget(position_group)
		options_layout.addStretch()
		options_layout.addWidget(start_game)
		self.computer_mode_options.setStyleSheet("background-color: white; border: none;")
		self.computer_mode_options.setLayout(options_layout)
		self.computer_mode_options.setFixedSize(QSize(math.floor(self.width() / 1.5), math.floor(self.height() / 1.5)))
		self.computer_mode_options.move(QPoint((self.width() - self.computer_mode_options.width()) // 2, (self.height() - self.computer_mode_options.height()) // 2))
		self.computer_mode_options.show()
		self.computer_mode_options.move(self.computer_mode_options.pos())
		self.computer_mode_options_widgets = {"level_group": computer_level_group, "level_button": computer_level_button, "tc_total": time_control_total, "tc_total_increment": time_control_total_increment, "tc_move": time_control_move, "tc_unlimited": time_control_unlimited, "time_control_group": time_control_group, "position_group": position_group, "time_control_button": time_control_button, "position_button": position_button, "startGame": startGame}
		if self.width() <= 1440 or self.height() <= 1080:
			self.computer_mode_options.setFixedSize(self.size())
			self.computer_mode_options.move(QPoint())
			self.computer_mode_options_close.move(QPoint())
			if not computer_level_button.isHidden():
				computer_level_button.hide()
				time_control_button.hide()
				position_button.hide()
			if computer_level_group.isHidden():
				computer_level_group.show()
			if time_control_group.isHidden():
				time_control_group.show()
			if position_group.isHidden():
				position_group.show()
			if options_layout.spacing() == 0:
				options_layout.setSpacing(5)
			computer_level_group.setFixedHeight(math.floor(self.height() / 11))
			computer_level_group.setStyleSheet("background-color: #DDD")
			time_control_group.setFixedHeight(math.floor(self.height() / 5))
			time_control_group.setStyleSheet("background-color: #DDD")
			position_group.setFixedHeight(math.floor(self.height() / 4))
			position_group.setStyleSheet("background-color: #DDD")
		else:
			self.computer_mode_options.setFixedSize(QSize(math.floor(self.width() / 1.5), math.floor(self.height() / 1.5)))
			self.computer_mode_options.move(QPoint((self.width() - self.computer_mode_options.width()) // 2, (self.height() - self.computer_mode_options.height()) // 2))
			self.computer_mode_options_close.move(self.computer_mode_options.pos())
			if self.computer_mode_options_widgets["level_button"].isHidden():
				self.computer_mode_options_widgets["level_button"].show()
				self.computer_mode_options_widgets["time_control_button"].show()
				self.computer_mode_options_widgets["position_button"].show()
			if self.computer_mode_options.layout().spacing() == 5:
				self.computer_mode_options.layout().setSpacing(0)
			self.computer_mode_options_widgets["level_group"].setFixedHeight(math.floor(self.height() / 20))
			self.computer_mode_options_widgets["time_control_group"].setFixedHeight(math.floor(self.height() / 6))
			self.computer_mode_options_widgets["position_group"].setFixedHeight(math.floor(self.height() / 8))

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
			nonlocal variant_standard, variant_antichess, variant_threecheck, variant_atomic, variant_selected
			variant_standard.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			variant_antichess.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			variant_threecheck.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			variant_atomic.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			variant_selected = text
			if text == "Standard":
				variant_standard.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			elif text == "Antichess":
				variant_antichess.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			elif text == "Atomic":
				variant_atomic.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
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
				if position_text.strip() == "" or chess.functions.FENvalid(position_text.strip()):
					position_widget_fen.setStyleSheet("background-color: #999; border: 3px solid #999;")
				else:
					position_widget_fen.setStyleSheet("background-color: #ff7e7e; border: 3px solid #ff7e7e;")
			else:
				position_text = position_widget_pgn.toPlainText()
				if position_text.strip() == "" or PGNValid(position_text):
					position_widget_pgn.setStyleSheet("background-color: #999; border: 3px solid #999;")
				else:
					position_widget_pgn.setStyleSheet("background-color: #ff7e7e; border: 3px solid #ff7e7e;")

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
			if selected_position == "FEN" and position_text.strip() == "":
				position_text = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
			close_dialog()
			self.two_player_mode_function(time_control_display.text(), variant_selected, selected_position, position_text.strip())

		def close_dialog():
			self.two_player_mode_options.deleteLater()
			self.two_player_mode_options_close.deleteLater()
			self.two_player_mode_options = self.two_player_mode_options_widgets = self.two_player_mode_options_close = None

		# Options scroll area
		self.two_player_mode_options = QGroupBox(self)
		options_layout = QVBoxLayout()
		# Title and close button
		title = Label(self.two_player_mode_options, "New 2 Player Game")
		title.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-Bold.ttf"))[0], 20))
		self.two_player_mode_options_close = QPushButton("×", self)
		self.two_player_mode_options_close.pressed.connect(close_dialog)
		self.two_player_mode_options_close.setCursor(Qt.CursorShape.PointingHandCursor)
		self.two_player_mode_options_close.setStyleSheet("QPushButton { background-color: white; border: 12px solid white; } QPushButton:hover, QPushButton:focus { background-color: #EEE; border: 12px solid #EEE; }")
		self.two_player_mode_options_close.show()
		# Add space
		spacing = QWidget(self.two_player_mode_options)
		spacing.setFixedSize(QSize(1, 30))
		# Time control section
		time_control_button = OptionButton(self, "Time Control")
		time_control_group = QGroupBox(self.two_player_mode_options)
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
		time_control_total = OptionsButton("Total Time", time_control_buttons, styleTimeControlButtons, center_text=True)
		time_control_total.setFixedSize(QSize(self.width() // 12, self.height() // 17))
		time_control_total.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		time_control_total_increment = OptionsButton("Total Time + Increment Per Move", time_control_buttons, styleTimeControlButtons, center_text=True)
		time_control_total_increment.setFixedSize(QSize(self.width() // 12, self.height() // 17))
		time_control_move = OptionsButton("Time Per Move", time_control_buttons, styleTimeControlButtons, center_text=True)
		time_control_move.setFixedSize(QSize(self.width() // 12, self.height() // 17))
		time_control_unlimited = OptionsButton("Unlimited", time_control_buttons, styleTimeControlButtons, center_text=True)
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
		time_control_widget_total_increment_total.setRange(0, 500)
		time_control_widget_total_increment_total.valueChanged.connect(lambda value: changeTimeDisplay("inc_total", value))
		time_control_widget_total_increment_increment = QSlider(Qt.Orientation.Horizontal, time_control_widget_total_increment)
		time_control_widget_total_increment_increment.setRange(1, 100)
		time_control_widget_total_increment_increment.valueChanged.connect(lambda value: changeTimeDisplay("inc_inc", value))
		time_control_widget_total_increment_layout.addWidget(time_control_widget_total_increment_total)
		time_control_widget_total_increment_layout.addWidget(time_control_widget_total_increment_increment)
		time_control_widget_total_increment_layout.addStretch()
		time_control_widget_total_increment.setLayout(time_control_widget_total_increment_layout)
		time_control_widget_total_increment.hide()
		time_control_widget_move = QSlider(Qt.Orientation.Horizontal, time_control_widget)
		time_control_widget_move.setRange(1, 100)
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
		variant_group = QGroupBox(self.two_player_mode_options)
		variant_group.setStyleSheet("background-color: #AAA;")
		variant_button.pressed.connect(lambda variant_group=variant_group: variant_group.show() if variant_group.isHidden() else variant_group.hide())
		variant_group.setFixedHeight(math.floor(self.height() / 10))
		variant_group_layout = QGridLayout()
		variant_group_layout.setSpacing(5)
		variant_standard = OptionsButton("Standard", variant_group, styleVariantButtons)
		variant_standard.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		variant_antichess = OptionsButton("Antichess", variant_group, styleVariantButtons)
		variant_threecheck = OptionsButton("Three Check", variant_group, styleVariantButtons)
		variant_atomic = OptionsButton("Atomic", variant_group, styleVariantButtons)
		variant_group_layout.addWidget(variant_standard, 1, 1)
		variant_group_layout.addWidget(variant_antichess, 1, 2)
		variant_group_layout.addWidget(variant_threecheck, 2, 1)
		variant_group_layout.addWidget(variant_atomic, 2, 2)
		variant_group.setLayout(variant_group_layout)
		variant_group.hide()
		# Position section
		selected_position = "FEN"
		position_text = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
		position_button = OptionButton(self, "FEN/PGN")
		position_group = QGroupBox(self.two_player_mode_options)
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
		position_widget_fen.textChanged.connect(updatePositionText)
		position_widget_pgn = PGNInput(self, key_press_function=updatePositionText)
		position_widget_pgn.setStyleSheet("background-color: #999; border: 3px solid #999;")
		position_widget_pgn.textChanged.connect(updatePositionText)
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
		start_game = StartGame(self.two_player_mode_options, "Start Game", startGame)
		start_game.setStyleSheet("StartGame { background-color: white; border: 5px solid white; color: black; } StartGame:hover, StartGame:focus { background-color: #EEEEEE; border: 5px solid #EEEEEE; color: black; }")
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
		self.two_player_mode_options.setStyleSheet("background-color: white; border: none;")
		self.two_player_mode_options.setLayout(options_layout)
		self.two_player_mode_options.setFixedSize(QSize(math.floor(self.width() / 1.5), math.floor(self.height() / 1.5)))
		self.two_player_mode_options.move(QPoint((self.width() - self.two_player_mode_options.width()) // 2, (self.height() - self.two_player_mode_options.height()) // 2))
		self.two_player_mode_options.show()
		self.two_player_mode_options.move(self.two_player_mode_options.pos())
		self.two_player_mode_options_widgets = {"tc_total": time_control_total, "tc_total_increment": time_control_total_increment, "tc_move": time_control_move, "tc_unlimited": time_control_unlimited, "time_control_group": time_control_group, "variant_group": variant_group, "position_group": position_group, "time_control_button": time_control_button, "variant_button": variant_button, "position_button": position_button, "startGame": startGame}
		if self.width() <= 1440 or self.height() <= 1080:
			self.two_player_mode_options.setFixedSize(self.size())
			self.two_player_mode_options.move(QPoint())
			self.two_player_mode_options_close.move(QPoint())
			if not time_control_button.isHidden():
				time_control_button.hide()
				variant_button.hide()
				position_button.hide()
			if time_control_group.isHidden():
				time_control_group.show()
			if variant_group.isHidden():
				variant_group.show()
			if position_group.isHidden():
				position_group.show()
			if options_layout.spacing() == 0:
				options_layout.setSpacing(5)
			time_control_group.setFixedHeight(math.floor(self.height() / 3))
			time_control_group.setStyleSheet("background-color: #DDD")
			variant_group.setFixedHeight(math.floor(self.height() / 6))
			variant_group.setStyleSheet("background-color: #DDD")
			position_group.setFixedHeight(math.floor(self.height() / 4))
			position_group.setStyleSheet("background-color: #DDD")
			time_control_total.setFixedSize(QSize(self.width() // 6, self.height() // 10))
			time_control_total_increment.setFixedSize(QSize(self.width() // 6, self.height() // 10))
			time_control_move.setFixedSize(QSize(self.width() // 6, self.height() // 10))
			time_control_unlimited.setFixedSize(QSize(self.width() // 6, self.height() // 10))
		else:
			self.two_player_mode_options.setFixedSize(QSize(math.floor(self.width() / 1.5), math.floor(self.height() / 1.5)))
			self.two_player_mode_options.move(QPoint((self.width() - self.two_player_mode_options.width()) // 2, (self.height() - self.two_player_mode_options.height()) // 2))
			self.two_player_mode_options_close.move(self.two_player_mode_options.pos())
			if self.two_player_mode_options_widgets["time_control_button"].isHidden():
				self.two_player_mode_options_widgets["time_control_button"].show()
				self.two_player_mode_options_widgets["variant_button"].show()
				self.two_player_mode_options_widgets["position_button"].show()
			if self.two_player_mode_options.layout().spacing() == 5:
				self.two_player_mode_options.layout().setSpacing(0)
			self.two_player_mode_options_widgets["tc_total"].setFixedSize(QSize(self.width() // 10, self.height() // 12))
			self.two_player_mode_options_widgets["tc_total_increment"].setFixedSize(QSize(self.width() // 10, self.height() // 12))
			self.two_player_mode_options_widgets["tc_move"].setFixedSize(QSize(self.width() // 10, self.height() // 12))
			self.two_player_mode_options_widgets["tc_unlimited"].setFixedSize(QSize(self.width() // 10, self.height() // 12))
			self.two_player_mode_options_widgets["time_control_group"].setFixedHeight(math.floor(self.height() / 6))
			self.two_player_mode_options_widgets["variant_group"].setFixedHeight(math.floor(self.height() / 10))
			self.two_player_mode_options_widgets["position_group"].setFixedHeight(math.floor(self.height() / 8))

	def keyPressEvent(self, event: QKeyEvent):
		if self.two_player_mode_options is not None:
			if event.key() == 16777220:
				self.two_player_mode_options_widgets["startGame"]()
		if self.computer_mode_options is not None:
			if event.key() == 16777220:
				self.computer_mode_options_widgets["startGame"]()
		super(MainPage, self).keyPressEvent(event)

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
		self.computer_mode_button.move((event.size().width() - self.computer_mode_button.width()) // 2, (event.size().height() // 20) + 325)
		if self.two_player_mode_options is not None:
			if event.size().width() <= 1440 or event.size().height() <= 1080:
				self.two_player_mode_options.setFixedSize(event.size())
				self.two_player_mode_options.move(QPoint())
				self.two_player_mode_options_close.move(QPoint())
				if not self.two_player_mode_options_widgets["time_control_button"].isHidden():
					self.two_player_mode_options_widgets["time_control_button"].hide()
					self.two_player_mode_options_widgets["variant_button"].hide()
					self.two_player_mode_options_widgets["position_button"].hide()
				if self.two_player_mode_options_widgets["time_control_group"].isHidden():
					self.two_player_mode_options_widgets["time_control_group"].show()
				if self.two_player_mode_options_widgets["variant_group"].isHidden():
					self.two_player_mode_options_widgets["variant_group"].show()
				if self.two_player_mode_options_widgets["position_group"].isHidden():
					self.two_player_mode_options_widgets["position_group"].show()
				if self.two_player_mode_options.layout().spacing() == 0:
					self.two_player_mode_options.layout().setSpacing(5)
				self.two_player_mode_options_widgets["time_control_group"].setFixedHeight(math.floor(event.size().height() / 3))
				self.two_player_mode_options_widgets["time_control_group"].setStyleSheet("background-color: #DDD")
				self.two_player_mode_options_widgets["variant_group"].setFixedHeight(math.floor(event.size().height() / 6))
				self.two_player_mode_options_widgets["variant_group"].setStyleSheet("background-color: #DDD")
				self.two_player_mode_options_widgets["position_group"].setFixedHeight(math.floor(event.size().height() / 4))
				self.two_player_mode_options_widgets["position_group"].setStyleSheet("background-color: #DDD")
				self.two_player_mode_options_widgets["tc_total"].setFixedSize(QSize(event.size().width() // 6, event.size().height() // 10))
				self.two_player_mode_options_widgets["tc_total_increment"].setFixedSize(QSize(event.size().width() // 6, event.size().height() // 10))
				self.two_player_mode_options_widgets["tc_move"].setFixedSize(QSize(event.size().width() // 6, event.size().height() // 10))
				self.two_player_mode_options_widgets["tc_unlimited"].setFixedSize(QSize(event.size().width() // 6, event.size().height() // 10))
			else:
				self.two_player_mode_options.setFixedSize(QSize(math.floor(self.width() / 1.5), math.floor(self.height() / 1.5)))
				self.two_player_mode_options.move(QPoint((self.width() - self.two_player_mode_options.width()) // 2, (self.height() - self.two_player_mode_options.height()) // 2))
				self.two_player_mode_options_close.move(self.two_player_mode_options.pos())
				if self.two_player_mode_options_widgets["time_control_button"].isHidden():
					self.two_player_mode_options_widgets["time_control_button"].show()
					self.two_player_mode_options_widgets["variant_button"].show()
					self.two_player_mode_options_widgets["position_button"].show()
					self.two_player_mode_options_widgets["time_control_button"].setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.4);")
					self.two_player_mode_options_widgets["time_control_button"].selected = True
					self.two_player_mode_options_widgets["variant_button"].setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.4);")
					self.two_player_mode_options_widgets["variant_button"].selected = True
					self.two_player_mode_options_widgets["position_button"].setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.4);")
					self.two_player_mode_options_widgets["position_button"].selected = True
				if self.two_player_mode_options.layout().spacing() == 5:
					self.two_player_mode_options.layout().setSpacing(0)
				self.two_player_mode_options_widgets["tc_total"].setFixedSize(QSize(event.size().width() // 10, event.size().height() // 12))
				self.two_player_mode_options_widgets["tc_total_increment"].setFixedSize(QSize(event.size().width() // 10, event.size().height() // 12))
				self.two_player_mode_options_widgets["tc_move"].setFixedSize(QSize(event.size().width() // 10, event.size().height() // 12))
				self.two_player_mode_options_widgets["tc_unlimited"].setFixedSize(QSize(event.size().width() // 10, event.size().height() // 12))
				self.two_player_mode_options_widgets["time_control_group"].setFixedHeight(math.floor(event.size().height() / 6))
				self.two_player_mode_options_widgets["variant_group"].setFixedHeight(math.floor(event.size().height() / 10))
				self.two_player_mode_options_widgets["position_group"].setFixedHeight(math.floor(event.size().height() / 8))
		if self.computer_mode_options is not None:
			if event.size().width() <= 1440 or event.size().height() <= 1080:
				self.computer_mode_options.setFixedSize(event.size())
				self.computer_mode_options.move(QPoint())
				self.computer_mode_options_close.move(QPoint())
				if not self.computer_mode_options_widgets["level_button"].isHidden():
					self.computer_mode_options_widgets["level_button"].hide()
					self.computer_mode_options_widgets["time_control_button"].hide()
					self.computer_mode_options_widgets["position_button"].hide()
				if self.computer_mode_options_widgets["time_control_group"].isHidden():
					self.computer_mode_options_widgets["level_group"].show()
				if self.computer_mode_options_widgets["time_control_group"].isHidden():
					self.computer_mode_options_widgets["time_control_group"].show()
				if self.computer_mode_options_widgets["position_group"].isHidden():
					self.computer_mode_options_widgets["position_group"].show()
				if self.computer_mode_options.layout().spacing() == 0:
					self.computer_mode_options.layout().setSpacing(5)
				self.computer_mode_options_widgets["level_group"].setFixedHeight(math.floor(event.size().height() / 11))
				self.computer_mode_options_widgets["level_group"].setStyleSheet("background-color: #DDD")
				self.computer_mode_options_widgets["time_control_group"].setFixedHeight(math.floor(event.size().height() / 5))
				self.computer_mode_options_widgets["time_control_group"].setStyleSheet("background-color: #DDD")
				self.computer_mode_options_widgets["position_group"].setFixedHeight(math.floor(event.size().height() / 4))
				self.computer_mode_options_widgets["position_group"].setStyleSheet("background-color: #DDD")
			else:
				self.computer_mode_options.setFixedSize(QSize(math.floor(self.width() / 1.5), math.floor(self.height() / 1.5)))
				self.computer_mode_options.move(QPoint((self.width() - self.computer_mode_options.width()) // 2, (self.height() - self.computer_mode_options.height()) // 2))
				self.computer_mode_options_close.move(self.computer_mode_options.pos())
				if self.computer_mode_options_widgets["level_button"].isHidden():
					self.computer_mode_options_widgets["level_button"].show()
					self.computer_mode_options_widgets["time_control_button"].show()
					self.computer_mode_options_widgets["position_button"].show()
					self.computer_mode_options_widgets["level_button"].setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.4);")
					self.computer_mode_options_widgets["level_button"].selected = True
					self.computer_mode_options_widgets["time_control_button"].setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.4);")
					self.computer_mode_options_widgets["time_control_button"].selected = True
					self.computer_mode_options_widgets["position_button"].setStyleSheet("width: 100%; height: 30px; background-color: rgba(0, 0, 0, 0.4);")
					self.computer_mode_options_widgets["position_button"].selected = True
				if self.computer_mode_options.layout().spacing() == 5:
					self.computer_mode_options.layout().setSpacing(0)
				self.computer_mode_options_widgets["level_group"].setFixedHeight(math.floor(self.height() / 20))
				self.computer_mode_options_widgets["time_control_group"].setFixedHeight(math.floor(self.height() / 6))
				self.computer_mode_options_widgets["variant_group"].setFixedHeight(math.floor(self.height() / 15))
				self.computer_mode_options_widgets["position_group"].setFixedHeight(math.floor(self.height() / 8))
		self.quit_button.resize(QSize(min_size // 20, min_size // 20))
		if not self.animated:
			self.title_opening_animation.setEndValue(QSize(self.title.maximumWidth(), 200))
			self.title_opening_animation.setStartValue(QSize(self.title.maximumWidth(), 0))
			self.title_opening_animation.start()
			self.animated = True
		self.settings_button.move(QPoint(event.size().width() - self.settings_button.width() - 10, 10))
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
		self.select_mode_label_animation.finished.connect(self.gameModeButtonsAnimation)

	def gameModeButtonsAnimation(self):
		self.select_mode_animation.start()
		self.two_player_mode_button.move(QPoint(self.two_player_mode_button.pos().x(), self.two_player_mode_button.pos().y() + 100))
		self.two_player_mode_animation = QPropertyAnimation(self.two_player_mode_button, b"color")
		self.two_player_mode_animation.setDuration(250)
		self.two_player_mode_animation.setStartValue(QColor("transparent"))
		self.two_player_mode_animation.setEndValue(QColor("#8400FF"))
		self.two_player_mode_animation.start()
		self.two_player_mode_animation.finished.connect(self.two_player_mode_button.animationFinished)
		self.computer_mode_button.move(QPoint(self.computer_mode_button.pos().x(), self.computer_mode_button.pos().y() + 100))
		self.computer_mode_button_animation = QPropertyAnimation(self.computer_mode_button, b"color")
		self.computer_mode_button_animation.setDuration(250)
		self.computer_mode_button_animation.setStartValue(QColor("transparent"))
		self.computer_mode_button_animation.setEndValue(QColor("#8400FF"))
		self.computer_mode_button_animation.start()
		self.computer_mode_button_animation.finished.connect(self.computer_mode_button.animationFinished)


class Window(QMainWindow):
	"""Main Window"""
	def __init__(self) -> None:
		super(Window, self).__init__()
		self.setWindowTitle("Chess")
		self.setMinimumSize(QSize(720, 720))
		self.stacked_pages, self.stacks = QStackedWidget(self), {"main-page": MainPage(self, self.twoPlayerMode, self.computerMode), "two-players": twoplayers.TwoPlayers(self), "settings": settings.Settings(self), "computer": computer.Computer(self)}
		self.stacked_pages.addWidget(self.stacks["main-page"])
		self.stacked_pages.addWidget(self.stacks["two-players"])
		self.stacked_pages.addWidget(self.stacks["settings"])
		self.stacked_pages.addWidget(self.stacks["computer"])
		self.showFullScreen()
		self.stacked_pages.move(0, 0)
		self.stacked_pages.setFixedSize(self.size())

	def twoPlayerMode(self, time_control, variant, position_type, position):
		self.stacks["two-players"].setTimeControl(time_control)
		self.stacks["two-players"].setupBoard(variant, position_type, position)
		self.setIndex(1, self.stacks["two-players"])
		self.stacks["two-players"].startClocks()
		self.setWindowTitle("2-Player Chess Game: White to move")

	def computerMode(self, computer_type, computer_, time_control, position_type, position):
		self.stacks["computer"].setTimeControl(time_control)
		self.stacks["computer"].setupBoard(position_type, position)
		if computer_type == "level":
			self.stacks["computer"].computer_level = int(computer_)
		else:
			self.stacks["computer"].computer_level = 0
			self.stacks["computer"].setupUCI(computer_)
		self.setIndex(3, self.stacks["computer"])
		self.stacks["computer"].startClocks()
		self.setWindowTitle("Player vs Computer Chess Game: White to move")

	def resetTwoPlayerGame(self):
		self.stacks["two-players"].deleteLater()
		self.stacks["two-players"] = twoplayers.TwoPlayers(self)
		self.stacked_pages.insertWidget(1, self.stacks["two-players"])

	def resetComputerGame(self):
		self.stacks["computer"].deleteLater()
		self.stacks["computer"] = computer.Computer(self)
		self.stacked_pages.insertWidget(3, self.stacks["computer"])

	def setIndex(self, index, widget):
		self.stacked_pages.setCurrentIndex(index)
		widget.animation.start()

	def resizeEvent(self, event: QResizeEvent) -> None:
		self.stacks["main-page"].resize(event.size())
		self.stacks["two-players"].resize(event.size())
		self.stacks["settings"].resize(event.size())
		super(Window, self).resizeEvent(event)


application, window = QApplication([]), Window()
application.exec_()
