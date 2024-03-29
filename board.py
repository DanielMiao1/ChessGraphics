# -*- coding: utf-8 -*-

"""
board.py
Chess Board Graphics
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from chess.functions import *


class Promotion(QLabel):
	def __init__(self, parent, piece_symbol, piece, color):
		super(Promotion, self).__init__(parent)
		self.setCursor(Qt.PointingHandCursor)
		self.piece_symbol, self.piece, self.color = piece_symbol, piece, color
		self.hide()

	def mouseReleaseEvent(self, event):
		if self.parent().piece is not None:
			self.parent().move_name.name = self.parent().move_name.name[:-1] + self.piece_symbol
			self.parent().move_name.name = self.parent().move_name.promotion = self.piece_symbol
			self.parent().piece.movePiece(self.parent().move_name, promotion=True)
		super(Promotion, self).mouseReleaseEvent(event)

	def resizeEvent(self, event):
		self.setPixmap(QPixmap("images/standard/" + self.color + "_" + self.piece + ".png").scaled(event.size().width(), event.size().width()))
		super(Promotion, self).resizeEvent(event)


class Promotions(QPushButton):
	def __init__(self, parent, color):
		super(Promotions, self).__init__(parent)
		self.piece = self.move_name = None
		self.promotions = []
		self.color = color
		for x, y in self.parent().game.properties["promotions"].items():
			self.promotions.append(Promotion(self, x, y, color))
		self.setStyleSheet("border: none; background: rgba(0, 0, 0, 0.2);")
		self.hide()

	def showEvent(self, event):
		for i in self.promotions:
			i.show()
		super(Promotions, self).showEvent(event)

	def hideEvent(self, event):
		for i in self.promotions:
			i.hide()
		super(Promotions, self).hideEvent(event)

	def updatePosition(self, position):
		self.move(position)
		self.resize(QSize((self.parent().parent().width() // 25), (self.parent().parent().width() // 25) * len(self.promotions)))
		for x, y in enumerate(self.promotions):
			y.move(QPoint(0, 0 + (self.parent().parent().width() // 25 * x)))
			y.resize(QSize(self.parent().parent().width() // 25, self.parent().parent().width() // 25))
		self.raise_()


class MoveBullet(QLabel):
	def __init__(self, parent, piece, move, position) -> None:
		super(MoveBullet, self).__init__(parent)
		self.hide()
		self.piece = piece
		self.position = position
		self.setCursor(Qt.PointingHandCursor)
		self.setPixmap(QPixmap("images/bullet.png").scaled(self.parent().parent().width() // 25, self.parent().parent().width() // 25))
		self.resize(QSize(self.parent().parent().width() // 25, self.parent().parent().width() // 25))
		self.move((coordinateToIndex(self.position)[1] + 1) * (self.parent().parent().width() // 25), (coordinateToIndex(self.position)[0] + 1) * (self.parent().parent().width() // 25))
		self.move_ = self.move
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
		super(MoveBullet, self).mousePressEvent(event)

	def resizeEvent(self, event):
		self.setPixmap(QPixmap("images/bullet.png").scaled(event.size().width(), event.size().width()))
		self.move_((coordinateToIndex(self.position)[1] + 1) * event.size().width(), (coordinateToIndex(self.position)[0] + 1) * event.size().width())
		super(MoveBullet, self).resizeEvent(event)


class Piece(QLabel):
	def __init__(self, parent, position, color, piece) -> None:
		super(Piece, self).__init__(parent=parent)
		self.piece, self.color = piece, color
		self.position = position
		self.move_animation = None
		self.moves_loaded = True
		self.moves = [MoveBullet(self.parent(), self, i, i.new_position) for i in self.parent().game.pieceAt(self.position).moves(show_data=True, evaluate_checks=self.parent().parent().variant == "Three Check")]
		self.showing_moves = False
		self.dragging = False
		self.setCursor(Qt.PointingHandCursor)
		self.setPixmap(QPixmap("images/standard/" + color + "_" + piece).scaled(self.parent().parent().width() // 25, self.parent().parent().width() // 25))
		self.resize(QSize(self.parent().parent().width() // 25, self.parent().parent().width() // 25))
		self.setFocusPolicy(Qt.ClickFocus)

	def showMoves(self, change_background=True):
		if self.parent() is None:
			return
		if self.parent().game.game_over:
			return
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
				self.moves = [MoveBullet(self.parent(), self, i, i.new_position) for i in self.parent().game.pieceAt(self.position).moves(show_data=True, evaluate_checks=self.parent().parent().variant == "Three Check")]
				self.moves_loaded = True
			for i in self.moves:
				i.show()

	def moveEvent(self, event):
		if not self.dragging:
			self.original_position = event.pos()
		super(Piece, self).moveEvent(event)

	def mousePressEvent(self, event) -> None:
		if event.button() == Qt.LeftButton:
			if self.color != self.parent().game.turn or (self.parent().parent().type_ == "computer" and self.color != self.parent().parent().player_color) or (self.parent().parent().type_ == "computer" and self.parent().parent().computer_moving):
				for x in self.parent().pieces:
					if x.showing_moves:
						for y in x.moves:
							y.hide()
						x.showing_moves = False
						x.setStyleSheet("background-color: transparent;")
				self.setStyleSheet("background-color: rgba(86, 12, 255, 0.5);")
				super(Piece, self).mousePressEvent(event)
				self.mouse_event_start = self.mouse_event_position = None
				return
		if event.button() == Qt.MouseButton.RightButton:
			self.showing_moves = False
			self.setStyleSheet("background-color: transparent;")
			for i in self.moves:
				i.hide()
		for i in self.parent().squares:
			if i.position == self.position:
				i.mousePressEvent(event, remove_move_bullets=False)
				break
		self.mouse_event_start = self.mouse_event_position = None
		if event.button() == Qt.LeftButton:
			self.mouse_event_start, self.mouse_event_position = event.globalPos(), event.globalPos()
		super(Piece, self).mousePressEvent(event)

	def mouseMoveEvent(self, event) -> None:
		if event.buttons() == Qt.LeftButton and not self.parent().parent().game_over and self.mouse_event_start is not None and self.mouse_event_position is not None:
			if self.dragging == False:
				self.dragging = True
				self.parent().drag_square = Square(self.parent(), "rgba(86, 12, 255, 0.5);", self.position)
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
				if not (self.parent().parent().type_ == "computer" and self.color != self.parent().parent().player_color) and not (self.parent().parent().type_ == "computer" and self.parent().parent().computer_moving):
					for i in self.moves:
						i.hide()
			else:
				if not (self.parent().parent().type_ == "computer" and self.color != self.parent().parent().player_color) and not (self.parent().parent().type_ == "computer" and self.parent().parent().computer_moving):
					self.showMoves()
			self.showing_moves = not self.showing_moves

	def movePiece(self, move, animate=True, promotion=False) -> None:
		if self.parent() is None:
			return
		if self.parent().parent().game_over:
			return
		self.setStyleSheet("background-color: transparent;")
		if self.piece == "pawn":
			if self.color == "white":
				if move.new_position[1] == "8":
					if promotion:
						self.parent().promotion_dialog_white.hide()
					else:
						self.parent().promotion_dialog_white.move_name = move
						self.parent().promotion_dialog_white.piece = self
						self.parent().promotion_dialog_white.updatePosition(QPoint((coordinateToIndex(move.new_position)[1] + 1) * (self.parent().parent().width() // 25), (coordinateToIndex(move.new_position)[0] + 1) * (self.parent().parent().width() // 25)))
						self.parent().promotion_dialog_white.show()
						return
			else:
				if move.new_position[1] == "1":
					if promotion:
						self.parent().promotion_dialog_black.hide()
					else:
						self.parent().promotion_dialog_black.move_name = move
						self.parent().promotion_dialog_black.piece = self
						self.parent().promotion_dialog_black.updatePosition(QPoint((coordinateToIndex(move.new_position)[1] + 1) * (self.parent().parent().width() // 25), (coordinateToIndex(move.new_position)[0] + 1) * (self.parent().parent().width() // 25)))
						self.parent().promotion_dialog_black.show()
						return
		if move.is_capture:
			for i in self.parent().pieces:
				i.moves_loaded = False
				if i.position == move.captured_piece.position:
					i.setParent(None)
		else:
			for i in self.parent().pieces:
				i.moves_loaded = False
		self.position = move.new_position
		if animate:
			self.move_animation = QPropertyAnimation(self, b"pos")
			self.move_animation.setEndValue(QPoint((coordinateToIndex(self.position)[1] + 1) * (self.parent().parent().width() // 25), (coordinateToIndex(self.position)[0] + 1) * (self.parent().parent().width() // 25)))
			self.move_animation.setDuration({"Default": 100, "Slow": 225, "Fast": 50}[self.parent().parent().settings_values["piece-animation-speed"]])
			self.move_animation.start()
		else:
			self.move(QPoint((coordinateToIndex(self.position)[1] + 1) * (self.parent().parent().width() // 25), (coordinateToIndex(self.position)[0] + 1) * (self.parent().parent().width() // 25)))
		if move.castle is not None:
			if animate:
				self.parent().castle_rook_animation = QPropertyAnimation(self.parent().pieceAt(move.castle_rook.position), b"pos")
			if move.castle == "kingside":
				if animate:
					self.parent().castle_rook_animation.setEndValue(QPoint(6 * (self.parent().parent().width() // 25), (coordinateToIndex(move.castle_rook.position)[0] + 1) * (self.parent().parent().width() // 25)))
				else:
					self.parent().pieceAt(move.castle_rook.position).move(QPoint(6 * (self.parent().parent().width() // 25), (coordinateToIndex(move.castle_rook.position)[0] + 1) * (self.parent().parent().width() // 25)))
				self.parent().pieceAt(move.castle_rook.position).position = "f" + move.old_position[1]
			else:
				if animate:
					self.parent().castle_rook_animation.setEndValue(QPoint(4 * (self.parent().parent().width() // 25), (coordinateToIndex(move.castle_rook.position)[0] + 1) * (self.parent().parent().width() // 25)))
				else:
					self.parent().pieceAt(move.castle_rook.position).move(QPoint(4 * (self.parent().parent().width() // 25), (coordinateToIndex(move.castle_rook.position)[0] + 1) * (self.parent().parent().width() // 25)))
				self.parent().pieceAt(move.castle_rook.position).position = "d" + move.old_position[1]
			if animate:
				self.parent().castle_rook_animation.setDuration({"Default": 100, "Slow": 225, "Fast": 50}[self.parent().parent().settings_values["piece-animation-speed"]])
				self.parent().castle_rook_animation.start()
		self.parent().game.move(move)
		if self.parent().parent().variant == "Atomic":
			if move.is_capture:
				squares = self.parent().parent().game.generateExplosionRadius(move.new_position)
				if squares:
					for i in self.parent().pieces[:]:
						if i.piece == "pawn":
							continue
						if i.position in squares:
							self.parent().pieces.remove(i)
							i.deleteLater()
		self.parent().white_king.setStyleSheet("background-color: transparent;")
		self.parent().black_king.setStyleSheet("background-color: transparent;")
		if self.parent().game.in_check:
			if self.parent().game.turn == "white":
				self.parent().white_king.setStyleSheet("background-color: #e96160;")
			else:
				self.parent().black_king.setStyleSheet("background-color: #e96160;")
		for i in self.moves:
			i.deleteLater()
		self.moves = []
		self.parent().parent().parent().parent().setWindowTitle("2-Player Chess Game: " + self.parent().game.turn.title() + " to move")
		self.parent().parent().addMove(move.name)
		if promotion:
			self.piece = move.piece.piece_type
			self.setPixmap(QPixmap("images/standard/" + self.color + "_" + self.piece).scaled(self.width(), self.width()))

	def resizeEvent(self, event):
		self.setPixmap(QPixmap("images/standard/" + self.color + "_" + self.piece).scaled(event.size().width(), event.size().width()))
		super(Piece, self).resizeEvent(event)


class Square(QPushButton):
	def __init__(self, parent, color, position) -> None:
		super(Square, self).__init__(parent=parent)
		self.resize(QSize((self.parent().parent().width() // 25), (self.parent().parent().width() // 25)))
		self.setStyleSheet(f"background-color: {color}; border: none;")
		self.position = position
		self.highlight_square = QPushButton(self.parent())
		self.highlight_square.setStyleSheet("background-color: rgba(0, 174, 255, 0.5); border: none;")
		self.highlight_square.resize(self.size())
		self.highlight_square.mousePressEvent = self.mousePressEvent
		self.highlight_square.hide()
		self.setFocusPolicy(Qt.ClickFocus)

	def highlight(self):
		if self.highlight_square.isHidden():
			self.highlight_square.show()
		else:
			self.highlight_square.hide()

	def mousePressEvent(self, event, remove_move_bullets=True) -> None:
		if event.button() == Qt.MouseButton.LeftButton:
			for i in self.parent().squares:
				if not i.highlight_square.isHidden():
					i.highlight_square.hide()
			if remove_move_bullets:
				for x in self.parent().pieces:
					if x.showing_moves:
						for y in x.moves:
							y.hide()
						x.showing_moves = False
						x.setStyleSheet("background-color: transparent;")
		else:
			self.highlight()
		super(Square, self).mousePressEvent(event)

	def moveEvent(self, event):
		self.highlight_square.move(event.pos())
		super(Square, self).moveEvent(event)

	def resizeEvent(self, event):
		self.highlight_square.resize(event.size())
		super(Square, self).resizeEvent(event)


class Board(QWidget):
	def __init__(self, parent, game) -> None:
		super(Board, self).__init__(parent=parent)
		self.game = game
		self.squares, self.pieces = [], []
		self.drag_square = None
		self.castle_rook_animation = None
		self.promotion_dialog_white, self.promotion_dialog_black = Promotions(self, "white"), Promotions(self, "black")
		for x in self.game.squares:
			for y in x:
				self.squares.append(Square(self, parent.settings_values["light-square-color"] if y.color == "white" else parent.settings_values["dark-square-color"], y.position))
				self.squares[-1].move((coordinateToIndex(y.position)[1] + 1) * (self.parent().width() // 25), (coordinateToIndex(y.position)[0] + 1) * (self.parent().width() // 25))
		for i in self.game.pieces:
			self.pieces.append(Piece(self, i.position, i.color, i.piece_type))
			self.pieces[-1].move((coordinateToIndex(i.position)[1] + 1) * (self.parent().width() // 25), (coordinateToIndex(i.position)[0] + 1) * (self.parent().width() // 25))
			if i.piece_type == "king":
				if i.color == "white":
					self.white_king = self.pieces[-1]
				if i.color == "black":
					self.black_king = self.pieces[-1]
		self.setFocusPolicy(Qt.ClickFocus)

	def updatePieces(self):
		for i in self.pieces:
			i.deleteLater()
		self.pieces = []
		for i in self.game.pieces:
			self.pieces.append(Piece(self, i.position, i.color, i.piece_type))
			self.pieces[-1].move((coordinateToIndex(i.position)[1] + 1) * (self.parent().width() // 25), (coordinateToIndex(i.position)[0] + 1) * (self.parent().width() // 25))
			self.pieces[-1].show()
			if i.piece_type == "king":
				if i.color == "white":
					self.white_king = self.pieces[-1]
				if i.color == "black":
					self.black_king = self.pieces[-1]

	def evaluateMove(self, string):
		try:
			string = toSAN(string, self.game)
		except:
			return False
		legal_moves = self.game.legal_moves(show_data=True)
		for i in legal_moves:
			if i.name == string:
				self.pieceAt(i.old_position).movePiece(i)
				return True
		return False

	@staticmethod
	def generateTemporaryValidCharacters(string):
		if not string:
			return ["a", "b", "c", "d", "e", "f", "g", "h", "P", "N", "B", "R", "Q", "K"]
		if string[-1] == "x":
			return ["a", "b", "c", "d", "e", "f", "g", "h"]
		if string[-1] in ["a", "b", "c", "d", "e", "f", "g", "h"]:
			return ["1", "2", "3", "4", "5", "6", "7", "8", "x"]
		if string[-1].isnumeric() and len([True for i in string if i.isnumeric()]) <= 1:
			return ["a", "b", "c", "d", "e", "f", "g", "h", "x"]
		if string[-1] in ["P", "N", "B", "R", "Q", "K"]:
			return ["a", "b", "c", "d", "e", "f", "g", "h", "x"]
		if string[-1].upper() == "O" and len(string) <= 4:
			return ["-"]
		if string[-1] == "-" and "O" in string.upper():
			return ["O"]
		return []

	def keyPressEvent(self, event):
		if self.parent().temporary_move is None:
			if event.text() in ["a", "b", "c", "d", "e", "f", "g", "h", "P", "N", "B", "R", "Q", "K", "O"]:
				self.parent().addTemporaryMove(event.text())
				if event.text() in ["O", "0"]:
					return
				if event.text() in ["a", "b", "c", "d", "e", "f", "g", "h"]:
					for i in self.squares:
						if i.position[0] == event.text():
							if i.highlight_square.isHidden():
								i.highlight_square.show()
				else:
					positions = list(map(lambda x: str(x.position), self.game.pieceType({"P": "pawn", "N": "knight", "B": "bishop", "R": "rook", "Q": "queen", "K": "king"}[event.text()], color=self.game.turn)))
					for i in self.squares:
						if i.position in positions:
							if i.highlight_square.isHidden():
								i.highlight_square.show()
						else:
							if not i.highlight_square.isHidden():
								i.highlight_square.hide()
		elif event.key() in [Qt.Key.Key_Backspace, Qt.Key.Key_Delete]:
			self.parent().temporary_move.setText(self.parent().temporary_move.text()[:-1])
		elif event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter] and self.parent().temporary_move is not None:
			temporary_move_text = self.parent().temporary_move.text()
			self.parent().moves_layout.removeWidget(self.parent().temporary_move)
			self.parent().move_buttons.remove(self.parent().temporary_move)
			self.parent().temporary_move.deleteLater()
			if self.evaluateMove(self.parent().temporary_move.text().replace("P", "")):
				self.parent().temporary_move = None
				for i in self.squares:
					if not i.highlight_square.isHidden():
						i.highlight_square.hide()
			else:
				self.parent().addTemporaryMove(temporary_move_text)
		elif event.key() == Qt.Key.Key_Escape:
			self.parent().moves_layout.removeWidget(self.parent().temporary_move)
			self.parent().move_buttons.remove(self.parent().temporary_move)
			self.parent().temporary_move.deleteLater()
			self.parent().temporary_move = None
			for i in self.squares:
				if not i.highlight_square.isHidden():
					i.highlight_square.hide()
		elif event.text() in self.generateTemporaryValidCharacters(self.parent().temporary_move.text()):
			self.parent().temporary_move.setText(self.parent().temporary_move.text() + event.text())
			if event.text() in ["P", "N", "B", "R", "Q", "K"]:
				positions = list(map(lambda x: str(x.position), self.game.pieceType({"P": "pawn", "N": "knight", "B": "bishop", "R": "rook", "Q": "queen", "K": "king"}[event.text()], color=self.game.turn)))
				for i in self.squares:
					if i.position in positions:
						if i.highlight_square.isHidden():
							i.highlight_square.show()
					else:
						if not i.highlight_square.isHidden():
							i.highlight_square.hide()
			elif event.text() in ["a", "b", "c", "d", "e", "f", "g", "h"]:
				for i in self.squares:
					if i.position[0] == event.text():
						if i.highlight_square.isHidden():
							i.highlight_square.show()
					else:
						if not i.highlight_square.isHidden():
							i.highlight_square.hide()
			elif event.text().isnumeric():
				if self.pieceAt(self.parent().temporary_move.text()[-2:]) and self.pieceAt(self.parent().temporary_move.text()[-2:]).color == self.game.turn:
					for i in self.squares:
						if not i.highlight_square.isHidden():
							i.highlight_square.hide()
					self.pieceAt(self.parent().temporary_move.text()[-2:]).showMoves()
					self.pieceAt(self.parent().temporary_move.text()[-2:]).showing_moves = True
					self.pieceAt(self.parent().temporary_move.text()[-2:]).setStyleSheet("background-color: rgba(86, 12, 255, 0.5);")
				else:
					for i in self.squares:
						if i.position == self.parent().temporary_move.text()[-2:]:
							if i.highlight_square.isHidden():
								i.highlight_square.show()
						else:
							if not i.highlight_square.isHidden():
								i.highlight_square.hide()
		super(Board, self).keyPressEvent(event)

	def pieceAt(self, position):
		for i in self.pieces:
			if i.position == position:
				return i
		return False

	def resizeComponents(self):
		self.resize(QSize(self.parent().width() // 25 * 9, self.parent().width() // 25 * 9))
		for i in self.squares:
			i.resize(QSize(self.parent().width() // 25, self.parent().width() // 25))
			i.move((coordinateToIndex(i.position)[1] + 1) * (self.parent().width() // 25), (coordinateToIndex(i.position)[0] + 1) * (self.parent().width() // 25))

		for x in self.pieces:
			x.resize(QSize(self.parent().width() // 25, self.parent().width() // 25))
			x.move((coordinateToIndex(x.position)[1] + 1) * (self.parent().width() // 25), (coordinateToIndex(x.position)[0] + 1) * (self.parent().width() // 25))
			for y in x.moves:
				y.resize(QSize(self.parent().width() // 25, self.parent().width() // 25))
