# -*- coding: utf-8 -*-

"""
computer.py
Player-vs-computer game mode
"""

import json
import random
import subprocess

import board
import chess
import asyncio

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
from PyQt5.QtWidgets import *

openings = {
	"1. e4": {
		"e5": 0.5,
		"c5": 0.5,
		"e6": 0.4,
		"c6": 0.4,
		"Nf6": 0.2,
		"Nc6": 0.2,
		"g6": 0.1,
		"d6": 0.1,
		"b6": 0.1
	},
	"1. d4": {
		"d5": 0.5,
		"Nf6": 0.5,
		"e6": 0.4,
		"d6": 0.3,
		"Nc6": 0.2
	},
	"1. c4": {
		"e5": 0.5,
		"c5": 0.45,
		"Nf6": 0.4,
		"e6": 0.4,
		"Nc6": 0.3,
		"d5": 0.3,
		"c6": 0.15,
		"d6": 0.15
	},
	"1. Nf3": {
		"d5": 0.5,
		"Nf6": 0.5,
		"c5": 0.45,
		"e6": 0.45,
		"Nc6": 0.3,
		"d6": 0.2,
		"c6": 0.2
	},
	"1. e4 e5 Nf3": {
		"Nc6": 0.5,
		"d6": 0.2,
	},
	"1. e4 e5 Bc4": {
		"Nf6": 0.5,
		"Nc6": 0.45,
		"Bc5": 0.4,
		"d6": 0.4,
		"c6": 0.3
	},
	"1. e4 e5 f4": {
		"exf4": 0.5,
		"d5": 0.3,
	},
	"1. e4 e5 Nc3": {
		"Nf6": 0.5
	},
	"1. e4 e6 d4": {
		"d5": 0.5
	},
	"1. e4 e6 Nf3": {
		"d5": 0.5
	},
	"1. e4 e6 Nc3": {
		"c5": 0.5,
		"d5": 0.45
	},
	"1. e4 e6 d3": {
		"d5": 0.5
	},
	"1. e4 c5 Nf3": {
		"e6": 0.5,
		"d6": 0.5,
		"Nc6": 0.4
	},
	"1. e4 c5 d4": {
		"cxd4": 0.5
	},
	"1. e4 c5 Nc3": {
		"Nc6": 0.5,
		"a6": 0.4,
		"d6": 0.4,
		"e6": 0.3
	},
	"1. e4 c6 d4": {
		"d5": 0.5
	},
	"1. e4 c6 Nc3": {
		"d5": 0.5
	},
	"1. e4 c6 Nf3": {
		"d5": 0.5
	},
	"1. d4 d5 Bf4": {
		"Nf6": 0.5,
		"c5": 0.5,
		"Bf5": 0.35
	},
	"1. d4 d5 Nf3": {
		"e6": 0.5,
		"c6": 0.5,
		"Nf6": 0.5,
		"Bf5": 0.35,
		"Nd7": 0.25
	},
	"1. d4 Nf6 c4": {
		"e6": 0.5,
		"c6": 0.5,
		"d6": 0.45,
		"g6": 0.4,
		"e5": 0.4,
	},
	"1. d4 e6 e4": {
		"d5": 0.5
	},
	"1. d4 e6 Nf3": {
		"d5": 0.5
	},
	"1. d4 e6 Nc3": {
		"d5": 0.5
	},
	"1. c4 e5 Nc3": {
		"Nf3": 0.5,
		"Bb4": 0.3
	},
	"1. c4 e5 g3": {
		"Nf6": 0.5,
		"d5": 0.4
	},
	"1. c4 e5 Nf3": {
		"e4": 0.5,
		"Nc6": 0.35
	},
	"1. c4 e5 e4": {
		"Bc5": 0.5,
		"Nc6": 0.5,
		"Nf6": 0.35
	},
	"1. c4 c5 Nf3": {
		"Nf6": 0.5,
		"Nc6": 0.35,
		"e6": 0.3
	},
	"1. c4 c5 e4": {
		"Nf6": 0.5,
		"Nc6": 0.5,
		"e5": 0.45,
		"d6": 0.4
	},
	"1. c4 c5 d4": {
		"cxd4": 0.5
	},
	"1. c4 c5 f4": {
		"g6": 0.5,
		"e6": 0.5,
		"Nc6": 0.4
	},
	"1. c4 Nf6 Nf3": {
		"e6": 0.5,
		"c5": 0.5,
		"c6": 0.4
	}
}


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
		if not self.parent().game.raw_move_list:
			return
		if self.parent().computer_moving:
			if self.parent().engine is not None:
				self.parent().engine.stdin.write("stop\n")
			else:
				self.parent().get_computer_move_thread.quit()
				self.parent().get_computer_move_runner.deleteLater()
				self.parent().get_computer_move_thread.deleteLater()
			self.parent().computer_moving = False
		else:
			self.parent().game.takeback()
		self.parent().game.takeback()
		self.parent().board.updatePieces()
		asyncio.get_event_loop().run_until_complete(self.parent().updateTakebackOpening())
		if self.parent().clocks[0].running:
			self.parent().clocks[0].pause()
			self.parent().clocks[1].start()
		else:
			self.parent().clocks[0].start()
			self.parent().clocks[1].pause()
		self.parent().moves_layout.removeWidget(self.parent().move_buttons[-1])
		self.parent().move_buttons[-1].deleteLater()
		self.parent().moves_count -= 0.5
		super(TakebackButton, self).mouseReleaseEvent(event)
	

class Thread(QObject):
	finished = pyqtSignal()
	output = pyqtSignal(str)

	def __init__(self, function):
		super(Thread, self).__init__()
		self.function = function
	
	def run(self):
		result = self.function()
		self.finished.emit()
		if type(result) == dict:
			self.output.emit(result["move"])
		else:
			self.output.emit(result)


class Computer(QWidget):
	def __init__(self, parent):
		super(Computer, self).__init__(parent=parent)
		self.player_color = "white"
		self.type_ = "computer"
		self.computer_level = "0"
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
		self.uci_process = QLabel("Connecting to engine...", self)
		self.uci_process.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(QDir.currentPath() + "/fonts/ChakraPetch-Bold.ttf"))[0], 17, italic=True))
		self.uci_process.hide()
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
		self.sidebar_layout.addWidget(self.uci_process)
		self.sidebar_layout.addWidget(self.moves_wrapper)
		self.sidebar.setLayout(self.sidebar_layout)
		self.back_button = BackButton(self)
		self.abort_button = AbortButton(self)
		self.new_button = NewButton(self)
		self.clocks = []
		self.sidebar.move(QPoint((self.width() // 2) + 400, 100))
		self.temporary_move = None
		self.setFocusPolicy(Qt.NoFocus)
		self.get_computer_move_thread = self.get_computer_move_runner = None
		self.computer_moving = False
		self.uci_identification = QLabel(self)
		self.engine = self.engine_properties = None

	def setTimeControl(self, time_control):
		if time_control == "unlimited":
			return
		self.time_control = time_control
		self.clocks.append(Clock(self, self.time_control, self.timeout))
		self.clocks[0].move(QPoint(self.width() - self.clocks[0].width(), self.height() - self.clocks[0].height()))
		self.clocks.append(Clock(self, self.time_control, self.timeout))
		self.clocks[1].move(QPoint(self.width() - self.clocks[1].width(), 20))

	async def getEngineResponse(self):
		self.engine.stdin.write("isready\n")
		response = ""
		while True:
			text = self.engine.stdout.readline().strip()
			if text == "readyok":
				break
			elif text:
				response += text + "\n"
		return response
	
	async def getEngineMove(self):
		response = ""
		while True:
			text = self.engine.stdout.readline().strip()
			response += text + "\n"
			if text.startswith("bestmove "):
				break
		print(response)
		return response

	def setupUCI(self, path):
		self.uci_process.show()
		self.engine = subprocess.Popen(path, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
		print(asyncio.get_event_loop().run_until_complete(self.getEngineResponse()))
		self.uci_process.setText("Connected to engine, preparing communication with engine...")
		self.engine.stdin.write("uci\n")
		self.engine_properties = asyncio.get_event_loop().run_until_complete(self.getEngineResponse())
		found_name = found_authors = False
		for i in self.engine_properties.splitlines():
			if i == "":
				continue
			if i.startswith("id name"):
				found_name = True
				self.uci_identification.setText("Playing with " + i[8:])
			elif i.startswith("id author"):
				found_authors = True
				self.uci_identification.setText(self.uci_identification.text() + " by " + i[10:])
		if not (found_name and found_authors):
			self.uci_identification.setText("")
		self.uci_process.setText("Engine initialization complete")

	def setupBoard(self, position_type, position):
		if position_type == "FEN":
			self.game = chess.Game(fen=position)
		else:
			self.game = chess.Game()
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
		if not self.uci_process.isHidden():
			self.uci_process.hide()
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
		if self.game.turn != self.player_color:
			if self.engine is not None:
				if "+" in self.time_control:
					self.computer_moving = True
					self.engine.stdin.write("ucinewgame\nposition fen " + self.game.FEN() + "\n")
					self.engine.stdin.write("go wtime " + str((self.clocks[0].clock_minutes * 60000 + (self.clocks[0].clock_seconds * 1000))) + " btime " + str((self.clocks[1].clock_minutes * 60000 + (self.clocks[1].clock_seconds * 1000))) + " winc " + self.time_control.split("+")[1] + " binc " + self.time_control.split("+")[1] + "\n")
					self.get_computer_move_thread = QThread()
					self.get_computer_move_runner = Thread(lambda: chess.functions.toSAN(asyncio.new_event_loop().run_until_complete(self.getEngineMove()).splitlines()[-1].split()[1], self.game))
					self.get_computer_move_runner.moveToThread(self.get_computer_move_thread)
					self.get_computer_move_thread.started.connect(self.get_computer_move_runner.run)
					self.get_computer_move_runner.output.connect(self.makeComputerMove)
					self.get_computer_move_runner.finished.connect(self.get_computer_move_thread.quit)
					self.get_computer_move_runner.finished.connect(self.get_computer_move_runner.deleteLater)
					self.get_computer_move_thread.finished.connect(self.get_computer_move_thread.deleteLater)
					self.get_computer_move_thread.start()
					return
				else:
					return
			if self.computer_level == 0:
				computer_move = random.choice(self.game.legal_moves(True))
				self.board.pieceAt(computer_move.old_position).movePiece(computer_move)
			else:
				self.computer_moving = True
				self.get_computer_move_thread = QThread()
				self.get_computer_move_runner = Thread(self.getComputerMove)
				self.get_computer_move_runner.moveToThread(self.get_computer_move_thread)
				self.get_computer_move_thread.started.connect(self.get_computer_move_runner.run)
				self.get_computer_move_runner.output.connect(self.makeComputerMove)
				self.get_computer_move_runner.finished.connect(self.get_computer_move_thread.quit)
				self.get_computer_move_runner.finished.connect(self.get_computer_move_runner.deleteLater)
				self.get_computer_move_thread.finished.connect(self.get_computer_move_thread.deleteLater)
				self.get_computer_move_thread.start()

	def makeComputerMove(self, move):
		if "+" not in move and "#" not in move:
			for i in self.game.legal_moves(True):
				if i.name.replace("+", "").replace("#", "") == move:
					self.board.pieceAt(i.old_position).movePiece(i)
					break
		else:
			for i in self.game.legal_moves(True):
				if i.name == move:
					self.board.pieceAt(i.old_position).movePiece(i)
					break
		self.computer_moving = False
	
	def getComputerMove(self):
		if self.game.gamePhase() == "opening":
			if len(self.game.raw_move_list) <= 4:
				for i, j in openings.items():
					if i == self.game.move_list:
						moves = []
						weights = []
						for x, y in j.items():
							moves.append(x)
							weights.append(y)
						return random.choices(population=moves, weights=weights)[0]
			moves = []
			for i in chess.openings.openings:
				if len(i["moves"].split()) != 1 and " ".join(i["moves"].split()[:-1]) == self.game.move_list:
					moves.append(i["moves"].split()[-1])
			if moves:
				return random.choice(moves)
		return self.game.minimax_evaluation(self.computer_level)
	
	async def updateOpening(self):
		position = self.game.FEN().split()[0]
		for i in chess.openings.openings:
			if i["position"] == position:
				self.opening.setText(i["eco"] + " " + i["name"])
				return

	async def updateTakebackOpening(self):
		if len(self.game.raw_move_list) >= 20:
			return
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
		super(Computer, self).keyPressEvent(event)

	def resizeEvent(self, event) -> None:
		self.sidebar.resize(QSize(event.size().width() - (self.width() // 2) + 400, event.size().height() - 200))
		self.sidebar.move(QPoint((event.size().width() // 2) + 400, 100))
		self.animation.setStartValue(QPoint(event.size().width(), 0))
		self.opening.move(QPoint(event.size().width() // 4 - self.opening.width(), event.size().height() // 2))
		self.takeback.move(QPoint(event.size().width() // 4 - self.opening.width(), event.size().height() // 2 + self.opening.height()))
		self.uci_identification.move(QPoint(event.size().width() // 4 - self.opening.width(), event.size().height() // 2 - self.opening.height()))
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
		super(Computer, self).resizeEvent(event)
	