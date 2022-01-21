"""
twoplayers.py
2 Player Chess Mode
"""

import json
import board
import chess
import asyncio

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def getMinutesSeconds(seconds):
	if seconds < 60:
		return 0, seconds
	return seconds // 60, seconds - (seconds // 60 * 60)


class MoveButton(QPushButton):
	def __init__(self, parent, text=""):
		super(MoveButton, self).__init__(parent=parent)
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-Regular.ttf"))[0], 15, weight=40))
		self.setText(text)
		self.setFixedSize(100, 30)
		self.setFocusPolicy(Qt.ClickFocus)

	def enterEvent(self, event: QHoverEvent) -> None:
		self.setStyleSheet("background-color: rgba(100, 0, 255, 0.75); color: white;")
		super(MoveButton, self).enterEvent(event)

	def leaveEvent(self, event: QHoverEvent) -> None:
		self.setStyleSheet("background-color: transparent; color: black;")
		super(MoveButton, self).leaveEvent(event)


class TemporaryMoveButton(MoveButton):
	def __init__(self, parent, text=""):
		super(TemporaryMoveButton, self).__init__(parent, text=text)
		self.setStyleSheet("background-color: rgba(0, 0, 0, 0.05); color: black;")
		self.setFocusPolicy(Qt.ClickFocus)
		
	def enterEvent(self, event: QHoverEvent) -> None:
		super(TemporaryMoveButton, self).enterEvent(event)
		self.setStyleSheet("background-color: rgba(0, 0, 0, 0.1); color: black;")

	def leaveEvent(self, event: QHoverEvent) -> None:
		super(TemporaryMoveButton, self).leaveEvent(event)
		self.setStyleSheet("background-color: rgba(0, 0, 0, 0.05); color: black;")


class AbortButton(QPushButton):
	def __init__(self, parent):
		super(AbortButton, self).__init__(parent=parent)
		self.setText("–")
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.pressed.connect(self.parent().abort)
		self.status_tip = QLabel("Abort", parent)
		self.status_tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
	
	def focusInEvent(self, event) -> None:
		if event.reason() <= 2:
			self.status_tip.show()
			self.setStyleSheet("color: black; background-color: yellow; border: none;")
		super(AbortButton, self).focusInEvent(event)
	
	def focusOutEvent(self, event) -> None:
		if event.reason() <= 2:
			self.status_tip.hide()
			self.setStyleSheet("color: black; background-color: white; border: none;")
		super(AbortButton, self).focusOutEvent(event)
	
	def resizeEvent(self, event) -> None:
		self.status_tip.setFixedWidth(event.size().width())
		self.status_tip.move(QPoint(self.pos().x(), self.pos().y() + event.size().width()))
		super(AbortButton, self).resizeEvent(event)

	def enterEvent(self, event: QEvent) -> None:
		self.status_tip.show()
		self.setStyleSheet("color: black; background-color: yellow; border: none;")
		super(AbortButton, self).enterEvent(event)

	def leaveEvent(self, event: QEvent) -> None:
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
		super(AbortButton, self).leaveEvent(event)


class BackButton(QPushButton):
	def __init__(self, parent):
		super(BackButton, self).__init__(parent=parent)
		self.setText("←")
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.pressed.connect(self.parent().back)
		self.status_tip = QLabel("Back", parent)
		self.status_tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
	
	def focusInEvent(self, event) -> None:
		if event.reason() <= 2:
			self.status_tip.show()
			self.setStyleSheet("color: black; background-color: limegreen; border: none;")
		super(BackButton, self).focusInEvent(event)
	
	def focusOutEvent(self, event) -> None:
		if event.reason() <= 2:
			self.status_tip.hide()
			self.setStyleSheet("color: black; background-color: white; border: none;")
		super(BackButton, self).focusOutEvent(event)

	def resizeEvent(self, event) -> None:
		self.status_tip.setFixedWidth(event.size().width())
		self.status_tip.move(QPoint(self.pos().x(), self.pos().y() + event.size().width()))
		super(BackButton, self).resizeEvent(event)

	def enterEvent(self, event: QEvent) -> None:
		self.status_tip.show()
		self.setStyleSheet("color: black; background-color: limegreen; border: none;")
		super(BackButton, self).enterEvent(event)

	def leaveEvent(self, event: QEvent) -> None:
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
		super(BackButton, self).leaveEvent(event)


class NewButton(QPushButton):
	def __init__(self, parent):
		super(NewButton, self).__init__(parent=parent)
		self.setText("+")
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.pressed.connect(self.parent().new)
		self.status_tip = QLabel("New", parent)
		self.status_tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
	
	def focusInEvent(self, event) -> None:
		if event.reason() <= 2:
			self.status_tip.show()
			self.setStyleSheet("color: black; background-color: green; border: none;")
		super(NewButton, self).focusInEvent(event)
	
	def focusOutEvent(self, event) -> None:
		if event.reason() <= 2:
			self.status_tip.hide()
			self.setStyleSheet("color: black; background-color: white; border: none;")
		super(NewButton, self).focusOutEvent(event)

	def resizeEvent(self, event) -> None:
		self.status_tip.setFixedWidth(event.size().width())
		self.status_tip.move(QPoint(self.pos().x(), self.pos().y() + event.size().width()))
		super(NewButton, self).resizeEvent(event)

	def enterEvent(self, event: QEvent) -> None:
		self.status_tip.show()
		self.setStyleSheet("color: black; background-color: green; border: none;")
		super(NewButton, self).enterEvent(event)

	def leaveEvent(self, event: QEvent) -> None:
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
		super(NewButton, self).leaveEvent(event)


class Clock(QPushButton):
	def __init__(self, parent, time_control, timeup_function=None):
		super(Clock, self).__init__(parent=parent)
		self.timeup_function = timeup_function
		self.time_control = time_control
		if time_control.endswith("+0s"):
			self.clock_minutes = int(time_control[:time_control.index(".")])
			self.clock_seconds = round(6 * float(time_control[time_control.index(".") + 1:time_control.index("+") - 1]))
		elif "+" in time_control:
			self.clock_minutes = int(float(time_control[:time_control.index("+") - 1]))
			self.clock_seconds = round(6 * float(time_control[time_control.index(".") + 1:time_control.index("+") - 1]))
		else:
			self.clock_minutes = getMinutesSeconds(int(time_control[:-1]))[0]
			self.clock_seconds = getMinutesSeconds(int(time_control[:-1]))[1]
		self.updateText()
		self.running = False
		self.timer = QTimer()
		self.timer.timeout.connect(self.updateClock)
		self.setStyleSheet("background-color: #EEE; border: none;")
		self.setFont(QFont("Arial", 30))
		self.setFocusPolicy(Qt.NoFocus)

	def updateText(self):
		self.setText(str(self.clock_minutes) + ":" + str(self.clock_seconds).rjust(2, "0"))

	def start(self):
		self.timer.start(1000)
		self.running = True

	def pause(self):
		self.timer.stop()
		self.running = False

	def updateClock(self):
		if self.clock_seconds == 0:
			if self.clock_minutes == 0:
				if self.timeup_function is not None:
					self.timeup_function(self)
				self.pause()
				return
			self.clock_seconds = 59
			self.clock_minutes -= 1
		else:
			self.clock_seconds -= 1
		self.updateText()

	def resetClock(self):
		if "+" not in self.time_control:
			self.clock_minutes = getMinutesSeconds(int(self.time_control[:-1]) + 1)[0]
			self.clock_seconds = getMinutesSeconds(int(self.time_control[:-1]) + 1)[1]
			self.updateClock()


class TakebackButton(QPushButton):
	def __init__(self, parent):
		super(TakebackButton, self).__init__("⇐", parent)
		self.setStyleSheet("TakebackButton { background-color: transparent; border: none; } TakebackButton:hover { background-color: #AAA; border: none; }")
		self.setCursor(Qt.PointingHandCursor)
		self.setToolTip("Takeback")
	
	def mouseReleaseEvent(self, event) -> None:
		self.parent().game.takeback()
		self.parent().board.updatePieces()
		asyncio.get_event_loop().run_until_complete(self.parent().updateTakebackOpening())
		super(TakebackButton, self).mouseReleaseEvent(event)
	

class TwoPlayers(QWidget):
	def __init__(self, parent):
		super(TwoPlayers, self).__init__(parent=parent)
		self.settings_values = json.load(open("settings.json"))
		self.game = None
		self.time_control = None
		self.game_over = False
		self.animation = QPropertyAnimation(self, b"pos")
		self.animation.setEndValue(QPoint())
		self.animation.setDuration(250)
		self.moves_count = 1
		self.board = None
		self.sidebar = QGroupBox(self)
		self.sidebar.setStyleSheet("border: none;")
		self.sidebar_layout = QGridLayout()
		self.opening = QLabel("Starting Position", self)
		self.opening.setWordWrap(True)
		self.opening.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-Bold.ttf"))[0], 17, italic=True))
		self.opening.resize(QSize(300, 50))
		self.moves = QWidget()
		self.moves_layout = QGridLayout()
		self.moves_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.moves_layout.setSpacing(0)
		self.move_buttons = []
		self.moves.setLayout(self.moves_layout)
		self.moves_wrapper = QScrollArea()
		self.moves_wrapper.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.moves_wrapper.setWidgetResizable(True)
		self.moves_wrapper.setWidget(self.moves)
		self.takeback = TakebackButton(self)
		self.game_over_label = self.game_result_label = None
		self.sidebar_layout.addWidget(self.moves_wrapper)
		self.sidebar.setLayout(self.sidebar_layout)
		self.back_button = BackButton(self)
		self.abort_button = AbortButton(self)
		self.new_button = NewButton(self)
		self.clocks = []
		self.sidebar.move(QPoint((self.width() // 2) + 400, 100))
		self.temporary_move = None
		self.setFocusPolicy(Qt.NoFocus)

	def setTimeControl(self, time_control):
		if time_control == "unlimited":
			return
		self.time_control = time_control
		self.clocks.append(Clock(self, self.time_control, self.timeout))
		self.clocks[0].move(QPoint(self.width() - self.clocks[0].width(), self.height() - self.clocks[0].height()))
		self.clocks.append(Clock(self, self.time_control, self.timeout))
		self.clocks[1].move(QPoint(self.width() - self.clocks[1].width(), 20))

	def setupBoard(self, variant, position_type, position):
		if variant == "Standard":
			if position_type == "FEN":
				self.game = chess.Game(fen=position)
			else:
				self.game = chess.Game()
				self.game.loadPGN(position)
		elif variant == "Antichess":
			if position_type == "FEN":
				self.game = chess.Antichess(fen=position)
			else:
				self.game = chess.Antichess()
				self.game.loadPGN(position)
		elif variant == "Three Check":
			if position_type == "FEN":
				self.game = chess.ThreeCheck(fen=position)
			else:
				self.game = chess.ThreeCheck()
				self.game.loadPGN(position)
		self.board = board.Board(self, self.game)
		self.sidebar.raise_()

	def addTemporaryMove(self, text):
		self.temporary_move = TemporaryMoveButton(self, text)
		self.move_buttons.append(self.temporary_move)
		self.moves_layout.addWidget(self.move_buttons[-1], self.getGridIndex()[0], self.getGridIndex()[1])
		self.move_buttons[-1].show()
		self.moves_wrapper.verticalScrollBar().setSliderPosition(self.moves_wrapper.verticalScrollBar().maximum())

	def startClocks(self):
		if self.clocks:
			self.clocks[0].start()

	def back(self):
		if self.clocks:
			if self.clocks[0].running:
				self.clocks[0].pause()
			if self.clocks[1].running:
				self.clocks[1].pause()
		self.parent().setCurrentIndex(0)

	def abort(self):
		if self.clocks[0].running:
			self.clocks[0].pause()
		if self.clocks[1].running:
			self.clocks[1].pause()
		self.parent().parent().resetTwoPlayerGame()
		self.parent().setCurrentIndex(0)

	def new(self):
		self.parent().parent().resetTwoPlayerGame()
		self.parent().setCurrentIndex(0)
		self.parent().parent().stacks["main-page"].twoPlayers()

	def getGridIndex(self) -> list:
		columns = 0
		for i in range(len(self.move_buttons)):
			if i % 2 == 0 and i != 0:
				columns += 1
		return [columns, int(len(self.move_buttons) % 2 == 0)]

	def timeout(self, clock):
		if self.clocks[0].running:
			self.clocks[0].pause()
		else:
			self.clocks[1].pause()
		self.game_over = True
		self.parent().parent().setWindowTitle("2-Player Chess Game: " + ("Black", "White")[self.clocks.index(clock)] + " wins")

	def addMove(self, move) -> None:
		self.move_buttons.append(MoveButton(self.moves, move))
		self.moves_layout.addWidget(self.move_buttons[-1], self.getGridIndex()[0], self.getGridIndex()[1])
		self.move_buttons[-1].show()
		self.moves_wrapper.verticalScrollBar().setSliderPosition(self.moves_wrapper.verticalScrollBar().maximum())
		self.moves_count += 0.5
		asyncio.get_event_loop().run_until_complete(self.updateOpening())
		if self.game.game_over:
			self.takeback.deleteLater()
			self.game_over_label = QLabel("Game Over", self)
			self.game_over_label.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-Light.ttf"))[0], 15))
			self.game_over_label.show()
			if self.game.drawn:
				self.parent().parent().setWindowTitle("2-Player Chess Game: Draw")
				self.game_result_label = QLabel("Draw | 1/2-1/2", self)
				self.game_result_label.show()
			else:
				self.parent().parent().setWindowTitle("2-Player Chess Game: " + {"white": "Black", "black": "White"}[self.game.turn] + " wins")
				self.game_result_label = QLabel({"white": "Black", "black": "White"}[self.game.turn] + " wins | " + self.game.tags["Result"], self)
				self.game_result_label.resize(QSize(150, 15))
				self.game_result_label.show()
			self.game_over_label.move(QPoint(self.width() // 4 - self.opening.width(), self.height() // 2 + self.opening.height()))
			self.game_result_label.move(QPoint(self.width() // 4 - self.opening.width(), self.height() // 2 + self.opening.height() + self.game_over_label.height()))
			self.game_result_label.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-Light.ttf"))[0], 15))
			if self.clocks:
				if self.clocks[0].running:
					self.clocks[0].pause()
				if self.clocks[1].running:
					self.clocks[1].pause()
			self.game_over = True
			return
		if self.clocks:
			if not self.time_control.endswith("+0") and "+" in self.time_control:
				if self.clocks[1].running:
					self.clocks[1].clock_seconds += int(self.time_control[self.time_control.index("+") + 1:-1])
					if self.clocks[1].clock_seconds > 59:
						self.clocks[1].clock_minutes += 1
						self.clocks[1].clock_seconds -= 60
					self.clocks[1].updateText()
				if self.clocks[0].running:
					self.clocks[0].clock_seconds += int(self.time_control[self.time_control.index("+") + 1:-1])
					if self.clocks[0].clock_seconds > 59:
						self.clocks[0].clock_minutes += 1
						self.clocks[0].clock_seconds -= 60
					self.clocks[0].updateText()
			if "+" not in self.time_control:
				self.clocks[0].resetClock()
				self.clocks[1].resetClock()
			if self.clocks[0].running:
				self.clocks[0].pause()
				self.clocks[1].start()
			elif self.clocks[1].running:
				self.clocks[1].pause()
				self.clocks[0].start()
				
	async def updateOpening(self):
		position = self.game.FEN().split()[0]
		for i in chess.openings.openings:
			if i["position"] == position:
				self.opening.setText(i["eco"] + " " + i["name"])
				return

	async def updateTakebackOpening(self):
		game = chess.Game()
		opening = "Starting Position"
		for x in self.game.raw_move_list:
			game.move(x.name, evaluate_checks=False, evaluate_move_checks=False, evaluate_move_checkmate=False)
			position = game.FEN().split()[0]
			for y in chess.openings.openings:
				if y["position"] == position:
					opening = y["eco"] + " " + y["name"]
					break
		self.opening.setText(opening)
	
	def updateSettingsValues(self):
		self.settings_values = json.load(open("settings.json"))

	def keyPressEvent(self, event):
		self.board.keyPressEvent(event)
		super(TwoPlayers, self).keyPressEvent(event)

	def resizeEvent(self, event) -> None:
		self.sidebar.resize(QSize(event.size().width() - (self.width() // 2) + 400, event.size().height() - 200))
		self.sidebar.move(QPoint((event.size().width() // 2) + 400, 100))
		self.animation.setStartValue(QPoint(event.size().width(), 0))
		self.opening.move(QPoint(event.size().width() // 4 - self.opening.width(), event.size().height() // 2))
		self.takeback.move(QPoint(event.size().width() // 4 - self.opening.width(), event.size().height() // 2 + self.opening.height()))
		if self.game_over_label is not None and self.game_result_label is not None:
			self.game_over_label.move(QPoint(event.size().width() // 4 - self.opening.width(), event.size().height() // 2 + self.opening.height()))
			self.game_result_label.move(QPoint(event.size().width() // 4 - self.opening.width(), event.size().height() // 2 + self.opening.height() + self.game_over_label.height()))
		if self.clocks:
			self.clocks[0].move(QPoint(event.size().width() - self.clocks[0].width() - 10, event.size().height() - self.clocks[0].height() - 20))
			self.clocks[1].move(QPoint(event.size().width() - self.clocks[0].width() - 10, 20))
		if event.size().width() > event.size().height():
			min_size = event.size().height()
		else:
			min_size = event.size().width()
		if self.board is not None:
			self.board.move(QPoint((event.size().width() - (self.board.squares[0].width() * 10)) // 2, (event.size().height() - (self.board.squares[0].width() * 10)) // 2))
		self.back_button.resize(QSize(min_size // 20, min_size // 20))
		self.back_button.move(QPoint(0, 0))
		self.abort_button.resize(QSize(min_size // 20, min_size // 20))
		self.abort_button.move(QPoint(min_size // 20, 0))
		self.new_button.resize(QSize(min_size // 20, min_size // 20))
		self.new_button.move(QPoint(min_size // 20 * 2, 0))
		self.takeback.resize(QSize(min_size // 40, min_size // 40))
		super(TwoPlayers, self).resizeEvent(event)
	