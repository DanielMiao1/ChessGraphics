"""
twoplayers.py
2 Player Chess Mode
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import board

class MoveButton(QPushButton):
	def __init__(self, parent, text = ""):
		super(MoveButton, self).__init__(parent = parent)
		self.setCursor(Qt.PointingHandCursor)
		self.setText(text)
		self.setFixedSize(100, 30)
	
	def enterEvent(self, event: QHoverEvent) -> None:
		self.setStyleSheet("background-color: rgba(100, 0, 255, 0.75); color: white;")
		super(MoveButton, self).enterEvent(event)
		
	def leaveEvent(self, event: QHoverEvent) -> None:
		self.setStyleSheet("background-color: transparent; color: black;")
		super(MoveButton, self).leaveEvent(event)

class QuitButton(QPushButton):
	def __init__(self, parent):
		super(QuitButton, self).__init__(parent = parent)
		self.setText("–")
		self.setFixedSize(QSize(40, 40))
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.pressed.connect(self.parent().back)
		self.status_tip = QLabel("Abort", parent)
		self.status_tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.status_tip.setFixedWidth(40)
		self.status_tip.move(QPoint(self.pos().x(), self.pos().y() + 40))
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
	
	def enterEvent(self, event: QEvent) -> None:
		self.status_tip.show()
		self.setStyleSheet("color: black; background-color: yellow; border: none;")
		super(QuitButton, self).enterEvent(event)
	
	def leaveEvent(self, event: QEvent) -> None:
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
		super(QuitButton, self).leaveEvent(event)

class TwoPlayers(QWidget):
	def __init__(self, parent):
		super(TwoPlayers, self).__init__(parent = parent)
		self.board = board.Board(self)
		self.sidebar = QGroupBox(self)
		self.sidebar.resize(500, 500)
		self.sidebar.setStyleSheet("border: none;")
		self.sidebar_layout = QGridLayout()
		self.moves = QWidget()
		self.moves.resize(200, 200)
		self.moves_layout = QGridLayout()
		self.moves_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.moves_layout.setSpacing(0)
		self.move_buttons = []
		self.moves.setLayout(self.moves_layout)
		self.moves_wrapper = QScrollArea()
		self.moves_wrapper.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.moves_wrapper.setWidgetResizable(True)
		self.moves_wrapper.setWidget(self.moves)
		self.sidebar_layout.addWidget(self.moves_wrapper)
		self.sidebar.setLayout(self.sidebar_layout)
		self.back_button = QuitButton(self)
	
	def back(self):
		self.parent().setCurrentIndex(0)
	
	def formatIndex(self, index: list) -> str: return str(("a", "b", "c", "d", "e", "f", "g", "h")[index[1]]) + str(self.absoluteValue(index[0] - 8))
	
	def getGridIndex(self) -> list:
		columns = 0
		for i in range(len(self.move_buttons)):
			if i % 2 == 0 and i != 0: columns += 1
		return [columns, int(len(self.move_buttons) % 2 == 0)]
	
	@staticmethod
	def absoluteValue(number: int) -> int:
		return -(number if number < 0 else -number)
	
	def addMove(self, piece, index: list or set or tuple, capture: bool, previous_position: list or set or tuple) -> None:
		piece = piece[6:]
		message = {"pawn": "", "knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}[piece]
		if capture:
			if piece == "pawn": message += self.formatIndex(previous_position)[0] + "x" + self.formatIndex(index)
			else: message += "x" + self.formatIndex(index)
		else: message += self.formatIndex(index)
		self.move_buttons.append(MoveButton(self.moves, message))
		self.moves_layout.addWidget(self.move_buttons[-1], self.getGridIndex()[0], self.getGridIndex()[1])
		self.move_buttons[-1].show()
		self.moves_wrapper.verticalScrollBar().setSliderPosition(self.moves_wrapper.verticalScrollBar().maximum())
