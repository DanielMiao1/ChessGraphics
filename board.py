"""
board.py
Chess Board Graphics
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from chess.functions import *


class MoveBullet(QLabel):
	def __init__(self, parent, piece, move, position) -> None:
		super(MoveBullet, self).__init__(parent=parent)
		self.hide()
		self.piece = piece
		self.position = position
		self.setCursor(Qt.PointingHandCursor)
		self.setPixmap(QPixmap("images/bullet.png"))
		self.move((coordinateToIndex(self.position)[1] + 1) * 100, (coordinateToIndex(self.position)[0] + 1) * 100)
		self.move = move

	def enterEvent(self, event: QHoverEvent) -> None:
		self.setStyleSheet("background-color: rgba(12, 36, 255, 0.5)")
		super(MoveBullet, self).enterEvent(event)

	def leaveEvent(self, event: QHoverEvent) -> None:
		self.setStyleSheet("background-color: transparent")
		super(MoveBullet, self).leaveEvent(event)

	def mousePressEvent(self, event) -> None:
		if event.button() == Qt.LeftButton:
			self.piece.movePiece(self.move)
		else:
			self.piece.mousePressEvent(event)
		super(MoveBullet, self).mousePressEvent(event)


class Piece(QLabel):
	def __init__(self, parent, position, color, piece) -> None:
		super(Piece, self).__init__(parent=parent)
		self.piece, self.color = piece, color
		self.position = position
		self.move_animation = None
		self.moves_loaded = True
		self.moves = [MoveBullet(self.parent(), self, i, i.new_position) for i in self.parent().game.pieceAt(self.position).moves(show_data=True, evaluate_checks=False)]
		self.showing_moves = False
		self.dragging = False
		self.setCursor(Qt.PointingHandCursor)
		self.setPixmap(QPixmap("images/standard/" + color + "_" + piece))

	def showMoves(self, change_background=True):
		if change_background:
			self.setStyleSheet("background-color: rgba(86, 12, 255, 0.5);")
		for x in self.parent().pieces:
			if x.showing_moves:
				x.showing_moves = False
				x.setStyleSheet("background-color: transparent;")
				for y in x.moves:
					y.hide()
		if self.parent().game.turn == self.color:
			if not self.moves_loaded:
				self.moves = [MoveBullet(self.parent(), self, i, i.new_position) for i in self.parent().game.pieceAt(self.position).moves(show_data=True, evaluate_checks=False)]
				self.moves_loaded = True
			for i in self.moves:
				i.show()

	def moveEvent(self, event):
		if not self.dragging:
			self.original_position = event.pos()
		super(Piece, self).moveEvent(event)

	def mousePressEvent(self, event) -> None:
		self.mouse_event_start = None
		self.mouse_event_position = None
		if event.button() == Qt.LeftButton:
			self.mouse_event_start = event.globalPos()
			self.mouse_event_position = event.globalPos()
		super(Piece, self).mousePressEvent(event)

	def mouseMoveEvent(self, event) -> None:
		if event.buttons() == Qt.LeftButton:
			if self.dragging == False:
				self.dragging = True
				self.parent().drag_square = Square(self.parent(), "rgba(86, 12, 255, 0.5);")
				self.parent().drag_square.move(self.pos())
				self.parent().drag_square.show()
				self.raise_()
			if self.showing_moves:
				self.setStyleSheet("background-color: transparent;")
			else:
				self.showMoves(False)
				self.showing_moves = True
				self.raise_()
			self.move(self.mapFromGlobal(self.mapToGlobal(self.pos()) + event.globalPos() - self.mouse_event_position))
			self.mouse_event_position = event.globalPos()
		super(Piece, self).mouseMoveEvent(event)

	def mouseReleaseEvent(self, event) -> None:
		super(Piece, self).mousePressEvent(event)
		if self.dragging:
			self.parent().drag_square.deleteLater()
			self.parent().drag_square = None
			self.dragging = False
			if (event.globalPos() - self.mouse_event_start).manhattanLength() < 50:
				self.move(self.original_position)
				self.showMoves()
				self.showing_moves = True
				self.setStyleSheet("background-color: rgba(86, 12, 255, 0.5);")
				return
			for i in self.moves:
				if event.globalPos() in QRect(self.parent().mapToGlobal(i.pos()), i.size()):
					if i.move.name in self.parent().game.legal_moves():
						self.movePiece(i.move, animate=False)
			self.showing_moves = False
			for i in self.moves:
				i.hide()
			self.move(self.original_position)
			return
		if event.button() == Qt.LeftButton:
			if self.showing_moves:
				self.setStyleSheet("background-color: transparent;")
				for i in self.moves:
					i.hide()
			else:
				self.showMoves()
			self.showing_moves = not self.showing_moves

	def movePiece(self, move, animate=True) -> None:
		self.setStyleSheet("background-color: transparent;")
		for i in self.parent().pieces:
			i.moves_loaded = False
			if i.position == move.new_position:
				i.setParent(None)
		self.position = move.new_position
		if animate:
			self.move_animation = QPropertyAnimation(self, b"pos")
			self.move_animation.setEndValue(QPoint((coordinateToIndex(self.position)[1] + 1) * 100, (coordinateToIndex(self.position)[0] + 1) * 100))
			self.move_animation.setDuration(100)
			self.move_animation.start()
		else:
			self.move(QPoint((coordinateToIndex(self.position)[1] + 1) * 100, (coordinateToIndex(self.position)[0] + 1) * 100))
		if move.castle is not None:
			if animate:
				self.parent().castle_rook_animation = QPropertyAnimation(self.parent().pieceAt(move.castle_rook.position), b"pos")
			if move.castle == "kingside":
				if animate:
					self.parent().castle_rook_animation.setEndValue(QPoint(600, (coordinateToIndex(move.castle_rook.position)[0] + 1) * 100))
				else:
					self.parent().pieceAt(move.castle_rook.position).move(QPoint(600, (coordinateToIndex(move.castle_rook.position)[0] + 1) * 100))
				self.parent().pieceAt(move.castle_rook.position).position = "f" + move.old_position[1]
			else:
				if animate:
					self.parent().castle_rook_animation.setEndValue(QPoint(400, (coordinateToIndex(move.castle_rook.position)[0] + 1) * 100))
				else:
					self.parent().pieceAt(move.castle_rook.position).move(QPoint(400, (coordinateToIndex(move.castle_rook.position)[0] + 1) * 100))
				self.parent().pieceAt(move.castle_rook.position).position = "d" + move.old_position[1]
			if animate:
				self.parent().castle_rook_animation.setDuration(100)
				self.parent().castle_rook_animation.start()
		self.parent().game.move(move)
		for i in self.moves:
			i.setParent(None)
		self.parent().parent().opening.setText(self.parent().game.opening)
		self.parent().parent().addMove(move.name)
		self.parent().parent().parent().parent().setWindowTitle("2-Player Chess Game: " + self.parent().game.turn.title() + " to move")


class Square(QPushButton):
	def __init__(self, parent, color) -> None:
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
	def __init__(self, parent, game) -> None:
		super(Board, self).__init__(parent=parent)
		self.game = game
		self.squares, self.pieces = [], []
		self.drag_square = None
		self.castle_rook_animation = None
		for x in self.game.squares:
			for y in x:
				self.squares.append(Square(self, "#FFFFDD" if y.color == "white" else "#86A666"))
				self.squares[-1].move((coordinateToIndex(y.position)[1] + 1) * 100, (coordinateToIndex(y.position)[0] + 1) * 100)
		for i in self.game.pieces:
			self.pieces.append(Piece(self, i.position, i.color, i.piece_type))
			self.pieces[-1].move((coordinateToIndex(i.position)[1] + 1) * 100, (coordinateToIndex(i.position)[0] + 1) * 100)

	def pieceAt(self, position) -> False or Piece:
		for i in self.pieces:
			if i.position == position:
				return i
		return False

	def resizeEvent(self, event: QResizeEvent) -> None:
		self.move((self.parent().parent().width() // 2) - (event.size().width() // 2), (self.parent().parent().height() // 2) - (event.size().height() // 2))
		self.parent().sidebar.move(self.pos().x() + event.size().width() + 10, self.pos().y())
