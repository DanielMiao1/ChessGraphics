"""
settings.py
Application Settings
"""

from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import json

settings_defaults = {"light-square-color": "#FFFFDD", "dark-square-color": "#86A666", "piece-animation-speed": "Default"}

try:
	settings = json.load(open("settings.json"))
	modified = False
	for x, y in settings_defaults.items():
		try:
			settings[x]
		except KeyError:
			settings[x] = y
			if not modified:
				modified = True
	if modified:
		json.dump(settings, open("settings.json", "w"))
except json.decoder.JSONDecodeError:
	json.dump(settings_defaults, open("settings.json", "w"))

settings_values = json.load(open("settings.json"))


def setJSON(key, value):
	items = json.load(open("settings.json"))
	items[key] = value
	json.dump(items, open("settings.json", "w"))


class BackButton(QPushButton):
	def __init__(self, parent):
		super(BackButton, self).__init__(parent=parent)
		self.setText("←")
		self.setCursor(Qt.CursorShape.PointingHandCursor)
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


class SaveButton(QPushButton):
	def __init__(self, parent):
		super(SaveButton, self).__init__(parent=parent)
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.save_icon = QSvgWidget(self)
		self.save_icon.renderer().load(bytearray('<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg width="13.75" height="15.625"><polygon points="0, 0 0, 15.625 13.75, 15.625 13.75, 2.5 11.25, 0 10, 0 10, 3.75 1.875, 3.75 1.875, 0" style="fill:black"/><rect x="7.5" y="0.9375" width="1.25" height="1.875" style="fill:black"/><rect x="1.875" y="5.625" width="10" height="8.125" style="fill:white"/><rect x="3.75" y="7.5" width="6.25" height="1.5" style="fill:black"/><rect x="3.75" y="10.625" width="6.25" height="1.5" style="fill:black"/></svg>', encoding='utf-8'))
		self.status_tip = QLabel("Save", parent)
		self.status_tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.status_tip.hide()
		self.setStyleSheet("color: black; background-color: white; border: none;")
	
	def focusInEvent(self, event) -> None:
		if event.reason() <= 2:
			self.status_tip.show()
			self.setStyleSheet("color: black; background-color: lightblue; border: none;")
			self.save_icon.renderer().load(bytearray('<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg width="13.75" height="15.625"><polygon points="0, 0 0, 15.625 13.75, 15.625 13.75, 2.5 11.25, 0 10, 0 10, 3.75 1.875, 3.75 1.875, 0" style="fill:black"/><rect x="7.5" y="0.9375" width="1.25" height="1.875" style="fill:black"/><rect x="1.875" y="5.625" width="10" height="8.125" style="fill:lightblue"/><rect x="3.75" y="7.5" width="6.25" height="1.5" style="fill:black"/><rect x="3.75" y="10.625" width="6.25" height="1.5" style="fill:black"/></svg>', encoding='utf-8'))
		super(SaveButton, self).focusInEvent(event)
	
	def focusOutEvent(self, event) -> None:
		if event.reason() <= 2:
			self.status_tip.hide()
			self.setStyleSheet("color: black; background-color: white; border: none;")
			self.save_icon.renderer().load(bytearray('<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg width="13.75" height="15.625"><polygon points="0, 0 0, 15.625 13.75, 15.625 13.75, 2.5 11.25, 0 10, 0 10, 3.75 1.875, 3.75 1.875, 0" style="fill:black"/><rect x="7.5" y="0.9375" width="1.25" height="1.875" style="fill:black"/><rect x="1.875" y="5.625" width="10" height="8.125" style="fill:white"/><rect x="3.75" y="7.5" width="6.25" height="1.5" style="fill:black"/><rect x="3.75" y="10.625" width="6.25" height="1.5" style="fill:black"/></svg>', encoding='utf-8'))
		super(SaveButton, self).focusOutEvent(event)
	
	def resizeEvent(self, event) -> None:
		self.status_tip.setFixedWidth(event.size().width())
		self.status_tip.move(QPoint(self.pos().x(), self.pos().y() + event.size().width()))
		self.save_icon.move(QPoint((event.size().width() - 13.75) // 2, (event.size().height() - 15.625) // 2))
		super(SaveButton, self).resizeEvent(event)

	def enterEvent(self, event: QEvent) -> None:
		self.status_tip.show()
		self.setStyleSheet("color: black; background-color: lightblue; border: none;")
		self.save_icon.renderer().load(bytearray('<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg width="13.75" height="15.625"><polygon points="0, 0 0, 15.625 13.75, 15.625 13.75, 2.5 11.25, 0 10, 0 10, 3.75 1.875, 3.75 1.875, 0" style="fill:black"/><rect x="7.5" y="0.9375" width="1.25" height="1.875" style="fill:black"/><rect x="1.875" y="5.625" width="10" height="8.125" style="fill:lightblue"/><rect x="3.75" y="7.5" width="6.25" height="1.5" style="fill:black"/><rect x="3.75" y="10.625" width="6.25" height="1.5" style="fill:black"/></svg>', encoding='utf-8'))
		super(SaveButton, self).enterEvent(event)

	def leaveEvent(self, event: QEvent) -> None:
		self.status_tip.hide()
		self.save_icon.renderer().load(bytearray('<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg width="13.75" height="15.625"><polygon points="0, 0 0, 15.625 13.75, 15.625 13.75, 2.5 11.25, 0 10, 0 10, 3.75 1.875, 3.75 1.875, 0" style="fill:black"/><rect x="7.5" y="0.9375" width="1.25" height="1.875" style="fill:black"/><rect x="1.875" y="5.625" width="10" height="8.125" style="fill:white"/><rect x="3.75" y="7.5" width="6.25" height="1.5" style="fill:black"/><rect x="3.75" y="10.625" width="6.25" height="1.5" style="fill:black"/></svg>', encoding='utf-8'))
		self.setStyleSheet("color: black; background-color: white; border: none;")
		super(SaveButton, self).leaveEvent(event)


class OptionsButton(QPushButton):
	def __init__(self, text, parent, pressed_function=None, center_text=False):
		super(OptionsButton, self).__init__(parent=parent)
		self.pressed_function = pressed_function
		self.text = QLabel(text, self)
		if center_text:
			self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.text.resize(self.size())
		self.text.setWordWrap(True)
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
	
	def resizeEvent(self, event):
		self.text.resize(event.size())
		super(OptionsButton, self).resizeEvent(event)
	
	def enterEvent(self, event) -> None:
		if self.styleSheet().split()[1] == "white;":
			self.setStyleSheet("background-color: #EEEEEE; border: 12px solid #EEEEEE; color: black")
		super(OptionsButton, self).enterEvent(event)
	
	def leaveEvent(self, event) -> None:
		if self.styleSheet().split()[1] == "#EEEEEE;":
			self.setStyleSheet("background-color: white; border: 12px solid white; color: black")
		super(OptionsButton, self).leaveEvent(event)
	
	def mousePressEvent(self, event) -> None:
		if self.pressed_function is not None:
			self.pressed_function(self.text.text())
		super(OptionsButton, self).mousePressEvent(event)


class Settings(QWidget):
	def __init__(self, parent):
		super(Settings, self).__init__(parent=parent)
		self.setStyleSheet("QGroupBox { background-color: #FFF; border: none; }")
		self.changed = {}
		self.animation = QPropertyAnimation(self, b"pos")
		self.animation.setEndValue(QPoint())
		self.animation.setDuration(250)
		self.back = BackButton(self)
		self.back.pressed.connect(lambda self=self: self.parent().setCurrentIndex(0))
		self.save = SaveButton(self)
		self.save.pressed.connect(self.saveSettings)
		self.unsaved_changes = QLabel("Has unsaved changes", self)
		self.unsaved_changes.hide()
		self.tabs = QTabWidget(self)
		self.tabs.setDocumentMode(True)
		self.board_settings = QGroupBox(self)
		self.board_settings_layout = QGridLayout()
		self.board_settings_light_square_color_label = QLabel("Light Square Color", self)
		self.board_settings_light_square_color = QLineEdit(settings_values["light-square-color"], self.board_settings)
		self.board_settings_light_square_color.setStyleSheet("background-color: #BBB; border: 3px solid #BBB;")
		self.board_settings_light_square_color.textChanged.connect(lambda _, self=self: self.squareColorChanged(self.board_settings_light_square_color, "light-square-color"))
		self.board_settings_light_square_color.setAttribute(Qt.WA_MacShowFocusRect, 0)
		self.board_settings_dark_square_color_label = QLabel("Dark Square Color", self)
		self.board_settings_dark_square_color = QLineEdit(settings_values["dark-square-color"], self.board_settings)
		self.board_settings_dark_square_color.setStyleSheet("background-color: #BBB; border: 3px solid #BBB;")
		self.board_settings_dark_square_color.textChanged.connect(lambda _, self=self: self.squareColorChanged(self.board_settings_dark_square_color, "dark-square-color"))
		self.board_settings_dark_square_color.setAttribute(Qt.WA_MacShowFocusRect, 0)
		self.board_settings_layout.addWidget(self.board_settings_light_square_color_label, 0, 1)
		self.board_settings_layout.addWidget(self.board_settings_dark_square_color_label, 0, 2)
		self.board_settings_layout.addWidget(self.board_settings_light_square_color, 1, 1)
		self.board_settings_layout.addWidget(self.board_settings_dark_square_color, 1, 2)
		self.board_settings_layout.setRowStretch(0, 0)
		self.board_settings_layout.setRowStretch(2, 1)
		self.board_settings.setLayout(self.board_settings_layout)
		self.animation_settings = QGroupBox(self)
		self.animation_settings_layout = QGridLayout()
		self.animation_settings_piece_animation_speed_label = QLabel("Piece animation speed", self)
		self.animation_settings_piece_animation_speed = QGroupBox(self.animation_settings)
		self.animation_settings_piece_animation_speed_layout = QHBoxLayout()

		def animationSpeedChanged(text):
			self.animation_settings_piece_animation_speed_slow.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			self.animation_settings_piece_animation_speed_default.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			self.animation_settings_piece_animation_speed_fast.setStyleSheet("background-color: white; border: 12px solid white; color: black;")
			if text == "Slow":
				self.animation_settings_piece_animation_speed_slow.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			elif text == "Default":
				self.animation_settings_piece_animation_speed_default.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			else:
				self.animation_settings_piece_animation_speed_fast.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
			self.changed["piece-animation-speed"] = text
			if self.unsaved_changes.isHidden():
				self.unsaved_changes.show()

		self.animation_settings_piece_animation_speed_slow = OptionsButton("Slow", self, pressed_function=animationSpeedChanged, center_text=True)
		self.animation_settings_piece_animation_speed_default = OptionsButton("Default", self, pressed_function=animationSpeedChanged, center_text=True)
		self.animation_settings_piece_animation_speed_fast = OptionsButton("Fast", self, pressed_function=animationSpeedChanged, center_text=True)
		if settings_values["piece-animation-speed"] == "Default":
			self.animation_settings_piece_animation_speed_default.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		elif settings_values["piece-animation-speed"] == "Slow":
			self.animation_settings_piece_animation_speed_slow.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		else:
			self.animation_settings_piece_animation_speed_fast.setStyleSheet("background-color: black; border: 12px solid black; color: white;")
		self.animation_settings_piece_animation_speed_layout.addWidget(self.animation_settings_piece_animation_speed_slow)
		self.animation_settings_piece_animation_speed_layout.addWidget(self.animation_settings_piece_animation_speed_default)
		self.animation_settings_piece_animation_speed_layout.addWidget(self.animation_settings_piece_animation_speed_fast)
		self.animation_settings_piece_animation_speed.setLayout(self.animation_settings_piece_animation_speed_layout)
		self.animation_settings_layout.addWidget(self.animation_settings_piece_animation_speed_label, 0, 1)
		self.animation_settings_layout.addWidget(self.animation_settings_piece_animation_speed, 1, 1)
		self.animation_settings_layout.setRowStretch(0, 0)
		self.animation_settings_layout.setRowStretch(2, 1)
		self.animation_settings.setLayout(self.animation_settings_layout)
		self.tabs.addTab(self.board_settings, "Board Settings")
		self.tabs.addTab(self.animation_settings, "Animation Settings")
	
	def saveSettings(self):
		for x, y in self.changed.items():
			setJSON(x, y)
		self.changed = {}
		if not self.unsaved_changes.isHidden():
			self.unsaved_changes.hide()
		self.parent().parent().stacks["two-players"].updateSettingsValues()
	
	def squareColorChanged(self, widget, key):
		if QColor.isValidColor(widget.text()):
			widget.setStyleSheet("background-color: #BBB; border: 3px solid #BBB;")
			self.changed[key] = widget.text()
		else:
			widget.setStyleSheet("background-color: #ff7e7e; border: 3px solid #ff7e7e;")
		if self.unsaved_changes.isHidden():
			self.unsaved_changes.show()
	
	def resizeEvent(self, event: QResizeEvent) -> None:
		self.animation.setStartValue(QPoint(event.size().width(), 0))
		if event.size().width() > event.size().height():
			min_size = event.size().height()
		else:
			min_size = event.size().width()
		self.back.resize(QSize(min_size // 20, min_size // 20))
		self.save.move(QPoint(min_size // 20, 0))
		self.save.resize(QSize(min_size // 20, min_size // 20))
		self.unsaved_changes.move(QPoint(min_size // 9, min_size // 50))
		self.tabs.resize(QSize(event.size().width(), event.size().height() - (min_size // 20) - self.back.status_tip.height()))
		self.board_settings.resize(QSize(event.size().width(), event.size().height() - (min_size // 20) - self.back.status_tip.height() - self.tabs.tabBar().height()))
		self.tabs.move(QPoint(0, (min_size // 20) + self.back.status_tip.height()))
		super(Settings, self).resizeEvent(event)
