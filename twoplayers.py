"""
twoplayers.py
2 Player Chess Mode
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import board

class TwoPlayers(QWidget):
	def __init__(self, parent):
		super(TwoPlayers, self).__init__(parent = parent)
		self.board = board.Board(self)
