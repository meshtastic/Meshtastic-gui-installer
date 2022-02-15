"""Test YesNo
"""

from PySide6 import QtCore
from PySide6.QtWidgets import QDialog

from meshtastic_flasher.yes_no import YesNo

def test_YesNo_yes_pressed(qtbot):
    """Test YesNo() when yes button pressed"""
    widget = YesNo()
    qtbot.addWidget(widget)
    def interact():
        buttons = widget.buttons()
        for button in buttons:
            if button.text() == '&Yes':
                yes_button = button
        qtbot.mouseClick(yes_button, QtCore.Qt.MouseButton.LeftButton)
    QtCore.QTimer.singleShot(1, interact)
    result = widget.exec()
    assert result == 16384

def test_YesNo_no_pressed(qtbot):
    """Test YesNo() when no button pressed"""
    widget = YesNo()
    qtbot.addWidget(widget)
    def interact():
        buttons = widget.buttons()
        for button in buttons:
            if button.text() == '&No':
                no_button = button
        qtbot.mouseClick(no_button, QtCore.Qt.MouseButton.LeftButton)
    QtCore.QTimer.singleShot(1, interact)
    result = widget.exec()
    assert result == 65536


def test_YesNo_y(qtbot):
    """Test YesNo() when 'y'"""
    widget = YesNo()
    qtbot.addWidget(widget)
    def interact():
        qtbot.keyPress(widget, "y")
    QtCore.QTimer.singleShot(1, interact)
    result = widget.exec()
    assert result == QDialog.Accepted


def test_YesNo_n(qtbot):
    """Test YesNo() when 'n'"""
    widget = YesNo()
    qtbot.addWidget(widget)
    def interact():
        qtbot.keyPress(widget, "n")
    QtCore.QTimer.singleShot(1, interact)
    result = widget.exec()
    assert result == QDialog.Rejected
