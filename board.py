"""
board.py
Board Class
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Piece(QLabel):
	def __init__(self, parent, pixmap = None):
		super(Piece, self).__init__(parent = parent)
		if pixmap is not None: self.setPixmap(pixmap)
		self.setCursor(Qt.PointingHandCursor)

class Board(QWidget):
	def __init__(self, parent):
		super(Board, self).__init__(parent = parent)
		self.squares, self.pieces = [], []
		for x in range(8):
			row = []
			for y in range(8):
				row.append(QWidget(self))
				row[-1].setFixedSize(QSize(100, 100))
				row[-1].move((y + 1) * 100, (x + 1) * 100)
				row[-1].setStyleSheet(f"background-color: {'#FFFFDD' if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 != 0) else '#86A666'};")
				if x in [0, 7]:
					if y in [0, 7]: self.pieces.append([Piece(self, pixmap = QPixmap(f"images/standard/{'black' if x == 0 else 'white'}_rook.png").scaled(75, 75, Qt.KeepAspectRatio)), [x, y]])
					elif y in [1, 6]: self.pieces.append([Piece(self, pixmap = QPixmap(f"images/standard/{'black' if x == 0 else 'white'}_knight.png").scaled(75, 75, Qt.KeepAspectRatioByExpanding)), [x, y]])
					elif y in [2, 5]: self.pieces.append([Piece(self, pixmap = QPixmap(f"images/standard/{'black' if x == 0 else 'white'}_bishop.png").scaled(75, 75, Qt.KeepAspectRatioByExpanding)), [x, y]])
					elif y == 3: self.pieces.append([Piece(self, pixmap = QPixmap(f"images/standard/{'black' if x == 0 else 'white'}_queen.png").scaled(75, 75, Qt.KeepAspectRatioByExpanding)), [x, y]])
					elif y == 4: self.pieces.append([Piece(self, pixmap = QPixmap(f"images/standard/{'black' if x == 0 else 'white'}_king.png").scaled(75, 75, Qt.KeepAspectRatioByExpanding)), [x, y]])
					self.pieces[-1][0].move(((y + 1) * 100) + (12.5 if y not in [0, 7] else 17), ((x + 1) * 100) + (12.5 if y not in [0, 7] else 15))
				elif x in [1, 6]:
					self.pieces.append([Piece(self, pixmap = QPixmap(f"images/standard/{'black' if x == 1 else 'white'}_pawn.png").scaled(75, 75, Qt.KeepAspectRatio)), [x, y]])
					self.pieces[-1][0].move(((y + 1) * 100) + 22.5, ((x + 1) * 100) + 12.5)
			self.squares.append(row)
