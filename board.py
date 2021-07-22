"""
board.py
Board Class
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Piece(QLabel):
	def __init__(self, parent, piece: str or None = None, index: list or None = None):
		super(Piece, self).__init__(parent = parent)
		self.parent, self.index = parent, index
		if piece is not None: self.setPixmap(QPixmap("images/standard/" + piece))
		self.setCursor(Qt.PointingHandCursor)
	
	def paintEvent(self, event: QPaintEvent):
		self.square = self.parent.squares[self.index[0]][self.index[1]]
		super(Piece, self).paintEvent(event)
	
	def mousePressEvent(self, event: QMouseEvent):
		if self.index is None: return
		if event.button() == Qt.RightButton:
			self.square.setStyleSheet(f"background-color: {self.square.original_color if self.square.highlighted else '#560CFF'}; border: none;")
			self.square.highlighted = not self.square.highlighted
		elif event.button() == Qt.LeftButton:
			for x in self.parent.squares:
				for y in x: y.setStyleSheet(f"background-color: {y.original_color}; border: none;")
		super(Piece, self).mousePressEvent(event)

class Square(QPushButton):
	def __init__(self, parent, color: str = "white"):
		super(Square, self).__init__(parent = parent)
		self.original_color, self.highlighted, self.parent = color, False, parent
		self.setStyleSheet(f"background-color: {color}; border: none;")
	
	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.RightButton:
			self.setStyleSheet(f"background-color: {self.original_color if self.highlighted else '#560CFF'}; border: none;")
			self.highlighted = not self.highlighted
		elif event.button() == Qt.LeftButton:
			for x in self.parent.squares:
				for y in x: y.setStyleSheet(f"background-color: {y.original_color}; border: none;")
	
class Board(QWidget):
	def __init__(self, parent):
		super(Board, self).__init__(parent = parent)
		self.squares, self.pieces = [], []
		for x in range(8):
			row = []
			for y in range(8):
				row.append(Square(self, color = "#FFFFDD" if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 != 0) else '#86A666'))
				row[-1].setFixedSize(QSize(100, 100))
				row[-1].move((y + 1) * 100, (x + 1) * 100)
				if x in [0, 7]:
					if y in [0, 7]: self.pieces.append([Piece(self, piece = ("black" if x == 0 else "white") + "_rook", index = [x, y]), [x, y]])
					elif y in [1, 6]: self.pieces.append([Piece(self, piece = ("black" if x == 0 else "white") + "_knight", index = [x, y]), [x, y]])
					elif y in [2, 5]: self.pieces.append([Piece(self, piece = ("black" if x == 0 else "white") + "_bishop", index = [x, y]), [x, y]])
					elif y == 3: self.pieces.append([Piece(self, piece = ("black" if x == 0 else "white") + "_queen", index = [x, y]), [x, y]])
					elif y == 4: self.pieces.append([Piece(self, piece = ("black" if x == 0 else "white") + "_king", index = [x, y]), [x, y]])
					self.pieces[-1][0].move((y + 1) * 100, (x + 1) * 100)
				elif x in [1, 6]:
					self.pieces.append([Piece(self, piece = ("black" if x == 1 else "white") + "_pawn", index = [x, y]), [x, y]])
					self.pieces[-1][0].move((y + 1) * 100, (x + 1) * 100)
			self.squares.append(row)
