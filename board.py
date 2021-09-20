"""
board.py
Graphical Chess Board, Pieces, and Squares
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from chess.functions import *


class MoveBullet(QLabel):
	def __init__(self, parent, piece, move, position):
		super(MoveBullet, self).__init__(parent=parent)
		self.hide()
		self.piece = piece
		self.position = position
		self.setCursor(Qt.PointingHandCursor)
		self.setPixmap(QPixmap("images/bullet.png"))
		self.move((coordinateToIndex(self.position)[1] + 1) * 100, (coordinateToIndex(self.position)[0] + 1) * 100)
		self.move = move
	
	def enterEvent(self, event: QHoverEvent):
		self.setStyleSheet("background-color: rgba(12, 36, 255, 0.5)")
		super(MoveBullet, self).enterEvent(event)
	
	def leaveEvent(self, event: QHoverEvent):
		self.setStyleSheet("background-color: transparent")
		super(MoveBullet, self).leaveEvent(event)
	
	def mousePressEvent(self, event) -> None:
		if event.button() == Qt.LeftButton:
			self.piece.movePiece(self.move)
		else:
			self.piece.mousePressEvent(event)
		super(MoveBullet, self).mousePressEvent(event)
		

class Piece(QLabel):
	def __init__(self, parent, position, color, piece):
		super(Piece, self).__init__(parent=parent)
		self.piece, self.color = piece, color
		self.position = position
		self.move_animation = None
		self.moves_loaded = True
		self.moves = [MoveBullet(self.parent(), self, i, i.new_position) for i in self.parent().game.pieceAt(self.position).moves(show_data=True)]
		self.showing_moves = False
		self.setCursor(Qt.PointingHandCursor)
		self.setPixmap(QPixmap("images/standard/" + color + "_" + piece))
	
	def mousePressEvent(self, event) -> None:
		if self.showing_moves:
			self.setStyleSheet("background-color: transparent;")
			for i in self.moves:
				i.hide()
		else:
			self.setStyleSheet("background-color: rgba(86, 12, 255, 0.5);")
			for x in self.parent().pieces:
				if x.showing_moves:
					x.showing_moves = False
					x.setStyleSheet("background-color: transparent;")
					for y in x.moves:
						y.hide()
			if self.parent().game.turn == self.color:
				if not self.moves_loaded:
					self.moves = [MoveBullet(self.parent(), self, i, i.new_position) for i in self.parent().game.pieceAt(self.position).moves(show_data=True)]
					self.moves_loaded = True
				for i in self.moves:
					i.show()
		self.showing_moves = not self.showing_moves
		super(Piece, self).mousePressEvent(event)
	
	def movePiece(self, move):
		self.setStyleSheet("background-color: transparent;")
		for i in self.parent().pieces:
			i.moves_loaded = False
			if i.position == move.new_position:
				i.setParent(None)
		self.position = move.new_position
		self.move_animation = QPropertyAnimation(self, b"pos")
		self.move_animation.setEndValue(QPoint((coordinateToIndex(self.position)[1] + 1) * 100, (coordinateToIndex(self.position)[0] + 1) * 100))
		self.move_animation.setDuration(100)
		self.move_animation.start()
		self.parent().game.move(move.name)
		for i in self.moves:
			i.setParent(None)
		self.parent().parent().opening.setText(self.parent().game.opening)
		self.parent().parent().addMove(move.name)
		self.parent().parent().parent().parent().setWindowTitle("2-Player Chess Game: " + self.parent().game.turn.title() + " to move")


class Square(QPushButton):
	def __init__(self, parent, color):
		super(Square, self).__init__(parent=parent)
		self.setFixedSize(QSize(100, 100))
		self.setStyleSheet(f"background-color: {color}; border: none;")
	
	def mousePressEvent(self, event) -> None:
		for x in self.parent().pieces:
			if x.showing_moves:
				for y in x.moves:
					y.hide()
				x.showing_moves = False
				x.setStyleSheet("background-color: transparent;")
		super(Square, self).mousePressEvent(event)


class Board(QWidget):
	def __init__(self, parent, game):
		super(Board, self).__init__(parent=parent)
		self.game = game
		self.squares, self.pieces = [], []
		for x in self.game.squares:
			for y in x:
				self.squares.append(Square(self, "#FFFFDD" if y.color == "white" else "#86A666"))
				self.squares[-1].move((coordinateToIndex(y.position)[1] + 1) * 100, (coordinateToIndex(y.position)[0] + 1) * 100)
		for i in self.game.pieces:
			self.pieces.append(Piece(self, i.position, i.color, i.piece_type))
			self.pieces[-1].move((coordinateToIndex(i.position)[1] + 1) * 100, (coordinateToIndex(i.position)[0] + 1) * 100)

	def resizeEvent(self, event: QResizeEvent) -> None:
		self.move((self.parent().parent().width() // 2) - (event.size().width() // 2), (self.parent().parent().height() // 2) - (event.size().height() // 2))
		self.parent().sidebar.move(self.pos().x() + event.size().width() + 10, self.pos().y())
