"""tests for AdvancedForm"""
import re

from pytestqt.qt_compat import qt_api

from PySide6.QtWidgets import QMessageBox

from meshtastic_flasher.installer import AdvancedForm

def test_advanced_form(qtbot, monkeypatch, capsys):
    """Test for AdvancedForm"""
    widget = AdvancedForm()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    qtbot.mouseClick(widget.ok_button, qt_api.QtCore.Qt.MouseButton.LeftButton)
    out, err = capsys.readouterr()
    assert re.search(r'OK button was clicked', out, re.MULTILINE)
    assert err == ''
