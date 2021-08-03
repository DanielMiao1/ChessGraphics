"""
board.py
Board Class
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MoveBullet(QLabel):
	def __init__(self, parent, piece, index: list or tuple or set = (0, 0), hide: bool = True, capture: bool = False, castle: 0 or 1 or False = False, castle_rook = None, double_pawn_move: bool = False, en_passant_pawn = False):
		super(MoveBullet, self).__init__(parent = parent)
		self.setPixmap(QPixmap("images/bullet.png"))
		self.piece, self.index, self.capture, self.castle, self.castle_rook, self.double_pawn_move, self.en_passant_pawn = piece, index, capture, castle, castle_rook, double_pawn_move, en_passant_pawn
		self.resize(100, 100)
		if hide: self.hide()
		self.setCursor(Qt.PointingHandCursor)
	
	def enterEvent(self, event: QHoverEvent):
		self.setStyleSheet("background-color: rgba(12, 36, 255, 0.5)")
		super(MoveBullet, self).enterEvent(event)
	
	def leaveEvent(self, event: QHoverEvent):
		self.setStyleSheet("background-color: transparent")
		super(MoveBullet, self).leaveEvent(event)
	
	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.LeftButton: self.piece.movePiece(self.pos(), index = self.index, capture = self.capture, castle = self.castle, castle_rook = self.castle_rook, double_pawn_move = self.double_pawn_move, en_passant_pawn = self.en_passant_pawn)
		else: self.parent().mousePressEvent(event)
		super(MoveBullet, self).mousePressEvent(event)

class PromotionButton(QToolButton):
	def __init__(self, parent_widget, piece, color):
		super(PromotionButton, self).__init__(parent = parent_widget.parent().parent())
		self.setFixedSize(100, 100)
		self.setCursor(Qt.PointingHandCursor)
		self.setStyleSheet("border-radius: 100%; background-color: rgba(12, 36, 255, 0.5);")
		self.setIcon(QIcon(f"images/standard/{color}_{piece}.png"))
		self.setIconSize(QSize(100, 100))
		self.setToolButtonStyle(Qt.ToolButtonIconOnly)
		self.piece, self.parent_widget = piece, parent_widget
		self.hide()
	
	def mousePressEvent(self, event: QMouseEvent) -> None:
		self.parent_widget.queen.hide()
		self.parent_widget.rook.hide()
		self.parent_widget.bishop.hide()
		self.parent_widget.knight.hide()
		super(PromotionButton, self).mousePressEvent(event)
	
class PromotionDialog(QWidget):
	def __init__(self, parent, side):
		super(PromotionDialog, self).__init__(parent = parent)
		self.queen, self.rook, self.bishop, self.knight = PromotionButton(self, piece = "queen", color = side), PromotionButton(self, piece = "rook", color = side), PromotionButton(self, piece = "bishop", color = side), PromotionButton(self, piece = "knight", color = side)
		self.queen.move(100, 0)
		self.rook.move(100, 50)
		self.bishop.move(100, 100)
		self.knight.move(100, 150)
		self.resize(QSize(1000, 1000))
		self.hide()
	
	def paintEvent(self, event: QPaintEvent) -> None:
		self.queen.move(self.parent().pos())
		self.rook.move(self.parent().pos().x(), self.parent().pos().y() + 100)
		self.bishop.move(self.parent().pos().x(), self.parent().pos().y() + 200)
		self.knight.move(self.parent().pos().x(), self.parent().pos().y() + 300)
		self.queen.raise_()
		self.rook.raise_()
		self.bishop.raise_()
		self.knight.raise_()
		super(PromotionDialog, self).paintEvent(event)
	
	def showEvent(self, event: QShowEvent) -> None:
		self.queen.show()
		self.rook.show()
		self.bishop.show()
		self.knight.show()
		super(PromotionDialog, self).showEvent(event)

class Piece(QLabel):
	def __init__(self, parent, piece: str or None = None, index: list or None = None):
		super(Piece, self).__init__(parent = parent)
		self.parent, self.index, self.piece, self.showing_moves, self.moves, self.first_paint_run, self.animation, self.promotion_dialog, self.moved, self.allow_en_passant = parent, index, piece, False, [], True, None, PromotionDialog(self, side = piece[:5]), False, False
		if piece is not None: self.setPixmap(QPixmap("images/standard/" + piece))
		self.setCursor(Qt.PointingHandCursor)
	
	def appendMoves(self):
		if self.piece in ["white_pawn", "black_pawn"]:
			for i in self.parent.pieces:
				if i[1] == [self.index[0], self.index[1] + 1] and i[0].allow_en_passant:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - (1 if self.piece[:5] == "white" else -1), self.index[1] + 1], en_passant_pawn = i[0]))
					self.moves[-1].move(self.parent.squares[self.index[0] - (1 if self.piece[:5] == "white" else -1)][self.index[1] + 1].pos())
				elif i[1] == [self.index[0], self.index[1] - 1] and i[0].allow_en_passant:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - (1 if self.piece[:5] == "white" else -1), self.index[1] - 1], en_passant_pawn = i[0]))
					self.moves[-1].move(self.parent.squares[self.index[0] - (1 if self.piece[:5] == "white" else -1)][self.index[1] - 1].pos())
			found = False
			for i in self.parent.pieces:
				if i[1] == [self.index[0] - (1 if self.piece == "white_pawn" else -1), self.index[1]]: found = True
			if not found:
				self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - (1 if self.piece == "white_pawn" else -1), self.index[1]]))
				self.moves[-1].move(self.parent.squares[self.index[0] - (1 if self.piece == "white_pawn" else -1)][self.index[1]].pos())
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - (2 if self.piece == "white_pawn" else -2), self.index[1]]: found = True
				if not found:
					if self.index[0] == 6 and self.piece == "white_pawn":
						self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - 2, self.index[1]], double_pawn_move = True))
						self.moves[-1].move(self.parent.squares[self.index[0] - 2][self.index[1]].pos())
					elif self.index[0] == 1 and self.piece == "black_pawn":
						self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] + 2, self.index[1]], double_pawn_move = True))
						self.moves[-1].move(self.parent.squares[self.index[0] + 2][self.index[1]].pos())
			piece_found, position, index = False, None, None
			if self.piece == "white_pawn":
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1] - 1] and i[0].piece[:5] == "black": piece_found, position, index = True, i[0], i[1]
				if piece_found:
					self.moves.append(MoveBullet(self.parent, self, index = index, capture = True))
					self.moves[-1].move(position.pos())
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1] + 1] and i[0].piece[:5] == "black": piece_found, position, index = True, i[0], i[1]
				if piece_found:
					self.moves.append(MoveBullet(self.parent, self, index = index, capture = True))
					self.moves[-1].move(position.pos())
			else:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1] - 1] and i[0].piece[:5] == "white": piece_found, position, index = True, i[0], i[1]
				if piece_found:
					self.moves.append(MoveBullet(self.parent, self, index = index, capture = True))
					self.moves[-1].move(position.pos())
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1] + 1] and i[0].piece[:5] == "white": piece_found, position, index = True, i[0], i[1]
				if piece_found:
					self.moves.append(MoveBullet(self.parent, self, index = index, capture = True))
					self.moves[-1].move(position.pos())
		elif self.piece in ["white_knight", "black_knight"]:
			found, valid = False, True
			if self.index[0] not in [0, 1] and self.index[1] != 0:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 2, self.index[1] - 1]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
						found = True
				if valid:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - 2, self.index[1] - 1], capture = found))
					self.moves[-1].move(self.parent.squares[self.index[0] - 2][self.index[1] - 1].pos())
			found, valid = False, True
			if self.index[0] not in [0, 1] and self.index[1] != 7:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 2, self.index[1] + 1]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
						found = True
				if valid:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - 2, self.index[1] + 1], capture = found))
					self.moves[-1].move(self.parent.squares[self.index[0] - 2][self.index[1] + 1].pos())
			found, valid = False, True
			if self.index[0] not in [6, 7] and self.index[1] != 0:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 2, self.index[1] - 1]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
						found = True
				if valid:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] + 2, self.index[1] - 1], capture = found))
					self.moves[-1].move(self.parent.squares[self.index[0] + 2][self.index[1] - 1].pos())
			found, valid = False, True
			if self.index[0] not in [6, 7] and self.index[1] != 7:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 2, self.index[1] + 1]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
						found = True
				if valid:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] + 2, self.index[1] + 1], capture = found))
					self.moves[-1].move(self.parent.squares[self.index[0] + 2][self.index[1] + 1].pos())
			found, valid = False, True
			if self.index[0] != 0 and self.index[1] not in [0, 1]:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1] - 2]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
						found = True
				if valid:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - 1, self.index[1] - 2], capture = found))
					self.moves[-1].move(self.parent.squares[self.index[0] - 1][self.index[1] - 2].pos())
			found, valid = False, True
			if self.index[0] != 7 and self.index[1] not in [0, 1]:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1] - 2]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
						found = True
				if valid:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] + 1, self.index[1] - 2], capture = found))
					self.moves[-1].move(self.parent.squares[self.index[0] + 1][self.index[1] - 2].pos())
			found, valid = False, True
			if self.index[0] != 0 and self.index[1] not in [6, 7]:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1] + 2]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
						found = True
				if valid:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - 1, self.index[1] + 2], capture = found))
					self.moves[-1].move(self.parent.squares[self.index[0] - 1][self.index[1] + 2].pos())
			found, valid = False, True
			if self.index[0] != 7 and self.index[1] not in [6, 7]:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1] + 2]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
						found = True
				if valid:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] + 1, self.index[1] + 2], capture = found))
					self.moves[-1].move(self.parent.squares[self.index[0] + 1][self.index[1] + 2].pos())
		elif self.piece in ["white_bishop", "black_bishop"]:
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 0:
				pos1, pos2 = pos1 - 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [pos1, pos2], capture = capture))
					self.moves[-1].move(self.parent.squares[pos1][pos2].pos())
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 7:
				pos1, pos2 = pos1 + 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [pos1, pos2], capture = capture))
					self.moves[-1].move(self.parent.squares[pos1][pos2].pos())
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 7:
				pos1, pos2 = pos1 - 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [pos1, pos2], capture = capture))
					self.moves[-1].move(self.parent.squares[pos1][pos2].pos())
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 0:
				pos1, pos2 = pos1 + 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [pos1, pos2], capture = capture))
					self.moves[-1].move(self.parent.squares[pos1][pos2].pos())
					if capture: break
					continue
				break
		elif self.piece in ["white_rook", "black_rook"]:
			capture = False
			for x in reversed(range(self.index[0])):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [x, self.index[1]], capture = capture))
					self.moves[-1].move(self.parent.squares[x][self.index[1]].pos())
					if capture: break
					continue
				break
			capture = False
			for x in reversed(range(self.index[1])):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0], x], capture = capture))
					self.moves[-1].move(self.parent.squares[self.index[0]][x].pos())
					if capture: break
					continue
				break
			capture = False
			for x in range(self.index[0] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [x, self.index[1]], capture = capture))
					self.moves[-1].move(self.parent.squares[x][self.index[1]].pos())
					if capture: break
					continue
				break
			capture = False
			for x in range(self.index[1] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0], x], capture = capture))
					self.moves[-1].move(self.parent.squares[self.index[0]][x].pos())
					if capture: break
					continue
				break
		elif self.piece in ["white_queen", "black_queen"]:
			capture = False
			for x in reversed(range(self.index[0])):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [x, self.index[1]], capture = capture))
					self.moves[-1].move(self.parent.squares[x][self.index[1]].pos())
					if capture: break
					continue
				break
			capture = False
			for x in reversed(range(self.index[1])):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0], x], capture = capture))
					self.moves[-1].move(self.parent.squares[self.index[0]][x].pos())
					if capture: break
					continue
				break
			capture = False
			for x in range(self.index[0] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [x, self.index[1]], capture = capture))
					self.moves[-1].move(self.parent.squares[x][self.index[1]].pos())
					if capture: break
					continue
				break
			capture = False
			for x in range(self.index[1] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [self.index[0], x], capture = capture))
					self.moves[-1].move(self.parent.squares[self.index[0]][x].pos())
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 0:
				pos1, pos2 = pos1 - 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [pos1, pos2], capture = capture))
					self.moves[-1].move(self.parent.squares[pos1][pos2].pos())
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 7:
				pos1, pos2 = pos1 + 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [pos1, pos2], capture = capture))
					self.moves[-1].move(self.parent.squares[pos1][pos2].pos())
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 7:
				pos1, pos2 = pos1 - 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [pos1, pos2], capture = capture))
					self.moves[-1].move(self.parent.squares[pos1][pos2].pos())
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 0:
				pos1, pos2 = pos1 + 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					self.moves.append(MoveBullet(self.parent, self, index = [pos1, pos2], capture = capture))
					self.moves[-1].move(self.parent.squares[pos1][pos2].pos())
					if capture: break
					continue
				break
		else:
			capture = False
			if self.index[0] != 0:
				if self.squareValidForKing([self.index[0] - 1, self.index[1]]):
					for i in self.parent.pieces:
						if i[1] == [self.index[0] - 1, self.index[1]]:
							if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
							capture = True
					else:
						self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - 1, self.index[1]], capture = capture))
						self.moves[-1].move(self.parent.squares[self.index[0] - 1][self.index[1]].pos())
			capture = False
			if self.index[0] != 7:
				if self.squareValidForKing([self.index[0] + 1, self.index[1]]):
					for i in self.parent.pieces:
						if i[1] == [self.index[0] + 1, self.index[1]]:
							if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
							capture = True
					else:
						self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] + 1, self.index[1]], capture = capture))
						self.moves[-1].move(self.parent.squares[self.index[0] + 1][self.index[1]].pos())
			capture = False
			if self.index[1] != 0:
				if self.squareValidForKing([self.index[0], self.index[1] - 1]):
					for i in self.parent.pieces:
						if i[1] == [self.index[0], self.index[1] - 1]:
							if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
							capture = True
					else:
						self.moves.append(MoveBullet(self.parent, self, index = [self.index[0], self.index[1] - 1], capture = capture))
						self.moves[-1].move(self.parent.squares[self.index[0]][self.index[1] - 1].pos())
			capture = False
			if self.index[1] != 7:
				if self.squareValidForKing([self.index[0], self.index[1] + 1]):
					for i in self.parent.pieces:
						if i[1] == [self.index[0], self.index[1] + 1]:
							if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
							capture = True
					else:
						self.moves.append(MoveBullet(self.parent, self, index = [self.index[0], self.index[1] + 1], capture = capture))
						self.moves[-1].move(self.parent.squares[self.index[0]][self.index[1] + 1].pos())
			capture = False
			if self.index[0] != 0 and self.index[1] != 0:
				if self.squareValidForKing([self.index[0] - 1, self.index[1] - 1]):
					for i in self.parent.pieces:
						if i[1] == [self.index[0] - 1, self.index[1] - 1]:
							if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
							capture = True
					else:
						self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - 1, self.index[1] - 1], capture = capture))
						self.moves[-1].move(self.parent.squares[self.index[0] - 1][self.index[1] - 1].pos())
			capture = False
			if self.index[0] != 7 and self.index[1] != 7:
				if self.squareValidForKing([self.index[0] + 1, self.index[1] + 1]):
					for i in self.parent.pieces:
						if i[1] == [self.index[0] + 1, self.index[1] + 1]:
							if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
							capture = True
					else:
						self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] + 1, self.index[1] + 1], capture = capture))
						self.moves[-1].move(self.parent.squares[self.index[0] + 1][self.index[1] + 1].pos())
			capture = False
			if self.index[0] != 0 and self.index[1] != 7:
				if self.squareValidForKing([self.index[0] - 1, self.index[1] + 1]):
					for i in self.parent.pieces:
						if i[1] == [self.index[0] - 1, self.index[1] + 1]:
							if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
							capture = True
					else:
						self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] - 1, self.index[1] + 1], capture = capture))
						self.moves[-1].move(self.parent.squares[self.index[0] - 1][self.index[1] + 1].pos())
			capture = False
			if self.index[0] != 7 and self.index[1] != 0:
				if self.squareValidForKing([self.index[0] + 1, self.index[1] - 1]):
					for i in self.parent.pieces:
						if i[1] == [self.index[0] + 1, self.index[1] - 1]:
							if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
							capture = True
					else:
						self.moves.append(MoveBullet(self.parent, self, index = [self.index[0] + 1, self.index[1] - 1], capture = capture))
						self.moves[-1].move(self.parent.squares[self.index[0] + 1][self.index[1] - 1].pos())
			if not self.moved:
				for x in self.parent.pieces:
					if x[0].piece == self.piece[:5] + "_rook" and not x[0].moved:
						if x[0].index == [7, 7] and not self.inCheck():
							for y in self.parent.pieces:
								if y[0].index in [[7, 5], [7, 6]]: break
							else:
								self.moves.append(MoveBullet(self.parent, self, index = [7, 7], castle = 0, castle_rook = x[0]))
								self.moves[-1].move(self.parent.squares[7][7].pos())
								self.moves.append(MoveBullet(self.parent, self, index = [7, 6], castle = 0, castle_rook = x[0]))
								self.moves[-1].move(self.parent.squares[7][6].pos())
						elif x[0].index == [7, 0] and not self.inCheck():
							for y in self.parent.pieces:
								if y[0].index in [[7, 1], [7, 2], [7, 3]]: break
							else:
								self.moves.append(MoveBullet(self.parent, self, index = [7, 0], castle = 1, castle_rook = x[0]))
								self.moves[-1].move(self.parent.squares[7][0].pos())
								self.moves.append(MoveBullet(self.parent, self, index = [7, 2], castle = 1, castle_rook = x[0]))
								self.moves[-1].move(self.parent.squares[7][2].pos())
						elif x[0].index == [0, 0] and not self.inCheck():
							for y in self.parent.pieces:
								if y[0].index in [[0, 1], [0, 2], [0, 3]]: break
							else:
								self.moves.append(MoveBullet(self.parent, self, index = [0, 0], castle = 1, castle_rook = x[0]))
								self.moves[-1].move(self.parent.squares[0][0].pos())
								self.moves.append(MoveBullet(self.parent, self, index = [0, 2], castle = 1, castle_rook = x[0]))
								self.moves[-1].move(self.parent.squares[0][2].pos())
						elif x[0].index == [0, 7] and not self.inCheck():
							for y in self.parent.pieces:
								if y[0].index in [[0, 5], [0, 6]]: break
							else:
								self.moves.append(MoveBullet(self.parent, self, index = [0, 7], castle = 0, castle_rook = x[0]))
								self.moves[-1].move(self.parent.squares[0][6].pos())
								self.moves.append(MoveBullet(self.parent, self, index = [0, 6], castle = 0, castle_rook = x[0]))
								self.moves[-1].move(self.parent.squares[0][7].pos())
	
	def inCheck(self): return self.parent.parent().move_buttons[-1].text().endswith("+") if self.parent.parent().move_buttons else False
	
	def resizeEvent(self, event: QResizeEvent) -> None:
		self.square = self.parent.squares[self.index[0]][self.index[1]]
		super(Piece, self).resizeEvent(event)
	
	def mousePressEvent(self, event: QMouseEvent):
		if self.index is None: return
		if event.button() == Qt.RightButton:
			if self.parent.piece_for_shown_moves is not None:
				for i in self.parent.piece_for_shown_moves.moves: i.hide()
				self.parent.piece_for_shown_moves.setStyleSheet("background-color: transparent;")
				self.parent.piece_for_shown_moves.showing_moves = False
				self.parent.piece_for_shown_moves = None
			if self.square.highlighted: self.square.highlight_mask.hide()
			else: self.square.highlight_mask.show()
			self.setStyleSheet("background-color: transparent;")
			self.square.highlighted = not self.square.highlighted
		elif event.button() == Qt.LeftButton:
			if self.showing_moves:
				for i in self.moves: i.hide()
				self.setStyleSheet("background-color: transparent;")
			else:
				self.moves = []
				if self.parent.piece_for_shown_moves is not None:
					self.parent.piece_for_shown_moves.setStyleSheet("background-color: transparent;")
					for i in self.parent.piece_for_shown_moves.moves: i.hide()
					self.parent.piece_for_shown_moves.showing_moves = False
				self.parent.piece_for_shown_moves = self
				if self.piece[:5] == self.parent.turn:
					self.appendMoves()
					for i in self.moves: i.show()
			for x in self.parent.squares:
				for y in x:
					if self.parent.squares.index(x) == self.index[0] and x.index(y) == self.index[1] and not self.showing_moves: self.setStyleSheet("background-color: rgba(86, 12, 255, 0.5);")
					y.highlight_mask.hide()
			self.showing_moves = not self.showing_moves
		super(Piece, self).mousePressEvent(event)
	
	def validMoves(self) -> list:
		moves = []
		if self.piece in ["white_pawn", "black_pawn"]:
			found = False
			for i in self.parent.pieces:
				if i[1] == [self.index[0] - (1 if self.piece == "white_pawn" else -1), self.index[1]]: found = True
			if not found:
				moves.append([self.index[0] - (1 if self.piece == "white_pawn" else -1), self.index[1]])
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - (2 if self.piece == "white_pawn" else -2), self.index[1]]: found = True
				if not found:
					if self.index[0] == 6 and self.piece == "white_pawn": moves.append([self.index[0] - 2, self.index[1]])
					elif self.index[0] == 1 and self.piece == "black_pawn": moves.append([self.index[0] + 2, self.index[1]])
			piece_found, position, index = False, None, None
			if self.piece == "white_pawn":
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1] - 1] and i[0].piece[:5] == "black": piece_found, position, index = True, i[0], i[1]
				if piece_found: moves.append(index)
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1] + 1] and i[0].piece[:5] == "black": piece_found, position, index = True, i[0], i[1]
				if piece_found: moves.append(index)
			else:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1] - 1] and i[0].piece[:5] == "white": piece_found, position, index = True, i[0], i[1]
				if piece_found: moves.append(index)
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1] + 1] and i[0].piece[:5] == "white": piece_found, position, index = True, i[0], i[1]
				if piece_found: moves.append(index)
		elif self.piece in ["white_knight", "black_knight"]:
			found, valid = False, True
			if self.index[0] not in [0, 1] and self.index[1] != 0:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 2, self.index[1] - 1]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
				if valid: moves.append([self.index[0] - 2, self.index[1] - 1])
			found, valid = False, True
			if self.index[0] not in [0, 1] and self.index[1] != 7:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 2, self.index[1] + 1]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
				if valid: moves.append([self.index[0] - 2, self.index[1] + 1])
			found, valid = False, True
			if self.index[0] not in [6, 7] and self.index[1] != 0:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 2, self.index[1] - 1]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
				if valid: moves.append([self.index[0] + 2, self.index[1] - 1])
			found, valid = False, True
			if self.index[0] not in [6, 7] and self.index[1] != 7:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 2, self.index[1] + 1]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
				if valid: moves.append([self.index[0] + 2, self.index[1] + 1])
			found, valid = False, True
			if self.index[0] != 0 and self.index[1] not in [0, 1]:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1] - 2]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
				if valid: moves.append([self.index[0] - 1, self.index[1] - 2])
			found, valid = False, True
			if self.index[0] != 7 and self.index[1] not in [0, 1]:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1] - 2]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
				if valid: moves.append([self.index[0] + 1, self.index[1] - 2])
			found, valid = False, True
			if self.index[0] != 0 and self.index[1] not in [6, 7]:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1] + 2]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
				if valid: moves.append([self.index[0] - 1, self.index[1] + 2])
			found, valid = False, True
			if self.index[0] != 7 and self.index[1] not in [6, 7]:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1] + 2]:
						if i[0].piece[:5] == self.piece[:5]: valid = False
				if valid: moves.append([self.index[0] + 1, self.index[1] + 2])
		elif self.piece in ["white_bishop", "black_bishop"]:
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 0:
				pos1, pos2 = pos1 - 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([pos1, pos2])
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 7:
				pos1, pos2 = pos1 + 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([pos1, pos2])
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 7:
				pos1, pos2 = pos1 - 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([pos1, pos2])
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 0:
				pos1, pos2 = pos1 + 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([pos1, pos2])
					if capture: break
					continue
				break
		elif self.piece in ["white_rook", "black_rook"]:
			capture = False
			for x in reversed(range(self.index[0])):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([x, self.index[1]])
					if capture: break
					continue
				break
			capture = False
			for x in reversed(range(self.index[1])):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([self.index[0], x])
					if capture: break
					continue
				break
			capture = False
			for x in range(self.index[0] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([x, self.index[1]])
					if capture: break
					continue
				break
			capture = False
			for x in range(self.index[1] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([x, self.index[1]])
					if capture: break
					continue
				break
		elif self.piece in ["white_queen", "black_queen"]:
			capture = False
			for x in reversed(range(self.index[0])):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([x, self.index[1]])
					if capture: break
					continue
				break
			capture = False
			for x in reversed(range(self.index[1])):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([self.index[0], x])
					if capture: break
					continue
				break
			capture = False
			for x in range(self.index[0] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([x, self.index[1]])
					if capture: break
					continue
				break
			capture = False
			for x in range(self.index[1] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([x, self.index[1]])
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 0:
				pos1, pos2 = pos1 - 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([pos1, pos2])
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 7:
				pos1, pos2 = pos1 + 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([pos1, pos2])
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 7:
				pos1, pos2 = pos1 - 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([pos1, pos2])
					if capture: break
					continue
				break
			capture, pos1, pos2 = False, self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 0:
				pos1, pos2 = pos1 + 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece[:5] == self.piece[:5]: break
						capture = True
				else:
					moves.append([pos1, pos2])
					if capture: break
					continue
				break
		else:
			if self.index[0] != 0:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1]]:
						if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
						for y in self.parent.pieces:
							if y[0].piece[:5] == ("white" if self.piece[:5] == "black" else "black"):
								if [self.index[0] - 1, self.index[1]] in y[0].validMoves(): break
				else: moves.append([self.index[0] - 1, self.index[1]])
			if self.index[0] != 7:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1]]:
						if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
						for y in self.parent.pieces:
							if y[0].piece[:5] == ("white" if self.piece[:5] == "black" else "black"):
								if [self.index[0] + 1, self.index[1]] in y[0].validMoves(): break
				else: moves.append([self.index[0] + 1, self.index[1]])
			if self.index[1] != 0:
				for i in self.parent.pieces:
					if i[1] == [self.index[0], self.index[1] - 1]:
						if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
						for y in self.parent.pieces:
							if y[0].piece[:5] == ("white" if self.piece[:5] == "black" else "black"):
								if [self.index[0], self.index[1] - 1] in y[0].validMoves(): break
				else: moves.append([self.index[0], self.index[1] - 1])
			if self.index[1] != 7:
				for i in self.parent.pieces:
					if i[1] == [self.index[0], self.index[1] + 1]:
						if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
						for y in self.parent.pieces:
							if y[0].piece[:5] == ("white" if self.piece[:5] == "black" else "black"):
								if [self.index[0], self.index[1] + 1] in y[0].validMoves(): break
				else: moves.append([self.index[0], self.index[1] + 1])
			if self.index[0] != 0 and self.index[1] != 0:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1] - 1]:
						if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
						for y in self.parent.pieces:
							if y[0].piece[:5] == ("white" if self.piece[:5] == "black" else "black"):
								if [self.index[0] - 1, self.index[1] - 1] in y[0].validMoves(): break
				else: moves.append([self.index[0] - 1, self.index[1] - 1])
			if self.index[0] != 7 and self.index[1] != 7:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1] + 1]:
						if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
						for y in self.parent.pieces:
							if y[0].piece[:5] == ("white" if self.piece[:5] == "black" else "black"):
								if [self.index[0] + 1, self.index[1] + 1] in y[0].validMoves(): break
				else: moves.append([self.index[0] + 1, self.index[1] + 1])
			if self.index[0] != 0 and self.index[1] != 7:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] - 1, self.index[1] + 1]:
						if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
						for y in self.parent.pieces:
							if y[0].piece[:5] == ("white" if self.piece[:5] == "black" else "black"):
								if [self.index[0] - 1, self.index[1] + 1] in y[0].validMoves(): break
				else: moves.append([self.index[0] - 1, self.index[1] + 1])
			if self.index[0] != 7 and self.index[1] != 0:
				for i in self.parent.pieces:
					if i[1] == [self.index[0] + 1, self.index[1] - 1]:
						if i[0].piece[:5] == self.piece[:5] or i[0].piece[6:] == "king": break
						for y in self.parent.pieces:
							if y[0].piece[:5] == ("white" if self.piece[:5] == "black" else "black"):
								if [self.index[0] + 1, self.index[1] - 1] in y[0].validMoves(): break
				else: moves.append([self.index[0] + 1, self.index[1] - 1])
		return moves
	
	def squareValidForKing(self, index: list) -> bool:
		for x in self.parent.pieces:
			if x[0].piece == ("white_king" if self.piece == "black_king" else "black_king"):
				if index in x[0].validMoves(): return False
		for x in self.parent.pieces:
			if x[0].piece in ["white_king", "black_king"] or x[0].piece[:5] == self.piece[:5]: continue
			x[0].appendMoves()
			if x[0].piece in ["white_pawn", "black_pawn"]:
				if self.piece[:5] == "white" and x[0].index in [[index[0] - 1, index[1] - 1], [index[0] - 1, index[1] + 1]]: return False
				elif self.piece[:5] == "black" and x[0].index in [[index[0] + 1, index[1] + 1], [index[0] + 1, index[1] - 1]]: return False
			else:
				for y in x[0].moves:
					if y.index == index: return False
		return True
	
	def isCheck(self, index: list) -> bool:
		if self.piece in ["white_pawn", "black_pawn"] and index[0] != 0:
			if self.piece == "white_pawn":
				for i in self.parent.pieces:
					if i[1] in [[index[0] - 1, index[1] - 1], [index[0] - 1, index[1] + 1]] and i[0].piece == "black_king": return True
			else:
				for i in self.parent.pieces:
					if i[1] in [[index[0] + 1, index[1] - 1], [index[0] + 1, index[1] + 1]] and i[0].piece == "white_king": return True
		elif self.piece in ["white_knight", "black_knight"]:
			if self.index[0] not in [0, 1] and self.index[1] != 0:
				for i in self.parent.pieces:
					if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king") and i[1] == [self.index[0] - 2, self.index[1] - 1]: return True
			if self.index[0] not in [0, 1] and self.index[1] != 7:
				for i in self.parent.pieces:
					if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king") and i[1] == [self.index[0] - 2, self.index[1] + 1]: return True
			if self.index[0] not in [6, 7] and self.index[1] != 0:
				for i in self.parent.pieces:
					if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king") and i[1] == [self.index[0] + 2, self.index[1] - 1]: return True
			if self.index[0] not in [6, 7] and self.index[1] != 7:
				for i in self.parent.pieces:
					if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king") and i[1] == [self.index[0] + 2, self.index[1] + 1]: return True
			if self.index[0] != 0 and self.index[1] not in [0, 1]:
				for i in self.parent.pieces:
					if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king") and i[1] == [self.index[0] - 1, self.index[1] - 2]: return True
			if self.index[0] != 7 and self.index[1] not in [0, 1]:
				for i in self.parent.pieces:
					if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king") and i[1] == [self.index[0] + 1, self.index[1] - 2]: return True
			if self.index[0] != 0 and self.index[1] not in [6, 7]:
				for i in self.parent.pieces:
					if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king") and i[1] == [self.index[0] - 1, self.index[1] + 2]: return True
			if self.index[0] != 7 and self.index[1] not in [6, 7]:
				for i in self.parent.pieces:
					if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king") and i[1] == [self.index[0] + 1, self.index[1] + 2]: return True
		elif self.piece in ["white_bishop", "black_bishop"]:
			pos1, pos2 = self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 0:
				pos1, pos2 = pos1 - 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			pos1, pos2 = self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 7:
				pos1, pos2 = pos1 + 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			pos1, pos2 = self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 7:
				pos1, pos2 = pos1 - 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			pos1, pos2 = self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 0:
				pos1, pos2 = pos1 + 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
		elif self.piece in ["white_rook", "black_rook"]:
			for x in reversed(range(self.index[0])):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			for x in reversed(range(self.index[1])):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			for x in range(self.index[0] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			for x in range(self.index[1] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
		elif self.piece in ["white_queen", "black_queen"]:
			pos1, pos2 = self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 0:
				pos1, pos2 = pos1 - 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			pos1, pos2 = self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 7:
				pos1, pos2 = pos1 + 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			pos1, pos2 = self.index[0], self.index[1]
			while pos1 != 0 and pos2 != 7:
				pos1, pos2 = pos1 - 1, pos2 + 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			pos1, pos2 = self.index[0], self.index[1]
			while pos1 != 7 and pos2 != 0:
				pos1, pos2 = pos1 + 1, pos2 - 1
				for i in self.parent.pieces:
					if i[1] == [pos1, pos2]:
						if i[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			for x in reversed(range(self.index[0])):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			for x in reversed(range(self.index[1])):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			for x in range(self.index[0] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [x, self.index[1]]:
						if y[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
			for x in range(self.index[1] + 1, 8):
				for y in self.parent.pieces:
					if y[1] == [self.index[0], x]:
						if y[0].piece == ("black_king" if self.piece[:5] == "white" else "white_king"): return True
						break
				else: continue
				break
		return False
	
	def movePiece(self, position, index: list or tuple or set = (0, 0), capture: bool = False, castle: 0 or 1 or False = False, castle_rook = None, add_move: bool = True, double_pawn_move: bool = False, en_passant_pawn = False):
		self.moved = True
		previous_position, self.allow_en_passant = self.index, double_pawn_move
		for i in self.parent.pieces:
			if i[0] == self: continue
			i[0].allow_en_passant = False
		if capture:
			for i in self.parent.pieces:
				if i[1] == index:
					i[0].deleteLater()
					self.parent.pieces.remove(i)
		elif en_passant_pawn:
			for i in self.parent.pieces:
				if i[0] == en_passant_pawn:
					i[0].deleteLater()
					self.parent.pieces.remove(i)
		self.setStyleSheet("background-color: transparent;")
		if str(castle) == "0" and castle_rook is not None:
			self.animation = QPropertyAnimation(self, b"pos")
			self.animation.setEndValue(self.parent.squares[7][6].pos() if self.piece[:5] == "white" else self.parent.squares[0][6].pos())
			self.animation.setDuration(100)
			self.animation.start()
			castle_rook.movePiece(self.parent.squares[7][5].pos() if self.piece[:5] == "white" else self.parent.squares[0][5].pos(), [7, 5] if self.piece[:5] == "white" else [0, 5], add_move = False)
			self.parent.turn = {"white": "black", "black": "white"}[self.parent.turn]
		elif str(castle) == "1" and castle_rook is not None:
			self.animation = QPropertyAnimation(self, b"pos")
			self.animation.setEndValue(self.parent.squares[7][2].pos() if self.piece[:5] == "white" else self.parent.squares[0][2].pos())
			self.animation.setDuration(100)
			self.animation.start()
			castle_rook.movePiece(self.parent.squares[7][3].pos() if self.piece[:5] == "white" else self.parent.squares[0][3].pos(), [7, 3] if self.piece[:5] == "white" else [0, 3], add_move = False)
			self.parent.turn = {"white": "black", "black": "white"}[self.parent.turn]
		else:
			self.animation = QPropertyAnimation(self, b"pos")
			self.animation.setEndValue(position)
			self.animation.setDuration(100)
			self.animation.start()
		for i in self.moves: i.deleteLater()
		self.index, self.moves = index if str(castle) == "False" else [0 if self.piece[:5] == "black" else 7, 2 if str(castle) == "1" else 6], []
		self.square = self.parent.squares[self.index[0]][self.index[1]]
		self.showing_moves, self.parent.piece_for_shown_moves = False, None
		self.raise_()
		self.parent.turn = {"white": "black", "black": "white"}[self.parent.turn]
		for i in range(len(self.parent.pieces)):
			if self.parent.pieces[i][0] == self: self.parent.pieces[i][1] = self.index
		if self.piece in ["white_pawn", "black_pawn"] and index[0] in [0, 7] and add_move:
			self.promotion_dialog.show()
			self.promotion_dialog.queen.pressed.connect(lambda: self.changePiece(self.piece[:6] + "queen", capture, previous_position, "Q"))
			self.promotion_dialog.rook.pressed.connect(lambda: self.changePiece(self.piece[:6] + "rook", capture, previous_position, "R"))
			self.promotion_dialog.bishop.pressed.connect(lambda: self.changePiece(self.piece[:6] + "bishop", capture, previous_position, "B"))
			self.promotion_dialog.knight.pressed.connect(lambda: self.changePiece(self.piece[:6] + "knight", capture, previous_position, "N"))
		elif str(castle) == "False" and add_move: self.parent.parent().addMove(self.piece, index, capture, previous_position, self.isCheck(index))
		elif add_move: self.parent.parent().addMove("", [], False, [], False, "O-O" if castle == 0 else "O-O-O")
	
	def changePiece(self, piece, capture, previous_position, piece_character):
		self.setPixmap(QPixmap(f"images/standard/{piece}.png"))
		self.piece = piece
		self.parent.parent().addMove("", [], False, [], False, f"{self.parent.parent().formatIndex(self.index)}={piece_character}" if not capture else f"{str(self.parent.parent().formatIndex(previous_position))[0]}x{self.parent.parent().formatIndex(self.index)}={piece_character}")
	
class Square(QPushButton):
	def __init__(self, parent, color: str = "white"):
		super(Square, self).__init__(parent = parent)
		self.original_color, self.highlighted, self.parent, self.highlight_mask = color, False, parent, QWidget(self)
		self.highlight_mask.resize(100, 100)
		self.highlight_mask.setStyleSheet("background-color: rgba(0, 174, 255, 0.5);")
		self.highlight_mask.hide()
		self.setStyleSheet(f"background-color: {color}; border: none;")
	
	def mousePressEvent(self, event: QMouseEvent):
		if self.parent.piece_for_shown_moves is not None:
			for i in self.parent.piece_for_shown_moves.moves: i.hide()
			self.parent.piece_for_shown_moves.setStyleSheet("background-color: transparent;")
			self.parent.piece_for_shown_moves.showing_moves = False
			self.parent.piece_for_shown_moves = None
		if event.button() == Qt.RightButton:
			if self.highlighted: self.highlight_mask.hide()
			else: self.highlight_mask.show()
			self.highlighted = not self.highlighted
		elif event.button() == Qt.LeftButton:
			for x in self.parent.squares:
				for y in x: y.highlight_mask.hide()
	
class Board(QWidget):
	def __init__(self, parent):
		super(Board, self).__init__(parent = parent)
		self.squares, self.pieces, self.showing_moves, self.piece_for_shown_moves, self.turn = [], [], False, None, "white"
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
	
	def resizeEvent(self, event: QResizeEvent) -> None:
		self.move((self.parent().parent().width() // 2) - (event.size().width() // 2), (self.parent().parent().height() // 2) - (event.size().height() // 2))
		self.parent().sidebar.move(self.pos().x() + event.size().width() + 10, self.pos().y())
